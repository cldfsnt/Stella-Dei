//! Shared save-file size boundary. Oversized output never replaces the canonical save.
const std = @import("std");
pub const max_save_bytes: usize = 128 * 1024 * 1024;

pub fn BoundedWriter(comptime Child: type) type {
    return struct {
        child: Child,
        limit: usize,
        written: usize = 0,
        const Self = @This();
        pub const Error = Child.Error || error{SaveTooLarge};
        pub const Writer = std.io.Writer(*Self, Error, write);
        pub fn writer(self: *Self) Writer { return .{ .context = self }; }
        fn write(self: *Self, bytes: []const u8) Error!usize {
            // Subtraction avoids overflow, including limits near usize max.
            if (bytes.len > self.limit - self.written) return error.SaveTooLarge;
            const count = try self.child.write(bytes);
            self.written += count;
            return count;
        }
    };
}

/// The caller owns its directory and validated JSON value. The limit is injectable
/// for tests; production always uses max_save_bytes for both reading and writing.
pub fn writeJsonAtomic(dir: std.fs.Dir, target: []const u8, temporary: []const u8, value: anytype, limit: usize) !void {
    std.debug.assert(!std.mem.eql(u8, target, temporary));
    const file = try dir.createFile(temporary, .{});
    var closed = false;
    var renamed = false;
    defer {
        if (!closed) file.close();
        if (!renamed) dir.deleteFile(temporary) catch {};
    }
    var buffer = std.io.bufferedWriter(file.writer());
    var bounded = BoundedWriter(@TypeOf(buffer.writer())){ .child = buffer.writer(), .limit = limit };
    try std.json.stringify(value, .{}, bounded.writer());
    try buffer.flush();
    file.close();
    closed = true;
    try dir.rename(temporary, target);
    renamed = true;
}

test "bounded JSON writer exact limit normal-byte parity and overflow" {
    const value = .{ .version = 6, .text = "exact UTF-8 ✓ and escaped \"" };
    const expected = try std.json.stringifyAlloc(std.testing.allocator, value, .{});
    defer std.testing.allocator.free(expected);
    var bytes: [256]u8 = undefined;
    var stream = std.io.fixedBufferStream(&bytes);
    var out = BoundedWriter(@TypeOf(stream.writer())){ .child = stream.writer(), .limit = expected.len };
    try std.json.stringify(value, .{}, out.writer());
    try std.testing.expectEqualStrings(expected, stream.getWritten());
    try std.testing.expectEqual(expected.len, out.written);
    try std.testing.expectError(error.SaveTooLarge, out.writer().writeAll("!"));
    try std.testing.expectEqualStrings(expected, stream.getWritten());
    var empty = BoundedWriter(@TypeOf(stream.writer())){ .child = stream.writer(), .limit = 0 };
    try empty.writer().writeAll("");
    try std.testing.expectError(error.SaveTooLarge, empty.writer().writeAll("x"));
}

test "bounded writer propagates partial sink failure without overcount" {
    var bytes: [2]u8 = undefined;
    var stream = std.io.fixedBufferStream(&bytes);
    var out = BoundedWriter(@TypeOf(stream.writer())){ .child = stream.writer(), .limit = 100 };
    try std.testing.expectError(error.NoSpaceLeft, out.writer().writeAll("abcd"));
    try std.testing.expectEqual(@as(usize, 2), out.written);
    try std.testing.expectEqualStrings("ab", stream.getWritten());
}

test "atomic JSON overflow retains previous bytes and removes temporary" {
    var tmp = std.testing.tmpDir(.{}); defer tmp.cleanup();
    try tmp.dir.writeFile(.{ .sub_path = "world.json", .data = "previous exact save" });
    const value = .{ .version = 6, .text = "new saved value" };
    const expected = try std.json.stringifyAlloc(std.testing.allocator, value, .{}); defer std.testing.allocator.free(expected);
    try std.testing.expectError(error.SaveTooLarge, writeJsonAtomic(tmp.dir, "world.json", "world.tmp", value, expected.len - 1));
    const old = try tmp.dir.readFileAlloc(std.testing.allocator, "world.json", 1000); defer std.testing.allocator.free(old);
    try std.testing.expectEqualStrings("previous exact save", old);
    try std.testing.expectError(error.FileNotFound, tmp.dir.openFile("world.tmp", .{}));
    try writeJsonAtomic(tmp.dir, "world.json", "world.tmp", value, expected.len);
    const actual = try tmp.dir.readFileAlloc(std.testing.allocator, "world.json", expected.len); defer std.testing.allocator.free(actual);
    try std.testing.expectEqualStrings(expected, actual);
    try std.testing.expectError(error.FileNotFound, tmp.dir.openFile("world.tmp", .{}));
}

test "atomic JSON open and rename failures retain destination and clean temporary" {
    var tmp = std.testing.tmpDir(.{}); defer tmp.cleanup();
    try tmp.dir.writeFile(.{ .sub_path = "world.json", .data = "old" });
    try std.testing.expectError(error.FileNotFound, writeJsonAtomic(tmp.dir, "world.json", "missing/world.tmp", .{ .x = 1 }, 100));
    const old = try tmp.dir.readFileAlloc(std.testing.allocator, "world.json", 100); defer std.testing.allocator.free(old);
    try std.testing.expectEqualStrings("old", old);
    try tmp.dir.makeDir("target-directory");
    if (writeJsonAtomic(tmp.dir, "target-directory", "world.tmp", .{ .x = 1 }, 100)) |_| return error.ExpectedRenameFailure else |_| {}
    try std.testing.expectError(error.FileNotFound, tmp.dir.openFile("world.tmp", .{}));
    var preserved = try tmp.dir.openDir("target-directory", .{}); preserved.close();
}

test "atomic JSON serialization failure cleans partial temporary without replacing canonical" {
    const Fails = struct {
        pub fn jsonStringify(_: @This(), writer: anytype) !void {
            try writer.beginObject();
            try writer.objectField("partial");
            try writer.write("new data");
            return error.InputOutput;
        }
    };
    var tmp = std.testing.tmpDir(.{}); defer tmp.cleanup();
    try tmp.dir.writeFile(.{ .sub_path = "world.json", .data = "canonical" });
    try std.testing.expectError(error.InputOutput, writeJsonAtomic(tmp.dir, "world.json", "world.tmp", Fails{}, 1000));
    const old = try tmp.dir.readFileAlloc(std.testing.allocator, "world.json", 100); defer std.testing.allocator.free(old);
    try std.testing.expectEqualStrings("canonical", old);
    try std.testing.expectError(error.FileNotFound, tmp.dir.openFile("world.tmp", .{}));
}

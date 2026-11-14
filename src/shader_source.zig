//! Shader dialect adaptation for the browser port. This does not supply a
//! browser renderer: windowing, GL bindings, assets and scheduling remain work.
const std = @import("std");

/// The caller owns the returned zero-terminated source. Desktop text is kept
/// byte-for-byte; the WebGL2 path uses GLSL ES 3.00 and explicit precision.
pub fn prepare(allocator: std.mem.Allocator, source: []const u8, webgl: bool) ![:0]u8 {
    if (!webgl) return allocator.dupeZ(u8, source);
    const desktop_header = "#version 330 core\n";
    if (!std.mem.startsWith(u8, source, desktop_header)) return error.UnsupportedShaderVersion;
    return std.fmt.allocPrintZ(
        allocator,
        "#version 300 es\nprecision highp float;\nprecision highp int;\n{s}",
        .{source[desktop_header.len..]},
    );
}

test "native source is unchanged" {
    const source = "#version 330 core\nvoid main() {}\n";
    const result = try prepare(std.testing.allocator, source, false);
    defer std.testing.allocator.free(result);
    try std.testing.expectEqualStrings(source, result);
}

test "browser source uses ES and explicit precision" {
    const result = try prepare(std.testing.allocator, "#version 330 core\nvoid main() {}", true);
    defer std.testing.allocator.free(result);
    try std.testing.expectEqualStrings("#version 300 es\nprecision highp float;\nprecision highp int;\nvoid main() {}", result);
}

test "reject unrecognized source rather than silently damaging it" {
    try std.testing.expectError(error.UnsupportedShaderVersion, prepare(std.testing.allocator, "void main() {}", true));
}

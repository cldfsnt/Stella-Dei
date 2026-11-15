//! Fixed real-topology kernel audit, not an ecology run or calibrated flight model.
const std = @import("std");
const W = @import("experimental/wind_dispersal.zig");
const Graph = struct { points: [][3]f32, neighbors: [][6]u32 };
pub fn main() !void {
    const a = std.heap.page_allocator;
    const args = try std.process.argsAlloc(a);
    defer std.process.argsFree(a, args);
    if (args.len != 2) return error.ExpectedGraph;
    const bytes = try std.fs.cwd().readFileAlloc(a, args[1], 32 * 1024 * 1024);
    defer a.free(bytes);
    const parsed = try std.json.parseFromSlice(Graph, a, bytes, .{});
    defer parsed.deinit();
    const g = parsed.value;
    if (g.points.len != 40962 or g.neighbors.len != g.points.len) return error.UnexpectedTopology;
    var success: usize = 0;
    var refused: usize = 0;
    var max_hops: usize = 0;
    var max_evaluations: usize = 0;
    for (0..64) |which| {
        const source = which * (g.points.len - 1) / 63;
        const p = g.points[source];
        const wind: [3]f64 = if (@abs(p[2]) < 0.99) .{ -@as(f64, p[1]), p[0], 0 } else .{ 0, -@as(f64, p[2]), p[1] };
        for ([_]f64{ 0, 0.5, 0.9, 0.999 }) |u| {
            const t = W.route(g.points, g.neighbors, source, wind, 5000, u) catch |err| {
                refused += 1;
                std.debug.print("REFUSED {d} {d} {s}\n", .{ source, u, @errorName(err) });
                continue;
            };
            if (t.index == source or t.index >= g.points.len or t.hops > W.max_hops or t.neighbor_evaluations > 6 * W.max_hops or t.distance_km <= 0 or t.distance_km > std.math.pi * 5000 or t.survival < 0 or t.survival > 1) return error.InvalidReceipt;
            const repeat = try W.route(g.points, g.neighbors, source, wind, 5000, u);
            try std.testing.expectEqualDeep(t, repeat);
            success += 1;
            max_hops = @max(max_hops, t.hops);
            max_evaluations = @max(max_evaluations, t.neighbor_evaluations);
            std.debug.print("ROUTE ", .{});
            const out = std.io.getStdErr().writer();
            try std.json.stringify(.{ .source = source, .u = u, .target = t }, .{}, out);
            try out.writeByte('\n');
        }
    }
    std.debug.print("SUMMARY success={d} refused={d} max_hops={d} max_neighbor_evaluations={d}\n", .{ success, refused, max_hops, max_evaluations });
}

//! Pure bounded wind-direction routing. Distances/radius in km; no resource or RNG writes.
const std = @import("std");
pub const max_hops: usize = 256;
pub const Target = struct { index: usize, requested_km: f64, distance_km: f64, survival: f64, hops: usize, neighbor_evaluations: usize };
pub const Error = error{ InvalidInput, InvalidGeometry, InvalidTopology, Calm, SameCell, HopLimit };
fn dot(a: [3]f64, b: [3]f64) f64 {
    @setFloatMode(.strict);
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
}
fn cross(a: [3]f64, b: [3]f64) [3]f64 {
    @setFloatMode(.strict);
    return .{ a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0] };
}
fn norm(a: [3]f64) Error![3]f64 {
    @setFloatMode(.strict);
    var scale: f64 = 0;
    for (a) |v| {
        if (!std.math.isFinite(v)) return error.InvalidGeometry;
        scale = @max(scale, @abs(v));
    }
    if (scale == 0) return error.InvalidGeometry;
    const b = [3]f64{ a[0] / scale, a[1] / scale, a[2] / scale };
    const length = @sqrt(dot(b, b));
    return .{ b[0] / length, b[1] / length, b[2] / length };
}
fn direction(point: anytype) Error![3]f64 {
    @setFloatMode(.strict);
    const p = if (@typeInfo(@TypeOf(point)) == .Struct) point.data else point;
    return norm(.{ @floatCast(p[0]), @floatCast(p[1]), @floatCast(p[2]) });
}
pub fn sampleDistance(radius_km: f64, u: f64) Error!f64 {
    @setFloatMode(.strict);
    if (!std.math.isFinite(radius_km) or radius_km <= 0 or !std.math.isFinite(u) or u < 0 or u >= 1) return error.InvalidInput;
    const maximum = @min(5000.0, 0.9 * std.math.pi * radius_km);
    if (!std.math.isFinite(maximum) or maximum < 100) return error.InvalidInput;
    const ratio = 100 / maximum;
    const denominator = 1 - u * (1 - ratio * @sqrt(ratio));
    const distance = 100 / std.math.pow(f64, denominator, 2.0 / 3.0);
    if (!std.math.isFinite(distance)) return error.InvalidInput;
    return std.math.clamp(distance, 100, maximum);
}
/// Existing Vec3 and plain [3] float arrays accepted without copying a world.
/// Read only current donor wind; no cached-wind freshness assumption.
pub fn route(points: anytype, neighbors: anytype, source: usize, wind: [3]f64, radius_km: f64, u: f64) Error!Target {
    @setFloatMode(.strict);
    const distance = try sampleDistance(radius_km, u);
    if (points.len == 0 or points.len != neighbors.len or source >= points.len) return error.InvalidInput;
    const normal = try direction(points[source]);
    var wind_scale: f64 = 0;
    for (wind) |v| {
        if (!std.math.isFinite(v)) return error.InvalidInput;
        wind_scale = @max(wind_scale, @abs(v));
    }
    if (wind_scale == 0) return error.Calm;
    const w = [3]f64{ wind[0] / wind_scale, wind[1] / wind_scale, wind[2] / wind_scale };
    // Double cross produces a tangent vector without cancellation of radial magnitude.
    const tangent = norm(cross(cross(normal, w), normal)) catch return error.Calm;
    const angle = distance / radius_km;
    const c = @cos(angle);
    const s = @sin(angle);
    const target = try norm(.{ c * normal[0] + s * tangent[0], c * normal[1] + s * tangent[1], c * normal[2] + s * tangent[2] });
    return walk(points, neighbors, source, normal, target, radius_km, distance);
}
fn walk(points: anytype, neighbors: anytype, source: usize, normal: [3]f64, target: [3]f64, radius: f64, requested: f64) Error!Target {
    @setFloatMode(.strict);
    var current = source;
    var score = dot(normal, target);
    var hops: usize = 0;
    var evaluated: usize = 0;
    while (hops < max_hops) {
        var best = current;
        var best_score = score;
        const row = neighbors[current];
        for (row, 0..) |raw, k| {
            const next: usize = @intCast(raw);
            if (next >= points.len) return error.InvalidTopology;
            if (next == current) continue;
            var duplicate = false;
            for (row[0..k]) |prior| {
                if (prior == raw) duplicate = true;
            }
            if (duplicate) continue;
            evaluated += 1;
            const candidate = dot(try direction(points[next]), target);
            if (candidate > best_score or (candidate == best_score and candidate > score and next < best)) {
                best = next;
                best_score = candidate;
            }
        }
        if (best == current) {
            if (current == source) return error.SameCell;
            const end = try direction(points[current]);
            const cr = cross(normal, end);
            const angle = std.math.atan2(@sqrt(dot(cr, cr)), std.math.clamp(dot(normal, end), -1, 1));
            const actual = radius * angle;
            if (!std.math.isFinite(actual) or actual <= 0) return error.InvalidGeometry;
            return .{ .index = current, .requested_km = requested, .distance_km = actual, .survival = @exp(-actual / 1000), .hops = hops, .neighbor_evaluations = evaluated };
        }
        current = best;
        score = best_score;
        hops += 1;
    }
    return error.HopLimit;
}

test "fixed distance bounds and invalid inputs" {
    try std.testing.expectEqual(@as(f64, 100), try sampleDistance(5000, 0));
    const far = try sampleDistance(5000, 0.999999999);
    try std.testing.expect(far > 4900 and far <= 5000);
    try std.testing.expectError(error.InvalidInput, sampleDistance(10, 0));
    try std.testing.expectError(error.InvalidInput, sampleDistance(5000, 1));
    try std.testing.expectError(error.InvalidInput, sampleDistance(5000, std.math.nan(f64)));
}
test "ties padding order and purity" {
    const p = [_][3]f64{ .{ 1, 0, 0 }, .{ 0, 1, 0 }, .{ 0, 1, 0 } };
    var n = [_][6]u32{ .{ 2, 0, 1, 2, 0, 1 }, .{ 0, 1, 1, 1, 1, 1 }, .{ 0, 2, 2, 2, 2, 2 } };
    const before = n;
    const t = try walk(&p, &n, 0, .{ 1, 0, 0 }, .{ 0, 1, 0 }, 5000, 100);
    try std.testing.expectEqual(@as(usize, 1), t.index);
    try std.testing.expectEqualDeep(before, n);
    n[0] = .{ 1, 2, 0, 1, 2, 0 };
    try std.testing.expectEqualDeep(t, try walk(&p, &n, 0, .{ 1, 0, 0 }, .{ 0, 1, 0 }, 5000, 100));
    try std.testing.expectError(error.Calm, route(&p, &n, 0, .{ 0, 0, 0 }, 5000, 0));
    try std.testing.expectError(error.Calm, route(&p, &n, 0, .{ 1, 0, 0 }, 5000, 0));
    try std.testing.expectError(error.InvalidInput, route(&p, &n, 0, .{ std.math.inf(f64), 0, 0 }, 5000, 0));
    n[0][0] = 99;
    try std.testing.expectError(error.InvalidTopology, route(&p, &n, 0, .{ 0, 1, 0 }, 5000, 0));
}
test "polar wrap near far and hard bound" {
    const count = 1024;
    var p: [count][3]f64 = undefined;
    var n: [count][6]u32 = undefined;
    for (&p, &n, 0..) |*point, *row, i| {
        const a = 2 * std.math.pi * @as(f64, @floatFromInt(i)) / count;
        point.* = .{ @cos(a), @sin(a), 0 };
        row.* = .{ @intCast((i + 1) % count), @intCast((i + count - 1) % count), @intCast(i), @intCast(i), @intCast(i), @intCast(i) };
    }
    const near = try route(&p, &n, count - 1, .{ -p[count - 1][1], p[count - 1][0], 0 }, 5000, 0);
    try std.testing.expect(near.index < 10);
    const far = try route(&p, &n, 0, .{ 0, 1, 0 }, 5000, 0.99);
    try std.testing.expect(far.distance_km > near.distance_km and far.survival < near.survival);
    try std.testing.expectError(error.HopLimit, walk(&p, &n, 0, .{ 1, 0, 0 }, .{ -1, 0, 0 }, 5000, 100));
    for (&p) |*point| {
        const x = point[0];
        point[0] = point[2];
        point[2] = x;
    }
    const polar = try route(&p, &n, 0, .{ 0, 1, 0 }, 5000, 0);
    try std.testing.expect(polar.index > 0);
    p[1][0] = std.math.nan(f64);
    try std.testing.expectError(error.InvalidGeometry, route(&p, &n, 0, .{ 0, 1, 0 }, 5000, 0));
}

test "borrowed Vec3-shaped storage and small-cell refusal" {
    const V = struct { data: [3]f32 };
    const points = [_]V{ .{ .data = .{ 1, 0, 0 } }, .{ .data = .{ 0.9998, 0.02, 0 } } };
    const neighbors = [_][6]u32{ .{ 1, 0, 0, 0, 0, 0 }, .{ 0, 1, 1, 1, 1, 1 } };
    const found = try route(&points, &neighbors, 0, .{ 0, 1, 0 }, 5000, 0);
    try std.testing.expectEqual(@as(usize, 1), found.index);
    try std.testing.expectError(error.InvalidInput, route(&points, &neighbors, 2, .{ 0, 1, 0 }, 5000, 0));
    try std.testing.expectError(error.SameCell, route(&points, &neighbors, 0, .{ 0, -1, 0 }, 5000, 0));
}

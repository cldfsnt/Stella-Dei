//! Pure camera contracts shared by the game and deterministic unit tests.
const std = @import("std");

/// Fit the globe to the narrower screen dimension, including portrait phones.
pub fn globeDistance(radius: f32, aspect: f32) f32 {
    const vertical = std.math.pi / 180.0 * 35.0;
    const horizontal = std.math.atan(@tan(vertical) * @max(0.2, aspect));
    return @min(radius * 4.5, radius / @sin(@min(vertical, horizontal) * 0.85));
}

pub fn zoomDistance(distance: f32, surface_radius: f32, steps: f32) f32 {
    const altitude = @max(100, distance - surface_radius);
    return std.math.clamp(surface_radius + altitude * std.math.pow(f32, 0.55, std.math.clamp(steps, -8, 8)), surface_radius + 100, surface_radius * 5);
}

/// Distance to the near intersection along a normalized world-space ray.
pub fn sphereHit(origin: [3]f32, direction: [3]f32, radius: f32) ?f32 {
    var b: f32 = 0;
    var c: f32 = -radius * radius;
    for (origin, direction) |o, d| {
        b += o * d;
        c += o * o;
    }
    const discriminant = b * b - c;
    if (discriminant < 0) return null;
    const t = -b - @sqrt(discriminant);
    return if (t > 0) t else null;
}

test "zoom tap reduces altitude meaningfully and clamps safely" {
    const first = zoomDistance(12500, 5000, 1);
    try std.testing.expectApproxEqAbs(@as(f32, 9125), first, 0.01);
    try std.testing.expect(zoomDistance(first, 5000, 1) < first);
    try std.testing.expectApproxEqAbs(@as(f32, 12500), zoomDistance(first, 5000, -1), 0.01);
    try std.testing.expectEqual(@as(f32, 5100), zoomDistance(5100, 5000, 8));
    try std.testing.expectEqual(@as(f32, 25000), zoomDistance(24000, 5000, -8));
}

test "planet picking hits front surface and rejects sky" {
    try std.testing.expectApproxEqAbs(@as(f32, 4000), sphereHit(.{ 0, -9000, 0 }, .{ 0, 1, 0 }, 5000).?, 0.01);
    try std.testing.expect(sphereHit(.{ 0, -9000, 0 }, .{ 1, 0, 0 }, 5000) == null);
    try std.testing.expect(sphereHit(.{ 0, -9000, 0 }, .{ 0, -1, 0 }, 5000) == null);
}

test "portrait globe fits horizontal field rather than cropping" {
    try std.testing.expect(globeDistance(5000, 390.0 / 600.0) > globeDistance(5000, 800.0 / 360.0));
    try std.testing.expect(globeDistance(5000, 390.0 / 600.0) < 20000);
}

test "repeated mobile zoom remains bounded and fractional steps compose" {
    var d: f32 = 9000;
    for (0..50) |_| d = zoomDistance(d, 5000, 1);
    try std.testing.expectEqual(@as(f32, 5100), d);
    for (0..50) |_| d = zoomDistance(d, 5000, -1);
    try std.testing.expectEqual(@as(f32, 25000), d);
    const halfway = zoomDistance(9000, 5000, 0.5);
    try std.testing.expectApproxEqAbs(zoomDistance(9000, 5000, 1), zoomDistance(halfway, 5000, 0.5), 0.01);
}

test "picking handles oblique surface hit and near miss" {
    const length: f32 = @sqrt(@as(f32, 34000000));
    const t = sphereHit(.{0,-9000,0}, .{3000/length,5000/length,0}, 5000).?;
    const x = 3000/length*t;
    const y = -9000+5000/length*t;
    try std.testing.expectApproxEqAbs(@as(f32, 25000000), x*x+y*y, 8);
    try std.testing.expect(sphereHit(.{5001,-9000,0}, .{0,1,0}, 5000) == null);
}

//! Physical edit amounts in kilometers, independent of simulation speed.
const std = @import("std");
pub fn amount(tap: bool, elapsed: f32, tap_km: f32, per_second_km: f32) f32 {
    if (tap) return tap_km;
    if (!std.math.isFinite(elapsed)) return 0;
    return std.math.clamp(elapsed, 0, 0.1) * per_second_km;
}
pub fn water(tap: bool, elapsed: f32) f32 { return amount(tap, elapsed, 0.001, 0.005); }
pub fn terrain(tap: bool, elapsed: f32) f32 { return amount(tap, elapsed, 0.1, 0.5); }
test "same two-second gesture at 15 30 60 120 Hz and every simulation speed" {
    for ([_]u32{15,30,60,120}) |fps| {
        for ([_]f32{3600,21600,86400}) |_| {
            var w = water(true,0); var t = terrain(true,0);
            for (0..fps*2) |_| { w += water(false,1/@as(f32,@floatFromInt(fps))); t += terrain(false,1/@as(f32,@floatFromInt(fps))); }
            try std.testing.expectApproxEqAbs(@as(f32,0.011),w,0.000001);
            try std.testing.expectApproxEqAbs(@as(f32,1.1),t,0.00001);
        }
    }
}
test "tap bounded and stalled or invalid elapsed cannot spike brush" {
    try std.testing.expectEqual(@as(f32,0.001),water(true,999));
    try std.testing.expectEqual(@as(f32,0.0005),water(false,999));
    try std.testing.expectEqual(@as(f32,0),water(false,std.math.nan(f32)));
    try std.testing.expectEqual(@as(f32,0),water(false,-1));
}

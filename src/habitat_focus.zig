//! Read-only camera targeting, not habitat creation or a survival guarantee.
const std = @import("std");
pub fn score(biomass: f32, latitude_z: f32, depth_km: f32, temperature: f32, suitable: bool, neighbours: f32) f32 {
    // Avoid the orbit camera's polar up-vector singularity.
    if (@abs(latitude_z) > 0.95) return -1;
    // A dying colony remains discoverable for inspection/rescue.
    if (biomass > 0.000001) return 300 + std.math.clamp(biomass,0,1) * 90;
    if (!suitable) return -1;
    const starter = @abs(latitude_z) < 0.35 and depth_km >= 0.001 and depth_km <= 0.005;
    return (if (starter) @as(f32,200) else 100) + std.math.clamp(neighbours,0,6) + 1 / (1 + @abs(temperature - 303));
}
test "live colonies outrank empty habitat even when unsafe" {
    try std.testing.expect(score(0.0001,0.4,1,220,false,0) > score(0,0.1,0.003,303,true,6));
    try std.testing.expect(score(0.8,0.1,0.003,303,true,0) > score(0.1,0.1,0.003,303,true,6));
}
test "low latitude one to five metres outranks neighbours, with suitable fallback" {
    const preferred=score(0,0.1,0.003,290,true,0);
    try std.testing.expect(preferred > score(0,0.5,0.003,303,true,6));
    try std.testing.expect(preferred > score(0,0.1,0.02,303,true,6));
    try std.testing.expect(score(0,0.5,0.02,290,true,0) > 0);
    try std.testing.expectEqual(@as(f32,-1),score(0,0.1,0,290,false,6));
    try std.testing.expectEqual(@as(f32,-1),score(1,0.99,0.003,290,true,6));
}

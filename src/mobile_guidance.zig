//! Bounded mobile guidance derived from actual habitat state, not tutorial flags.
const std = @import("std");
pub fn rabbitWaterSafe(depth_km: f32) bool {
    return std.math.isFinite(depth_km) and depth_km <= 0.002;
}
pub fn rabbitWarning(depth_km: f32, temperature: f32, food: f32) ?[]const u8 {
    if (!rabbitWaterSafe(depth_km)) return "Too much water: choose dry land";
    if (!std.math.isFinite(temperature) or temperature > 333.15 or temperature < 243.15) return "Extreme temperature: rabbits cannot survive";
    if (food <= 0.01) return "Little food here: plant a patch first";
    return null;
}
pub fn plantWarning(depth_km: f32) ?[]const u8 {
    return if (depth_km > 0.0005) "Flooded: drain water before planting" else null;
}
pub fn nextSpeed(seconds: f32) f32 {
    return if (seconds < 3600) 3600 else if (seconds < 21600) 21600 else if (seconds < 86400) 86400 else 3600;
}
test "placement matches actual two metre drowning limit" {
    try std.testing.expect(rabbitWaterSafe(0));
    try std.testing.expect(rabbitWaterSafe(0.001));
    try std.testing.expect(rabbitWaterSafe(0.002));
    try std.testing.expect(!rabbitWaterSafe(0.00201));
    try std.testing.expect(!rabbitWaterSafe(std.math.nan(f32)));
    try std.testing.expect(rabbitWarning(0,293.15,0.3)==null);
    try std.testing.expect(rabbitWarning(0,293.15,0)!=null);
    try std.testing.expect(rabbitWarning(0,340,0.3)!=null);
}
test "plant flood guidance and speed cycle are bounded" {
    try std.testing.expect(plantWarning(0.00001)==null);
    try std.testing.expect(plantWarning(0.001)!=null);
    try std.testing.expectEqual(@as(f32,21600),nextSpeed(3600));
    try std.testing.expectEqual(@as(f32,86400),nextSpeed(21600));
    try std.testing.expectEqual(@as(f32,3600),nextSpeed(86400));
}

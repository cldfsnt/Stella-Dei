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
pub const default_browser_speed: f32 = 21600;
pub fn speedLabel(seconds: f32) []const u8 {
    return if (seconds == 3600) "1h/s" else if (seconds == 21600) "6h/s" else if (seconds == 86400) "24h/s" else "Custom";
}
pub fn speedHint(seconds: f32, paused: bool) []const u8 {
    if (paused) return "Pace ready; press Play to run";
    return if (seconds == 3600) "Target 1h/s; actual rate depends on device" else if (seconds == 21600) "Target 6h/s; actual rate depends on device" else if (seconds == 86400) "Target 24h/s; actual rate depends on device" else "Custom target; see More > Speed for exact rate";
}
test "pace names describe bounded existing rates" {
    try std.testing.expectEqual(@as(f32,21600),default_browser_speed);
    try std.testing.expectEqualStrings("1h/s",speedLabel(3600));
    try std.testing.expectEqualStrings("6h/s",speedLabel(21600));
    try std.testing.expectEqualStrings("24h/s",speedLabel(86400));
    try std.testing.expectEqualStrings("Custom",speedLabel(7200));
    try std.testing.expectEqualStrings("Custom",speedLabel(43200));
    try std.testing.expectEqualStrings("Pace ready; press Play to run",speedHint(86400,true));
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

//! Small, deterministic plant population model used by the real planet.
//! Traits belong to locally reproducing populations, not an arbitrary global color.
const std = @import("std");
pub const Plant = struct {
    optimum: f32 = 295.15,
    generation: u32 = 0,
};
pub fn fitness(temperature: f32, optimum: f32) f32 {
    return std.math.clamp(1 - @abs(temperature - optimum) / 50, 0, 1);
}
pub fn grow(biomass: f32, temperature: f32, optimum: f32, water_depth_km: f32, light: f32, co2: bool, dt: f32) f32 {
    if (!std.math.isFinite(biomass) or !std.math.isFinite(temperature)) return 0;
    if (water_depth_km > 0.0005) return biomass * @exp(-dt / 12000);
    const suitability = fitness(temperature, optimum);
    // Respiration continues at night, but night is not wholesale plant death.
    const rate = (suitability * (0.3 + 0.7 * light) * @as(f32, if (co2) 1 else 0) * 6 - (1 - suitability) * 3 - 0.15) / 86400;
    if (rate <= 0) return std.math.clamp(biomass * @exp(rate * dt), 0, 1);
    const e = @exp(-rate * dt);
    return std.math.clamp(biomass / @max(0.000001, biomass + (1 - biomass) * e), 0, 1);
}
pub fn offspring(parent: Plant, seed: u64) Plant {
    var rng = std.rand.DefaultPrng.init(seed);
    return .{ .optimum = std.math.clamp(parent.optimum + (rng.random().float(f32) - 0.5) * 6, 260, 330), .generation = parent.generation +| 1 };
}
test "plants thrive, grazed cover regrows, and water/heat kill" {
    try std.testing.expect(grow(0.2, 295.15, 295.15, 0, 1, true, 86400) > 0.9);
    try std.testing.expect(grow(0.2, 295.15, 295.15, 0.00001, 1, true, 86400) > 0.9); // 1cm rain is not a flood
    try std.testing.expect(grow(0.2, 295.15, 295.15, 0, 0, true, 86400) > 0.2);
    try std.testing.expect(grow(1, 295.15, 295.15, 10, 1, true, 86400) < 0.001);
    try std.testing.expect(grow(1, 380, 295.15, 0, 1, true, 86400) < 0.1);
}
test "offspring inherit with variation and selection favors local adaptation" {
    const p: Plant = .{};
    const child = offspring(p, 42);
    try std.testing.expectEqual(@as(u32, 1), child.generation);
    try std.testing.expect(child.optimum != p.optimum);
    try std.testing.expect(@abs(child.optimum - p.optimum) <= 3);
    try std.testing.expect(fitness(310, 308) > fitness(310, 295));
}

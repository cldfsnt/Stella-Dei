//! Explicit one-cell exposed-detritus oxidation, not wildfire.
//! Pure inventory primitive: no biology edits, propagation, ignition threshold or seeds.
//! Inputs/output inventories are per square metre; gas fields are carbon-equivalent.
const std = @import("std");
pub const temperature_ceiling: f64 = 500;
/// Gameplay calibration, NOT a measured fuel composition or scientific constant.
pub const gameplay_heat_per_kg_carbon: f64 = 30_000_000;
pub const Reservoir = struct { oxygen_carbon: f64, carbon_dioxide_carbon: f64, temperature_k: f64 };
pub const Input = struct { depth_m: f64, heat_capacity_per_area: f64, heat_per_kg_carbon: f64 = gameplay_heat_per_kg_carbon };
pub const Failure = enum { none, invalid, wet, no_fuel, no_oxygen, heat_limit, precision };
pub const Receipt = struct {
    failure: Failure = .none,
    burned_carbon: f64 = 0,
    oxygen_mass_consumed: f64 = 0,
    carbon_dioxide_mass_added: f64 = 0,
    heat_per_area: f64 = 0,
    temperature_delta: f64 = 0,
    pub fn success(self: Receipt) bool {
        return self.failure == .none and self.burned_carbon > 0;
    }
};
fn failed(reason: Failure) Receipt {
    return .{ .failure = reason };
}
fn closeTransfer(actual: f64, wanted: f64) bool {
    return std.math.isFinite(actual) and @abs(actual - wanted) <= wanted * 1e-9;
}
/// Only detritus and explicitly supplied gas/thermal reservoirs can change.
/// Caller must supply a real finite oxygen allocation and commit its own ledger.
/// Detrital nutrients were already released on mortality: do not release them again.
pub fn ignite(detritus: *f32, reservoir: *Reservoir, input: Input) Receipt {
    return calculate(detritus, reservoir, input, true);
}
pub fn preview(detritus: *f32, reservoir: *Reservoir, input: Input) Receipt {
    return calculate(detritus, reservoir, input, false);
}
fn calculate(detritus: *f32, reservoir: *Reservoir, input: Input, apply: bool) Receipt {
    const old: f64 = detritus.*;
    const r = reservoir.*;
    if (!std.math.isFinite(old) or old < 0 or !std.math.isFinite(r.oxygen_carbon) or r.oxygen_carbon < 0 or
        !std.math.isFinite(r.carbon_dioxide_carbon) or r.carbon_dioxide_carbon < 0 or
        !std.math.isFinite(r.temperature_k) or r.temperature_k < 0 or
        !std.math.isFinite(input.depth_m) or input.depth_m < 0 or
        !std.math.isFinite(input.heat_capacity_per_area) or input.heat_capacity_per_area <= 0 or
        !std.math.isFinite(input.heat_per_kg_carbon) or input.heat_per_kg_carbon <= 0) return failed(.invalid);
    if (input.depth_m > 0) return failed(.wet);
    if (old == 0) return failed(.no_fuel);
    if (r.oxygen_carbon == 0) return failed(.no_oxygen);
    if (r.temperature_k >= temperature_ceiling) return failed(.heat_limit);
    const thermal_budget = (temperature_ceiling - r.temperature_k) * input.heat_capacity_per_area / input.heat_per_kg_carbon;
    if (!std.math.isFinite(thermal_budget) or thermal_budget <= 0) return failed(.invalid);
    const budget = @min(old, @min(r.oxygen_carbon, thermal_budget));
    // Round remaining f32 fuel UP if necessary; never overspend O2/heat budget.
    var remaining: f32 = @floatCast(old - budget);
    if (old - @as(f64, remaining) > budget) remaining = std.math.nextAfter(f32, remaining, detritus.*);
    const burned = old - @as(f64, remaining);
    if (burned <= 0 or burned > budget) return failed(.precision);
    const next_oxygen = r.oxygen_carbon - burned;
    const next_carbon_dioxide = r.carbon_dioxide_carbon + burned;
    const heat = burned * input.heat_per_kg_carbon;
    const next_temperature = r.temperature_k + heat / input.heat_capacity_per_area;
    if (!std.math.isFinite(heat) or heat <= 0 or next_oxygen < 0 or !std.math.isFinite(next_temperature) or next_temperature > temperature_ceiling or
        !closeTransfer(r.oxygen_carbon - next_oxygen, burned) or !closeTransfer(next_carbon_dioxide - r.carbon_dioxide_carbon, burned) or
        !closeTransfer((next_temperature - r.temperature_k) * input.heat_capacity_per_area, heat)) return failed(.precision);
    const result = Receipt{ .burned_carbon = burned, .oxygen_mass_consumed = burned * (32.0 / 12.0), .carbon_dioxide_mass_added = burned * (44.0 / 12.0), .heat_per_area = heat, .temperature_delta = next_temperature - r.temperature_k };
    if (apply) {
        detritus.* = remaining;
        reservoir.* = .{ .oxygen_carbon = next_oxygen, .carbon_dioxide_carbon = next_carbon_dioxide, .temperature_k = next_temperature };
    }
    return result;
}

test "fuel oxidation conserves carbon oxygen nutrients and unrelated living state" {
    var cell = struct { detritus: f32 = 0.25, nutrient: f32 = 0.03, live_biomass: f32 = 0.4, support: f32 = 0.1, rng: u64 = 123, lineage: u64 = 77 }{};
    const original = cell;
    var r = Reservoir{ .oxygen_carbon = 1, .carbon_dioxide_carbon = 2, .temperature_k = 300 };
    const before = r;
    const input = Input{ .depth_m = 0, .heat_capacity_per_area = 400_000 };
    const predicted = preview(&cell.detritus, &r, input);
    try std.testing.expectEqualDeep(original, cell);
    try std.testing.expectEqualDeep(before, r);
    const receipt = ignite(&cell.detritus, &r, input);
    try std.testing.expectEqualDeep(predicted, receipt);
    try std.testing.expect(receipt.success());
    try std.testing.expectEqual(@as(f64, 0.25), receipt.burned_carbon);
    try std.testing.expectApproxEqAbs(receipt.burned_carbon + receipt.oxygen_mass_consumed, receipt.carbon_dioxide_mass_added, 1e-12);
    try std.testing.expectApproxEqAbs(before.carbon_dioxide_carbon + original.detritus, r.carbon_dioxide_carbon + cell.detritus, 1e-12);
    try std.testing.expectApproxEqAbs(before.oxygen_carbon - r.oxygen_carbon, receipt.burned_carbon, 1e-12);
    try std.testing.expectApproxEqAbs(receipt.heat_per_area, receipt.temperature_delta * input.heat_capacity_per_area, 1e-8);
    cell.detritus = original.detritus;
    try std.testing.expectEqualDeep(original, cell);
}
test "oxygen and thermal caps leave unburned fuel without discarding heat" {
    for (0..2) |kind| {
        var fuel: f32 = 1;
        var r = Reservoir{ .oxygen_carbon = if (kind == 0) 0.1 else 10, .carbon_dioxide_carbon = 0, .temperature_k = if (kind == 0) 300 else 499 };
        const before = r;
        const receipt = ignite(&fuel, &r, .{ .depth_m = 0, .heat_capacity_per_area = 400_000 });
        try std.testing.expect(receipt.success() and fuel > 0 and r.oxygen_carbon >= 0 and r.temperature_k <= 500);
        try std.testing.expect(receipt.burned_carbon <= before.oxygen_carbon);
        try std.testing.expectApproxEqAbs(@as(f64, 1), @as(f64, fuel) + r.carbon_dioxide_carbon, 1e-12);
        try std.testing.expectApproxEqAbs(receipt.heat_per_area, receipt.temperature_delta * 400_000, 1e-7);
    }
}
test "repetition cannot consume absent fuel or oxygen and never resurrects fuel" {
    var fuel: f32 = 0.1;
    var r = Reservoir{ .oxygen_carbon = 1, .carbon_dioxide_carbon = 0, .temperature_k = 300 };
    try std.testing.expect(ignite(&fuel, &r, .{ .depth_m = 0, .heat_capacity_per_area = 400_000 }).success());
    const before = r;
    for (0..100) |_| try std.testing.expectEqual(Failure.no_fuel, ignite(&fuel, &r, .{ .depth_m = 0, .heat_capacity_per_area = 400_000 }).failure);
    try std.testing.expectEqualDeep(before, r);
    try std.testing.expectEqual(@as(f32, 0), fuel);
    fuel = 0.1;
    r.oxygen_carbon = 0;
    const no_oxygen = r;
    try std.testing.expectEqual(Failure.no_oxygen, ignite(&fuel, &r, .{ .depth_m = 0, .heat_capacity_per_area = 400_000 }).failure);
    try std.testing.expectEqualDeep(no_oxygen, r);
    try std.testing.expectEqual(@as(f32, 0.1), fuel);
}
test "wet invalid nonfinite and subresolution inputs refuse atomically" {
    for (0..15) |which| {
        var fuel: f32 = 1;
        var r = Reservoir{ .oxygen_carbon = 1, .carbon_dioxide_carbon = 0, .temperature_k = 300 };
        var input = Input{ .depth_m = 0, .heat_capacity_per_area = 400_000 };
        switch (which) {
            0 => input.depth_m = 0.001,
            1 => input.depth_m = -1,
            2 => input.depth_m = std.math.nan(f64),
            3 => input.heat_capacity_per_area = 0,
            4 => input.heat_per_kg_carbon = std.math.inf(f64),
            5 => r.oxygen_carbon = -1,
            6 => r.carbon_dioxide_carbon = std.math.inf(f64),
            7 => r.temperature_k = std.math.nan(f64),
            8 => fuel = -1,
            9 => fuel = std.math.nan(f32),
            10 => r.temperature_k = 500,
            11 => r.oxygen_carbon = 1e-20,
            12 => r.carbon_dioxide_carbon = 1e30,
            13 => input.heat_capacity_per_area = 1e30,
            14 => {
                fuel = 0.1;
                input.heat_per_kg_carbon = 5e-324;
            },
            else => unreachable,
        }
        const before = r;
        const old = fuel;
        const receipt = ignite(&fuel, &r, input);
        try std.testing.expect(!receipt.success());
        try std.testing.expectEqualSlices(u8, std.mem.asBytes(&before), std.mem.asBytes(&r));
        try std.testing.expectEqual(@as(u32, @bitCast(old)), @as(u32, @bitCast(fuel)));
    }
}
test "deterministic bounded parameter sweep closes ledgers" {
    var successes: usize = 0;
    for (1..101) |i| {
        var fuel: f32 = @as(f32, @floatFromInt(i)) / 73;
        var r = Reservoir{ .oxygen_carbon = @as(f64, @floatFromInt(i % 11)) / 7, .carbon_dioxide_carbon = 0.3, .temperature_k = 290 + @as(f64, @floatFromInt(i)) };
        const before = r;
        const old: f64 = fuel;
        const input = Input{ .depth_m = 0, .heat_capacity_per_area = 385_910 };
        const receipt = ignite(&fuel, &r, input);
        if (receipt.success()) {
            successes += 1;
            try std.testing.expectApproxEqAbs(old + before.carbon_dioxide_carbon, @as(f64, fuel) + r.carbon_dioxide_carbon, 1e-12);
            try std.testing.expectApproxEqAbs(before.oxygen_carbon - r.oxygen_carbon, receipt.burned_carbon, 1e-12);
            try std.testing.expectApproxEqAbs((r.temperature_k - before.temperature_k) * input.heat_capacity_per_area, receipt.heat_per_area, 1e-6);
            try std.testing.expect(fuel >= 0 and r.oxygen_carbon >= 0 and r.temperature_k <= temperature_ceiling);
        } else {
            try std.testing.expectEqualDeep(before, r);
            try std.testing.expectEqual(old, @as(f64, fuel));
        }
    }
    try std.testing.expect(successes >= 90);
}

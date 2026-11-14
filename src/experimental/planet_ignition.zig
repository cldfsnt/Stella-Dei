//! EXPERIMENT ONLY. Actual Planet accounting adapter; not wired to gameplay.
const std = @import("std");
const P = @import("../simulation/planet.zig").Planet;
const M = @import("../simulation/microbes.zig");
const Burn = @import("detritus_ignition.zig");
pub const Failure = enum { none, invalid, stale, mode, wet, no_fuel, no_oxygen, heat_limit, precision };
pub const Receipt = struct {
    failure: Failure = .none,
    cell: usize = 0,
    burned_carbon_per_area: f64 = 0,
    burned_carbon_kg: f64 = 0,
    oxygen_allocation_carbon_per_area: f64 = 0,
    oxygen_consumed_kg: f64 = 0,
    oxygen_ideal_kg: f64 = 0,
    oxygen_rounding_kg: f64 = 0,
    oxygen_rounding_budget_kg: f64 = 0,
    carbon_dioxide_added_kg: f64 = 0,
    carbon_dioxide_ideal_kg: f64 = 0,
    carbon_dioxide_rounding_kg: f64 = 0,
    carbon_dioxide_rounding_budget_kg: f64 = 0,
    fuel_heat_joules: f64 = 0,
    stored_heat_joules: f64 = 0,
    /// Signed numerical residual, not a modeled physical heat sink/source.
    thermal_rounding_joules: f64 = 0,
    temperature_delta: f64 = 0,
    pub fn success(self: Receipt) bool {
        return self.failure == .none and self.burned_carbon_kg > 0;
    }
};
fn fail(reason: Failure, cell: usize) Receipt {
    return .{ .failure = reason, .cell = cell };
}
fn ulp(value: f64) f64 {
    return @max(std.math.nextAfter(f64, value, std.math.inf(f64)) - value, value - std.math.nextAfter(f64, value, -std.math.inf(f64)));
}
/// Bound the rounded division, average update, delta subtraction and scaling.
/// One full ULP per operation conservatively covers half-ULP rounding plus
/// bound evaluation. Directed O2 correction adds one more average ULP.
/// Never allow numerical uncertainty above one part per million of the event.
fn transferBudget(before: f64, after: f64, intended: f64, normalization: f64, directed: bool) f64 {
    const difference = @abs(before - after);
    const actual = difference * normalization;
    const bound = (ulp(intended / normalization) + ulp(after) * (if (directed) @as(f64, 2) else 1) + ulp(difference)) * normalization + ulp(actual) + ulp(intended);
    return @min(bound, intended * 0.000001);
}
fn transferMatches(actual: f64, intended: f64, budget: f64) bool {
    return std.math.isFinite(actual) and actual > 0 and std.math.isFinite(budget) and budget > 0 and @abs(actual - intended) <= budget;
}
pub fn ignite(p: *P, expected: usize, selected: usize) Receipt {
    return calculate(p, expected, selected, true);
}
pub fn preview(p: *P, expected: usize, selected: usize) Receipt {
    return calculate(p, expected, selected, false);
}
fn calculate(p: *P, expected: usize, selected: usize, apply: bool) Receipt {
    if (expected != selected) return fail(.stale, selected);
    if (p.worldMode != .origin) return fail(.mode, selected);
    const n = p.vertices.len;
    if (n == 0 or p.microbeCells.len != n or p.temperature.len != n or p.waterMass.len != n or selected >= n or
        !std.math.isFinite(p.radius) or p.radius <= 0) return fail(.invalid, selected);
    const area: f64 = p.getMeanPointArea();
    const heat_capacity = p.currentHeatCapacity(selected);
    const water = p.waterMass[selected];
    if (!std.math.isFinite(area) or area <= 0 or !std.math.isFinite(heat_capacity) or heat_capacity <= 0 or
        !std.math.isFinite(water) or water < 0 or !M.validCell(p.microbeCells[selected], p.microbeStats.next_lineage) or
        !std.math.isFinite(p.averageOxygenMass) or p.averageOxygenMass < 0 or
        !std.math.isFinite(p.averageCarbonDioxideMass) or p.averageCarbonDioxideMass < 0) return fail(.invalid, selected);
    if (water > 0) return fail(.wet, selected);
    const old_temperature: f64 = p.temperature[selected];
    const oxygen_allocation = p.averageOxygenMass * 1e9 / area * (12.0 / 32.0);
    var local = Burn.Reservoir{ .oxygen_carbon = oxygen_allocation, .carbon_dioxide_carbon = p.averageCarbonDioxideMass * 1e9 / area * (12.0 / 44.0), .temperature_k = old_temperature };
    var fuel = p.microbeCells[selected].detritus;
    const result = Burn.ignite(&fuel, &local, .{ .depth_m = 0, .heat_capacity_per_area = heat_capacity / area });
    if (!result.success()) return fail(switch (result.failure) {
        .none => .invalid,
        .invalid => .invalid,
        .wet => .wet,
        .no_fuel => .no_fuel,
        .no_oxygen => .no_oxygen,
        .heat_limit => .heat_limit,
        .precision => .precision,
    }, selected);
    const burned_kg = result.burned_carbon * area;
    const oxygen_kg = burned_kg * (32.0 / 12.0);
    const carbon_dioxide_kg = burned_kg * (44.0 / 12.0);
    // Stored atmosphere is AVERAGE 1e9kg per patch, not total planetary mass.
    const normalization = 1e9 * @as(f64, @floatFromInt(n));
    var next_oxygen = p.averageOxygenMass - oxygen_kg / normalization;
    // A round-to-nearest subtraction may spend slightly more than the patch's
    // allocation. Move one representable average toward the old value instead.
    const allocation_kg = p.averageOxygenMass * 1e9;
    var directed = false;
    if ((p.averageOxygenMass - next_oxygen) * normalization > allocation_kg) {
        next_oxygen = std.math.nextAfter(f64, next_oxygen, p.averageOxygenMass);
        directed = true;
    }
    const next_carbon_dioxide = p.averageCarbonDioxideMass + carbon_dioxide_kg / normalization;
    const next_temperature: f32 = @floatCast(local.temperature_k);
    const fuel_heat = result.heat_per_area * area;
    const stored_heat = (@as(f64, next_temperature) - old_temperature) * heat_capacity;
    const rounding = fuel_heat - stored_heat;
    const actual_oxygen = (p.averageOxygenMass - next_oxygen) * normalization;
    const actual_co2 = (next_carbon_dioxide - p.averageCarbonDioxideMass) * normalization;
    const oxygen_budget = transferBudget(p.averageOxygenMass, next_oxygen, oxygen_kg, normalization, directed);
    const co2_budget = transferBudget(p.averageCarbonDioxideMass, next_carbon_dioxide, carbon_dioxide_kg, normalization, false);
    if (next_oxygen < 0 or actual_oxygen > allocation_kg or !std.math.isFinite(next_temperature) or next_temperature > Burn.temperature_ceiling or stored_heat <= 0 or
        !std.math.isFinite(fuel_heat) or !std.math.isFinite(stored_heat) or @abs(rounding) > fuel_heat * 0.0001 or
        !transferMatches(actual_oxygen, oxygen_kg, oxygen_budget) or
        !transferMatches(actual_co2, carbon_dioxide_kg, co2_budget)) return fail(.precision, selected);
    const receipt = Receipt{ .cell = selected, .burned_carbon_per_area = result.burned_carbon, .burned_carbon_kg = burned_kg, .oxygen_allocation_carbon_per_area = oxygen_allocation, .oxygen_consumed_kg = actual_oxygen, .oxygen_ideal_kg = oxygen_kg, .oxygen_rounding_kg = actual_oxygen - oxygen_kg, .oxygen_rounding_budget_kg = oxygen_budget, .carbon_dioxide_added_kg = actual_co2, .carbon_dioxide_ideal_kg = carbon_dioxide_kg, .carbon_dioxide_rounding_kg = actual_co2 - carbon_dioxide_kg, .carbon_dioxide_rounding_budget_kg = co2_budget, .fuel_heat_joules = fuel_heat, .stored_heat_joules = stored_heat, .thermal_rounding_joules = rounding, .temperature_delta = @as(f64, next_temperature) - old_temperature };
    if (apply) {
        p.microbeCells[selected].detritus = fuel;
        p.temperature[selected] = next_temperature;
        p.averageOxygenMass = next_oxygen;
        p.averageCarbonDioxideMass = next_carbon_dioxide;
    }
    // Deliberately no recycled_carbon or other ecology stats increment. This
    // experimental explicit receipt is the only event ledger; no saved counter.
    return receipt;
}

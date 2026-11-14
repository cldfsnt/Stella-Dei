//! Controlled real Planet fixture, no production imports of experimental ignition.
const std = @import("std");
const P = @import("simulation/planet.zig").Planet;
const M = @import("simulation/microbes.zig");
const Fire = @import("experimental/planet_ignition.zig");
const V = @import("zalgebra").Vec3;
const N = 7;
const A = std.testing.allocator;
fn init() !P {
    return initCount(N);
}
fn initCount(n: usize) !P {
    var p: P = undefined;
    p.simulationArena = std.heap.ArenaAllocator.init(A);
    errdefer p.simulationArena.deinit();
    const a = p.simulationArena.allocator();
    p.radius = 100;
    p.worldMode = .origin;
    p.vertices = try a.alloc(V, n);
    @memset(p.vertices, V.new(1, 0, 0));
    p.microbeCells = try a.alloc(M.Cell, n);
    p.microbeStats = .{ .next_lineage = n + 10, .births = 7, .recycled_carbon = 8 };
    p.temperature = try a.alloc(f32, n);
    @memset(p.temperature, 300);
    p.waterMass = try a.alloc(f32, n);
    @memset(p.waterMass, 0);
    for (p.microbeCells, 0..) |*cell, i| {
        cell.* = M.initialized(i + 1);
        cell.detritus = 0.25;
        cell.cohorts[0] = .{ .biomass = 0.1, .support_mass = 0.01, .lineage = i + 1 };
    }
    const area: f64 = p.getMeanPointArea();
    p.averageOxygenMass = area / 1e9 * (32.0 / 12.0);
    p.averageCarbonDioxideMass = area / 1e9 * (44.0 / 12.0);
    return p;
}
const Snapshot = struct { cells: [N]M.Cell, water: [N]f32, temperature: [N]f32, stats: M.Stats, oxygen: f64, carbon_dioxide: f64 };
fn snapshot(p: *const P) Snapshot {
    return .{ .cells = p.microbeCells[0..N].*, .water = p.waterMass[0..N].*, .temperature = p.temperature[0..N].*, .stats = p.microbeStats, .oxygen = p.averageOxygenMass, .carbon_dioxide = p.averageCarbonDioxideMass };
}
fn carbon(p: *const P) f64 {
    const air = p.averageCarbonDioxideMass * 1e9 * @as(f64, @floatFromInt(p.vertices.len)) * (12.0 / 44.0);
    const area: f64 = p.getMeanPointArea();
    var total: f64 = 0;
    var correction: f64 = 0;
    // Accumulate tissue separately from the far larger atmospheric baseline.
    for (p.microbeCells) |cell| {
        const value = (@as(f64, cell.detritus) + M.biomass(cell)) * area - correction;
        const next = total + value;
        correction = (next - total) - value;
        total = next;
    }
    return air + total;
}
fn nutrients(p: *const P) f64 {
    var out: f64 = 0;
    for (p.microbeCells) |cell| out += M.nutrientTotal(cell);
    return out;
}
test "real Planet ignition closes global gas carbon and stored heat ledgers" {
    var p = try init();
    defer p.simulationArena.deinit();
    const before = snapshot(&p);
    const before_c = carbon(&p);
    const before_n = nutrients(&p);
    const expected = Fire.preview(&p, 2, 2);
    try std.testing.expectEqualDeep(before, snapshot(&p));
    const r = Fire.ignite(&p, 2, 2);
    try std.testing.expect(r.success());
    try std.testing.expectEqualDeep(expected, r);
    try std.testing.expectApproxEqRel(before_c, carbon(&p), 1e-12);
    try std.testing.expectEqual(before_n, nutrients(&p));
    try std.testing.expectEqualDeep(before.stats, p.microbeStats);
    for (p.microbeCells, 0..) |cell, i| {
        if (i != 2) {
            try std.testing.expectEqualDeep(before.cells[i], cell);
            try std.testing.expectEqual(before.temperature[i], p.temperature[i]);
        } else {
            var restored = cell;
            restored.detritus = before.cells[i].detritus;
            try std.testing.expectEqualDeep(before.cells[i], restored);
        }
        try std.testing.expectEqual(before.water[i], p.waterMass[i]);
    }
    try std.testing.expectApproxEqRel(r.burned_carbon_kg, r.oxygen_consumed_kg * (12.0 / 32.0), 1e-12);
    try std.testing.expectApproxEqRel(r.burned_carbon_kg, r.carbon_dioxide_added_kg * (12.0 / 44.0), 1e-12);
    try std.testing.expectApproxEqAbs(r.fuel_heat_joules, r.stored_heat_joules + r.thermal_rounding_joules, 1);
    try std.testing.expect(@abs(r.thermal_rounding_joules) <= r.fuel_heat_joules * 0.0001);
    std.debug.print("PLANET_FIRE N={d} fuel_kg={d} O2_kg={d} CO2_kg={d} heat_J={d} stored_J={d} rounding_J={d} delta_K={d} carbon_error={d} nutrients_unchanged=true other_cells_unchanged=true stats_unchanged=true\n", .{ N, r.burned_carbon_kg, r.oxygen_consumed_kg, r.carbon_dioxide_added_kg, r.fuel_heat_joules, r.stored_heat_joules, r.thermal_rounding_joules, r.temperature_delta, carbon(&p) - before_c });
}
test "real Planet limited patch oxygen allocation does not spend whole atmosphere" {
    var p = try init();
    defer p.simulationArena.deinit();
    p.averageOxygenMass *= 0.1;
    const old_oxygen = p.averageOxygenMass;
    const total_oxygen = old_oxygen * 1e9 * N;
    const r = Fire.ignite(&p, 0, 0);
    try std.testing.expect(r.success());
    try std.testing.expect(r.oxygen_consumed_kg <= total_oxygen / N * 1.00000001);
    try std.testing.expect(p.microbeCells[0].detritus > 0 and p.averageOxygenMass > 0);
    try std.testing.expectApproxEqRel(total_oxygen - r.oxygen_consumed_kg, p.averageOxygenMass * 1e9 * N, 1e-12);
}
test "real Planet refusals preserve all candidate inputs atomically" {
    for (0..9) |kind| {
        var p = try init();
        defer p.simulationArena.deinit();
        switch (kind) {
            0 => p.waterMass[0] = 1,
            1 => p.averageOxygenMass = 0,
            2 => {},
            3 => p.microbeCells[0].detritus = 1e-10,
            4 => p.temperature[0] = 500,
            5 => p.worldMode = .sandbox,
            6 => p.microbeCells[0].detritus = 0,
            7 => p.averageCarbonDioxideMass = 1e30,
            8 => p.averageOxygenMass = -1,
            else => unreachable,
        }
        const before = snapshot(&p);
        const r = Fire.ignite(&p, if (kind == 2) 1 else 0, 0);
        try std.testing.expect(!r.success());
        try std.testing.expectEqualDeep(before, snapshot(&p));
        std.debug.print("PLANET_FIRE_REFUSAL case={d} failure={s} unchanged=true\n", .{ kind, @tagName(r.failure) });
    }
    var p = try init();
    defer p.simulationArena.deinit();
    const before = snapshot(&p);
    try std.testing.expectEqual(Fire.Failure.invalid, Fire.ignite(&p, N, N).failure);
    try std.testing.expectEqualDeep(before, snapshot(&p));
}

test "repeated real Planet burns share finite global oxygen without gas duplication" {
    var p = try init();
    defer p.simulationArena.deinit();
    p.averageOxygenMass *= 0.1;
    const initial_c = carbon(&p);
    const initial_n = nutrients(&p);
    const initial_oxygen = p.averageOxygenMass * 1e9 * N;
    var spent: f64 = 0;
    var successes: usize = 0;
    for (0..100) |attempt| {
        const selected = attempt % N;
        const before = snapshot(&p);
        const r = Fire.ignite(&p, selected, selected);
        if (r.success()) {
            spent += r.oxygen_consumed_kg;
            successes += 1;
        } else try std.testing.expectEqualDeep(before, snapshot(&p));
        try std.testing.expect(p.averageOxygenMass >= 0 and spent <= initial_oxygen * 1.00000001);
        try std.testing.expectApproxEqRel(initial_c, carbon(&p), 1e-12);
        try std.testing.expectEqual(initial_n, nutrients(&p));
        try std.testing.expectApproxEqAbs(initial_oxygen, spent + p.averageOxygenMass * 1e9 * N, initial_oxygen * 1e-12);
    }
    try std.testing.expect(successes >= N);
    std.debug.print("PLANET_FIRE_REPEAT attempts=100 successes={d} O2_initial_kg={d} O2_spent_kg={d} O2_remaining_kg={d} carbon_error={d} nutrients_unchanged=true\n", .{ successes, initial_oxygen, spent, p.averageOxygenMass * 1e9 * N, carbon(&p) - initial_c });
}

test "generated world scale diagnoses representable atmospheric transfer" {
    var p = try initCount(40962);
    defer p.simulationArena.deinit();
    p.radius = 5000;
    const index = 13596;
    p.microbeCells[index].detritus = 0.07642566412687302;
    p.temperature[index] = 295.4659423828125;
    p.averageOxygenMass = 26334.627192919306;
    p.averageCarbonDioxideMass = 754.3573973337534;
    const area: @TypeOf(p.averageOxygenMass) = p.getMeanPointArea();
    const cap = p.currentHeatCapacity(index);
    const norm = 1e9 * @as(f64, @floatFromInt(p.vertices.len));
    const burned = @as(f64, p.microbeCells[index].detritus) * area;
    const expected_o2 = burned * (32.0 / 12.0);
    const expected_co2 = burned * (44.0 / 12.0);
    const next_o2 = p.averageOxygenMass - expected_o2 / norm;
    const next_co2 = p.averageCarbonDioxideMass + expected_co2 / norm;
    const actual_o2 = (p.averageOxygenMass - next_o2) * norm;
    const actual_co2 = (next_co2 - p.averageCarbonDioxideMass) * norm;
    const half_ulp_o2 = (std.math.nextAfter(f64, next_o2, std.math.inf(f64)) - next_o2) * norm / 2;
    const before_cell = p.microbeCells[index];
    const before_t = p.temperature[index];
    const before_o = p.averageOxygenMass;
    const before_c = p.averageCarbonDioxideMass;
    const r = Fire.ignite(&p, index, index);
    try std.testing.expect(r.success());
    try std.testing.expect(@abs(r.oxygen_rounding_kg) <= r.oxygen_rounding_budget_kg and @abs(r.carbon_dioxide_rounding_kg) <= r.carbon_dioxide_rounding_budget_kg);
    try std.testing.expect(r.oxygen_rounding_budget_kg <= r.oxygen_ideal_kg * 0.000001);
    try std.testing.expect(r.oxygen_consumed_kg <= before_o * 1e9);
    var restored = p.microbeCells[index];
    restored.detritus = before_cell.detritus;
    try std.testing.expectEqualDeep(before_cell, restored);
    try std.testing.expectApproxEqAbs(r.temperature_delta, @as(f64, p.temperature[index]) - before_t, 1e-12);
    try std.testing.expectApproxEqAbs(r.oxygen_consumed_kg, (before_o - p.averageOxygenMass) * norm, 1e-6);
    try std.testing.expectApproxEqAbs(r.carbon_dioxide_added_kg, (p.averageCarbonDioxideMass - before_c) * norm, 1e-6);
    std.debug.print("PLANET_FIRE_SCALE N={d} radius={d} area={d} heat_capacity={d} O2_ideal={d} O2_actual={d} O2_residual={d} O2_old_budget={d} O2_half_ULP={d} CO2_ideal={d} CO2_actual={d} CO2_residual={d} failure={s} gas_residuals_explicit=true\n", .{ p.vertices.len, p.radius, area, cap, expected_o2, actual_o2, actual_o2 - expected_o2, expected_o2 * 1e-8, half_ulp_o2, expected_co2, actual_co2, actual_co2 - expected_co2, @tagName(r.failure) });
}

test "large mesh oxygen-limited sweep never spends more than allocated patch share" {
    var p = try initCount(40962);
    defer p.simulationArena.deinit();
    p.radius = 5000;
    const area: f64 = p.getMeanPointArea();
    var successes: usize = 0;
    var directed_cases: usize = 0;
    for (1..33) |i| {
        p.microbeCells[0].detritus = 1;
        p.temperature[0] = 300;
        p.averageCarbonDioxideMass = 754.3573973337534;
        p.averageOxygenMass = area / 1e9 * (32.0 / 12.0) * @as(f64, @floatFromInt(i)) / 64;
        const allocation_kg = p.averageOxygenMass * 1e9;
        const before_cell = p.microbeCells[0];
        const before_o = p.averageOxygenMass;
        const before_c = p.averageCarbonDioxideMass;
        const before_t = p.temperature[0];
        const r = Fire.ignite(&p, 0, 0);
        if (r.success()) {
            successes += 1;
            const norm = 1e9 * @as(f64, @floatFromInt(p.vertices.len));
            const raw_actual = (before_o - (before_o - r.oxygen_ideal_kg / norm)) * norm;
            if (raw_actual > allocation_kg) {
                directed_cases += 1;
                try std.testing.expect(r.oxygen_consumed_kg < raw_actual);
            }
            try std.testing.expect(r.oxygen_consumed_kg <= allocation_kg and p.averageOxygenMass >= 0);
            try std.testing.expect(@abs(r.oxygen_rounding_kg) <= r.oxygen_rounding_budget_kg and r.oxygen_rounding_budget_kg <= r.oxygen_ideal_kg * 0.000001);
            try std.testing.expect(@abs(r.carbon_dioxide_rounding_kg) <= r.carbon_dioxide_rounding_budget_kg);
        } else {
            try std.testing.expectEqualDeep(before_cell, p.microbeCells[0]);
            try std.testing.expectEqual(before_o, p.averageOxygenMass);
            try std.testing.expectEqual(before_c, p.averageCarbonDioxideMass);
            try std.testing.expectEqual(before_t, p.temperature[0]);
        }
    }
    try std.testing.expect(successes >= 30);
    try std.testing.expect(directed_cases > 0);
    std.debug.print("PLANET_FIRE_ALLOCATION_SWEEP N=40962 cases=32 successes={d} directed_corrections={d} actual_O2_within_equal_patch_share=true residuals_within_ULP_and_1ppm=true\n", .{ successes, directed_cases });
}

fn spacing(value: f64) f64 {
    return std.math.nextAfter(f64, value, std.math.inf(f64)) - value;
}
test "cumulative large mesh burns reconcile actual gas fuel and explicit residuals" {
    var p = try initCount(40962);
    defer p.simulationArena.deinit();
    p.radius = 5000;
    p.averageOxygenMass = 26334.627192919306;
    p.averageCarbonDioxideMass = 754.3573973337534;
    const norm = 1e9 * @as(f64, @floatFromInt(p.vertices.len));
    const area: f64 = p.getMeanPointArea();
    const before_o = p.averageOxygenMass;
    const before_c = p.averageCarbonDioxideMass;
    const before_carbon = carbon(&p);
    const before_n = nutrients(&p);
    const before_stats = p.microbeStats;
    var actual_o: f64 = 0;
    var actual_c: f64 = 0;
    var ideal_o: f64 = 0;
    var ideal_c: f64 = 0;
    var residual_o: f64 = 0;
    var residual_c: f64 = 0;
    var burned: f64 = 0;
    var successes: usize = 0;
    for (0..1028) |attempt| {
        const selected = attempt % 257;
        const old_o = p.averageOxygenMass;
        const old_c = p.averageCarbonDioxideMass;
        const old_cell = p.microbeCells[selected];
        const old_t = p.temperature[selected];
        const r = Fire.ignite(&p, selected, selected);
        if (r.success()) {
            successes += 1;
            actual_o += r.oxygen_consumed_kg;
            actual_c += r.carbon_dioxide_added_kg;
            ideal_o += r.oxygen_ideal_kg;
            ideal_c += r.carbon_dioxide_ideal_kg;
            residual_o += r.oxygen_rounding_kg;
            residual_c += r.carbon_dioxide_rounding_kg;
            burned += r.burned_carbon_kg;
            try std.testing.expect(r.oxygen_consumed_kg <= old_o * 1e9);
        } else {
            try std.testing.expectEqualDeep(old_cell, p.microbeCells[selected]);
            try std.testing.expectEqual(old_t, p.temperature[selected]);
            try std.testing.expectEqual(old_o, p.averageOxygenMass);
            try std.testing.expectEqual(old_c, p.averageCarbonDioxideMass);
        }
    }
    try std.testing.expectEqual(@as(usize, 257), successes);
    const final_o_delta = (before_o - p.averageOxygenMass) * norm;
    const final_c_delta = (p.averageCarbonDioxideMass - before_c) * norm;
    const o_tolerance = (spacing(actual_o) + spacing(ideal_o)) * @as(f64, @floatFromInt(successes)) * 2;
    const c_tolerance = (spacing(actual_c) + spacing(ideal_c)) * @as(f64, @floatFromInt(successes)) * 2;
    try std.testing.expectApproxEqAbs(final_o_delta, actual_o, o_tolerance);
    try std.testing.expectApproxEqAbs(final_c_delta, actual_c, c_tolerance);
    try std.testing.expectApproxEqAbs(actual_o, ideal_o + residual_o, o_tolerance);
    try std.testing.expectApproxEqAbs(actual_c, ideal_c + residual_c, c_tolerance);
    var remaining: f64 = 0;
    for (p.microbeCells) |cell| remaining += cell.detritus;
    const removed = (@as(f64, @floatFromInt(p.vertices.len)) * 0.25 - remaining) * area;
    try std.testing.expectApproxEqRel(removed, burned, 1e-12);
    try std.testing.expectApproxEqAbs(removed * (32.0 / 12.0), ideal_o, o_tolerance);
    try std.testing.expectApproxEqAbs(removed * (44.0 / 12.0), ideal_c, c_tolerance);
    // Net global carbon difference must be the disclosed CO2 rounding carbon,
    // within the ULP resolution of adding/subtracting the large total stocks.
    const total_tolerance = 4 * (spacing(before_carbon) + spacing(carbon(&p))) + c_tolerance;
    try std.testing.expectApproxEqAbs(residual_c * (12.0 / 44.0), carbon(&p) - before_carbon, total_tolerance);
    try std.testing.expectEqual(before_n, nutrients(&p));
    try std.testing.expectEqualDeep(before_stats, p.microbeStats);
    try std.testing.expect(p.averageOxygenMass >= 0);
    std.debug.print("PLANET_FIRE_CUMULATIVE N={d} attempts=1028 successes={d} burned_kg={d} O2_actual_sum={d} O2_final_delta={d} O2_residual_sum={d} CO2_actual_sum={d} CO2_final_delta={d} CO2_residual_sum={d} carbon_delta={d} carbon_residual_expected={d} global_ulp_budget_kg={d} nutrients_stats_unchanged=true no_gas_resets=true\n", .{ p.vertices.len, successes, burned, actual_o, final_o_delta, residual_o, actual_c, final_c_delta, residual_c, carbon(&p) - before_carbon, residual_c * (12.0 / 44.0), total_tolerance });
}

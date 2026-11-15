const std = @import("std");
const H = @import("experimental/capillary_bucket_f64.zig");
const A = @import("simulation/atmosphere_water.zig");
const area: f64 = 7669529600;
fn emit(name: []const u8, s: H.State, p: H.Params, r: H.Result) !void {
    const old = A.PhaseStep.init(p.dt).phase(s.liquid, s.vapor, p.saturation, p.temperature, s.rain).?;
    const legacy = H.State{ .liquid = @floatCast(old.liquid), .vapor = @floatCast(old.vapor), .soil = s.soil, .rain = @floatCast(old.rain_rate) };
    const j = try std.json.stringifyAlloc(std.testing.allocator, .{ .name = name, .before = s, .params = p, .result = r, .legacy = legacy }, .{});
    defer std.testing.allocator.free(j);
    std.debug.print("HYBRID {s}\n", .{j});
}
fn check(name: []const u8, s: H.State, p: H.Params) !void {
    const r = H.step(s, p).?;
    try std.testing.expect(r.state.soil >= 0 and r.state.soil <= p.capacity);
    if (p.temperature <= 273.15) try std.testing.expect(r.soil_evap_density == 0 and r.infiltrated_density == 0 and r.drained_density == 0);
    if (r.stages[0].liquid > 0) try std.testing.expect(r.soil_evap_density == 0 and r.exposed_seconds == 0);
    try emit(name, s, p, r);
    var disabled = p;
    disabled.enabled = false;
    const off = H.step(s, disabled).?;
    const old = A.PhaseStep.init(p.dt).phase(s.liquid, s.vapor, p.saturation, p.temperature, s.rain).?;
    try std.testing.expectEqual(old.liquid, off.state.liquid);
    try std.testing.expectEqual(old.vapor, off.state.vapor);
    try std.testing.expectEqual(old.rain_rate, off.state.rain);
    try std.testing.expectEqual(s.soil, off.state.soil);
}
test "bucket fixed structural cold wet dry depleted supersaturated cases" {
    const cases = [_]H.State{ .{ .liquid = 0, .vapor = 1, .soil = 0.25 }, .{ .liquid = 100, .vapor = 1, .soil = 0.25 }, .{ .liquid = @as(f32, 0.0001), .vapor = 1, .soil = 0.25 }, .{ .liquid = 0, .vapor = 4, .soil = 0.25 }, .{ .liquid = 0, .vapor = 1, .soil = 0 }, .{ .liquid = 100, .vapor = 1, .soil = 1 } };
    const boundary: f32 = 273.15;
    for (cases) |s| for ([_]f64{ 270, 273.15, boundary, std.math.nextAfter(f32, boundary, std.math.inf(f32)), 300 }) |temp| for ([_]f64{ 360, 720, 1440 }) |dt| try check("controlled", s, .{ .dt = dt, .area = area, .temperature = temp, .saturation = 2 });
}
test "bucket actual nine world boundary operands no biology" {
    const Fixture = struct { name: []const u8, sha256: []const u8, cell: usize, state: H.State, temperature: f64 };
    const f = try std.json.parseFromSlice([]Fixture, std.testing.allocator, @embedFile("experimental/hybrid_abiotic_fixtures.json"), .{});
    defer f.deinit();
    for (f.value) |x| for ([_]f64{ 0, 0.25 }) |soil| for ([_]f64{ 0.5, 1, 2 }) |multiplier| for ([_]f64{ 360, 720, 1440 }) |dt| {
        var s = x.state;
        s.soil = soil;
        try check(x.name, s, .{ .dt = dt, .area = area, .temperature = x.temperature, .saturation = @as(f64, s.vapor) * multiplier });
    };
}
test "bucket cold warm cold no catchup or capacity reset" {
    var s = H.State{ .liquid = 0, .vapor = 1, .soil = 0.25 };
    for ([_]f64{ 270, 300, 270 }) |temp| {
        const p = H.Params{ .dt = 1440, .area = area, .temperature = temp, .saturation = 2 };
        const r = H.step(s, p).?;
        if (temp == 270) try std.testing.expectEqual(s.soil, r.state.soil);
        try emit("cold_warm_cold", s, p, r);
        s = r.state;
    }
}
test "bucket zero and invalid atomic pure input" {
    const s = H.State{ .liquid = 1, .vapor = 2, .soil = 0.25 };
    const p = H.Params{ .dt = 0, .area = area, .temperature = 300, .saturation = 2 };
    try std.testing.expectEqualDeep(s, H.step(s, p).?.state);
    var bad = p;
    bad.area = 0;
    try std.testing.expect(H.step(s, bad) == null);
    bad = p;
    bad.dt = -1;
    try std.testing.expect(H.step(s, bad) == null);
    bad = p;
    bad.area = 1e-300;
    bad.dt = 1440;
    try std.testing.expect(H.step(s, bad) == null);
}
test "bucket nearly exhausted represented liquid still excludes soil" {
    for ([_]f64{ 360, 720, 1440 }) |dt| {
        const request = A.PhaseStep.init(dt).evaporation;
        var pool: f32 = @floatCast(request);
        pool = std.math.nextAfter(f32, pool, std.math.inf(f32));
        const s = H.State{ .liquid = pool, .vapor = 1, .soil = 0.25 };
        const p = H.Params{ .dt = dt, .area = area, .temperature = 300, .saturation = 2 };
        const r = H.step(s, p).?;
        try std.testing.expect(r.stages[0].liquid > 0 and r.soil_evap_density == 0);
        try emit("near_depletion_residual", s, p, r);
    }
}

test "bucket capacity and head boundaries" {
    for ([_]f64{ 0, 0.5, 1 }) |soil| for ([_]f32{ 0, 0.000001, 1, 1000 }) |liquid| {
        const s = H.State{ .liquid = liquid, .vapor = 2, .soil = soil };
        const p = H.Params{ .dt = 360, .area = area, .temperature = 300, .saturation = 2, .capacity = if (soil == 0) 0 else 1 };
        const r = H.step(s, p).?;
        try std.testing.expect(r.drained_density == 0);
        if (p.capacity == 0 or soil == p.capacity or liquid == 0) try std.testing.expect(r.infiltrated_density == 0);
        try emit("head_edges", s, p, r);
    };
    const c = H.State{ .liquid = 0, .vapor = 2, .soil = std.math.nextAfter(f64, 1, 0) };
    const r = H.step(c, .{ .dt = 360, .area = area, .temperature = 300, .saturation = 2 }).?;
    try std.testing.expect(r.infiltrated_density == 0);
}
test "bucket fixed seven day abiotic timestep sequences" {
    const starts = [_]H.State{ .{ .liquid = 0, .vapor = 1, .soil = 0.25 }, .{ .liquid = 1000, .vapor = 1, .soil = 0 }, .{ .liquid = @as(f32, 0.0001), .vapor = 1, .soil = 0.25 } };
    for (starts, 0..) |initial, index| for ([_]f64{ 360, 720, 1440 }) |dt| {
        var s = initial;
        const p = H.Params{ .dt = dt, .area = area, .temperature = 300, .saturation = 2 };
        var infiltration: f64 = 0;
        var soil_evap: f64 = 0;
        var time: f64 = 0;
        while (time < 7 * 86400) {
            const r = H.step(s, p).?;
            try emit("seven_day_sequence", s, p, r);
            infiltration += r.infiltrated_density;
            soil_evap += r.soil_evap_density;
            s = r.state;
            time += dt;
        }
        const line = try std.json.stringifyAlloc(std.testing.allocator, .{ .fixture = index, .dt = dt, .initial = initial, .final = s, .infiltrated = infiltration, .soil_evaporated = soil_evap }, .{});
        defer std.testing.allocator.free(line);
        std.debug.print("BUCKET_SEVEN_DAY {s}\n", .{line});
    };
}

test "bucket actual vapor dry counterfactual boundary probes" {
    const Fixture = struct { name: []const u8, sha256: []const u8, cell: usize, state: H.State, temperature: f64 };
    const f = try std.json.parseFromSlice([]Fixture, std.testing.allocator, @embedFile("experimental/hybrid_abiotic_fixtures.json"), .{});
    defer f.deinit();
    for (f.value) |x| for ([_]f64{ 0.5, 1, 2 }) |multiplier| for ([_]f64{ 360, 720, 1440 }) |dt| {
        var s = x.state;
        s.liquid = 0;
        s.soil = 0.25;
        const p = H.Params{ .dt = dt, .area = area, .temperature = x.temperature, .saturation = @as(f64, s.vapor) * multiplier };
        const r = H.step(s, p).?;
        try emit("actual_vapor_counterfactual_dry", s, p, r);
    };
}

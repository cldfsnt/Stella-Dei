//! New isolated capillary bucket. No upward outlet; no production changes.
const std = @import("std");
const A = @import("../simulation/atmosphere_water.zig");
const P = @import("physical_water_f64.zig");
pub const State = struct { liquid: f32, vapor: f32, soil: f64 = 0, rain: f32 = 0 };
// drainage_rate is retained solely for old fixture compatibility; ignored by this model.
pub const Params = struct { enabled: bool = true, dt: f64, area: f64, temperature: f64, saturation: f64, capacity: f64 = 1, infiltration_rate: f64 = 1.0 / 86400.0, drainage_rate: f64 = 0.01 / 86400.0 };
pub const Result = struct { state: State, stages: [5]State, request_native: f64 = 0, standing_evap_native: f64 = 0, soil_evap_density: f64 = 0, condensed_native: f64 = 0, infiltrated_density: f64 = 0, drained_density: f64 = 0, exposed_seconds: f64 = 0, head_factor: f64 = 0, infiltration_requested_density: f64 = 0 };
fn valid(x: f64) bool {
    return std.math.isFinite(x) and x >= 0;
}
fn toDensity(native: f64, area: f64) f64 {
    return P.downRatio(P.downProduct(native, 1e9), area);
}
fn toNative(density: f64, area: f64) f64 {
    return P.downRatio(P.downProduct(density, area), 1e9);
}
fn take32(pool: *f32, want: f64) ?f64 {
    @setFloatMode(.strict);
    if (!valid(pool.*) or !valid(want)) return null;
    const old: f64 = pool.*;
    const request = @min(old, want);
    var after: f32 = @floatCast(@max(0, old - request));
    const d = P.difference(old, after);
    if (d.hi > request or (d.hi == request and d.lo > 0)) after = std.math.nextAfter(f32, after, pool.*);
    if (after < 0 or after > pool.*) return null;
    pool.* = after;
    return P.downDifference(old, after);
}
fn add32(pool: *f32, amount: f64) ?void {
    if (!valid(amount)) return null;
    const x = @as(f64, pool.*) + amount;
    if (!valid(x) or x > std.math.floatMax(f32)) return null;
    pool.* = @floatCast(x);
}
fn creditSoil(pool: *f64, amount: f64) ?f64 {
    @setFloatMode(.strict);
    const old = pool.*;
    var after = old + amount;
    if (!valid(after)) return null;
    const d = P.difference(after, old);
    if (d.hi > amount or (d.hi == amount and d.lo > 0)) after = std.math.nextAfter(f64, after, old);
    pool.* = after;
    return P.downDifference(after, old);
}
pub fn step(initial: State, p: Params) ?Result {
    @setFloatMode(.strict);
    if (!valid(initial.liquid) or !valid(initial.vapor) or !valid(initial.soil) or !valid(initial.rain) or !valid(p.dt) or !valid(p.area) or p.area == 0 or !valid(p.saturation) or !std.math.isFinite(p.temperature) or !valid(p.capacity) or initial.soil > p.capacity or !valid(p.infiltration_rate) or !valid(p.drainage_rate) or !valid(p.infiltration_rate * p.dt) or !valid(p.drainage_rate * p.dt) or !valid(1e9 / p.area)) return null;
    var r = Result{ .state = initial, .stages = .{ initial, initial, initial, initial, initial } };
    const c = A.PhaseStep.init(p.dt);
    if (!p.enabled) {
        const old = c.phase(initial.liquid, initial.vapor, p.saturation, p.temperature, initial.rain) orelse return null;
        if (old.liquid > std.math.floatMax(f32) or old.vapor > std.math.floatMax(f32) or old.rain_rate > std.math.floatMax(f32)) return null;
        r.state.liquid = @floatCast(old.liquid);
        r.state.vapor = @floatCast(old.vapor);
        r.state.rain = @floatCast(old.rain_rate);
        r.stages = .{ r.state, r.state, r.state, r.state, r.state };
        return r;
    }
    if (p.dt == 0) return r;
    const warm = p.temperature > 273.15;
    const deficit = @max(0, p.saturation - @as(f64, initial.vapor));
    r.request_native = if (warm) deficit * c.evaporation else 0;
    if (!valid(r.request_native)) return null;
    r.standing_evap_native = take32(&r.state.liquid, r.request_native) orelse return null;
    add32(&r.state.vapor, r.standing_evap_native) orelse return null;
    r.stages[0] = r.state;
    // A represented residual standing pool excludes soil evaporation for this tick.
    if (warm and r.state.liquid == 0 and r.request_native > 0) {
        if (initial.liquid == 0) r.exposed_seconds = p.dt else if (deficit > initial.liquid) {
            const depletion = -A.evaporation_seconds * std.math.log1p(-@as(f64, initial.liquid) / deficit);
            if (!valid(depletion)) return null;
            r.exposed_seconds = @max(0, p.dt - @min(p.dt, depletion));
        }
        const remaining = P.downDifference(r.request_native, r.standing_evap_native);
        const wanted = toDensity(remaining, p.area);
        if (!valid(wanted)) return null;
        const removed = P.remove(r.state.soil, wanted) orelse return null;
        r.state.soil = removed.after;
        r.soil_evap_density = removed.paid;
        const native = toNative(removed.paid, p.area);
        add32(&r.state.vapor, native) orelse return null;
    }
    r.stages[1] = r.state;
    const rain_request = @min(@as(f64, r.state.vapor), @max(0, @as(f64, r.state.vapor) - p.saturation) * c.condensation);
    r.condensed_native = take32(&r.state.vapor, rain_request) orelse return null;
    add32(&r.state.liquid, r.condensed_native) orelse return null;
    const rain_rate = @as(f64, initial.rain) * (1 - c.rain_memory) + (r.condensed_native / p.dt * 86400) * c.rain_memory;
    if (!valid(rain_rate) or rain_rate > std.math.floatMax(f32)) return null;
    r.state.rain = @floatCast(rain_rate);
    r.stages[2] = r.state;
    if (warm and p.capacity > 0) {
        const liquid_density = toDensity(r.state.liquid, p.area);
        if (!valid(liquid_density)) return null;
        const gap = P.downDifference(p.capacity, r.state.soil);
        r.head_factor = if (liquid_density >= r.state.soil) 1 else @min(1, P.lowerSum(.{ P.downRatio(gap, p.capacity), P.downRatio(liquid_density, p.capacity), 0, 0 }));
        const wanted = @min(liquid_density, @min(gap, P.downProduct(P.downProduct(p.infiltration_rate, p.dt), r.head_factor)));
        r.infiltration_requested_density = wanted;
        const native = toNative(wanted, p.area);
        if (!valid(native)) return null;
        const debit = take32(&r.state.liquid, native) orelse return null;
        const funded = toDensity(debit, p.area);
        if (!valid(funded)) return null;
        r.infiltrated_density = creditSoil(&r.state.soil, funded) orelse return null;
    }
    r.stages[3] = r.state;
    // No positive soil head and no lower reservoir: no upward drainage in this model.
    r.stages[4] = r.state;
    return r;
}

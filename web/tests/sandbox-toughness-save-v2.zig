//! EXPERIMENT ONLY. Copy beside save_game.zig and sandbox-toughness-save.zig.
//! Explicit event-keyed mutation identity; never writes a canonical production save.
const std = @import("std");
const saves = @import("save_game.zig");
const v1 = @import("sandbox-toughness-save.zig");
pub const Envelope = struct {
    format: []const u8,
    law: u32,
    mutation_law: u32,
    mutation_enabled: bool,
    stream_seed: u64,
    state: saves.schema.Save,
};
pub fn validate(value: Envelope) !void {
    if (!std.mem.eql(u8, value.format, "sandbox-toughness-v2") or value.law != 1 or value.mutation_law != 2)
        return error.UnsupportedToughnessLaw;
    // Reuse v1's complete physiology/mode/trait validation without claiming the
    // v2 mutation flag belongs to v1. Every u64 seed is valid, also while disabled.
    try v1.validate(.{ .format = "sandbox-toughness-v1", .law = 1, .mutation_enabled = false, .state = value.state });
}
/// Borrowed capture: immediately serialize/deep-parse before mutating live state.
pub fn capture(allocator: std.mem.Allocator, state: anytype) !Envelope {
    const config = state.planet.toughnessMutation;
    const result = Envelope{ .format = "sandbox-toughness-v2", .law = 1, .mutation_law = 2, .mutation_enabled = config.enabled, .stream_seed = config.stream_seed, .state = try saves.capture(allocator, state) };
    try validate(result);
    return result;
}
pub fn apply(state: anytype, value: Envelope) !void {
    try validate(value);
    try saves.apply(state, value.state);
    state.planet.toughnessMutation = .{ .enabled = value.mutation_enabled, .stream_seed = value.stream_seed };
}
pub fn applyV1(state: anytype, value: v1.Envelope) !void {
    // Explicit legacy experiment import retains all toughness traits but does not
    // borrow a previously enabled world's mutation configuration.
    try v1.apply(state, value);
    state.planet.toughnessMutation = .{ .enabled = false, .stream_seed = 0 };
}
pub fn applyLegacy(state: anytype, saved: saves.schema.Save) !void {
    try v1.applyLegacy(state, saved);
    state.planet.toughnessMutation = .{ .enabled = false, .stream_seed = 0 };
}

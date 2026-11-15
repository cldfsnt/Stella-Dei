//! EXPERIMENT ONLY. Copy beside save_game.zig in the isolated toughness tree.
//! This is not a production-compatible save format or a canonical-save writer.
const std = @import("std");
const saves = @import("save_game.zig");
pub const Envelope = struct {
    format: []const u8,
    law: u32,
    mutation_enabled: bool,
    state: saves.schema.Save,
};
fn validateState(saved: saves.schema.Save, legacy: bool) !void {
    try saved.validate();
    if (saved.mode != .sandbox or saved.origin != null) return error.UnsupportedToughnessMode;
    // Includes empty patches: dormant values must not be silently erased or revived.
    for (saved.plants) |plant| {
        const d = plant.toughness;
        if (!std.math.isFinite(d) or d < 0 or d > 1) return error.InvalidToughness;
        if (legacy and d != 0) return error.DisguisedToughness;
    }
}
pub fn validate(value: Envelope) !void {
    if (!std.mem.eql(u8, value.format, "sandbox-toughness-v1") or value.law != 1 or value.mutation_enabled)
        return error.UnsupportedToughnessLaw;
    try validateState(value.state, false);
}
/// Borrowed capture, like save_game.capture. Serialize immediately and parse with
/// alloc_always before changing the engine to obtain an immutable independent save.
pub fn capture(allocator: std.mem.Allocator, state: anytype) !Envelope {
    const result = Envelope{ .format = "sandbox-toughness-v1", .law = 1, .mutation_enabled = false, .state = try saves.capture(allocator, state) };
    try validate(result);
    return result;
}
pub fn apply(state: anytype, value: Envelope) !void {
    // Reject the entire unsupported/invalid document before touching live state.
    try validate(value);
    try saves.apply(state, value.state);
}
/// Explicit import only. Typed JSON must retain its default unknown-field rejection.
/// Absent trait defaults to zero in the isolated Plant; positive supplied traits refuse.
pub fn applyLegacy(state: anytype, saved: saves.schema.Save) !void {
    try validateState(saved, true);
    try saves.apply(state, saved);
}

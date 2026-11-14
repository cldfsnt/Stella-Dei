//! Versioned, graphics-independent browser save format. Never includes pointers.
const std = @import("std");
pub const VERSION: u32 = 5;
pub const Microbes = @import("simulation/microbes.zig");
pub const WorldMode = Microbes.Mode;
/// Wire representation accepts legacy two-slot data without advancing biology.
pub const IndexedCohort = struct { index: u8, value: Microbes.Cohort };
pub fn canonicalEmpty(cohort: Microbes.Cohort) bool {
    const empty: Microbes.Cohort = .{};
    inline for (std.meta.fields(Microbes.Cohort)) |field| {
        const a = @field(cohort, field.name);
        const b = @field(empty, field.name);
        if (@typeInfo(field.type) == .Float) {
            const Bits = std.meta.Int(.unsigned, @bitSizeOf(field.type));
            if (@as(Bits, @bitCast(a)) != @as(Bits, @bitCast(b))) return false;
        } else if (a != b) return false;
    }
    return true;
}
pub const SavedCell = struct {
    cohorts: []const Microbes.Cohort = &.{},
    sparse: ?[]const IndexedCohort = null,
    nutrient: f32 = 0.02,
    detritus: f32 = 0,
    rng: u64 = 1,
    pub fn capture(cell: *const Microbes.Cell) SavedCell {
        return .{ .cohorts = &cell.cohorts, .nutrient = cell.nutrient, .detritus = cell.detritus, .rng = cell.rng };
    }
    pub fn jsonStringify(self: SavedCell, writer: anytype) !void {
        try writer.beginObject();
        if (self.sparse) |entries| {
            try writer.objectField("sparse");
            try writer.write(entries);
        } else {
            try writer.objectField("cohorts");
            try writer.write(self.cohorts);
        }
        try writer.objectField("nutrient");
        try writer.write(self.nutrient);
        try writer.objectField("detritus");
        try writer.write(self.detritus);
        try writer.objectField("rng");
        try writer.write(self.rng);
        try writer.endObject();
    }
    pub fn runtime(self: SavedCell) Microbes.Cell {
        var cell: Microbes.Cell = .{ .nutrient = self.nutrient, .detritus = self.detritus, .rng = self.rng };
        std.debug.assert(self.cohorts.len <= cell.cohorts.len);
        if (self.sparse) |entries| {
            for (entries) |entry| cell.cohorts[entry.index] = entry.value;
        } else @memcpy(cell.cohorts[0..self.cohorts.len], self.cohorts);
        return cell;
    }
};
pub const SparseCapture = struct {
    cells: []SavedCell,
    entries: []IndexedCohort,
    pub fn deinit(self: SparseCapture, allocator: std.mem.Allocator) void {
        allocator.free(self.cells);
        allocator.free(self.entries);
    }
};
pub fn captureSparse(allocator: std.mem.Allocator, source: []const Microbes.Cell) !SparseCapture {
    var count: usize = 0;
    for (source) |cell| for (cell.cohorts) |cohort| {
        if (!canonicalEmpty(cohort)) {
            count += 1;
        }
    };
    const cells = try allocator.alloc(SavedCell, source.len);
    errdefer allocator.free(cells);
    const entries = try allocator.alloc(IndexedCohort, count);
    var cursor: usize = 0;
    for (source, cells) |cell, *out| {
        const start = cursor;
        for (cell.cohorts, 0..) |cohort, index| {
            if (!canonicalEmpty(cohort)) {
                entries[cursor] = .{ .index = @intCast(index), .value = cohort };
                cursor += 1;
            }
        }
        out.* = .{ .sparse = entries[start..cursor], .nutrient = cell.nutrient, .detritus = cell.detritus, .rng = cell.rng };
    }
    return .{ .cells = cells, .entries = entries };
}
pub const Origin = struct {
    cohort_encoding: enum { dense, sparse_indexed } = .dense,
    model_revision: u32 = 1,
    cells: []const SavedCell,
    stats: Microbes.Stats,
};
pub const Plant = @import("simulation/ecology.zig").Plant;
pub const Rabbit = struct {
    position: [3]f32,
    velocity: [3]f32,
    born: f64,
    state: enum { wander, go_to_point, gestation },
    target: [3]f32 = .{ 0, 0, 0 },
    gestation_since: f64 = 0,
    female: bool,
    satiety: f32,
    criteria: f32,
    cooldown: f32,
    random: [4]u64,
};
pub const Save = struct {
    // Missing version is legacy, never implicitly upgrade unknown data.
    version: u32 = 1,
    mode: WorldMode = .sandbox,
    origin: ?Origin = null,
    radius: f32,
    subdivisions: usize,
    seed: u64,
    game_time: f64,
    time_scale: f32,
    solar_constant: f32,
    rotation_time: f32,
    axial_tilt: f32,
    paused: bool,
    daylight: bool,
    display_mode: u8,
    camera: [3]f32,
    camera_target: [3]f32,
    camera_distance: f32,
    target_distance: f32,
    nitrogen: f64,
    oxygen: f64,
    carbon_dioxide: f64,
    plant_generations: u32,
    plant_births: u64,
    rabbit_births: u64,
    rabbit_meals: u64,
    rabbit_deaths: u64,
    plant_color: f32,
    elevation: []const f32,
    temperature: []const f32,
    vegetation: []const f32,
    water: []const f32,
    vapor: []const f32,
    rainfall: []const f32,
    wind: []const [2]f32,
    wind_error: []const [2]f32,
    plants: []const Plant,
    rabbits: []const Rabbit,

    pub fn validate(self: Save) !void {
        if ((self.version < 1 or self.version > VERSION) or self.subdivisions > 7 or self.radius != 5000) return error.IncompatibleSave;
        if (self.version == 1 and (self.mode != .sandbox or self.origin != null)) return error.IncompatibleSave;
        const count = 10 * std.math.pow(usize, 4, self.subdivisions) + 2;
        if (self.elevation.len != count or self.temperature.len != count or self.vegetation.len != count or self.water.len != count or self.vapor.len != count or self.rainfall.len != count or self.wind.len != count or self.wind_error.len != count or self.plants.len != count or self.rabbits.len > 100000) return error.InvalidShape;
        switch (self.mode) {
            .sandbox => if (self.origin != null) return error.InvalidValue,
            .origin => {
                const origin = self.origin orelse return error.InvalidShape;
                if (origin.cells.len != count) return error.InvalidShape;
                if (origin.model_revision != self.version - 1) return error.IncompatibleSave;
                if (origin.stats.next_lineage == 0 or origin.stats.next_lineage > 1_000_000_000_000_000 or origin.stats.births >= origin.stats.next_lineage) return error.InvalidValue;
                try finiteRange(origin.stats.fixed_carbon, 0, 1e30);
                try finiteRange(origin.stats.recycled_carbon, 0, 1e30);
                try finiteRange(origin.stats.nutrient_added, 0, 1e30);
                try finiteRange(origin.stats.grazed_carbon, 0, 1e30);
                try finiteRange(origin.stats.grazing_respired_carbon, 0, 1e30);
                if (self.version < 4 and (origin.stats.grazed_carbon != 0 or origin.stats.grazing_respired_carbon != 0)) return error.IncompatibleSave;
                try finiteRange(origin.stats.movement_respired_carbon, 0, 1e30);
                if (origin.stats.relocations > 1_000_000_000_000_000) return error.InvalidValue;
                if (self.version < 5 and (origin.stats.relocations != 0 or origin.stats.movement_respired_carbon != 0 or origin.cohort_encoding != .dense)) return error.IncompatibleSave;
                if (origin.stats.failed_patches > 1_000_000_000_000_000) return error.InvalidValue;
                for (origin.cells, 0..) |saved_cell, cell_index| {
                    if (origin.cohort_encoding == .sparse_indexed) {
                        if (saved_cell.cohorts.len != 0) return error.InvalidShape;
                        const entries = saved_cell.sparse orelse return error.InvalidShape;
                        if (entries.len > 4) return error.InvalidShape;
                        var seen: u8 = 0;
                        for (entries) |entry| {
                            if (entry.index >= 4) return error.InvalidValue;
                            const bit = @as(u8, 1) << @as(u3, @intCast(entry.index));
                            if (seen & bit != 0) return error.InvalidValue;
                            seen |= bit;
                        }
                    } else {
                        const required_slots: usize = if (self.version == 2) 2 else 4;
                        if (saved_cell.cohorts.len != required_slots or saved_cell.sparse != null) return error.InvalidShape;
                    }
                    const cell = saved_cell.runtime();
                    for (cell.cohorts) |cohort| {
                        if (self.version == 2 and cohort.structure != 0) return error.IncompatibleSave;
                        try finiteRange(cohort.feeding, 0, 1);
                        try finiteRange(cohort.lifetime_grazed, 0, 1e12);
                        if (self.version < 4 and (cohort.feeding != 0 or cohort.lifetime_grazed != 0)) return error.IncompatibleSave;
                        try finiteRange(cohort.mobility, 0, 1);
                        try finiteRange(cohort.last_move_time, 0, self.game_time);
                        if (cohort.relocations > 0 and (cohort.last_from >= count or cohort.last_to >= count or cohort.last_from == cohort.last_to or cohort.last_to != cell_index)) return error.InvalidValue;
                        if (self.version < 5 and (cohort.mobility != 0 or cohort.relocations != 0 or cohort.last_from != 0 or cohort.last_to != 0 or cohort.last_move_time != 0)) return error.IncompatibleSave;
                    }
                    if (!Microbes.validCell(cell, origin.stats.next_lineage)) return error.InvalidValue;
                    // Generous numerical safety bounds, not gameplay resource caps.
                    try finiteRange(cell.nutrient, 0, 1e12);
                    try finiteRange(cell.detritus, 0, 1e12);
                    for (cell.cohorts) |cohort| try finiteRange(cohort.reproduction_credit, 0, 1e12);
                }
            },
        }
        try finiteRange(self.game_time, 0, 1e15);
        try finiteRange(self.time_scale, 0, 2e8);
        try finiteRange(self.solar_constant, 0, 5000);
        try finiteRange(self.rotation_time, 1, 1e12);
        try finiteRange(self.axial_tilt, -360, 360);
        try finiteRange(self.nitrogen, 0, 1e20);
        try finiteRange(self.oxygen, 0, 1e20);
        try finiteRange(self.carbon_dioxide, 0, 1e20);
        try finiteRange(self.plant_color, 100, 1000);
        if (self.display_mode > 4) return error.InvalidValue;
        for (self.camera) |v| try finiteRange(v, -1e8, 1e8);
        for (self.camera_target) |v| try finiteRange(v, -1e8, 1e8);
        if (length2(self.camera) < 1 or length2(self.camera_target) < 1) return error.InvalidValue;
        try finiteRange(self.camera_distance, self.radius + 1, self.radius * 100);
        try finiteRange(self.target_distance, self.radius + 1, self.radius * 100);
        for (self.elevation) |v| try finiteRange(v, self.radius - 200, self.radius + 200);
        for (self.temperature) |v| try finiteRange(v, 0, 10000);
        for (self.vegetation) |v| try finiteRange(v, 0, 1);
        for (self.water) |v| try finiteRange(v, 0, 1e15);
        for (self.vapor) |v| try finiteRange(v, 0, 1e15);
        for (self.rainfall) |v| try finiteRange(v, -1e15, 1e15);
        for (self.wind) |vector| for (vector) |v| {
            try finiteRange(v, -1e10, 1e10);
        };
        for (self.wind_error) |vector| for (vector) |v| {
            try finiteRange(v, -1e10, 1e10);
        };
        for (self.plants) |plant| try finiteRange(plant.optimum, 100, 1000);
        for (self.rabbits) |rabbit| {
            for (rabbit.position) |v| try finiteRange(v, -1e8, 1e8);
            if (length2(rabbit.position) < 1) return error.InvalidValue;
            for (rabbit.velocity) |v| try finiteRange(v, -1e10, 1e10);
            for (rabbit.target) |v| try finiteRange(v, -1e8, 1e8);
            try finiteRange(rabbit.born, 0, self.game_time);
            try finiteRange(rabbit.gestation_since, 0, self.game_time);
            try finiteRange(rabbit.satiety, 0, 1e6);
            try finiteRange(rabbit.criteria, 0, 1e6);
            try finiteRange(rabbit.cooldown, 0, 1e15);
            if (rabbit.random[0] | rabbit.random[1] | rabbit.random[2] | rabbit.random[3] == 0) return error.InvalidValue;
        }
    }
};
fn length2(v: [3]f32) f32 {
    return v[0] * v[0] + v[1] * v[1] + v[2] * v[2];
}
fn finiteRange(v: f64, low: f64, high: f64) !void {
    if (!std.math.isFinite(v) or v < low or v > high) return error.InvalidValue;
}
pub fn parse(allocator: std.mem.Allocator, bytes: []const u8) !std.json.Parsed(Save) {
    var parsed = try std.json.parseFromSlice(Save, allocator, bytes, .{ .allocate = .alloc_always });
    errdefer parsed.deinit();
    try parsed.value.validate();
    return parsed;
}

fn fixture() Save {
    return .{
        .radius = 5000,
        .subdivisions = 0,
        .seed = 123,
        .game_time = 123456,
        .time_scale = 3600,
        .solar_constant = 1361,
        .rotation_time = 86400,
        .axial_tilt = 0,
        .paused = true,
        .daylight = true,
        .display_mode = 0,
        .camera = .{ 0, -9000, 1000 },
        .camera_target = .{ 0, -9000, 1000 },
        .camera_distance = 9055,
        .target_distance = 9055,
        .nitrogen = 10,
        .oxygen = 2,
        .carbon_dioxide = 1,
        .plant_generations = 8,
        .plant_births = 154,
        .rabbit_births = 9,
        .rabbit_meals = 32,
        .rabbit_deaths = 2,
        .plant_color = 530,
        .elevation = &([_]f32{5001} ** 12),
        .temperature = &([_]f32{293.15} ** 12),
        .vegetation = &([_]f32{0.75} ** 12),
        .water = &([_]f32{0} ** 12),
        .vapor = &([_]f32{0.5} ** 12),
        .rainfall = &([_]f32{0.1} ** 12),
        .wind = &([_][2]f32{.{ 1, 2 }} ** 12),
        .wind_error = &([_][2]f32{.{ 0.1, 0.2 }} ** 12),
        .plants = &([_]Plant{.{ .optimum = 302, .generation = 8 }} ** 12),
        .rabbits = &.{ .{ .position = .{ 0, -5001, 1 }, .velocity = .{ 0.1, 0.2, 0.3 }, .born = 100000, .state = .gestation, .gestation_since = 120000, .female = true, .satiety = 83, .criteria = 0.4, .cooldown = 360, .random = .{ 1, 2, 3, 4 } }, .{ .position = .{ 10, -5001, 1 }, .velocity = .{ 0, 0, 0 }, .born = 100001, .state = .go_to_point, .target = .{ 25, -5001, 1 }, .female = false, .satiety = 75, .criteria = 0.3, .cooldown = 0, .random = .{ 10, 20, 30, 40 } } },
    };
}

test "versioned world roundtrip preserves rabbits, growth, climate and exact PRNG" {
    const original = fixture();
    const bytes = try std.json.stringifyAlloc(std.testing.allocator, original, .{});
    defer std.testing.allocator.free(bytes);
    var loaded = try parse(std.testing.allocator, bytes);
    defer loaded.deinit();
    try std.testing.expectEqual(original.seed, loaded.value.seed);
    try std.testing.expectEqualSlices(f32, original.elevation, loaded.value.elevation);
    try std.testing.expectEqualSlices(f32, original.vegetation, loaded.value.vegetation);
    try std.testing.expectEqual(original.plant_births, loaded.value.plant_births);
    try std.testing.expectEqual(original.rabbit_meals, loaded.value.rabbit_meals);
    try std.testing.expectEqualDeep(original.plants[0], loaded.value.plants[0]);
    try std.testing.expectEqualDeep(original.rabbits[0], loaded.value.rabbits[0]);
    try std.testing.expectEqualDeep(original.rabbits[1], loaded.value.rabbits[1]);
    var before = std.rand.DefaultPrng{ .s = original.rabbits[0].random };
    var after = std.rand.DefaultPrng{ .s = loaded.value.rabbits[0].random };
    try std.testing.expectEqual(before.next(), after.next());
}

test "corrupt incompatible and nonfinite saves rejected before application" {
    try std.testing.expectError(error.SyntaxError, parse(std.testing.allocator, "{bad save"));
    var saved = fixture();
    saved.version = 999;
    try std.testing.expectError(error.IncompatibleSave, saved.validate());
    saved = fixture();
    saved.elevation = &.{5000};
    try std.testing.expectError(error.InvalidShape, saved.validate());
    saved = fixture();
    saved.game_time = std.math.nan(f64);
    try std.testing.expectError(error.InvalidValue, saved.validate());
    saved = fixture();
    saved.camera = .{ 0, 0, 0 };
    try std.testing.expectError(error.InvalidValue, saved.validate());
}

test "legacy v1 remains sandbox with exact climate plants rabbits and topology" {
    const old = fixture();
    const with_mode = try std.json.stringifyAlloc(std.testing.allocator, old, .{});
    defer std.testing.allocator.free(with_mode);
    // Original v1 files had no mode key. Exercise that exact input shape.
    const marker = "\"mode\":\"sandbox\",";
    const offset = std.mem.indexOf(u8, with_mode, marker).?;
    const bytes = try std.mem.concat(std.testing.allocator, u8, &.{ with_mode[0..offset], with_mode[offset + marker.len ..] });
    defer std.testing.allocator.free(bytes);
    var loaded = try parse(std.testing.allocator, bytes);
    defer loaded.deinit();
    try std.testing.expectEqual(WorldMode.sandbox, loaded.value.mode);
    try std.testing.expectEqualDeep(old, loaded.value);
    var upgraded = loaded.value;
    upgraded.version = VERSION;
    const next_bytes = try std.json.stringifyAlloc(std.testing.allocator, upgraded, .{});
    defer std.testing.allocator.free(next_bytes);
    var reloaded = try parse(std.testing.allocator, next_bytes);
    defer reloaded.deinit();
    reloaded.value.version = 1;
    try std.testing.expectEqualDeep(old, reloaded.value);
}

test "legacy version cannot reinterpret original habitat as origin world" {
    var old = fixture();
    old.mode = .origin;
    try std.testing.expectError(error.IncompatibleSave, old.validate());
}

test "Origin v5 preserves cohorts lineage resources RNG and deterministic continuation" {
    var cells = [_]Microbes.Cell{Microbes.initialized(41)} ** 12;
    var stats: Microbes.Stats = .{};
    _ = Microbes.seed(&cells[0], &stats, 1);
    const env: Microbes.Environment = .{ .temperature = 303, .depth_km = 0.002, .light = 1, .carbon_available = 1, .oxygen_carbon_capacity = 1 };
    for (0..200) |_| {
        const flux = Microbes.step(&cells[0], env, 3600);
        stats.fixed_carbon += flux.fixed;
        stats.recycled_carbon += flux.recycled;
    }
    try std.testing.expect(Microbes.reproduce(&cells[0], 0, &cells[1], &stats, true));
    var original = fixture();
    original.version = VERSION;
    original.mode = .origin;
    var saved_cells: [12]SavedCell = undefined;
    for (&cells, &saved_cells) |*cell, *out| out.* = SavedCell.capture(cell);
    original.origin = .{ .model_revision = 4, .cells = &saved_cells, .stats = stats };
    const bytes = try std.json.stringifyAlloc(std.testing.allocator, original, .{});
    defer std.testing.allocator.free(bytes);
    var parsed = try parse(std.testing.allocator, bytes);
    defer parsed.deinit();
    try std.testing.expectEqualDeep(original, parsed.value);
    var before = cells[0];
    var after = parsed.value.origin.?.cells[0].runtime();
    try std.testing.expectEqualDeep(Microbes.step(&before, env, 86400), Microbes.step(&after, env, 86400));
    try std.testing.expectEqualDeep(before, after);
    try std.testing.expectEqual(Microbes.random(&before.rng), Microbes.random(&after.rng));
    try std.testing.expectEqualDeep(stats, parsed.value.origin.?.stats);
}

test "Origin rejects absent state invalid shape resources lineage RNG and version confusion" {
    var saved = fixture();
    saved.version = VERSION;
    saved.mode = .origin;
    try std.testing.expectError(error.InvalidShape, saved.validate());
    var cells = [_]Microbes.Cell{Microbes.initialized(42)} ** 12;
    var saved_cells: [12]SavedCell = undefined;
    for (&cells, &saved_cells) |*cell, *out| out.* = SavedCell.capture(cell);
    saved.origin = .{ .model_revision = 4, .cells = &saved_cells, .stats = .{} };
    try saved.validate();
    cells[0].nutrient = std.math.nan(f32);
    saved_cells[0] = SavedCell.capture(&cells[0]);
    try std.testing.expectError(error.InvalidValue, saved.validate());
    cells[0] = Microbes.initialized(42);
    cells[0].rng = 0;
    saved_cells[0] = SavedCell.capture(&cells[0]);
    try std.testing.expectError(error.InvalidValue, saved.validate());
    cells[0] = Microbes.initialized(42);
    cells[0].cohorts[0] = .{ .biomass = 0.01, .lineage = 1, .parent = 1 };
    saved_cells[0] = SavedCell.capture(&cells[0]);
    try std.testing.expectError(error.InvalidValue, saved.validate());
    cells[0] = Microbes.initialized(42);
    cells[0].detritus = -1;
    saved_cells[0] = SavedCell.capture(&cells[0]);
    try std.testing.expectError(error.InvalidValue, saved.validate());
    cells[0] = Microbes.initialized(42);
    saved.origin.?.cells = saved_cells[0..11];
    try std.testing.expectError(error.InvalidShape, saved.validate());
    saved.origin.?.cells = &saved_cells;
    saved.version = 1;
    try std.testing.expectError(error.IncompatibleSave, saved.validate());
    saved.version = VERSION;
    saved.mode = .sandbox;
    saved_cells[0] = SavedCell.capture(&cells[0]);
    try std.testing.expectError(error.InvalidValue, saved.validate());
}

test "v2 wire migration preserves tiny colonies resources IDs RNG and pads only" {
    const old_cell_json =
        \\{"cohorts":[{"biomass":0.000001,"optimum":301.25,"efficiency":0.85,"generation":4,"lineage":12,"parent":9,"reproduction_credit":0.017},{"biomass":0.12,"optimum":309,"efficiency":1.1,"generation":3,"lineage":9,"parent":2,"reproduction_credit":0.04}],"nutrient":0.031,"detritus":0.002,"rng":18446744073709551600}
    ;
    var legacy = try std.json.parseFromSlice(SavedCell, std.testing.allocator, old_cell_json, .{});
    defer legacy.deinit();
    const migrated = legacy.value.runtime();
    try std.testing.expectEqual(@as(usize, 4), migrated.cohorts.len);
    try std.testing.expectEqualDeep(legacy.value.cohorts[0], migrated.cohorts[0]);
    try std.testing.expectEqualDeep(legacy.value.cohorts[1], migrated.cohorts[1]);
    try std.testing.expectEqual(@as(f32, 0), migrated.cohorts[0].structure);
    try std.testing.expectEqualDeep(Microbes.Cohort{}, migrated.cohorts[2]);
    try std.testing.expectEqualDeep(Microbes.Cohort{}, migrated.cohorts[3]);
    try std.testing.expectEqual(legacy.value.rng, migrated.rng);
    try std.testing.expectEqual(legacy.value.nutrient, migrated.nutrient);
    try std.testing.expectEqual(legacy.value.detritus, migrated.detritus);
    const old_cells = [_]SavedCell{legacy.value} ** 12;
    var saved = fixture();
    saved.version = 2;
    saved.mode = .origin;
    saved.origin = .{ .cells = &old_cells, .stats = .{ .next_lineage = 13, .births = 10 } };
    try saved.validate();
    const new_cells = [_]SavedCell{SavedCell.capture(&migrated)} ** 12;
    saved.version = VERSION;
    saved.origin.?.model_revision = 4;
    saved.origin.?.cells = &new_cells;
    const bytes = try std.json.stringifyAlloc(std.testing.allocator, saved, .{});
    defer std.testing.allocator.free(bytes);
    var parsed = try parse(std.testing.allocator, bytes);
    defer parsed.deinit();
    try std.testing.expectEqualDeep(saved, parsed.value);
    try std.testing.expectEqualDeep(migrated, parsed.value.origin.?.cells[0].runtime());
}

test "v3 structural state migrates with zero feeding then v4 preserves real consumption" {
    const legacy_json =
        \\{"cohorts":[{"biomass":0.023,"optimum":301,"efficiency":0.9,"structure":0.27,"generation":5,"lineage":14,"parent":8,"reproduction_credit":0.07},{},{},{}],"nutrient":0.043,"detritus":0.017,"rng":18446744073709551599}
    ;
    var legacy = try std.json.parseFromSlice(SavedCell, std.testing.allocator, legacy_json, .{});
    defer legacy.deinit();
    var migrated = legacy.value.runtime();
    try std.testing.expectEqual(@as(f32, 0), migrated.cohorts[0].feeding);
    try std.testing.expectEqual(@as(f32, 0), migrated.cohorts[0].lifetime_grazed);
    try std.testing.expectEqualDeep(legacy.value.cohorts[0], migrated.cohorts[0]);
    const old_cells = [_]SavedCell{legacy.value} ** 12;
    var saved = fixture();
    saved.version = 3;
    saved.mode = .origin;
    saved.origin = .{ .model_revision = 2, .cells = &old_cells, .stats = .{ .next_lineage = 15, .births = 11 } };
    try saved.validate();
    migrated.cohorts[0].feeding = 0.42;
    migrated.cohorts[0].lifetime_grazed = 0.125;
    const new_cells = [_]SavedCell{SavedCell.capture(&migrated)} ** 12;
    saved.version = VERSION;
    saved.origin.?.model_revision = 4;
    saved.origin.?.cells = &new_cells;
    saved.origin.?.stats.grazed_carbon = 12345.125;
    saved.origin.?.stats.grazing_respired_carbon = 4567.25;
    const bytes = try std.json.stringifyAlloc(std.testing.allocator, saved, .{});
    defer std.testing.allocator.free(bytes);
    var parsed = try parse(std.testing.allocator, bytes);
    defer parsed.deinit();
    try std.testing.expectEqualDeep(saved, parsed.value);
    try std.testing.expectEqualDeep(migrated, parsed.value.origin.?.cells[0].runtime());
    migrated.cohorts[0].feeding = std.math.nan(f32);
    try std.testing.expectError(error.InvalidValue, saved.validate());
    migrated.cohorts[0].feeding = 0.42;
    migrated.cohorts[0].lifetime_grazed = -1;
    try std.testing.expectError(error.InvalidValue, saved.validate());
    migrated.cohorts[0].lifetime_grazed = 0.125;
    saved.origin.?.stats.grazing_respired_carbon = std.math.inf(f64);
    try std.testing.expectError(error.InvalidValue, saved.validate());
}

test "sparse exactness retains inactive history signed zero and movement events" {
    var cells = [_]Microbes.Cell{.{}} ** 12;
    cells[0].cohorts[1].biomass = -0.0;
    cells[0].cohorts[2].lineage = 91; // inactive history is not canonical empty
    cells[1].cohorts[0] = .{ .biomass = 0.05, .lineage = 1, .mobility = 0.4, .relocations = 2, .last_from = 0, .last_to = 1, .last_move_time = 120000, .lifetime_grazed = 0.125 };
    try std.testing.expect(!canonicalEmpty(cells[0].cohorts[1]));
    try std.testing.expect(!canonicalEmpty(cells[0].cohorts[2]));
    const sparse = try captureSparse(std.testing.allocator, &cells);
    defer sparse.deinit(std.testing.allocator);
    try std.testing.expectEqual(@as(usize, 3), sparse.entries.len);
    var saved = fixture();
    saved.version = VERSION;
    saved.mode = .origin;
    saved.origin = .{ .model_revision = 4, .cohort_encoding = .sparse_indexed, .cells = sparse.cells, .stats = .{ .next_lineage = 100, .relocations = 2, .movement_respired_carbon = 0.0125 } };
    try saved.validate();
    const bytes = try std.json.stringifyAlloc(std.testing.allocator, saved, .{});
    defer std.testing.allocator.free(bytes);
    var parsed = try parse(std.testing.allocator, bytes);
    defer parsed.deinit();
    for (cells, parsed.value.origin.?.cells) |before, wire| {
        const after = wire.runtime();
        try std.testing.expectEqualDeep(before, after);
        for (before.cohorts, after.cohorts) |a, b| {
            try std.testing.expectEqual(@as(u32, @bitCast(a.biomass)), @as(u32, @bitCast(b.biomass)));
            try std.testing.expectEqual(@as(u64, @bitCast(a.last_move_time)), @as(u64, @bitCast(b.last_move_time)));
        }
    }
    const again = try std.json.stringifyAlloc(std.testing.allocator, parsed.value, .{});
    defer std.testing.allocator.free(again);
    try std.testing.expectEqualSlices(u8, bytes, again);
    var bad_entries = [_]IndexedCohort{ .{ .index = 0, .value = .{} }, .{ .index = 0, .value = .{} } };
    const original = sparse.cells[0];
    sparse.cells[0].sparse = &bad_entries;
    try std.testing.expectError(error.InvalidValue, saved.validate());
    bad_entries[1].index = 4;
    try std.testing.expectError(error.InvalidValue, saved.validate());
    sparse.cells[0] = original;
    sparse.cells[0].cohorts = &cells[0].cohorts;
    try std.testing.expectError(error.InvalidShape, saved.validate());
    sparse.cells[0] = original;
    sparse.entries[2].value.last_to = 3;
    try std.testing.expectError(error.InvalidValue, saved.validate());
}

test "fully occupied sparse capture retains all four slots without loss" {
    var cells = [_]Microbes.Cell{.{}} ** 12;
    for (&cells) |*cell| for (&cell.cohorts, 0..) |*cohort, index| {
        cohort.* = .{ .biomass = 0.1, .lineage = index + 1, .optimum = 290 + @as(f32, @floatFromInt(index)) };
    };
    const sparse = try captureSparse(std.testing.allocator, &cells);
    defer sparse.deinit(std.testing.allocator);
    try std.testing.expectEqual(@as(usize, 48), sparse.entries.len);
    for (cells, sparse.cells) |before, wire| try std.testing.expectEqualDeep(before, wire.runtime());
}

test "v4 grazing wire defaults movement fields without altering feeding history" {
    const wire =
        \\{"cohorts":[{"biomass":0.04,"optimum":303,"efficiency":1,"structure":0.12,"feeding":0.32,"lifetime_grazed":0.1875,"lineage":7,"parent":3,"generation":2},{},{},{}],"nutrient":0.03,"detritus":0.01,"rng":778899}
    ;
    var parsed = try std.json.parseFromSlice(SavedCell, std.testing.allocator, wire, .{});
    defer parsed.deinit();
    const before = parsed.value.runtime();
    try std.testing.expectEqual(@as(f32, 0), before.cohorts[0].mobility);
    try std.testing.expectEqual(@as(u32, 0), before.cohorts[0].relocations);
    const dense = [_]SavedCell{parsed.value} ** 12;
    var old = fixture();
    old.version = 4;
    old.mode = .origin;
    old.origin = .{ .model_revision = 3, .cells = &dense, .stats = .{ .next_lineage = 8, .births = 6, .grazed_carbon = 45.25, .grazing_respired_carbon = 12.5 } };
    try old.validate();
    const runtime = [_]Microbes.Cell{before} ** 12;
    const sparse = try captureSparse(std.testing.allocator, &runtime);
    defer sparse.deinit(std.testing.allocator);
    var migrated = old;
    migrated.version = VERSION;
    migrated.origin.?.model_revision = 4;
    migrated.origin.?.cohort_encoding = .sparse_indexed;
    migrated.origin.?.cells = sparse.cells;
    try migrated.validate();
    for (sparse.cells) |cell| try std.testing.expectEqualDeep(before, cell.runtime());
    try std.testing.expectEqualDeep(old.origin.?.stats, migrated.origin.?.stats);
}

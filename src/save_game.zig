//! Filesystem save adapter. Browser shell syncs /saves to IndexedDB explicitly.
const std = @import("std");
pub const schema = @import("save_schema.zig");
pub const path = "/saves/world.json";

pub fn capture(allocator: std.mem.Allocator, state: anytype) !schema.Save {
    const p = &state.planet;
    const wind = try allocator.alloc([2]f32, p.airVelocity.len);
    const wind_error = try allocator.alloc([2]f32, p.airPositionError.len);
    const rabbits = try allocator.alloc(schema.Rabbit, p.lifeforms.items.len);
    for (p.airVelocity, wind) |v, *out| out.* = v.data;
    for (p.airPositionError, wind_error) |v, *out| out.* = v.data;
    for (p.lifeforms.items, rabbits) |life, *out| {
        out.* = .{ .position = life.position.data, .velocity = life.velocity.data, .born = life.timeBorn, .state = switch (life.state) {
            .wander => .wander,
            .go_to_point => .go_to_point,
            .gestation => .gestation,
        }, .female = life.genome.gender == .Female, .satiety = life.satiety, .criteria = life.sexualCriteria, .cooldown = life.reproductionCooldown, .random = life.prng.s };
        switch (life.state) {
            .go_to_point => |v| out.target = v.data,
            .gestation => |info| out.gestation_since = info.since,
            else => {},
        }
    }
    var origin: ?schema.Origin = null;
    if (p.worldMode == .origin) {
        const sparse = try schema.captureSparse(allocator, p.microbeCells);
        origin = .{ .model_revision = schema.VERSION - 1, .cohort_encoding = .sparse_indexed, .cells = sparse.cells, .stats = p.microbeStats };
    }
    return .{ .version = schema.VERSION, .mode = p.worldMode, .origin = origin, .radius = p.radius, .subdivisions = p.numSubdivisions, .seed = p.seed, .game_time = state.gameTime, .time_scale = state.timeScale, .solar_constant = state.solarConstant, .rotation_time = state.planetRotationTime, .axial_tilt = state.axialTilt, .paused = state.paused, .daylight = state.stableDaylight, .display_mode = @intCast(@intFromEnum(state.displayMode)), .camera = state.cameraPos.data, .camera_target = state.targetCameraPos.data, .camera_distance = state.cameraDistance, .target_distance = state.targetCameraDistance, .nitrogen = p.averageNitrogenMass, .oxygen = p.averageOxygenMass, .carbon_dioxide = p.averageCarbonDioxideMass, .plant_generations = p.plantGenerations, .plant_births = p.plantBirths, .rabbit_births = p.rabbitBirths, .rabbit_meals = p.rabbitMeals, .rabbit_deaths = p.rabbitDeaths, .plant_color = p.plantColorWavelength, .elevation = p.elevation, .temperature = p.temperature, .vegetation = p.vegetation, .water = p.waterMass, .vapor = p.waterVaporMass, .rainfall = p.rainfall, .wind = wind, .wind_error = wind_error, .plants = p.plantTraits, .rabbits = rabbits };
}
pub fn write(state: anytype, allocator: std.mem.Allocator) !void {
    var arena = std.heap.ArenaAllocator.init(allocator);
    defer arena.deinit();
    const saved = try capture(arena.allocator(), state);
    try saved.validate();
    try std.fs.cwd().makePath("/saves");
    const file = try std.fs.cwd().createFile("/saves/world.tmp", .{});
    var closed = false;
    defer if (!closed) file.close();
    var buffer = std.io.bufferedWriter(file.writer());
    try std.json.stringify(saved, .{}, buffer.writer());
    try buffer.flush();
    file.close();
    closed = true;
    try std.fs.cwd().rename("/saves/world.tmp", path);
}
pub fn read(allocator: std.mem.Allocator) !std.json.Parsed(schema.Save) {
    const bytes = try std.fs.cwd().readFileAlloc(allocator, path, 128 * 1024 * 1024);
    defer allocator.free(bytes);
    return schema.parse(allocator, bytes);
}
/// All validation and allocations precede mutation. A failed load retains live data.
pub fn apply(state: anytype, saved: schema.Save) !void {
    try saved.validate();
    const p = &state.planet;
    if (p.radius != saved.radius or p.numSubdivisions != saved.subdivisions or p.vertices.len != saved.elevation.len) return error.IncompatibleSave;
    try p.lifeforms.ensureTotalCapacity(p.simulationArena.allocator(), saved.rabbits.len);
    // Capacity changes may allocate but do not alter the active world mode/data.
    // No fallible operations follow this reservation boundary.
    if (saved.mode == .origin) try p.ensureMicrobeStorage();
    p.worldMode = saved.mode;
    if (saved.origin) |origin| {
        for (p.microbeCells, origin.cells) |*cell, saved_cell| cell.* = saved_cell.runtime();
        p.microbeStats = origin.stats;
    } else {
        // Retain allocated storage for later loads, never reinterpret Sandbox
        // vegetation as microbial biomass or activate stale Origin state.
        p.microbeStats = .{};
        for (p.microbeCells) |*cell| cell.* = .{};
    }
    @memcpy(p.elevation, saved.elevation);
    @memcpy(p.temperature, saved.temperature);
    @memcpy(p.vegetation, saved.vegetation);
    @memcpy(p.waterMass, saved.water);
    @memcpy(p.waterVaporMass, saved.vapor);
    @memcpy(p.rainfall, saved.rainfall);
    @memcpy(p.plantTraits, saved.plants);
    @memcpy(p.newTemperature, saved.temperature);
    @memcpy(p.newWaterMass, saved.water);
    @memcpy(p.newWaterVaporMass, saved.vapor);
    @memcpy(p.vegetationSnapshot, saved.vegetation);
    for (p.airVelocity, saved.wind) |*v, data| v.data = data;
    for (p.airPositionError, saved.wind_error) |*v, data| v.data = data;
    p.seed = saved.seed;
    p.averageNitrogenMass = saved.nitrogen;
    p.averageOxygenMass = saved.oxygen;
    p.averageCarbonDioxideMass = saved.carbon_dioxide;
    p.plantGenerations = saved.plant_generations;
    p.plantBirths = saved.plant_births;
    p.rabbitBirths = saved.rabbit_births;
    p.rabbitMeals = saved.rabbit_meals;
    p.rabbitDeaths = saved.rabbit_deaths;
    p.plantColorWavelength = saved.plant_color;
    p.lifeforms.clearRetainingCapacity();
    for (saved.rabbits) |rabbit| {
        const Life = @TypeOf(p.lifeforms.items[0]);
        var life: Life = undefined;
        life.position = .{ .data = rabbit.position };
        life.velocity = .{ .data = rabbit.velocity };
        life.kind = .Rabbit;
        life.timeBorn = rabbit.born;
        life.genome = .{ .gender = if (rabbit.female) .Female else .Male };
        life.satiety = rabbit.satiety;
        life.sexualCriteria = rabbit.criteria;
        life.reproductionCooldown = rabbit.cooldown;
        life.prng = .{ .s = rabbit.random };
        life.state = switch (rabbit.state) {
            .wander => .wander,
            .go_to_point => .{ .go_to_point = .{ .data = rabbit.target } },
            .gestation => .{ .gestation = .{ .since = rabbit.gestation_since } },
        };
        p.lifeforms.appendAssumeCapacity(life);
    }
    state.gameTime = saved.game_time;
    state.renderGameTime = saved.game_time;
    state.timeScale = saved.time_scale;
    state.simulationClock.reset();state.rawFrameDelta=null;state.simulationStepsLastFrame=0;
    state.solarConstant = saved.solar_constant;
    state.planetRotationTime = saved.rotation_time;
    state.axialTilt = saved.axial_tilt;
    state.paused = saved.paused;
    state.stableDaylight = saved.daylight;
    state.displayMode = @enumFromInt(saved.display_mode);
    state.cameraPos.data = saved.camera;
    state.targetCameraPos.data = saved.camera_target;
    state.cameraDistance = saved.camera_distance;
    state.targetCameraDistance = saved.target_distance;
    state.freeCam = false;
    var total_temperature: f64 = 0;
    for (saved.temperature) |temperature| total_temperature += temperature;
    state.meanTemperature = @floatCast(total_temperature / @as(f64, @floatFromInt(saved.temperature.len)));
    // Rendering/input caches and transient effects belong to the previous view.
    if (@hasField(@TypeOf(state.*), "colonyTargets")) state.colonyTargets.count = 0;
    if (@hasField(@TypeOf(state.*), "seedTargets")) state.seedTargets.count = 0;
    if (@hasField(@TypeOf(state.*), "detritusFinder")) state.detritusFinder = .{};
    if (@hasField(@TypeOf(state.*), "godReceipt")) state.godReceipt = null;
    if (@hasField(@TypeOf(state.*), "godEffectSeconds")) state.godEffectSeconds = 0;
    state.selectedTool = .None;
    state.selectedPoint = 0;
    state.clickedPoint = 0;
    state.pointerOnPlanet = false;
    state.showEscapeMenu = false;
    state.showPlanetControl = false;
    state.showPointDetails = false;
    state.debug_clearWater = false;
    state.debug_deluge = false;
    state.debug_spawnRabbits = false;
    state.defer_saveGame = false;
    p.uploadNo = 0;
    // Observation effects are transient, not historical save-state facts.
    if(@hasField(@TypeOf(p.*),"propaguleFeedback")){
        p.propaguleFeedback=.{};p.propaguleAttempts=0;p.propaguleArrivals=0;p.propaguleTrackedLosses=0;
    }
    if(@hasField(@TypeOf(state.*),"colonyPeek"))state.colonyPeek.clear();
    if(@hasField(@TypeOf(state.*),"propaguleVisuals"))state.propaguleVisuals=.{};
    if(@hasField(@TypeOf(state.*),"watchLifeView"))state.watchLifeView=false;
}

/// Restore the saved grid exactly. Build/apply a replacement in isolation so
/// parse, validation, generation or allocation failure cannot discard a world.
/// Caller must finish pending simulation/normal jobs before this operation.
pub fn replaceWorld(state: anytype, saved: schema.Save) !void {
    try saved.validate();
    // Deinit must never spin on a queued browser job that cannot progress.
    if (state.planet.normalComputeJob) |job| {
        if (!job.isCompleted()) return error.WorldBusy;
    }
    if (state.planet.radius == saved.radius and state.planet.numSubdivisions == saved.subdivisions) {
        return apply(state, saved);
    }
    const Planet = @TypeOf(state.planet);
    const replacement = try Planet.generate(state.planet.allocator, saved.subdivisions, saved.radius, saved.seed, .{ .generate_terrain = false });
    var candidate = state.*;
    candidate.planet = replacement;
    errdefer candidate.planet.deinit();
    try apply(&candidate, saved);
    const previous = state.planet;
    state.* = candidate;
    previous.deinit();
}

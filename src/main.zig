const std = @import("std");
// Emscripten owns linear-memory growth and must refresh its JS heap views.
// Zig's default wasm page allocator calls memory.grow directly and detaches them.
pub const os = if (@import("builtin").os.tag == .emscripten) struct {
    pub const heap = struct {
        pub const page_allocator = std.heap.c_allocator;
    };
} else struct {};
const is_web = @import("builtin").target.cpu.arch == .wasm32;
extern "c" fn emscripten_get_now() f64;
extern "c" fn emscripten_set_main_loop(callback: *const fn () callconv(.C) void, fps: c_int, simulate_infinite_loop: c_int) void;
pub const gl = @import("gl");
const glfw = @import("glfw");
const za = @import("zalgebra");
const tracy = @import("vendor/tracy.zig");

const Renderer = @import("renderer.zig").Renderer;
const Texture = @import("renderer.zig").Texture;
const AudioSubsystem = @import("audio.zig").AudioSubsystem;
const EventLoop = @import("loop.zig").EventLoop;
const Job = @import("loop.zig").Job;

var renderer: Renderer = undefined;

const SplashScreenState = @import("states/splash_screen.zig").SplashScreenState;
const MainMenuState = @import("states/main_menu.zig").MainMenuState;
const GameIntroState = @import("states/game_intro.zig").GameIntroState;
const PlayState = @import("states/play.zig").PlayState;

pub const log_level = .debug;

pub const GameState = union(enum) {
    SplashScreen: SplashScreenState,
    MainMenu: MainMenuState,
    GameIntro: GameIntroState,
    Playing: PlayState,
};

pub const Game = struct {
    state: GameState,
    /// False if the state doesn't contain a valid value
    state_init: bool = false,
    startOriginNext: bool = false,
    newWorldChoice: @import("world_setup.zig").Choice = .{},
    audio: AudioSubsystem,
    window: glfw.Window,
    renderer: *Renderer,
    loop: *EventLoop,
    allocator: std.mem.Allocator,
    imgui_state: std.StringHashMap(@import("ui.zig").UiComponentState),
    fps: f32 = 60,
    /// Job that will be deinit at the end. In the code this is only used for a
    /// job's that's created to call Game.setState from a state, but then can't
    /// be deinit immediately because otherwise you'd have a biting-its-tail problem
    ///   setState -> calls deinit -> deinits setState's (and deinit's) stack
    ///      = /!\ PROBLEM
    /// So the job in this field will only be called during Game.deinit
    /// Note: it could be called sooner, as it only needs to be called anytime
    /// after setState.
    deinitJob: ?*Job(void) = null,
    oldMouseX: f32 = 0,
    oldMouseY: f32 = 0,

    pub fn init(allocator: std.mem.Allocator, window: glfw.Window, ptrRenderer: *Renderer, ptrLoop: *EventLoop) !Game {
        return Game{
            .state = .{ .MainMenu = undefined },
            .audio = try AudioSubsystem.init(allocator),
            .window = window,
            .renderer = ptrRenderer,
            .loop = ptrLoop,
            .allocator = allocator,
            .imgui_state = std.StringHashMap(@import("ui.zig").UiComponentState).init(allocator),
        };
    }

    pub fn setState(self: *Game, comptime NewState: type) void {
        std.log.info("Loading {s}...", .{@typeName(NewState)});
        defer std.log.info("Loaded", .{});

        const new_state = NewState.init(self);
        if (self.state_init) self.deinitState();
        self.imgui_state.clearRetainingCapacity();

        inline for (std.meta.fields(GameState)) |field| {
            if (field.type == NewState) {
                self.state = @unionInit(GameState, field.name, new_state);
                self.state_init = true;
                return;
            }
        }
        @compileError(@typeName(NewState) ++ " is not in the GameState union");
    }

    pub fn getTime() f64 {
        if (is_web) return emscripten_get_now();
        return @as(f64, @floatFromInt(std.time.milliTimestamp()));
    }

    pub fn deinitState(self: *Game) void {
        inline for (std.meta.fields(GameState)) |field| {
            // if the field is active
            if (std.mem.eql(u8, @tagName(std.meta.activeTag(game.state)), field.name)) {
                if (@hasDecl(field.type, "deinit")) {
                    @field(self.state, field.name).deinit(self);
                    return;
                }
            }
        }
    }

    pub fn deinit(self: *Game) void {
        if (self.deinitJob) |job| {
            job.deinit();
        }
        self.deinitState();
        self.audio.deinit();
        self.imgui_state.deinit();
    }
};

var game: Game = undefined;

fn mousePressed(window: glfw.Window, button: glfw.mouse_button.MouseButton) void {
    _ = window;
    inline for (std.meta.fields(GameState)) |field| {
        // if it is the current game state
        if (std.mem.eql(u8, @tagName(std.meta.activeTag(game.state)), field.name)) {
            // and it has mousePressed()
            if (comptime @hasDecl(field.type, "mousePressed")) {
                // call it
                @field(game.state, field.name).mousePressed(&game, button);
                return;
            }
        }
    }
}

fn mouseScroll(window: glfw.Window, xOffset: f64, yOffset: f64) void {
    _ = window;
    _ = xOffset;
    inline for (std.meta.fields(GameState)) |field| {
        // if it is the current game state
        if (std.mem.eql(u8, @tagName(std.meta.activeTag(game.state)), field.name)) {
            // and it has mouseScroll()
            if (comptime @hasDecl(field.type, "mouseScroll")) {
                // call it
                @field(game.state, field.name).mouseScroll(&game, yOffset);
                return;
            }
        }
    }
}

fn cursorPosCallback(window: glfw.Window, xpos: f64, ypos: f64) void {
    _ = window;
    inline for (std.meta.fields(GameState)) |field| {
        // if it is the current game state
        if (std.mem.eql(u8, @tagName(std.meta.activeTag(game.state)), field.name)) {
            // and it has mouseMoved()
            if (comptime @hasDecl(field.type, "mouseMoved")) {
                // call it
                @field(game.state, field.name).mouseMoved(
                    &game,
                    @as(f32, @floatCast(xpos)),
                    @as(f32, @floatCast(ypos)),
                    @as(f32, @floatCast(xpos)) - game.oldMouseX,
                    @as(f32, @floatCast(ypos)) - game.oldMouseY,
                );
                game.oldMouseX = @as(f32, @floatCast(xpos));
                game.oldMouseY = @as(f32, @floatCast(ypos));
                return;
            }
        }
    }
}

fn keyCallback(window: glfw.Window, key: glfw.Key, scancode: i32, action: glfw.Action, mods: glfw.Mods) void {
    if (key == .F11 and action == .press) {
        if (window.getMonitor() == null) {
            const monitor = glfw.Monitor.getPrimary().?;
            const videoMode = monitor.getVideoMode().?;
            window.setMonitor(monitor, 0, 0, videoMode.getWidth(), videoMode.getHeight(), null);
        } else {
            window.setMonitor(null, 100, 100, 1280, 720, null);
        }
    }

    inline for (std.meta.fields(GameState)) |field| {
        // if it is the current game state
        if (std.mem.eql(u8, @tagName(std.meta.activeTag(game.state)), field.name)) {
            // and it has mouseMoved()
            if (comptime @hasDecl(field.type, "keyCallback")) {
                // call it
                @field(game.state, field.name).keyCallback(&game, key, scancode, action, mods);
                return;
            }
        }
    }
}

fn render(window: glfw.Window) void {
    game.audio.update();

    const size = window.getFramebufferSize();
    gl.viewport(0, 0, @as(c_int, @intCast(size.width)), @as(c_int, @intCast(size.height)));
    gl.clearColor(0, 0, 0, 1);
    gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT | gl.STENCIL_BUFFER_BIT);
    renderer.framebufferSize = za.Vec2.new(@as(f32, @floatFromInt(size.width)), @as(f32, @floatFromInt(size.height)));

    const zone = tracy.ZoneN(@src(), "Render");
    defer zone.End();
    // Call the render() function of the current game state
    inline for (std.meta.fields(GameState)) |field| {
        if (std.mem.eql(u8, @tagName(std.meta.activeTag(game.state)), field.name)) {
            @field(game.state, field.name).render(&game, &renderer);
        }
    }

    const ui_stage=PerformanceDetails.beginStage();
    defer PerformanceDetails.endStage(ui_stage,.ui);
    renderer.startUI();
    // Call the renderUI() function of the current game state, if it has one.
    inline for (std.meta.fields(GameState)) |field| {
        if (std.mem.eql(u8, @tagName(std.meta.activeTag(game.state)), field.name)) {
            if (comptime @hasDecl(field.type, "renderUI")) {
                @field(game.state, field.name).renderUI(&game, &renderer);
                break;
            }
        }
    }
    renderer.endUI();
}

fn updateLoop(loop: *EventLoop, window: glfw.Window) void {
    _ = loop;
    var fullLoopTime: f32 = 0;
    var dt: f32 = 0.016;
    while (!window.shouldClose()) {
        // Call the update() function of the current game state, if it has one.

        var timer = std.time.Timer.start() catch unreachable; // this just assumes a clock is available
        inline for (std.meta.fields(GameState)) |field| {
            if (std.mem.eql(u8, @tagName(std.meta.activeTag(game.state)), field.name)) {
                if (comptime @hasDecl(field.type, "update")) {
                    dt = dt * 0.9 + fullLoopTime * 0.1; // smoothly go to fullLoopTime
                    @field(game.state, field.name).update(&game, dt);
                    break;
                }
            }
        }
        const elapsed = timer.read();
        std.time.sleep((16666666 * 2) -| elapsed);
        fullLoopTime = @as(f32, @floatFromInt(timer.read())) / @as(f32, @floatFromInt(std.time.ns_per_s));
    }
}

const perlin = @import("perlin.zig").p2d;

/// This is used by zig-opengl library to load OpenGL functions from GLFW
fn getProcAddress(_: void, name: [:0]const u8) ?*anyopaque {
    const proc = glfw.getProcAddress(name);
    return @as(?*anyopaque, @ptrFromInt(@intFromPtr(proc)));
}

fn mouseButtonCallback(window: glfw.Window, button: glfw.mouse_button.MouseButton, action: glfw.Action, _: glfw.Mods) void {
    if (action == .press) {
        mousePressed(window, button);
    }
}

/// Shows an error message box on Windows, logs on console on other platforms.
/// In all cases it exists with return code 1.
fn fatalCrash(allocator: std.mem.Allocator, comptime fmt: []const u8, args: anytype) noreturn {
    const L = std.unicode.utf8ToUtf16LeStringLiteral;
    if (@import("builtin").target.os.tag == .windows) {
        const msgUtf8 = std.fmt.allocPrint(allocator, fmt, args) catch std.process.exit(1);
        defer allocator.free(msgUtf8);

        const msgUtf16 = std.unicode.utf8ToUtf16LeWithNull(allocator, msgUtf8) catch std.process.exit(1);
        defer allocator.free(msgUtf16);

        _ = std.os.windows.user32.messageBoxW(null, msgUtf16, L("Fatal Error"), std.os.windows.user32.MB_ICONERROR | std.os.windows.user32.MB_OK) catch std.process.exit(1);
    } else {
        std.log.err(fmt, args);
    }
    std.process.exit(1);
}

pub fn main() !void {
    if (is_web) return main_web();
    std.valgrind.callgrind.stopInstrumentation();
    // Only manually catch errors (and show them as message boxes) on Windows
    if (@import("builtin").target.os.tag == .windows) {
        main_wrap() catch |err| {
            var buffer: [16 * 1024]u8 = undefined;
            var stream = std.io.fixedBufferStream(&buffer);
            try stream.writer().print("Dang, we crashed! And it says {s} !\n", .{@errorName(err)});
            if (@errorReturnTrace()) |trace| {
                try stream.writer().print("\r\n  You even got a stack trace!\r\n\r\n", .{});
                try std.debug.writeStackTrace(trace.*, stream.writer(), std.heap.page_allocator, try std.debug.getSelfDebugInfo(), std.debug.TTY.Config.no_color);
            }
            fatalCrash(std.heap.page_allocator, "{s}", .{stream.getWritten()});
        };
    } else {
        // Let Zig handle it (it'll log in the terminal, along with optional debug info)
        try main_wrap();
    }
}

// Browser state outlives main(), unlike the stack-bound native run loop.
var web_loop = EventLoop.init();
var web_previous_time: f64 = 0;
var web_initialized = false;
export fn stella_resize(width: u32, height: u32) void {
    if (is_web and web_initialized) game.window.setSize(.{ .width = @max(240, width), .height = @max(180, height) });
}

fn webPlayState() ?*PlayState {
    if (!is_web or !web_initialized or !game.state_init) return null;
    return switch (game.state) {
        .Playing => &game.state.Playing,
        else => null,
    };
}
export fn stella_zoom(steps: f32) void {
    if (webPlayState()) |state| state.zoom(steps);
}
export fn stella_focus_land() i32 {
    return if (webPlayState()) |state| (if (state.focusLand()) @as(i32, 1) else 0) else -1;
}
export fn stella_reset_view() void {
    if (webPlayState()) |state| state.resetView();
}
export fn stella_camera_distance() f32 {
    return if (webPlayState()) |state| state.cameraDistance else -1;
}
export fn stella_target_distance() f32 {
    return if (webPlayState()) |state| state.targetCameraDistance else -1;
}

var lifeSnapshotBuffer: [8192]u8 = undefined;
/// On-demand current-cell snapshot, not a fabricated historical lineage tree.
export fn stella_life_snapshot() [*:0]const u8 {
    const state = webPlayState() orelse return "{\"status\":\"no_world\"}";
    if (state.planet.worldMode != .origin) return "{\"status\":\"sandbox\"}";
    const point = state.selectedPoint;
    if (point >= state.planet.microbeCells.len) return "{\"status\":\"no_cell\"}";
    const cell = state.planet.microbeCells[point];
    const depth = state.planet.waterMass[point] * state.planet.getKmPerWaterMass();
    const surfaceLight = @max(0, state.planet.transformedPoints[point].norm().dot(state.simulationSolarVector())) * std.math.clamp(state.solarConstant / 1361, 0, 2);
    const biologicalLight = @import("simulation/microbes.zig").availableLight(surfaceLight, depth);
    const Microbes = @import("simulation/microbes.zig");
    const shares = Microbes.producerLightShares(cell, surfaceLight, depth);
    const Tissue = struct { form:[]const u8, support_mass:f32, frond_mass:f32, height_m:f32, available_light:f32, maintenance_potential:f32 };
    var tissues:[4]Tissue=undefined;
    for(cell.cohorts,0..) |co,slot| tissues[slot]=.{.form=Microbes.producerFormName(Microbes.producerForm(co)),.support_mass=co.support_mass,.frond_mass=Microbes.frondMass(co),.height_m=Microbes.producerHeightMeters(co),.available_light=shares[slot],.maintenance_potential=Microbes.supportMaintenancePerDay(co)};
    var movement_reasons: [4][]const u8 = undefined;
    for (&movement_reasons, 0..) |*reason, slot| {
        reason.* = @tagName(state.planet.microbeRelocationOpportunity(point, slot, state.gameTime).reason);
    }
    var stream = std.io.fixedBufferStream(lifeSnapshotBuffer[0 .. lifeSnapshotBuffer.len - 1]);
    std.json.stringify(.{
        .status = "origin", .cell = point, .day = state.gameTime / 86400,
        .seed_reason = @tagName(state.planet.seedEligibility(point)),
        .producer_habitat = @import("producer_habitat.zig").inspect(cell,depth,state.planet.temperature[point]),
        .temperature_c = state.planet.temperature[point] - 273.15,
        .water_m = state.planet.waterMass[point] * state.planet.getKmPerWaterMass() * 1000,
        .nutrients = cell.nutrient, .detritus = cell.detritus, .simulation_light = biologicalLight,
        .cohorts = cell.cohorts, .movement_reasons = movement_reasons, .tissues = tissues,
    }, .{ .emit_nonportable_numbers_as_strings = true }, stream.writer()) catch return "{\"status\":\"error\"}";
    lifeSnapshotBuffer[stream.pos] = 0;
    return @ptrCast(&lifeSnapshotBuffer);
}

export fn stella_world_mode() i32 {
    return if (webPlayState()) |state| (if (state.planet.worldMode == .origin) @as(i32,1) else 0) else -1;
}

export fn stella_goal_stage() i32 {
    if (webPlayState()) |state| {
        if (state.planet.worldMode == .origin) {
            return @import("habitat_feedback.zig").originStage(state.planet.microbeCells);
        }
        return @intFromEnum(@import("habitat_feedback.zig").goalStage(state.planet));
    }
    return -1;
}

export fn stella_selected_point() i32 {
    return if (webPlayState()) |state| (if (state.pointerOnPlanet) @as(i32, @intCast(state.selectedPoint)) else -1) else -1;
}
export fn stella_selected_water() f32 {
    return if (webPlayState()) |state| state.planet.waterMass[state.selectedPoint] else -1;
}
export fn stella_selected_vegetation() f32 {
    return if (webPlayState()) |state| state.planet.vegetation[state.selectedPoint] else -1;
}
export fn stella_selected_elevation() f32 {
    return if (webPlayState()) |state| state.planet.elevation[state.selectedPoint] else -1;
}
export fn stella_adjust_water(expected_point: u32, delta_m: f32) f32 {
    const state=webPlayState() orelse return std.math.nan(f32);
    return state.adjustSelectedWater(expected_point, delta_m);
}

export fn stella_set_water_target(expected_point:u32,target_m:f32) f32 {
    const state=webPlayState() orelse return std.math.nan(f32);
    return state.setSelectedWaterTarget(expected_point,target_m);
}

var godTargetBuffer:[512]u8=undefined;
export fn stella_god_target() [*:0]const u8 {
    const state=webPlayState() orelse return "{\"status\":\"no_world\"}";
    const i=state.selectedPoint;if(i>=state.planet.temperature.len)return "{\"status\":\"invalid\"}";
    var stream=std.io.fixedBufferStream(godTargetBuffer[0..godTargetBuffer.len-1]);
    std.json.stringify(.{.status="ready",.cell=i,.water_m=state.planet.waterMass[i]*state.planet.getKmPerWaterMass()*1000,.temperature_c=state.planet.temperature[i]-273.15},.{.emit_nonportable_numbers_as_strings=true},stream.writer()) catch return "{}";
    godTargetBuffer[stream.pos]=0;return @ptrCast(&godTargetBuffer);
}
var godActionBuffer:[4096]u8=undefined;
export fn stella_god_action(kind:u32,expected:u32) [*:0]const u8 {
    const state=webPlayState() orelse return "{\"failure\":\"no_world\"}";
    if(kind>1)return "{\"failure\":\"invalid\"}";
    const result=state.applyGodAction(if(kind==0).wave else .lightning,expected);
    var stream=std.io.fixedBufferStream(godActionBuffer[0..godActionBuffer.len-1]);
    std.json.stringify(.{.kind=@tagName(result.kind),.failure=@tagName(result.failure),.count=result.count,.affected=result.affected[0..result.count],.moved_mass=result.moved_mass,.moved_depth_m=result.moved_mass*state.planet.getKmPerWaterMass()*1000,.heat_joules=result.heat_joules},.{.emit_nonportable_numbers_as_strings=true},stream.writer()) catch return "{\"failure\":\"error\"}";
    godActionBuffer[stream.pos]=0;return @ptrCast(&godActionBuffer);
}

/// Leave placement overlays without moving the view or changing time/pause.
var speed_json:[512]u8=undefined;
export fn stella_set_speed(seconds:f32)i32 {
    const state=webPlayState() orelse return -1;
    if(!std.math.isFinite(seconds) or (seconds!=3600 and seconds!=21600 and seconds!=86400))return -1;
    state.timeScale=seconds;state.simulationClock.reset();return 1;
}
export fn stella_speed_snapshot()[*:0]const u8 {
    const state=webPlayState() orelse return "{\"status\":\"unavailable\"}";
    const text=std.fmt.bufPrintZ(&speed_json,"{{\"requested\":{d},\"achieved\":{d},\"paused\":{},\"step\":{d},\"steps_last_frame\":{d}}}",.{state.timeScale,state.simulationClock.achieved,state.paused,PlayState.simulation_step_seconds,state.simulationStepsLastFrame}) catch return "{}";
    return text.ptr;
}

const PerformanceDetails=@import("performance_details.zig");
var performance_json:[2048]u8=undefined;
export fn stella_performance_enable(enabled:i32)i32 {
    if(webPlayState()==null){PerformanceDetails.metrics.setEnabled(false);return -1;}
    PerformanceDetails.metrics.setEnabled(enabled==1);return 1;
}
export fn stella_performance_snapshot()[*:0]const u8 {
    const state=webPlayState() orelse return "{\"status\":\"unavailable\"}";
    const sample=PerformanceDetails.metrics.sample();
    var stream=std.io.fixedBufferStream(&performance_json);
    std.json.stringify(.{.enabled=PerformanceDetails.metrics.enabled,.world_serial=PerformanceDetails.world_serial,.paused=state.paused,.menu_open=state.showEscapeMenu or state.showPlanetControl or state.showPointDetails,.interrupted=PerformanceDetails.metrics.interrupted,.game_time=state.gameTime,.requested=state.timeScale,.cells=state.planet.transformedPoints.len,.frames=sample.frames,.ticks=sample.ticks,.physics_frames=sample.physics_frames,
      .frame_avg_ms=sample.frame_sum/@max(@as(f64,@floatFromInt(sample.frames)),1),.frame_max_ms=sample.frame_max,.frame_p95_ms=sample.frame_p95,.long_frames=sample.long_frames,
      .physics_avg_ms=sample.physics_sum/@max(@as(f64,@floatFromInt(sample.physics_frames)),1),.physics_max_ms=sample.physics_max,
      .render_cpu_avg_ms=sample.render_sum/@max(@as(f64,@floatFromInt(sample.frames)),1),.render_cpu_max_ms=sample.render_max,.render_context=PerformanceDetails.metrics.context,.stage_sum_ms=sample.stage_sum,.stage_max_ms=sample.stage_max},.{},stream.writer()) catch return "{}";
    if(stream.pos>=performance_json.len)return "{}";performance_json[stream.pos]=0;return @ptrCast(&performance_json);
}

export fn stella_fit_life() i32 {
    const state=webPlayState() orelse return -1;
    const size=game.window.getFramebufferSize();
    return state.fitLivingClusterResult(@floatFromInt(size.width),@floatFromInt(size.height));
}

export fn stella_watch_life() i32 {
    const state=webPlayState() orelse return 0;
    state.watchLife();
    return 1;
}

export fn stella_seed_colony(expected_point:u32) i32 {
    const state=webPlayState() orelse return -1;
    return state.seedSelectedColony(expected_point);
}

export fn stella_make_nursery(expected_point:u32) i32 {
    const state=webPlayState() orelse return -1;
    return state.makeSelectedNursery(expected_point);
}

export fn stella_make_pond(expected_point:u32) i32 {
    const state=webPlayState() orelse return -1;
    return state.makeSelectedPond(expected_point);
}

export fn stella_test_action(tool: i32) i32 {
    return if (webPlayState()) |state| @intFromBool(state.testAction(tool)) else 0;
}

export fn stella_test_pick(x: f32, y: f32) i32 {
    if (webPlayState()) |state| {
        state.mouseMoved(&game, x, y, 0, 0);
        return if (state.pointerOnPlanet) @intCast(state.selectedPoint) else -1;
    }
    return -1;
}

// Save data is durable only after the shell's FS.syncfs(false) callback.
export fn stella_save() i32 {
    if (!is_web or !web_initialized) return -1;
    web_loop.pump(1024);
    const state = webPlayState() orelse return -1;
    @import("save_game.zig").write(state, game.allocator) catch |err| {
        std.log.err("Save failed: {s}", .{@errorName(err)});
        return -2;
    };
    return 0;
}

export fn stella_load() i32 {
    if (!is_web or !web_initialized) return -3;
    const saves = @import("save_game.zig");
    var parsed = saves.read(game.allocator) catch |err| {
        if (err == error.FileNotFound) return -1;
        std.log.err("Load rejected: {s}", .{@errorName(err)});
        return -2;
    };
    defer parsed.deinit();
    // Version-1 saves retain their original grid and point IDs, including
    // older high-resolution browser worlds. Never resample a saved ecosystem.
    if (parsed.value.subdivisions != 6 and parsed.value.subdivisions != 7) return -2;
    web_loop.pump(1024);
    // The existing menu also owns a planet. Never deinit it while its normal
    // computation is still queued on this browser's cooperative event loop.
    switch (game.state) {
        .MainMenu => |*menu| if (menu.planet.normalComputeJob) |job| {
            if (!job.isCompleted()) return -3;
        },
        else => {},
    }
    if (webPlayState()) |state| {
        saves.replaceWorld(state, parsed.value) catch |err| {
            std.log.err("Load could not apply: {s}", .{@errorName(err)});
            return -3;
        };
    } else {
        // Use the existing state transition: direct union assignment of the
        // large candidate triggers a Zig 0.13 WASM backend trap. No live user
        // world exists in the menu. Failed load leaves an empty new planet.
        game.setState(PlayState);
        saves.replaceWorld(webPlayState().?, parsed.value) catch |err| {
            std.log.err("Load could not apply: {s}", .{@errorName(err)});
            return -3;
        };
    }
    PerformanceDetails.worldChanged();
    return 0;
}

fn web_frame() callconv(.C) void {
    const now = emscripten_get_now();
    // Clamp background-tab pauses rather than simulating minutes at once.
    const raw_dt:f32=@floatCast(@max((now-web_previous_time)/1000,0));
    const dt:f32=std.math.clamp(raw_dt,0.001,0.1);
    web_previous_time = now;
    glfw.pollEvents();
    web_loop.pump(16);
    inline for (std.meta.fields(GameState)) |field| {
        if (std.mem.eql(u8, @tagName(std.meta.activeTag(game.state)), field.name)) {
            if (comptime @hasDecl(field.type, "update")) {
                if(comptime @hasDecl(field.type,"setRawFrameDelta")) @field(game.state,field.name).setRawFrameDelta(raw_dt);
                @field(game.state, field.name).update(&game, dt);
            }
            break;
        }
    }
    // State transitions queued by update must finish before rendering.
    web_loop.pump(16);
    const measure=PerformanceDetails.metrics.enabled;
    const render_start=if(measure) emscripten_get_now() else 0;
    render(game.window);
    game.window.swapBuffers();
    if(measure)PerformanceDetails.metrics.frame(@as(f64,raw_dt)*1000,emscripten_get_now()-render_start);
    game.fps = 1.0 / dt;
}

/// C entry used when this Zig program is linked as an Emscripten library.
export fn stella_main() void {
    if (is_web) {
        main_web() catch |err| {
            std.log.err("Could not initialize Stella Dei: {s}", .{@errorName(err)});
            @panic("Stella Dei initialization failed");
        };
    }
}

fn main_web() !void {
    const allocator = std.heap.c_allocator;
    if (!glfw.init(.{})) return error.WindowInitializationFailed;
    const window = glfw.Window.create(1280, 720, "Stella Dei", null, null, .{
        .opengl_profile = .opengl_core_profile,
        .context_version_major = 3,
        .context_version_minor = 0,
    }) orelse return error.WindowCreationFailed;
    window.setCursorPosCallback(cursorPosCallback);
    window.setMouseButtonCallback(mouseButtonCallback);
    window.setScrollCallback(mouseScroll);
    window.setKeyCallback(keyCallback);
    glfw.makeContextCurrent(window);
    try gl.load({}, getProcAddress);
    renderer = try Renderer.init(allocator, window);
    web_loop.beginEvent();
    try web_loop.start(allocator);
    game = try Game.init(allocator, window, &renderer, &web_loop);
    game.setState(MainMenuState);
    web_initialized = true;
    web_previous_time = emscripten_get_now();
    // Return normally; all browser-owned state above has static lifetime.
    emscripten_set_main_loop(web_frame, 0, 0);
}

fn main_wrap() !void {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer _ = gpa.deinit();

    //     // If Tracy is enabled, pass-through all allocations to it
    // var tracyAlloc = @import("tracy_allocator.zig").TracyAllocator.init(gpa.allocator());
    // const allocator = if (tracy.enabled) tracyAlloc.allocator() else gpa.allocator();
    // _ = allocator;
    const allocator = gpa.allocator();
    // tracy.InitThread();

    if (glfw.init(.{}) == false) {
        fatalCrash(std.heap.page_allocator, "could not initialize glfw", .{});
    }
    defer glfw.terminate();

    var window = glfw.Window.create(1280, 720, "Stella Dei", null, null, .{
        .opengl_profile = .opengl_core_profile,
        .context_version_major = 4,
        .context_version_minor = 0,
    }) orelse blk: {
        glfw.getErrorCode() catch |err| {
            switch (err) {
                error.APIUnavailable => fatalCrash(allocator, "OpenGL is not available! Install drivers!", .{}),
                error.VersionUnavailable => {
                    std.log.warn("Switching to OpenGL 3.3 as support for OpenGL 4.0+ is missing", .{});
                    break :blk glfw.Window.create(1280, 720, "Stella Dei", null, null, .{
                        .opengl_profile = .opengl_core_profile,
                        .context_version_major = 3,
                        .context_version_minor = 3,
                    }) orelse {
                        fatalCrash(allocator, "OpenGL 3.3 (core profile) is not available! Upgrade your drivers!", .{});
                    };
                },
                else => fatalCrash(allocator, "Could not create the game window: {s}", .{@errorName(err)}),
            }
        };
        unreachable;
    };
    defer window.destroy();
    window.setCursorPosCallback(cursorPosCallback);
    window.setMouseButtonCallback(mouseButtonCallback);
    window.setScrollCallback(mouseScroll);
    window.setKeyCallback(keyCallback);

    glfw.makeContextCurrent(window);
    glfw.swapInterval(1);
    std.log.debug("Load OpenGL functions", .{});
    try gl.load({}, getProcAddress);

    std.log.debug("Initializing renderer..", .{});
    renderer = try Renderer.init(allocator, window);
    defer renderer.deinit();

    std.log.debug("Initializing event loop..", .{});
    var loop = EventLoop.init();

    loop.beginEvent(); // begin main() event to avoid the loop stopping too soon
    defer loop.endEvent();
    try loop.start(allocator);
    game = try Game.init(allocator, window, &renderer, &loop);

    // Start with opening sequence
    // To see the code, look in src/states/splash_screen.zig
    if (@import("builtin").mode == .Debug) {
        // Skip the opening sequence if we're in debug mode
        // To see the code, look in src/states/main_menu.zig
        nosuspend game.setState(MainMenuState);
    } else {
        nosuspend game.setState(SplashScreenState);
    }
    defer game.deinit();

    std.log.debug("Creating update loop job..", .{});
    var updateLoopJob = try Job(void).create(&loop);
    defer {
        // 'await' without making the function async
        while (!updateLoopJob.isCompleted()) {
            std.atomic.spinLoopHint();
        }
        updateLoopJob.deinit();
    }
    try updateLoopJob.call(updateLoop, .{ &loop, window });

    std.log.debug("Done!", .{});

    var fpsTimer = try std.time.Timer.start();
    while (!window.shouldClose()) {
        glfw.makeContextCurrent(window);
        render(window);

        window.swapBuffers();
        glfw.pollEvents();
        tracy.FrameMark();

        const frameTime = fpsTimer.lap();
        const fps = 1.0 / (@as(f32, @floatFromInt(frameTime)) / std.time.ns_per_s);
        game.fps = fps;
        // std.log.debug("{d} fps", .{fps});
    }
}

const expect = std.testing.expect;

test "main menu state" {
    var testGame = Game.init();
    try expect(std.meta.activeTag(testGame.state) == .MainMenu);

    testGame.setState(PlayState);
    try expect(std.meta.activeTag(testGame.state) == .Playing);
}

extern fn qa_capture(path:[*:0]const u8) void;
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
const AdvanceDay = @import("advance_day.zig");
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
    startWetlandsNext:bool=false,
    startCombinedNext:bool=false,
    startCalmNext:bool=false,
    startProtectionNext:bool=false,
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
        AdvanceDay.invalidate("world changed");
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
var advance_cursor_reset:bool=false;

fn mousePressed(window: glfw.Window, button: glfw.mouse_button.MouseButton) void {
    if(AdvanceDay.blocksInput())return;
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
    if(AdvanceDay.blocksInput())return;
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
    if(AdvanceDay.blocksInput())return;
    if(advance_cursor_reset){game.oldMouseX=@floatCast(xpos);game.oldMouseY=@floatCast(ypos);advance_cursor_reset=false;}
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
    if(AdvanceDay.blocksInput())return;
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
    if (!web_initialized or !game.state_init) return null;
    return switch (game.state) {
        .Playing => &game.state.Playing,
        else => null,
    };
}
fn webEditableState() ?*PlayState {if(AdvanceDay.blocksInput())return null;return webPlayState();}
var defense_json:[768]u8=undefined;
pub fn defenseSnapshot(state:?*PlayState,status:[]const u8)[*:0]const u8 {
 const v=state orelse return "{\"status\":\"unavailable\"}";
 var out=std.io.fixedBufferStream(&defense_json);
 const preview=@import("sandbox_defense.zig").previewPlantDefended(&v.planet,v.selectedPoint,if(v.defensePlantKind==1)0.5 else 0);
 std.json.stringify(.{.eligibility=@tagName(preview.status),.depth_m=preview.depth_m,.status=status,.world=PerformanceDetails.world_serial,.cell=v.selectedPoint,.mode=if(v.planet.worldMode==.sandbox) "sandbox" else "origin",.enabled=v.planet.sandboxDefense.enabled,.kind=v.defensePlantKind},.{},out.writer()) catch return "{}";
 const n=out.pos;defense_json[n]=0;return defense_json[0..n:0].ptr;
}
export fn stella_defense_status()[*:0]const u8 {return defenseSnapshot(webPlayState(),"ready");}
export fn stella_defense_action(world:u32,cell:u32,action:i32)[*:0]const u8 {
 const v=webEditableState() orelse return defenseSnapshot(null,"unavailable");
 if(world!=PerformanceDetails.world_serial or cell!=v.selectedPoint)return defenseSnapshot(v,"stale");
 if(v.planet.worldMode!=.sandbox)return defenseSnapshot(v,"wrong_mode");
 if(action==0){@import("plant_receipt.zig").invalidate();const receipt=@import("sandbox_defense.zig").enableDefenses(&v.planet);return defenseSnapshot(v,@tagName(receipt.status));}
 if(action==3){v.defensePlantKind=-1;v.selectedTool=.None;return defenseSnapshot(v,"cancelled");}
 if(action!=1 and action!=2)return defenseSnapshot(v,"invalid");
 if(!v.planet.sandboxDefense.enabled)return defenseSnapshot(v,"disabled");
 v.defensePlantKind=action-1;v.selectGameTool(.PlaceVegetation);v.showPointDetails=false;v.showPlanetControl=false;v.showEscapeMenu=false;
 return defenseSnapshot(v,"selected");
}
var advance_json:[768]u8=undefined;
pub fn advanceStatusForState(state:?*PlayState,ok:bool)[*:0]const u8 {
 const c=&AdvanceDay.current;var stream=std.io.fixedBufferStream(advance_json[0..advance_json.len-1]);
 std.json.stringify(.{.ok=ok,.available=if(state)|v|v.planet.worldMode==.origin else false,.token=c.token,.world=c.world,.phase=@tagName(c.phase),.busy=c.busy(),.running=c.phase==.running,.redraw_pending=c.phase==.redraw,.waiting_for_view=c.phase==.redraw and (!c.visible or !c.context_ok),.completed=c.completed,.total=@as(u32,60),.seconds=c.completed*1440,.reason=c.reason,.paused=if(state)|v|v.paused else false,.redraw_complete=!c.busy() and !c.recovery_required,.recovery_required=c.recovery_required,.recovery_save_allowed=if(state)|v|c.canRecoverySave(v,PerformanceDetails.world_serial) else false,.dismissed=c.dismissed,.input_blocked=c.blocks(),.visible=c.visible,.context_ok=c.context_ok},.{},stream.writer()) catch return "{}";
 const n=stream.pos;advance_json[n]=0;return @ptrCast(&advance_json);
}
pub fn advanceStartForState(state:*PlayState,world:u32,expected:u32)bool {
 if(!AdvanceDay.current.start(state,world,expected))return false;
 ManualTransport.reset();PatchWatch.current.stop("explicit day advance");PerformanceDetails.interrupted();PerformanceDetails.metrics.setEnabled(false);return true;
}
export fn stella_advance_start(expected:u32)[*:0]const u8 {const state=webPlayState();const ok=if(state)|v|advanceStartForState(v,PerformanceDetails.world_serial,expected) else false;return advanceStatusForState(state,ok);}
export fn stella_advance_status()[*:0]const u8 {return advanceStatusForState(webPlayState(),true);}
export fn stella_advance_cancel(token:u32)[*:0]const u8 {const ok=token!=0 and token==AdvanceDay.current.token;if(ok)AdvanceDay.current.cancel("cancelled by player");return advanceStatusForState(webPlayState(),ok);}
export fn stella_advance_dismiss(token:u32)[*:0]const u8 {const ok=AdvanceDay.current.dismiss(token);return advanceStatusForState(webPlayState(),ok);}
export fn stella_advance_environment(visible:i32,context_ok:i32)[*:0]const u8 {AdvanceDay.current.environment(visible==1,context_ok==1);return advanceStatusForState(webPlayState(),true);}
export fn stella_scene_resolution_set(value:i32)i32 {
    if(webEditableState()==null or value<0)return 0;
    const choice=@import("render_scale.zig");const before=choice.percent();
    if(!choice.set(@intCast(value)))return 0;
    if(before!=choice.percent())PerformanceDetails.interrupted();
    return 1;
}
export fn stella_scene_resolution_get()u32{return @import("render_scale.zig").percent();}

export fn stella_zoom(steps: f32) void {
    if (webEditableState()) |state| state.zoom(steps);
}
export fn stella_focus_land() i32 {
    return if (webEditableState()) |state| (if (state.focusLand()) @as(i32, 1) else 0) else -1;
}
export fn stella_reset_view() void {
    if (webEditableState()) |state| state.resetView();
}
export fn stella_camera_distance() f32 {
    return if (webPlayState()) |state| state.cameraDistance else -1;
}
export fn stella_target_distance() f32 {
    return if (webPlayState()) |state| state.targetCameraDistance else -1;
}

const HabitatPreview=@import("habitat_preview.zig");
export fn stella_habitat_prepare(world:u32,cell:i32,nursery:i32)[*:0]const u8{return if(webEditableState())|s|HabitatPreview.prepare(s,PerformanceDetails.world_serial,world,cell,nursery).ptr else "{\"ok\":false,\"reason\":\"World unavailable\"}";}
export fn stella_habitat_execute(token:u32)[*:0]const u8{return if(webEditableState())|s|HabitatPreview.execute(s,PerformanceDetails.world_serial,token).ptr else "{\"ok\":false,\"reason\":\"World unavailable\"}";}
export fn stella_habitat_cancel()void{HabitatPreview.cancel();}
export fn stella_habitat_status()[*:0]const u8{return if(webEditableState())|s|HabitatPreview.status(s,PerformanceDetails.world_serial).ptr else blk:{HabitatPreview.cancel();break :blk "{\"pending\":false,\"token\":0,\"available\":false,\"reason\":\"World unavailable\"}";};}
const ManualTransport=@import("manual_transport.zig");
export fn stella_transport_options()[*:0]const u8{return if(webPlayState())|s|ManualTransport.options(s,PerformanceDetails.world_serial).ptr else "{\"available\":false,\"reason\":\"Start an Origin world first\"}";}
export fn stella_transport_status()[*:0]const u8{return if(webPlayState())|s|ManualTransport.status(s,PerformanceDetails.world_serial).ptr else "{\"pending\":false,\"token\":0}";}
export fn stella_transport_prepare(world:u32,cell:i32,slot:i32,target:i32,id:[*:0]const u8)[*:0]const u8{return if(webEditableState())|s|ManualTransport.prepare(s,PerformanceDetails.world_serial,world,cell,slot,target,std.mem.span(id)).ptr else "{\"ok\":false,\"reason\":\"World unavailable\"}";}
export fn stella_transport_execute(token:u32)[*:0]const u8{return if(webEditableState())|s|ManualTransport.execute(s,PerformanceDetails.world_serial,token).ptr else "{\"ok\":false,\"reason\":\"World unavailable\"}";}
export fn stella_transport_cancel()void{ManualTransport.cancel();}
export fn stella_transport_inspect(world:u32,target:i32,id:[*:0]const u8)[*:0]const u8{return if(webEditableState())|s|ManualTransport.inspect(s,PerformanceDetails.world_serial,world,target,std.mem.span(id)).ptr else "{\"ok\":false,\"reason\":\"World unavailable\"}";}

var lifeSnapshotBuffer: [8192]u8 = undefined;
/// On-demand current-cell snapshot, not a fabricated historical lineage tree.
var plant_receipt_json:[1536]u8=undefined;
export fn stella_life_snapshot() [*:0]const u8 {
    const state = webPlayState() orelse return "{\"status\":\"no_world\"}";
    return lifeSnapshotForState(state);
}
pub fn lifeSnapshotForState(state:*PlayState) [*:0]const u8 {
    if (state.planet.worldMode != .origin) {
        var stream=std.io.fixedBufferStream(plant_receipt_json[0..plant_receipt_json.len-1]);
        std.json.stringify(.{.status="sandbox",.world_serial=PerformanceDetails.world_serial,.cell=state.selectedPoint,.time=state.gameTime,.plant_receipt=@import("plant_receipt.zig").view(&state.planet,PerformanceDetails.world_serial,state.selectedPoint,state.gameTime)},.{},stream.writer()) catch return "{}";
        plant_receipt_json[stream.pos]=0;return @ptrCast(&plant_receipt_json);
    }
    const point = state.selectedPoint;
    if (point >= state.planet.microbeCells.len) return "{\"status\":\"no_cell\"}";
    const cell = state.planet.microbeCells[point];
    const depth = state.planet.waterMass[point] * state.planet.getKmPerWaterMass();
    const surfaceLight = @max(0, state.planet.transformedPoints[point].norm().dot(state.simulationSolarVector())) * std.math.clamp(state.solarConstant / 1361, 0, 2);
    const biologicalLight = @import("simulation/microbes.zig").availableLight(surfaceLight, depth);
    const Microbes = @import("simulation/microbes.zig");
    const shares = Microbes.producerLightShares(cell, surfaceLight, depth);
    const Tissue = struct { form:[]const u8, support_mass:f32, frond_mass:f32, height_m:f32, available_light:f32, maintenance_potential:f32, living_traits:@import("producer_habitat.zig").LivingTraits };
    var tissues:[4]Tissue=undefined;
    for(cell.cohorts,0..) |co,slot| tissues[slot]=.{.form=Microbes.producerFormName(Microbes.producerForm(co)),.support_mass=co.support_mass,.frond_mass=Microbes.frondMass(co),.height_m=Microbes.producerHeightMeters(co),.available_light=shares[slot],.maintenance_potential=Microbes.supportMaintenancePerDay(co),.living_traits=@import("producer_habitat.zig").livingTraits(co,depth,state.planet.temperature[point])};
    const Identity=struct{id:[]const u8,parent:[]const u8,living:bool,generation:u32};
    var id_buffers:[4][20]u8=undefined;var parent_buffers:[4][20]u8=undefined;var identities:[4]Identity=undefined;
    for(cell.cohorts,0..)|c,i|identities[i]=.{.id=std.fmt.bufPrint(&id_buffers[i],"{d}",.{c.lineage}) catch "",.parent=std.fmt.bufPrint(&parent_buffers[i],"{d}",.{c.parent}) catch "",.living=@import("offspring_finder.zig").alive(c),.generation=c.generation};
    var movement_reasons: [4][]const u8 = undefined;
    for (&movement_reasons, 0..) |*reason, slot| {
        reason.* = @tagName(state.planet.microbeRelocationOpportunity(point, slot, state.gameTime).reason);
    }
    var stream = std.io.fixedBufferStream(lifeSnapshotBuffer[0 .. lifeSnapshotBuffer.len - 1]);
    std.json.stringify(.{
        .status = "origin", .cell = point, .day = state.gameTime / 86400, .world_serial = PerformanceDetails.world_serial, .paused = state.paused,
        .seed_reason = @tagName(state.planet.seedEligibility(point)),
        .producer_habitat = @import("producer_habitat.zig").inspect(cell,depth,state.planet.temperature[point]),
        .temperature_c = state.planet.temperature[point] - 273.15,
        .water_m = state.planet.waterMass[point] * state.planet.getKmPerWaterMass() * 1000,
        .nutrients = cell.nutrient, .detritus = cell.detritus, .simulation_light = biologicalLight,
        .cohorts = cell.cohorts, .identities = identities, .movement_reasons = movement_reasons, .tissues = tissues,
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
            return state.sampleOriginCommunity();
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
    const state=webEditableState() orelse return std.math.nan(f32);
    return state.adjustSelectedWater(expected_point, delta_m);
}

export fn stella_set_water_target(expected_point:u32,target_m:f32) f32 {
    const state=webEditableState() orelse return std.math.nan(f32);
    return state.setSelectedWaterTarget(expected_point,target_m);
}

const AutoSeed=@import("auto_seed.zig");
export fn stella_auto_seed_start(world:u32)[*:0]const u8{return if(webEditableState())|s|AutoSeed.start(s,PerformanceDetails.world_serial,world).ptr else "{\"ok\":false,\"phase\":\"failed\",\"reason\":\"World unavailable\"}";}
export fn stella_auto_seed_step(token:u32)[*:0]const u8{return if(webEditableState())|s|AutoSeed.step(s,PerformanceDetails.world_serial,token).ptr else "{\"ok\":false,\"phase\":\"failed\",\"reason\":\"World unavailable\"}";}
export fn stella_auto_seed_status()[*:0]const u8{return if(webPlayState())|s|AutoSeed.status(s,PerformanceDetails.world_serial).ptr else "{\"ok\":false,\"phase\":\"failed\",\"reason\":\"World unavailable\"}";}
export fn stella_auto_seed_apply(token:u32)[*:0]const u8{return if(webEditableState())|s|AutoSeed.apply(s,PerformanceDetails.world_serial,token).ptr else "{\"ok\":false,\"phase\":\"failed\",\"reason\":\"World unavailable\"}";}
export fn stella_auto_seed_cancel(token:u32)[*:0]const u8{return AutoSeed.cancel(token).ptr;}

var godTargetBuffer:[768]u8=undefined;
export fn stella_god_target() [*:0]const u8 {
    const state=webPlayState() orelse return "{\"status\":\"no_world\"}";
    const i=state.selectedPoint;if(i>=state.planet.temperature.len or i>=state.planet.waterMass.len)return "{\"status\":\"invalid\"}";
    var stream=std.io.fixedBufferStream(godTargetBuffer[0..godTargetBuffer.len-1]);
    const Actions=@import("god_actions.zig");const heat=state.planet.currentHeatCapacity(i);
    const wave=Actions.previewWave(&state.planet,i,i);const lightning=Actions.previewLightning(&state.planet,i,i,heat);const scorch=Actions.previewScorch(&state.planet,i,i,heat);const ignition=state.previewIgnition(i);
    std.json.stringify(.{.status="ready",.cell=i,.water_m=state.planet.waterMass[i]*state.planet.getKmPerWaterMass()*1000,.temperature_c=state.planet.temperature[i]-273.15,.eligibility=.{.wave=@tagName(wave.failure),.lightning=@tagName(lightning.failure),.scorch=@tagName(scorch.failure),.ignition=@tagName(ignition.failure)}},.{.emit_nonportable_numbers_as_strings=true},stream.writer()) catch return "{}";
    godTargetBuffer[stream.pos]=0;return @ptrCast(&godTargetBuffer);
}
var godActionBuffer:[4096]u8=undefined;
export fn stella_god_action(kind:u32,expected:u32) [*:0]const u8 {
    const state=webEditableState() orelse return "{\"failure\":\"no_world\"}";
    if(kind==3){
        const ignition=state.applyIgnition(expected);
        var stream=std.io.fixedBufferStream(godActionBuffer[0..godActionBuffer.len-1]);
        std.json.stringify(ignition,.{.emit_nonportable_numbers_as_strings=true},stream.writer()) catch return "{\"failure\":\"error\"}";
        godActionBuffer[stream.pos]=0;return @ptrCast(&godActionBuffer);
    }
    if(kind>3){state.godReceipt=null;state.godEffectSeconds=0;return "{\"failure\":\"invalid\"}";}
    const result=state.applyGodAction(if(kind==0).wave else if(kind==1).lightning else .scorch,expected);
    var stream=std.io.fixedBufferStream(godActionBuffer[0..godActionBuffer.len-1]);
    std.json.stringify(.{.kind=@tagName(result.kind),.failure=@tagName(result.failure),.count=result.count,.affected=result.affected[0..result.count],.moved_mass=result.moved_mass,.moved_depth_m=result.moved_mass*state.planet.getKmPerWaterMass()*1000,.heat_joules=result.heat_joules},.{.emit_nonportable_numbers_as_strings=true},stream.writer()) catch return "{\"failure\":\"error\"}";
    godActionBuffer[stream.pos]=0;return @ptrCast(&godActionBuffer);
}

/// Leave placement overlays without moving the view or changing time/pause.
var speed_json:[512]u8=undefined;
export fn stella_set_speed(seconds:f32)i32 {
    const state=webEditableState() orelse return -1;
    if(@import("web_shell.zig").enabled and !mobileGuard(state,PerformanceDetails.world_serial))return -2;
    if(!std.math.isFinite(seconds) or (seconds!=3600 and seconds!=21600 and seconds!=86400))return -1;
    HabitatPreview.cancel();state.timeScale=seconds;state.simulationClock.reset();return 1;
}
export fn stella_speed_snapshot()[*:0]const u8 {
    const state=webPlayState() orelse return "{\"status\":\"unavailable\"}";
    const text=std.fmt.bufPrintZ(&speed_json,"{{\"requested\":{d},\"achieved\":{d},\"paused\":{},\"step\":{d},\"steps_last_frame\":{d}}}",.{state.timeScale,state.simulationClock.achieved,state.paused,PlayState.simulation_step_seconds,state.simulationStepsLastFrame}) catch return "{}";
    return text.ptr;
}

const PerformanceDetails=@import("performance_details.zig");
const PatchWatch=@import("patch_watch.zig");
var patch_watch_json:[4096]u8=undefined;
export fn stella_patch_watch_start(expected:i32)i32 {
 const state=webEditableState() orelse return -1;
 return patchWatchStartForState(state,expected);
}
export fn stella_patch_watch_start_checked(expected:i32,world:u32,resume_explicit:i32)i32 {
 const state=webEditableState() orelse return -1;
 return patchWatchStartCheckedForState(state,expected,world,resume_explicit==1);
}
pub fn patchWatchStartCheckedForState(state:*PlayState,expected:i32,world:u32,resume_explicit:bool)i32 {
 if(world!=PerformanceDetails.world_serial or state.planet.worldMode!=.origin or expected<0 or state.selectedPoint!=@as(usize,@intCast(expected)) or state.selectedPoint>=state.planet.microbeCells.len or state.showEscapeMenu or state.showPlanetControl or (state.paused and !resume_explicit))return -2;
 // Prepare privately: refusal preserves the prior watch, pause and native Inspect.
 // This explicit Watch transition dismisses Inspect only after valid baseline capture.
 var next=PatchWatch.Watch{};
 if(!next.start(state.selectedPoint,world,state.gameTime,PatchWatch.nowMs()))return -3;
 if(!next.startPopulation(PatchWatch.Watch.population(state.planet.microbeCells[state.selectedPoint].cohorts)))return -3;
 next.owner=@intFromPtr(&state.planet);
 PatchWatch.current=next;
 state.showPointDetails=false;
 if(resume_explicit)state.paused=false;
 return 1;
}
pub fn patchWatchStartForState(state:*PlayState,expected:i32)i32 {
 return patchWatchStartCheckedForState(state,expected,PerformanceDetails.world_serial,false);
}
export fn stella_patch_watch_stop(complete:i32)void {
 if(complete==1){if(webPlayState())|s|PatchWatch.current.guard(s.selectedPoint,PerformanceDetails.world_serial,s.gameTime,PatchWatch.nowMs(),s.paused or s.showEscapeMenu or s.showPlanetControl or s.showPointDetails);}
 PatchWatch.current.stop("cancelled");
}
export fn stella_patch_watch_snapshot()[*:0]const u8 {
 if(webPlayState())|s|PatchWatch.current.guard(s.selectedPoint,PerformanceDetails.world_serial,s.gameTime,PatchWatch.nowMs(),s.paused or s.showEscapeMenu or s.showPlanetControl or s.showPointDetails) else PatchWatch.current.stop("world unavailable");
 var stream=std.io.fixedBufferStream(&patch_watch_json);
 std.json.stringify(.{.active=PatchWatch.current.active,.status=PatchWatch.current.status,.cell=PatchWatch.current.cell,.world=PatchWatch.current.world,.elapsed=PatchWatch.current.elapsed,.consumed=PatchWatch.current.consumed,.ticks=PatchWatch.current.ticks,.fixed=PatchWatch.current.fixed,.recycled=PatchWatch.current.recycled,.start_biomass=PatchWatch.current.start_biomass,.end_biomass=PatchWatch.current.end_biomass,.start_colonies=PatchWatch.current.start_colonies,.end_colonies=PatchWatch.current.end_colonies,.start_members=if(PatchWatch.current.start_members.valid) @as(?[]const @import("colony_snapshot.zig").Entry,PatchWatch.current.start_members.entries[0..PatchWatch.current.start_members.len]) else null,.end_members=if(PatchWatch.current.end_members.valid) @as(?[]const @import("colony_snapshot.zig").Entry,PatchWatch.current.end_members.entries[0..PatchWatch.current.end_members.len]) else null},.{},stream.writer()) catch return "{}";
 if(stream.pos>=patch_watch_json.len)return "{}";patch_watch_json[stream.pos]=0;return @ptrCast(&patch_watch_json);
}

var performance_json:[2048]u8=undefined;
export fn stella_performance_enable(enabled:i32)i32 {
    if(webEditableState()==null){PerformanceDetails.metrics.setEnabled(false);return -1;}
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
    const state=webEditableState() orelse return -1;
    const size=game.window.getFramebufferSize();
    return state.fitLivingClusterResult(@floatFromInt(size.width),@floatFromInt(size.height));
}

export fn stella_find_detritus(restart:u32) i32 {
    const state=webEditableState() orelse return -1;
    if(restart==2){state.detritusFinder=.{};return -4;}
    return state.findDetritus(restart==1);
}
export fn stella_find_feeding(restart:u32) i32 {
    const state=webEditableState() orelse return -1;
    if(restart==2){state.feedingFinder=.{};return -4;}
    return state.findRecordedFeeding(restart==1);
}

export fn stella_find_offspring(restart:u32,world:u32,source:u32,parent_text:[*:0]const u8)i32 {
    const state=webEditableState() orelse return -1;
    if(restart==2){state.offspringFinder=.{};return -4;}
    if(restart>2){state.offspringFinder=.{};return -4;}
    const parent=@import("offspring_finder.zig").parseId(std.mem.span(parent_text)) orelse {state.offspringFinder=.{};return -4;};
    return state.findOffspring(restart==1,world,source,parent);
}

export fn stella_find_sandbox_life(kind:u32) i32 {
    const state=webEditableState() orelse return -1;
    const size=game.window.getFramebufferSize();
    return state.findSandboxLife(kind,@floatFromInt(size.width),@floatFromInt(size.height));
}

export fn stella_visit_growth_form(world:u32,form:u32)i32 {
    const state=webPlayState() orelse return -1;
    if(AdvanceDay.blocksInput())return -2;
    const size=game.window.getFramebufferSize();
    return state.visitGrowthForm(world,form,@floatFromInt(size.width),@floatFromInt(size.height));
}

export fn stella_find_life() i32 {
    const state=webEditableState() orelse return -1;
    const size=game.window.getFramebufferSize();
    return state.findLivingClusterResult(@floatFromInt(size.width),@floatFromInt(size.height));
}

export fn stella_watch_life() i32 {
    const state=webEditableState() orelse return 0;
    state.watchLife();
    return 1;
}

/// Session display preference only; never serialized or an ecology action.
export fn stella_seed_targets(mode:i32)i32 {
    const state=webPlayState() orelse return -1;
    if(state.planet.worldMode!=.origin or mode < -1 or mode > 1)return -1;
    if(mode>=0){_ = webEditableState() orelse return -1;state.setSeedTargetsVisible(mode==1);}
    return @intFromBool(state.seedTargetsVisible);
}

/// Bounded read-only world census and session event history.
export fn stella_world_ecology(restart:u32)[*:0]const u8 {
    const state=webPlayState() orelse return "{\"status\":\"unavailable\"}";
    if(restart>1)return "{\"status\":\"unavailable\"}";
    return @import("world_ecology.zig").snapshot(&state.planet,PerformanceDetails.world_serial,state.gameTime,restart==1).ptr;
}

/// Hides visual arrival/loss receipts, not the underlying event tracker.
export fn stella_arrival_effects(mode:i32)i32 {
    const state=webPlayState() orelse return -1;
    if(state.planet.worldMode!=.origin or mode < -1 or mode > 1)return -1;
    if(mode>=0){_ = webEditableState() orelse return -1;state.setArrivalEffectsVisible(mode==1);}
    return @intFromBool(state.arrivalEffectsVisible);
}

export fn stella_seed_colony(expected_point:u32) i32 {
    const state=webEditableState() orelse return -1;
    return state.seedSelectedColony(expected_point);
}

export fn stella_make_nursery(expected_point:u32) i32 {
    const state=webEditableState() orelse return -1;
    return state.makeSelectedNursery(expected_point);
}

export fn stella_make_pond(expected_point:u32) i32 {
    const state=webEditableState() orelse return -1;
    return state.makeSelectedPond(expected_point);
}

export fn stella_test_action(tool: i32) i32 {
    return if (webEditableState()) |state| @intFromBool(state.testAction(tool)) else 0;
}

export fn stella_test_pick(x: f32, y: f32) i32 {
    if (webEditableState()) |state| {
        state.mouseMoved(&game, x, y, 0, 0);
        return if (state.pointerOnPlanet) @intCast(state.selectedPoint) else -1;
    }
    return -1;
}

// Save data is durable only after the shell's FS.syncfs(false) callback.
export fn stella_save() i32 {
    if(AdvanceDay.current.recovery_required){
      const state=webPlayState() orelse return -4;
      if(!AdvanceDay.current.canRecoverySave(state,PerformanceDetails.world_serial))return -4;
      @import("save_game.zig").write(state,game.allocator) catch |err| return if (err == error.SaveTooLarge) -5 else -2;
      return 0; // Shell must still complete FS.syncfs(false) before claiming durability.
    }
    if(AdvanceDay.blocksInput())return -4;
    if (!is_web or !web_initialized) return -1;
    web_loop.pump(1024);
    const state = webPlayState() orelse return -1;
    @import("save_game.zig").write(state, game.allocator) catch |err| {
        std.log.err("Save failed: {s}", .{@errorName(err)});
        return if (err == error.SaveTooLarge) -5 else -2;
    };
    return 0;
}

export fn stella_load() i32 {
    if(AdvanceDay.blocksInput())return -4;
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

/// Shared native/browser callback boundary for the explicit advance job.
pub fn advanceFrame(raw_dt:f64)bool {
    if(AdvanceDay.current.recovery_required)return true;
    if(AdvanceDay.current.input_latched and AdvanceDay.current.dismissed and !AdvanceDay.busy()){
      if(game.window.getMouseButton(.left)!=.press and game.window.getMouseButton(.right)!=.press and game.window.getMouseButton(.middle)!=.press and game.window.getKey(.w)!=.press and game.window.getKey(.s)!=.press){AdvanceDay.current.releaseInput(true);game.imgui_state.clearRetainingCapacity();const cursor=game.window.getCursorPos();game.oldMouseX=@floatCast(cursor.xpos);game.oldMouseY=@floatCast(cursor.ypos);advance_cursor_reset=true;if(webPlayState())|state|{state.dragStart=za.Vec2.new(game.oldMouseX,game.oldMouseY);state.pointerOnPlanet=false;state.rawFrameDelta=null;state.simulationClock.reset();}}
    }
    if(AdvanceDay.busy()){
      if(webPlayState())|state|{state.syncPlantReceipt();_=AdvanceDay.current.tick(state,game.loop,PerformanceDetails.world_serial,raw_dt);}else AdvanceDay.invalidate("world unavailable");
      game.loop.pump(16);
      if(AdvanceDay.current.phase==.redraw and AdvanceDay.current.visible and AdvanceDay.current.context_ok){render(game.window);game.window.swapBuffers();AdvanceDay.current.didRedraw();game.imgui_state.clearRetainingCapacity();}
      return true;
    }
    return false;
}

fn web_frame() callconv(.C) void {
    const now = emscripten_get_now();
    // Clamp background-tab pauses rather than simulating minutes at once.
    const raw_dt:f32=@floatCast(@max((now-web_previous_time)/1000,0));
    const dt:f32=std.math.clamp(raw_dt,0.001,0.1);
    web_previous_time = now;
    glfw.pollEvents();
    web_loop.pump(16);
    if(advanceFrame(raw_dt))return;
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
        game.startOriginNext=true;nosuspend game.setState(PlayState);
    } else {
        game.startOriginNext=true;nosuspend game.setState(PlayState);
    }
    defer game.deinit();

    const saves=@import("save_game.zig");var arena=std.heap.ArenaAllocator.init(allocator);defer arena.deinit();const a=arena.allocator();web_initialized=true;const state=&game.state.Playing;
    const bytes=try std.fs.cwd().readFileAlloc(a,"/workspace/scratch/f67c3ac60ca3/site-tmp/unified-land-starter/preseed.json",128*1024*1024);const parsed=try saves.schema.parse(a,bytes);try saves.apply(state,parsed.value);for(0..16)|_|game.loop.pump(4096);
    state.showEscapeMenu=false;state.showPlanetControl=false;state.showPointDetails=false;state.paused=true;const w=PerformanceDetails.world_serial;
    var chosen:?u32=null;for(state.planet.microbeCells,0..)|_,i|{state.selectedPoint=i;const r=rootedFounderVariantForState(state,w,@intCast(i),false,true);if(r.status==.eligible){chosen=@intCast(i);break;}}
    const cell=chosen orelse return error.NoEligibleFixture;const before_camera=state.targetCameraPos;const planted=rootedFounderVariantForState(state,w,cell,true,true);std.debug.assert(planted.status==.planted and std.meta.eql(before_camera,state.targetCameraPos));
    var id_buf:[20]u8=undefined;const id=try std.fmt.bufPrint(&id_buf,"{d}",.{planted.lineage});const before=try saves.capture(a,state);const before_json=try std.json.stringifyAlloc(a,before,.{});
    std.debug.assert(viewPlantedForState(state,w+%1,cell,id,390,700)==0);std.debug.assert(viewPlantedForState(state,w,cell,"0",390,700)==0);std.debug.assert(viewPlantedForState(state,w,cell,id,100,700)==-3);std.debug.assert(std.mem.eql(u8,before_json,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
    _=stella_web_shell_set(1,28,0);render(window);gl.finish();window.swapBuffers();qa_capture("/workspace/scratch/f67c3ac60ca3/site-tmp/planted-discovery-native/before.ppm");
    std.debug.assert(viewPlantedForState(state,w,cell,id,390,700)==1);std.debug.assert(state.colonyPeek.focused==planted.lineage and state.selectedPoint==cell);
    var after=try saves.capture(a,state);after.camera=before.camera;after.camera_target=before.camera_target;after.camera_distance=before.camera_distance;after.target_distance=before.target_distance;
    std.debug.assert(std.mem.eql(u8,before_json,try std.json.stringifyAlloc(a,after,.{})));
    render(window);gl.finish();window.swapBuffers();qa_capture("/workspace/scratch/f67c3ac60ca3/site-tmp/planted-discovery-native/after.ppm");
    std.debug.assert(viewPlantedForState(state,w,cell,id,700,390)==1);std.debug.assert(viewPlantedForState(state,w,cell,id,390,700)==1);
    state.showEscapeMenu=true;std.debug.assert(viewPlantedForState(state,w,cell,id,390,700)==-2);state.showEscapeMenu=false;
    const geometry=state.planet.transformedPoints[cell];state.planet.transformedPoints[cell]=@TypeOf(geometry).new(0,0,state.planet.radius);std.debug.assert(viewPlantedForState(state,w,cell,id,390,700)==-3);state.planet.transformedPoints[cell]=geometry;
    _=stella_web_shell_set(1,240,240);std.debug.assert(viewPlantedForState(state,w,cell,id,390,390)==-3);_=stella_web_shell_set(1,28,0);
    const before_mixed=state.planet.microbeCells[cell];var founder_slot:usize=0;for(before_mixed.cohorts,0..)|co,i|{if(co.lineage==planted.lineage)founder_slot=i;}
    const other=(founder_slot+1)%4;state.planet.microbeCells[cell].cohorts[other]=before_mixed.cohorts[founder_slot];state.planet.microbeCells[cell].cohorts[other].lineage=999;state.planet.microbeCells[cell].cohorts[other].biomass*=2;
    std.debug.assert(viewPlantedForState(state,w,cell,id,390,700)==1 and state.colonyPeek.focused==planted.lineage);state.planet.microbeCells[cell]=before_mixed;
    const living=state.planet.microbeCells[cell];for(&state.planet.microbeCells[cell].cohorts)|*co|if(co.lineage==planted.lineage){co.biomass=0;};std.debug.assert(viewPlantedForState(state,w,cell,id,390,700)==0);state.planet.microbeCells[cell]=living;
    try saves.apply(state,parsed.value);for(0..16)|_|game.loop.pump(4096);std.debug.assert(viewPlantedForState(state,w,cell,id,390,700)==0);
    std.debug.print("PLANTED_VIEW_ACTUAL_PAID_ID_SAVE_PURITY_REPEATED_DEAD_LOAD_PASS cell={} id={}\n",.{cell,planted.lineage});std.process.exit(0);
}

const expect = std.testing.expect;

test "main menu state" {
    var testGame = Game.init();
    try expect(std.meta.activeTag(testGame.state) == .MainMenu);

    testGame.setState(PlayState);
    try expect(std.meta.activeTag(testGame.state) == .Playing);
}

// Preview-only explicit fresh factory. Never converts the current saved world.
pub fn wetlandsNewForGame(g:*Game,expected:u32)i32 {
    if(!g.state_init)return -1;
    if(expected!=PerformanceDetails.world_serial)return -2;
    if(AdvanceDay.blocksInput())return -3;
    switch(g.state){
      .Playing=>|*v|{if(v.planet.normalComputeJob)|job|if(!job.isCompleted())return -3;},
      .MainMenu=>|*v|{if(v.planet.normalComputeJob)|job|if(!job.isCompleted())return -3;},
      else=>return -1,
    }
    g.startProtectionNext=false;g.startCalmNext=false;g.startCombinedNext=false;g.startWetlandsNext=true;g.startOriginNext=false;g.setState(PlayState);return 1;
}
export fn stella_wetlands_new(expected:u32)i32 {
    if(!web_initialized)return -1;
    web_loop.pump(1024);return wetlandsNewForGame(&game,expected);
}
export fn stella_wetlands_snapshot()[*:0]const u8 {return @import("wetlands_view.zig").snapshot(webPlayState(),PerformanceDetails.world_serial);}

const RootedFounder=@import("rooted_founder.zig");
var rooted_plan:?struct{world:u32,point:u32,token:u32,hardy:bool=false,time:f64,solar:f32,tilt:f32,snapshot:RootedFounder.Snapshot}=null;
var rooted_nonce:u32=0;
var rooted_receipt_buffer:[2048]u8=undefined;
fn rootedReceiptJson(receipt:@import("rooted_founder.zig").Receipt,world:u32,point:u32,token:u32)[*:0]const u8{
 var stream=std.io.fixedBufferStream(rooted_receipt_buffer[0..rooted_receipt_buffer.len-1]);var id:[20]u8=undefined;
 const founder_id=if(receipt.lineage!=0) std.fmt.bufPrint(&id,"{d}",.{receipt.lineage}) catch "" else "";
 std.json.stringify(.{.world_serial=world,.cell=point,.token=token,.status=receipt.status,.founder_id=founder_id,.carbon_kg_m2=receipt.carbon_kg_m2,.nitrogen_kg_m2=receipt.nitrogen_kg_m2,.carbon_source_kg=receipt.carbon_source_kg,.carbon_rounding_kg=receipt.carbon_rounding_kg,.support_kg_c_m2=receipt.support_kg_c_m2,.root_kg_c_m2=receipt.root_kg_c_m2,.root_fraction=receipt.root_fraction,.organization=receipt.organization,.soil_kg_m2=receipt.soil_kg_m2,.depth_m=receipt.depth_m,.water_support=receipt.water_support,.conditions=receipt.conditions,.structure=receipt.structure},.{},stream.writer()) catch return "{}";
 rooted_receipt_buffer[stream.pos]=0;return @ptrCast(&rooted_receipt_buffer);
}
const PlantedView=@import("planted_view.zig");
var planted_view:PlantedView.Receipt=.{};
pub fn viewPlantedForState(state:*PlayState,world:u32,point:u32,id:[]const u8,width:f32,height:f32)i32 {
 return planted_view.view(state,PerformanceDetails.world_serial,world,point,id,width,height);
}
export fn stella_view_planted(world:u32,point:u32,id:[*:0]const u8)i32 {
 const state=webEditableState() orelse return -2;
 const size=game.window.getFramebufferSize();
 return viewPlantedForState(state,world,point,std.mem.span(id),@floatFromInt(size.width),@floatFromInt(size.height));
}
pub fn rootedFounderForState(state:*PlayState,world:u32,point:u32,apply:bool)@import("rooted_founder.zig").Receipt{return rootedFounderVariantForState(state,world,point,apply,false);}
pub fn rootedFounderVariantForState(state:*PlayState,world:u32,point:u32,apply:bool,hardy:bool)@import("rooted_founder.zig").Receipt{
 const R=@import("rooted_founder.zig");
 if(world!=PerformanceDetails.world_serial or point!=state.selectedPoint)return .{.status=.stale};
 if(AdvanceDay.blocksInput() or state.showEscapeMenu or state.showPlanetControl or state.showPointDetails)return .{.status=.busy};
 if(state.planet.normalComputeJob)|job|if(!job.isCompleted())return .{.status=.busy};
 var receipt=if(hardy) (if(apply) R.applyHardy(&state.planet,point) else R.previewHardy(&state.planet,point)) else (if(apply) R.apply(&state.planet,point) else R.preview(&state.planet,point));
 if((receipt.status==.eligible or receipt.status==.planted) and point<state.planet.transformedPoints.len){
  const depth=state.planet.waterMass[point]*state.planet.getKmPerWaterMass();
  const solar_dot=state.planet.transformedPoints[point].norm().dot(state.simulationSolarVector());
  if(std.math.isFinite(solar_dot) and std.math.isFinite(state.solarConstant) and std.math.isFinite(depth)){
   const surface=@max(0,solar_dot)*std.math.clamp(state.solarConstant/1361,0,2);
   receipt.conditions=R.currentConditions(receipt,state.planet.temperature[point],@import("simulation/microbes.zig").availableLight(surface,depth));
   receipt.water_support=R.waterSupport(&state.planet,point,receipt,surface);
  }
 }

 if(receipt.status==.planted){
  planted_view.record(state,PerformanceDetails.world_serial,point,receipt.lineage);
  @import("plant_receipt.zig").invalidate();@import("patch_watch.zig").current.stop("Rooted founder planted");
  state.colonyPeek.set(point,state.planet.microbeCells[point],state.gameTime);state.colonyPeek.focused=receipt.lineage;
  for(state.planet.microbeCells[point].cohorts)|c|{if(c.lineage==receipt.lineage){state.colonyPeek.focused_form=@import("simulation/microbes.zig").producerForm(c);break;}}
  state.mobileFeedback="Paid rooted founder planted; chosen traits, not proof of water uptake";state.mobileFeedbackSeconds=6;
 }
 return receipt;
}

pub fn rootedPreviewForState(state:*PlayState,world:u32,point:u32)[*:0]const u8{return rootedPreviewVariantForState(state,world,point,false);}
pub fn rootedPreviewVariantForState(state:*PlayState,world:u32,point:u32,hardy:bool)[*:0]const u8{
 rooted_plan=null;const receipt=rootedFounderVariantForState(state,world,point,false,hardy);
 if(receipt.status!=.eligible)return rootedReceiptJson(receipt,PerformanceDetails.world_serial,point,0);
 if(rooted_nonce==std.math.maxInt(u32))return rootedReceiptJson(.{.status=.unrepresentable},PerformanceDetails.world_serial,point,0);
 const snap=RootedFounder.snapshot(&state.planet,point) orelse return rootedReceiptJson(.{.status=.invalid},PerformanceDetails.world_serial,point,0);
 rooted_nonce+=1;rooted_plan=.{.world=world,.point=point,.token=rooted_nonce,.hardy=hardy,.time=state.gameTime,.solar=state.solarConstant,.tilt=state.axialTilt,.snapshot=snap};return rootedReceiptJson(receipt,world,point,rooted_nonce);
}
pub fn rootedApplyForState(state:*PlayState,world:u32,point:u32,token:u32)[*:0]const u8{
 const plan=rooted_plan orelse return rootedReceiptJson(.{.status=.stale},PerformanceDetails.world_serial,point,token);
 if(token!=plan.token or world!=plan.world or point!=plan.point)return rootedReceiptJson(.{.status=.stale},PerformanceDetails.world_serial,point,token);
 rooted_plan=null;
 const snap=RootedFounder.snapshot(&state.planet,point) orelse return rootedReceiptJson(.{.status=.stale},PerformanceDetails.world_serial,point,token);
 if(state.gameTime!=plan.time or state.solarConstant!=plan.solar or state.axialTilt!=plan.tilt or !std.meta.eql(snap,plan.snapshot))return rootedReceiptJson(.{.status=.stale},PerformanceDetails.world_serial,point,token);
 return rootedReceiptJson(rootedFounderVariantForState(state,world,point,true,plan.hardy),PerformanceDetails.world_serial,point,token);
}
export fn stella_rooted_founder_preview(world:u32,point:u32)[*:0]const u8{
 const state=webPlayState() orelse return rootedReceiptJson(.{.status=.disabled},PerformanceDetails.world_serial,point,0);
 return rootedPreviewForState(state,world,point);
}
export fn stella_seed_rooted(world:u32,point:u32,token:u32)[*:0]const u8{
 const state=webPlayState() orelse return rootedReceiptJson(.{.status=.disabled},PerformanceDetails.world_serial,point,token);
 return rootedApplyForState(state,world,point,token);
}
export fn stella_rooted_founder_cancel(token:u32)i32{
 if(rooted_plan)|plan|{if(plan.token==token){rooted_plan=null;return 1;}}return 0;
}

/// Additive preview; existing apply consumes the immutable chosen variant.
export fn stella_hardy_rooted_founder_preview(world:u32,point:u32)[*:0]const u8{
 const state=webPlayState() orelse return rootedReceiptJson(.{.status=.disabled},PerformanceDetails.world_serial,point,0);
 return rootedPreviewVariantForState(state,world,point,true);
}

pub fn combinedNewForGame(g:*Game,expected:u32)i32{return combinedVariantNewForGame(g,expected,false);}
pub fn combinedVariantNewForGame(g:*Game,expected:u32,calmer:bool)i32{return combinedOptionsNewForGame(g,expected,calmer,false);}
pub fn combinedOptionsNewForGame(g:*Game,expected:u32,calmer:bool,protection:bool)i32 {
    if(protection and !calmer)return -1;
    if(!g.state_init)return -1;
    if(expected!=PerformanceDetails.world_serial)return -2;
    if(AdvanceDay.blocksInput())return -3;
    switch(g.state){
      .Playing=>|*v|{if(v.planet.normalComputeJob)|job|if(!job.isCompleted())return -3;},
      .MainMenu=>|*v|{if(v.planet.normalComputeJob)|job|if(!job.isCompleted())return -3;},
      else=>return -1,
    }
    g.startProtectionNext=protection;g.startCalmNext=calmer;g.startCombinedNext=true;g.startWetlandsNext=true;g.startOriginNext=false;g.setState(PlayState);return 1;
}
export fn stella_wetlands_combined_new(expected:u32)i32 {
    if(!web_initialized)return -1;
    web_loop.pump(1024);return combinedNewForGame(&game,expected);
}

export fn stella_combined_snapshot()[*:0]const u8{return @import("combined_view.zig").snapshot(webPlayState(),PerformanceDetails.world_serial);}
pub fn pioneerForState(state:*PlayState,world:u32,point:u32)i32 {
    if(world!=PerformanceDetails.world_serial or point!=state.selectedPoint)return -2;
    if(AdvanceDay.blocksInput() or state.showEscapeMenu or state.showPlanetControl or state.showPointDetails)return -3;
    if(state.planet.worldMode!=.origin or !state.planet.windDispersal.enabled or !state.planet.windDispersal.valid())return -1;
    if(point>=state.planet.microbeCells.len)return -2;
    const paid=state.planet.seedPioneer(point);
    if(paid){
        @import("plant_receipt.zig").invalidate();
        @import("patch_watch.zig").current.stop("Pioneer seeded");
        state.mobileFeedback="Paid Pioneer seeded: aerial allocation 0.5; arrival is not guaranteed";
    }else state.mobileFeedback="No Pioneer planted: check habitat, free cohort slot and available carbon/nutrients";
    state.mobileFeedbackSeconds=6;
    return @intFromBool(paid);
}
export fn stella_seed_pioneer(world:u32,point:u32)i32 {
    const state=webPlayState() orelse return -1;
    return pioneerForState(state,world,point);
}
// The asynchronous backup is in JS; token/schema are checked after the pump.
export fn stella_save_expected(world:u32,writer:u32)i32 {
    if(!web_initialized)return -1;
    if(!AdvanceDay.current.recovery_required)web_loop.pump(1024);
    const state=webPlayState() orelse return -1;
    if(world!=PerformanceDetails.world_serial or writer!=@import("combined_view.zig").writerVersion(state))return -6;
    if(AdvanceDay.current.recovery_required){
      if(!AdvanceDay.current.canRecoverySave(state,PerformanceDetails.world_serial))return -4;
    }else if(AdvanceDay.blocksInput())return -4;
    @import("save_game.zig").write(state,game.allocator) catch |err| return if(err==error.SaveTooLarge) -5 else -2;
    return 0;
}


export fn stella_auto_seed_pioneer_start(world:u32)[*:0]const u8{return if(webEditableState())|state|AutoSeed.startPioneer(state,PerformanceDetails.world_serial,world).ptr else "{\"ok\":false,\"phase\":\"failed\",\"reason\":\"World unavailable\"}";}

fn recoveryState()?*PlayState{
 if(AdvanceDay.blocksInput())return null;
 const state=webPlayState() orelse return null;
 if(state.planet.normalComputeJob)|job|if(!job.isCompleted())return null;
 return state;
}
export fn stella_recovery_prepare(world:u32,writer:u32)[*:0]const u8{
 const state=recoveryState() orelse return "{\"status\":\"unavailable\",\"token\":0}";
 return @import("combined_recovery.zig").prepare(state,PerformanceDetails.world_serial,world,writer);
}
export fn stella_recovery_apply(token:u32,kind:u32,hash:[*:0]const u8)i32{
 if(!web_initialized)return -1;
 if(AdvanceDay.blocksInput())return -1;web_loop.pump(1024);
 const state=recoveryState() orelse return -1;
 const result=@import("combined_recovery.zig").apply(state,PerformanceDetails.world_serial,token,kind,std.mem.span(hash));
 if(result==0)PerformanceDetails.worldChanged();return result;
}
export fn stella_recovery_cancel(token:u32)i32{return @import("combined_recovery.zig").cancel(token);}

export fn stella_combined_calm_new(expected:u32)i32{
 if(!web_initialized)return -1;
 web_loop.pump(1024);return combinedVariantNewForGame(&game,expected,true);
}

export fn stella_combined_protective_new(expected:u32)i32{
 if(!web_initialized)return -1;
 web_loop.pump(1024);return combinedOptionsNewForGame(&game,expected,true,true);
}
export fn stella_protective_snapshot()[*:0]const u8{return @import("protective_view.zig").snapshot(webPlayState(),PerformanceDetails.world_serial);}

// Explicit browser presentation bridge. No save/model fields.
export fn stella_web_shell_set(on:i32,top:f32,bottom:f32)i32{
 const was=@import("web_shell.zig").enabled;
 if(!@import("web_shell.zig").set(on,top,bottom))return -1;
 if(webPlayState())|v|{if(on==1 and !was){v.selectGameTool(.None);v.colonyTargets.count=0;v.seedTargets.count=0;}}
 return 1;
}
var mobile_json:[1024]u8=undefined;
pub fn mobileSnapshot(state:?*PlayState)[*:0]const u8{
 const v=state orelse return "{\"available\":false}";
 var stream=std.io.fixedBufferStream(mobile_json[0..mobile_json.len-1]);
 std.json.stringify(.{.available=true,.world_serial=PerformanceDetails.world_serial,.paused=v.paused,.blocked=v.showEscapeMenu or v.showPlanetControl or v.showPointDetails or AdvanceDay.blocksInput(),.tool=@intFromEnum(v.selectedTool),.selected=v.selectedPoint,.day=v.gameTime/86400,.speed=v.timeScale,.feedback=v.mobileFeedback},.{.emit_nonportable_numbers_as_strings=true},stream.writer()) catch return "{}";
 mobile_json[stream.pos]=0;return @ptrCast(&mobile_json);
}
export fn stella_mobile_snapshot()[*:0]const u8{return mobileSnapshot(webPlayState());}
pub fn mobileGuard(v:*PlayState,world:u32)bool{
 if(world!=PerformanceDetails.world_serial or AdvanceDay.blocksInput() or v.showEscapeMenu or v.showPlanetControl or v.showPointDetails)return false;
 if(v.planet.normalComputeJob)|job|if(!job.isCompleted())return false;
 return true;
}
pub fn mobilePause(v:*PlayState,world:u32,paused:i32)i32{
 if(paused!=0 and paused!=1)return -1;if(!mobileGuard(v,world))return -2;
 HabitatPreview.cancel();v.paused=paused==1;v.simulationClock.reset();return 1;
}
pub fn mobileTool(v:*PlayState,world:u32,tool:i32)i32{
 if(tool<0 or tool>6)return -1;
 if(!mobileGuard(v,world))return -2;
 HabitatPreview.cancel();v.selectGameTool(@enumFromInt(tool));return 1;
}
export fn stella_mobile_pause(world:u32,paused:i32)i32{return if(webEditableState())|v|mobilePause(v,world,paused) else -1;}
export fn stella_mobile_tool(world:u32,tool:i32)i32{return if(webEditableState())|v|mobileTool(v,world,tool) else -1;}
export fn stella_mobile_climate(world:u32)i32{
 const v=webEditableState() orelse return -1;if(!mobileGuard(v,world))return -2;
 HabitatPreview.cancel();v.selectGameTool(.None);v.showPlanetControl=true;return 1;
}

export fn stella_mobile_menu(world:u32)i32{
 const v=webEditableState() orelse return -1;if(!mobileGuard(v,world))return -2;
 HabitatPreview.cancel();v.selectGameTool(.None);v.leavePlanetArmed=false;v.showEscapeMenu=true;return 1;
}

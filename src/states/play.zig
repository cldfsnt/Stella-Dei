const SeedTargets = @import("../seed_targets.zig");
const habitat_focus = @import("../habitat_focus.zig");
const Microbes = @import("../simulation/microbes.zig");
const habitat_feedback = @import("../habitat_feedback.zig");
const edit_rates = @import("../edit_rates.zig");
const biology_visuals = @import("../biology_visuals.zig");
const guidance = @import("../mobile_guidance.zig");
const camera_math = @import("../camera_math.zig");
const std = @import("std");
const gl = @import("gl");
const za = @import("zalgebra");
const glfw = @import("glfw");
const nvg = @import("nanovg");
const ui = @import("../ui.zig");
const utils = @import("../utils.zig");

const Game = @import("../main.zig").Game;
const Renderer = @import("../renderer.zig").Renderer;
const Texture = @import("../renderer.zig").Texture;
const Framebuffer = @import("../renderer.zig").Framebuffer;
const MouseButton = glfw.mouse_button.MouseButton;
const SoundTrack = @import("../audio.zig").SoundTrack;
const MainMenuState = @import("main_menu.zig").MainMenuState;

const Lifeform = @import("../simulation/life.zig").Lifeform;
const Planet = @import("../simulation/planet.zig").Planet;

const Vec2 = za.Vec2;
const Vec3 = za.Vec3;
const Vec4 = za.Vec4;
const Mat4 = za.Mat4;
const CubeMesh = @import("../utils.zig").CubeMesh;

pub const QuadMesh = struct {
    // zig fmt: off
    const vertices = [6 * 4]f32{
        // position + texture coords
        -1.0,  1.0, 0.0, 1.0,
        -1.0, -1.0, 0.0, 0.0,
         1.0, -1.0, 1.0, 0.0,
        -1.0,  1.0, 0.0, 1.0,
         1.0, -1.0, 1.0, 0.0,
         1.0,  1.0, 1.0, 1.0,
    };
    // zig fmt: on

    var quad_vao: ?gl.GLuint = null;

    pub fn getVAO() gl.GLuint {
        if (quad_vao == null) {
            var vao: gl.GLuint = undefined;
            gl.genVertexArrays(1, &vao);
            var vbo: gl.GLuint = undefined;
            gl.genBuffers(1, &vbo);

            gl.bindVertexArray(vao);
            gl.bindBuffer(gl.ARRAY_BUFFER, vbo);
            gl.bufferData(gl.ARRAY_BUFFER, @as(isize, @intCast(vertices.len * @sizeOf(f32))), &vertices, gl.STATIC_DRAW);
            gl.vertexAttribPointer(0, 2, gl.FLOAT, gl.FALSE, 4 * @sizeOf(f32), @as(?*anyopaque, @ptrFromInt(0 * @sizeOf(f32)))); // position
            gl.vertexAttribPointer(1, 2, gl.FLOAT, gl.FALSE, 4 * @sizeOf(f32), @as(?*anyopaque, @ptrFromInt(2 * @sizeOf(f32)))); // position
            gl.enableVertexAttribArray(0);
            gl.enableVertexAttribArray(1);
            quad_vao = vao;
        }
        return quad_vao.?;
    }
};

pub const SunMesh = struct {
    const IcosphereMesh = @import("../utils.zig").IcosphereMesh;

    var sun_mesh: ?IcosphereMesh = null;

    pub fn getMesh(allocator: std.mem.Allocator) IcosphereMesh {
        if (sun_mesh == null) {
            const mesh = IcosphereMesh.generate(allocator, 3, false) catch unreachable;
            gl.bindVertexArray(mesh.vao[0]);
            gl.bindBuffer(gl.ARRAY_BUFFER, mesh.vbo);
            gl.vertexAttribPointer(0, 3, gl.FLOAT, gl.FALSE, 3 * @sizeOf(f32), @as(?*anyopaque, @ptrFromInt(0 * @sizeOf(f32)))); // position
            gl.enableVertexAttribArray(0);
            gl.bufferData(gl.ARRAY_BUFFER, @as(isize, @intCast(mesh.vertices.len * @sizeOf(f32))), mesh.vertices.ptr, gl.STREAM_DRAW);
            sun_mesh = mesh;
        }
        return sun_mesh.?;
    }

    pub fn deinit(allocator: std.mem.Allocator) void {
        if (sun_mesh) |mesh| {
            mesh.deinit(allocator);
            sun_mesh = null;
        }
    }
};

const GameTool = enum {
    None,
    /// When enabled, emits water at selected point on click
    EmitWater,
    /// When enabled, set vegetation level to 1 at selected point on click
    DrainWater,
    /// When enabled, drains all water near selected point on click
    PlaceVegetation,
    /// When enabled, place lifeform on click
    PlaceLife,
    RaiseTerrain,
    LowerTerrain,
};

pub const PlayState = struct {
    /// The previous mouse position that was recorded during dragging (to move the camera).
    dragStart: Vec2,
    planet: Planet,
    /// Noise cubemap used for rendering terrains with a terrain quality that
    /// seems higher than it is really.
    noiseCubemap: Texture,
    skyboxCubemap: Texture,
    framebuffer: Framebuffer,
    blurFramebuffer: Framebuffer,
    bloomFramebuffer: Framebuffer,

    /// The position of the camera
    /// This is already scaled by cameraDistance
    cameraPos: Vec3 = Vec3.new(0, -8000, 2000),
    /// The target camera position, every frame, a linear interpolation is done
    /// between the current camera position and the target position, to create a
    /// smooth moving effect.
    targetCameraPos: Vec3 = Vec3.new(0, -8, 2),
    /// The distance the camera is from the planet's center
    cameraDistance: f32,
    targetCameraDistance: f32,
    freeCam: bool = false,
    /// Euler angles of the camera's rotation in degrees.
    /// This only applies when freeCam = true
    cameraRotation: Vec3 = Vec3.new(0, 0, 0),
    /// The index of the currently selected point
    selectedPoint: usize = 0,
    cameraGroundPoint: usize = 0,
    visibleSprouts: usize = 0,
    sproutCandidates: usize = 0,
    pointerOnPlanet: bool = false,
    viewportAspect: f32 = 16.0 / 9.0,
    clickedPoint: usize = 0,
    displayMode: Planet.DisplayMode = .Normal,
    /// Inclination of rotation, in degrees
    axialTilt: f32 = 0, //23.4, // TODO: fix axial tilt with wind and solar vector
    /// The solar constant in W.m-2
    solarConstant: f32 = 1361,
    /// The time it takes for the planet to do a full rotation on itself, in seconds
    planetRotationTime: f32 = 86400,
    /// The time elapsed in seconds since the start of the game.
    /// Updated at every tick.
    gameTime: f64 = 0,
    /// The time elapsed in seconds since the start of the game.
    /// Updated at every frame. This will periodically resynchronise with gameTime
    /// The reason this exists is to have smooth rendering even when the simulation is slow
    renderGameTime: f64 = 0,
    simulationClock: @import("../simulation_clock.zig").Clock = .{},
    rawFrameDelta: ?f32 = null,
    simulationStepsLastFrame: u8 = 0,

    /// The average time a tick takes to execute.
    averageUpdateTime: f32 = 0,
    /// Time scale for the simulation.
    /// This is the number of in-game seconds that passes for each real second
    /// TODO: only expose 3 selectable time scales like in most game (normal, fast, super fast)
    /// and they would have different values depending on the geological/biological/technological time scale
    timeScale: f32 = guidance.default_browser_speed,
    /// Whether the game is paused, this has the same effect as setting timeScale to
    /// 0 except it preserves the time scale value.
    paused: bool = false,
    /// Visual inspection light only; physical solar heating still cycles.
    stableDaylight: bool = @import("builtin").target.cpu.arch == .wasm32,
    showPlanetControl: bool = false,
    showPointDetails: bool = false,
    inspectAnimal: bool = false,
    leavePlanetArmed: bool = false,

    debug_showMoreInfo: bool = false,
    debug_clearWater: bool = false,
    debug_deluge: bool = false,
    debug_spawnRabbits: bool = false,
    /// Save the game on the next call to update()
    defer_saveGame: bool = false,
    showEscapeMenu: bool = false,

    selectedTool: GameTool = .None,
    meanTemperature: f32 = 293.15,
    mobileFeedback: []const u8 = "",
    mobileFeedbackSeconds: f32 = 0,
    // Session-only compact observation UI; never a change to simulation or camera.
    watchLifeView: bool = false,
    blenderAtlas: ?nvg.Image = null,
    blenderAtlasAttempted: bool = false,
    propaguleVisuals: @import("../propagule_visuals.zig").Pool = .{},
    seedTargets: SeedTargets.List = .{},
    seedTargetWidth:f32=0,
    seedTargetHeight:f32=0,
    seedTargetWorld:usize=0,
    godReceipt: ?@import("../god_actions.zig").Receipt = null,
    godEffectSeconds: f32 = 0,

    pub const simulation_step_seconds: f32 = 1440;
    pub fn setRawFrameDelta(self:*PlayState, seconds:f32) void {self.rawFrameDelta=seconds;}

    pub fn init(game: *Game) PlayState {
        // Browser-created planets use a lighter grid. Loading preserves the
        // saved topology exactly through initWithTopology/replaceWorld.
        const subdivisions: usize = if (@import("builtin").target.cpu.arch == .wasm32 or @import("builtin").mode == .Debug) 6 else 7;
        var state = initNewWorld(game, subdivisions, game.newWorldChoice.preset);
        if (game.startOriginNext) {
            game.startOriginNext = false;
            state.planet.beginOrigin() catch unreachable;
            state.paused = true;
            state.selectedTool = .PlaceVegetation;
            const found = state.focusHabitat();
            if (found) state.mobileFeedback = "Origin: seed existing life in shallow water";
            state.mobileFeedbackSeconds = 8;
        }
        return state;
    }

    pub fn initWithTopology(game: *Game, subdivisions: usize) PlayState {
        // Loading/replacement topology must never consume a menu preset.
        return initNewWorld(game, subdivisions, .random);
    }

    fn initNewWorld(game: *Game, subdivisions: usize, preset: @import("../world_setup.zig").Preset) PlayState {
        std.debug.assert(subdivisions == 6 or subdivisions == 7);
        const soundTrack = SoundTrack{ .items = &.{
            "assets/music/music1.mp3",
            "assets/music/music2.mp3",
            "assets/music/music3.mp3",
        } };
        game.audio.playSoundTrack(soundTrack);

        // Create the noise cubemap for terrain detail
        const cubemap = Texture.initCubemap();
        var data: []u8 = game.allocator.alloc(u8, 512 * 512 * 3) catch unreachable;
        defer game.allocator.free(data);

        // The seed is constant as it should not be changed between plays for consistency
        var prng = std.rand.DefaultPrng.init(1234);
        var randomPrng = std.rand.DefaultPrng.init(@as(u64, @bitCast(std.time.milliTimestamp())));

        // Generate white noise (using the PRNG) to fill all of the cubemap's faces
        const faces = [_]Texture.CubemapFace{ .PositiveX, .NegativeX, .PositiveY, .NegativeY, .PositiveZ, .NegativeZ };
        for (faces) |face| {
            var y: usize = 0;
            while (y < 512) : (y += 1) {
                var x: usize = 0;
                while (x < 512) : (x += 1) {
                    // Currently, cubemap faces are in RGB format so only the red channel
                    // is filled. (TODO: switch to GRAY8 format)
                    data[(y * 512 + x) * 3 + 0] = prng.random().int(u8);
                }
            }
            cubemap.setCubemapFace(face, 512, 512, data);
        }

        // Create the skybox
        const skybox = Texture.initCubemap();
        for (faces) |face| {
            skybox.loadCubemapFace(game.allocator, face, "assets/starsky-1024.png") catch {};
        }

        // TODO: make a loading scene
        const planetRadius = 5000; // a radius a bit smaller than Earth's (~6371km)
        const seed = randomPrng.random().int(u64);
        const planet = Planet.generate(game.allocator, subdivisions, planetRadius, seed, .{.water_preset=preset}) catch unreachable;

        if (false) {
            // Load Earth
            var file = std.fs.cwd().openFile("assets/big-earth.png", .{}) catch unreachable;
            defer file.close();
            planet.loadFromImage(game.allocator, &file) catch {};
        }

        // Temperature difference breaks the start of the game for some reason
        // TODO: fix the bug
        @memset(planet.temperature, 293.15);

        Lifeform.initMeshes(game.allocator) catch unreachable;

        const framebuffer = Framebuffer.create(800, 600) catch unreachable;
        const blurFramebuffer = Framebuffer.createColorOnly(800, 600) catch unreachable;
        const bloomFramebuffer = Framebuffer.createColorOnly(800, 600) catch unreachable;

        const cursorPos = game.window.getCursorPos();
        std.valgrind.callgrind.startInstrumentation();
        var state = PlayState{
            .dragStart = Vec2.new(@as(f32, @floatCast(cursorPos.xpos)), @as(f32, @floatCast(cursorPos.ypos))),
            .noiseCubemap = cubemap,
            .skyboxCubemap = skybox,
            .planet = planet,
            .framebuffer = framebuffer,
            .blurFramebuffer = blurFramebuffer,
            .bloomFramebuffer = bloomFramebuffer,
            .cameraDistance = planetRadius * 10,
            .targetCameraDistance = planetRadius * 2.5,
        };
        if (@import("builtin").target.cpu.arch == .wasm32) {
            _ = state.focusLand();
            const viewport = game.window.getFramebufferSize();
            state.viewportAspect = @as(f32, @floatFromInt(viewport.width)) / @as(f32, @floatFromInt(@max(1, viewport.height)));
            state.resetView();
        }
        return state;
    }

    pub fn render(self: *PlayState, game: *Game, renderer: *Renderer) void {
        const window = renderer.window;
        const size = renderer.framebufferSize;
        self.viewportAspect = size.x() / @max(1, size.y());

        // Move the camera when dragging the mouse
        if (self.freeCam) {
            const right = self.cameraPos.cross(Vec3.forward()).norm();
            const down = self.cameraPos.cross(right).norm();
            _ = down;

            const yaw = za.toRadians(self.cameraRotation.x());
            const pitch = za.toRadians(self.cameraRotation.y());
            const forward = Vec3.new(
                std.math.cos(yaw) * std.math.cos(pitch),
                std.math.sin(yaw) * std.math.cos(pitch),
                std.math.sin(pitch),
            );
            const speed = (self.cameraPos.length() - self.planet.radius) / 100.0;
            if (window.getKey(.w) == .press) {
                self.cameraPos = self.cameraPos.add(forward.scale(speed));
            }
            if (window.getKey(.s) == .press) {
                self.cameraPos = self.cameraPos.sub(forward.scale(speed));
            }

            {
                self.cameraGroundPoint = self.planet.getNearestPointTo(self.cameraPos);
                const cameraPoint = self.planet.transformedPoints[self.cameraGroundPoint];
                if (self.cameraPos.length() < cameraPoint.length() + 100) {
                    self.cameraPos = self.cameraPos.norm().scale(cameraPoint.length() + 100);
                }
            }
        } else {
            if (window.getMouseButton(.right) == .press and !self.cameraInputBlocked()) {
                const glfwCursorPos = game.window.getCursorPos();
                const cursorPos = Vec2.new(@as(f32, @floatCast(glfwCursorPos.xpos)), @as(f32, @floatCast(glfwCursorPos.ypos)));
                const delta = cursorPos.sub(self.dragStart).scale(1.0 / 100.0);
                const right = self.targetCameraPos.cross(Vec3.forward()).norm();
                const backward = self.targetCameraPos.cross(right).norm();
                self.targetCameraPos = self.targetCameraPos
                    .add(right.scale(delta.x())
                    .add(backward.scale(-delta.y()))
                    .scale(self.targetCameraDistance / 5));
                self.dragStart = cursorPos;

                self.targetCameraPos = self.targetCameraPos.norm()
                    .scale(self.targetCameraDistance);
            }

            {
                self.cameraGroundPoint = self.planet.getNearestPointTo(self.targetCameraPos);
                const cameraPoint = self.planet.transformedPoints[self.cameraGroundPoint];
                if (self.targetCameraDistance < cameraPoint.length() + 100) {
                    self.targetCameraDistance = cameraPoint.length() + 100;
                }
            }

            // Smooth camera move using linear interpolation
            self.targetCameraPos = self.targetCameraPos.norm()
                .scale(self.targetCameraDistance);
            if (!(std.math.approxEqAbs(f32, self.cameraPos.x(), self.targetCameraPos.x(), 0.01) and
                std.math.approxEqAbs(f32, self.cameraPos.y(), self.targetCameraPos.y(), 0.01) and
                std.math.approxEqAbs(f32, self.cameraPos.z(), self.targetCameraPos.z(), 0.01) and
                std.math.approxEqAbs(f32, self.cameraDistance, self.targetCameraDistance, 0.01)))
            {
                // TODO: maybe use Quaternion lerp ? It could help on rotation near the poles.
                self.cameraPos = self.cameraPos.scale(0.9).add(self.targetCameraPos.scale(0.1));
                self.cameraDistance = self.cameraDistance * 0.9 + self.targetCameraDistance * 0.1;
                self.cameraPos = self.cameraPos.norm()
                    .scale(self.cameraDistance);
            }
        }

        const scale = 1;
        const fbWidth = @as(c_int, @intFromFloat(size.x() * scale));
        const fbHeight = @as(c_int, @intFromFloat(size.y() * scale));
        if (fbWidth != self.framebuffer.width or fbHeight != self.framebuffer.height) {
            self.framebuffer.deinit();
            self.framebuffer = Framebuffer.create(fbWidth, fbHeight) catch unreachable;

            self.blurFramebuffer.deinit();
            self.blurFramebuffer = Framebuffer.createColorOnly(fbWidth, fbHeight) catch unreachable;
            self.bloomFramebuffer.deinit();
            self.bloomFramebuffer = Framebuffer.createColorOnly(fbWidth, fbHeight) catch unreachable;
        }

        {
            self.framebuffer.bind();
            gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);
            gl.enable(gl.DEPTH_TEST);
            gl.viewport(0, 0, fbWidth, fbHeight);
            defer gl.viewport(0, 0, @as(c_int, @intFromFloat(size.x())), @as(c_int, @intFromFloat(size.y())));

            self.renderScene(game, renderer);
            self.framebuffer.unbind();
        }

        const diagnostic_camera=self.cameraPos.length();
        const post_timer=@import("../performance_details.zig").beginStage();
        defer @import("../performance_details.zig").endStage(post_timer,.postprocess);
        const useBloom=!@import("../empty_bloom.zig").canSkip(
            @import("builtin").target.cpu.arch == .wasm32,self.planet.worldMode==.origin,
            self.displayMode==.Normal,self.stableDaylight,!self.freeCam,
            self.planet.lifeforms.items.len,diagnostic_camera);
        // Capture actual last-render settings only while local diagnostics are open.
        @import("../performance_details.zig").metrics.renderContext(.{
            .valid=true,.world=@tagName(self.planet.worldMode),.map=@tagName(self.displayMode),
            .canvas_width=@intFromFloat(size.x()),.canvas_height=@intFromFloat(size.y()),
            .scene_width=fbWidth,.scene_height=fbHeight,.bloom_active=useBloom,
            .bloom_passes=if(useBloom)5 else 0,.stable_daylight=self.stableDaylight,.orbit=!self.freeCam,
            .animals=self.planet.lifeforms.items.len,.camera_valid=std.math.isFinite(diagnostic_camera),
            .camera_radius=if(std.math.isFinite(diagnostic_camera))diagnostic_camera else 0,.planet_radius=self.planet.radius,
        });
        // Compute a texture from the HDR framebuffer with only bright parts.
        // Skip only the provablyzero contribution, not an active visual effect.
        if(useBloom) {
            const program = &renderer.postprocessProgram;
            self.bloomFramebuffer.bind();
            defer self.bloomFramebuffer.unbind();

            program.use();
            program.setUniformBool("doBrightTexture", true);
            gl.viewport(0, 0, fbWidth, fbHeight);
            defer gl.viewport(0, 0, @as(c_int, @intFromFloat(size.x())), @as(c_int, @intFromFloat(size.y())));

            gl.bindVertexArray(QuadMesh.getVAO());
            gl.disable(gl.DEPTH_TEST);
            gl.activeTexture(gl.TEXTURE0);
            gl.bindTexture(gl.TEXTURE_2D, self.framebuffer.colorTextures[0]);
            gl.drawArrays(gl.TRIANGLES, 0, 6);
        }

        // Blur the bright part to create bloom
        if(useBloom) {
            const program = &renderer.postprocessProgram;

            // Horizontal blurring (framebuffer -> blurFramebuffer)
            program.use();
            program.setUniformBool("doBrightTexture", false);
            program.setUniformBool("doBlurring", true);

            for (0..4) |i| {
                program.setUniformBool("horizontalBlurring", i % 2 == 0);

                const source = if (i % 2 == 0) self.bloomFramebuffer.colorTextures[0] else self.blurFramebuffer.colorTextures[0];
                const target = if (i % 2 == 0) self.blurFramebuffer else self.bloomFramebuffer;
                {
                    target.bind();
                    defer target.unbind();
                    gl.viewport(0, 0, fbWidth, fbHeight);
                    defer gl.viewport(0, 0, @as(c_int, @intFromFloat(size.x())), @as(c_int, @intFromFloat(size.y())));
                    gl.bindVertexArray(QuadMesh.getVAO());
                    gl.disable(gl.DEPTH_TEST);
                    gl.activeTexture(gl.TEXTURE0);
                    gl.bindTexture(gl.TEXTURE_2D, source);
                    gl.drawArrays(gl.TRIANGLES, 0, 6);
                }
            }
        }

        gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);
        {
            const program = &renderer.postprocessProgram;
            const sunPhi: f32 = @as(f32, @floatCast(@mod(self.renderGameTime / self.planetRotationTime * 2 * std.math.pi, 2 * std.math.pi)));
            const sunTheta: f32 = std.math.pi / 2.0;
            const solarVector = if (self.stableDaylight) self.cameraPos.norm() else Vec3.new(@cos(sunPhi) * @sin(sunTheta), @sin(sunPhi) * @sin(sunTheta), @cos(sunTheta));
            const zFar = self.planet.radius * 5;
            const zNear = zFar / 10000;
            const target = self.getViewTarget();

            program.use();
            program.setUniformInt("screenTexture", 0);
            program.setUniformInt("bloomTexture", 1);
            program.setUniformBool("enableBloom",useBloom);
            program.setUniformInt("screenDepth", 2);
            program.setUniformMat4("projMatrix", Mat4.perspective(70, size.x() / size.y(), zNear, zFar));
            program.setUniformMat4("viewMatrix", Mat4.lookAt(self.cameraPos, target, Vec3.new(0, 0, 1)));
            program.setUniformVec3("viewPos", self.cameraPos);
            program.setUniformVec3("lightDir", solarVector);
            program.setUniformFloat("planetRadius", self.planet.radius);
            program.setUniformFloat("atmosphereRadius", self.planet.radius + 50 * 10); // * HEIGHT_ELEVATION
            program.setUniformFloat("lightIntensity", self.solarConstant / 1500);
            program.setUniformBool("enableAtmosphere", self.displayMode == .Normal and @import("builtin").target.cpu.arch != .wasm32);
            program.setUniformBool("doBrightTexture", false);
            program.setUniformBool("doBlurring", false);

            gl.bindVertexArray(QuadMesh.getVAO());
            gl.disable(gl.DEPTH_TEST);
            gl.activeTexture(gl.TEXTURE0);
            gl.bindTexture(gl.TEXTURE_2D, self.framebuffer.colorTextures[0]); // color
            gl.activeTexture(gl.TEXTURE1);
            gl.bindTexture(gl.TEXTURE_2D, self.bloomFramebuffer.colorTextures[0]); // blur
            gl.activeTexture(gl.TEXTURE2);
            gl.bindTexture(gl.TEXTURE_2D, self.framebuffer.depthTexture); // depth
            gl.drawArrays(gl.TRIANGLES, 0, 6);
        }

        if (!self.paused) {
            self.renderGameTime = self.gameTime;
        }
    }

    fn getViewTarget(self: *PlayState) Vec3 {
        // Planet-lab orbit stays centered even at close zoom. The old
        // horizon bias moved land away from the picking ray on phones.
        if (@import("builtin").target.cpu.arch == .wasm32 and !self.freeCam) return Vec3.zero();
        const right = self.cameraPos.cross(Vec3.forward()).norm();
        const forward = self.cameraPos.cross(right).norm().negate();
        const planetTarget = Vec3.new(0, 0, 0).sub(self.cameraPos).norm();
        const distToPlanet = self.cameraDistance - self.planet.radius;
        var target = self.cameraPos.add(Vec3.lerp(planetTarget, forward, std.math.pow(f32, 2, -distToPlanet / self.planet.radius * 5) * 0.6));

        if (self.freeCam) {
            //const rotMatrix = Mat4.fromEulerAngles(self.cameraRotation);
            const yaw = za.toRadians(self.cameraRotation.x());
            const pitch = za.toRadians(self.cameraRotation.y());
            const direction = Vec3.new(
                std.math.cos(yaw) * std.math.cos(pitch),
                std.math.sin(yaw) * std.math.cos(pitch),
                std.math.sin(pitch),
            );
            target = self.cameraPos.add(direction);
        }

        return target;
    }

    pub fn renderScene(self: *PlayState, game: *Game, renderer: *Renderer) void {
        const stage_timer=@import("../performance_details.zig").beginStage();
        defer @import("../performance_details.zig").endStage(stage_timer,.scene_draw);
        const size = renderer.framebufferSize;

        const planet = &self.planet;
        const sunPhi: f32 = @as(f32, @floatCast(@mod(self.renderGameTime / self.planetRotationTime * 2 * std.math.pi, 2 * std.math.pi)));
        const sunTheta: f32 = std.math.pi / 2.0;
        const solarVector = if (self.stableDaylight) self.cameraPos.norm() else Vec3.new(@cos(sunPhi) * @sin(sunTheta), @sin(sunPhi) * @sin(sunTheta), @cos(sunTheta));

        const zFar = planet.radius * 5;
        const zNear = zFar / 10000;

        const target = self.getViewTarget();

        // Start by rendering the skybox
        {
            const program = &renderer.skyboxProgram;
            program.use();
            program.setUniformMat4("projMatrix", Mat4.perspective(70, size.x() / size.y(), 0.01, 100));
            var newViewMatrix = Mat4.lookAt(self.cameraPos, target, Vec3.new(0, 0, 1));
            // remove all the translation part
            newViewMatrix.data[0][3] = 0;
            newViewMatrix.data[1][3] = 0;
            newViewMatrix.data[2][3] = 0;
            newViewMatrix.data[3][3] = 1;
            newViewMatrix.data[3][0] = 0;
            newViewMatrix.data[3][1] = 0;
            newViewMatrix.data[3][2] = 0;
            program.setUniformMat4("viewMatrix", newViewMatrix);
            gl.depthMask(gl.FALSE);

            gl.activeTexture(gl.TEXTURE0);
            gl.bindTexture(gl.TEXTURE_CUBE_MAP, self.skyboxCubemap.texture);
            program.setUniformInt("skyboxCubemap", 0);

            gl.bindVertexArray(CubeMesh.getVAO());
            gl.drawArrays(gl.TRIANGLES, 0, 36);

            gl.depthMask(gl.TRUE);
        }

        // Then render the sun
        {
            // TODO: do like skybox so it looks infinitely far
            const program = &renderer.sunProgram;
            program.use();
            program.setUniformMat4("projMatrix", Mat4.perspective(70, size.x() / size.y(), 1, 1000000));
            program.setUniformMat4("viewMatrix", Mat4.lookAt(self.cameraPos, target, Vec3.new(0, 0, 1)));
            const modelMatrix = Mat4.recompose(solarVector.scale(300000), Vec3.new(0, 0, 0), Vec3.new(8000, 8000, 8000));
            program.setUniformMat4("modelMatrix", modelMatrix);

            const mesh = SunMesh.getMesh(game.allocator);
            gl.bindVertexArray(mesh.vao[0]);
            gl.drawElements(gl.TRIANGLES, @as(c_int, @intCast(mesh.indices.len)), gl.UNSIGNED_INT, null);
        }

        // Then render the planet
        {
            const program = &renderer.terrainProgram;
            program.use();
            program.setUniformMat4("projMatrix", Mat4.perspective(70, size.x() / size.y(), zNear, zFar));
            program.setUniformMat4("viewMatrix", Mat4.lookAt(self.cameraPos, target, Vec3.new(0, 0, 1)));

            const modelMatrix = Mat4.recompose(Vec3.new(0, 0, 0), Vec3.new(0, 0, 0), Vec3.new(1, 1, 1));
            program.setUniformMat4("modelMatrix", modelMatrix);

            program.setUniformVec3("lightColor", Vec3.new(1.0, 1.0, 1.0));
            program.setUniformVec3("lightDir", solarVector);
            program.setUniformFloat("lightIntensity", self.solarConstant / 1500);
            program.setUniformVec3("viewPos", self.cameraPos);
            program.setUniformFloat("planetRadius", planet.radius);
            program.setUniformBool("clearSurface", @import("builtin").target.cpu.arch == .wasm32);
            program.setUniformBool("mapContext", @import("builtin").target.cpu.arch == .wasm32);
            program.setUniformInt("displayMode", @intFromEnum(self.displayMode)); // display mode
            program.setUniformVec3("selectedVertexPos", planet.transformedPoints[self.selectedPoint]);
            program.setUniformBool("compactSelection", @import("builtin").target.cpu.arch == .wasm32);
            program.setUniformFloat("kmPerWaterMass", planet.getKmPerWaterMass());
            program.setUniformVec3("vegetationColor", utils.getWavelengthColor(planet.plantColorWavelength));

            gl.activeTexture(gl.TEXTURE0);
            gl.bindTexture(gl.TEXTURE_CUBE_MAP, self.noiseCubemap.texture);
            program.setUniformInt("noiseCubemap", 0);

            const terrainNormalMap = renderer.textureCache.getExt("normal-map", .{ .mipmaps = true });
            gl.activeTexture(gl.TEXTURE1);
            gl.bindTexture(gl.TEXTURE_2D, terrainNormalMap.texture);
            program.setUniformInt("terrainNormalMap", 1);

            const waterNormalMap = renderer.textureCache.getExt("water-normal-map", .{ .mipmaps = true });
            gl.activeTexture(gl.TEXTURE2);
            gl.bindTexture(gl.TEXTURE_2D, waterNormalMap.texture);
            program.setUniformInt("waterNormalMap", 2);

            gl.enable(gl.CULL_FACE);
            defer gl.disable(gl.CULL_FACE);
            gl.frontFace(gl.CW);
            defer gl.frontFace(gl.CCW);

            // gl.polygonMode(gl.FRONT_AND_BACK, gl.LINE);
            planet.render(game.loop, self.displayMode, self.axialTilt);
            // gl.polygonMode(gl.FRONT_AND_BACK, gl.FILL);
        }

        // Then the clouds
        {
            const program = &renderer.cloudsProgram;
            program.use();
            program.setUniformMat4("projMatrix", Mat4.perspective(70, size.x() / size.y(), zNear, zFar));
            program.setUniformMat4("viewMatrix", Mat4.lookAt(self.cameraPos, target, Vec3.new(0, 0, 1)));

            const modelMatrix = Mat4.recompose(Vec3.new(0, 0, 0), Vec3.new(0, 0, 0), Vec3.new(1, 1, 1));
            program.setUniformMat4("modelMatrix", modelMatrix);

            program.setUniformVec3("lightColor", Vec3.new(1.0, 1.0, 1.0));
            program.setUniformVec3("lightDir", solarVector);
            program.setUniformFloat("lightIntensity", self.solarConstant / 1500);
            program.setUniformVec3("viewPos", self.cameraPos);
            program.setUniformFloat("planetRadius", planet.radius);
            program.setUniformFloat("kmPerWaterMass", planet.getKmPerWaterMass());
            program.setUniformFloat("gameTime", @as(f32, @floatCast(self.gameTime)));

            gl.activeTexture(gl.TEXTURE0);
            gl.bindTexture(gl.TEXTURE_CUBE_MAP, self.noiseCubemap.texture);
            program.setUniformInt("noiseCubemap", 0);

            const waterNormalMap = renderer.textureCache.getExt("water-normal-map", .{ .mipmaps = true });
            gl.activeTexture(gl.TEXTURE1);
            gl.bindTexture(gl.TEXTURE_2D, waterNormalMap.texture);
            program.setUniformInt("waterNormalMap", 1);

            if (self.displayMode == .Normal and @import("builtin").target.cpu.arch != .wasm32)
                planet.renderWater();
        }

        const entity = &renderer.entityProgram;
        entity.use();
        entity.setUniformMat4("projMatrix", Mat4.perspective(70, size.x() / size.y(), zNear, zFar));
        entity.setUniformMat4("viewMatrix", Mat4.lookAt(self.cameraPos, target, Vec3.new(0, 0, 1)));

        gl.frontFace(gl.CCW);
        for (planet.lifeforms.items) |lifeform| {
            const animalScale: f32 = if (@import("builtin").target.cpu.arch == .wasm32) 0.12 else 1;
            const modelMat: Mat4 = if (@import("builtin").target.cpu.arch == .wasm32) .{ .data = biology_visuals.groundedRabbit(lifeform.position.data, animalScale) } else Mat4.recompose(lifeform.position, Vec3.new(0, 0, 0), Vec3.new(animalScale, animalScale, animalScale));
            entity.setUniformMat4("modelMatrix", modelMat);
            entity.setUniformVec3("lightColor", Vec3.new(1.0, 1.0, 1.0));
            entity.setUniformVec3("lightDir", solarVector);

            const mesh = lifeform.getMesh();
            gl.bindVertexArray(mesh.vao);
            gl.drawArrays(gl.TRIANGLES, 0, mesh.numTriangles);
        }
    }

    // As updated slices (temperature and water elevation) are updated by a
    // swap. This is atomic.
    /// Biological illumination, independent of the stable-daylight viewing aid.
    pub fn simulationSolarVector(self: *const PlayState) Vec3 {
        const phi: f32 = @floatCast(@mod(self.gameTime / self.planetRotationTime * 2 * std.math.pi, 2 * std.math.pi));
        const theta: f32 = std.math.pi / 2.0;
        return Vec3.new(@cos(phi) * @sin(theta), @sin(phi) * @sin(theta), @cos(theta));
    }

    pub fn update(self: *PlayState, game: *Game, dt: f32) void {
        self.mobileFeedbackSeconds = @max(0, self.mobileFeedbackSeconds - dt);
        self.propaguleVisuals.advance(dt);
        self.godEffectSeconds = @max(0,self.godEffectSeconds-dt);
        const raw_dt=self.rawFrameDelta orelse dt;self.rawFrameDelta=null;
        self.simulationStepsLastFrame=0;
        self.simulationClock.begin(raw_dt,self.timeScale,simulation_step_seconds,self.paused or self.showEscapeMenu);
        if (self.showEscapeMenu) return;

        const planet = &self.planet;

        if (game.window.getMouseButton(.left) == .press and !self.mobilePointerOnUI(game) and self.pointerOnPlanet) {
            _ = self.applySelectedTool(self.selectedTool, false, dt);
        }

        if (self.debug_clearWater) {
            @memset(self.planet.waterMass, 0);
            @memset(self.planet.waterVaporMass, 0);
            self.debug_clearWater = false;
        }

        if (self.debug_deluge) {
            @memset(self.planet.waterVaporMass, 5_000_000);
            self.debug_deluge = false;
        }

        if (self.debug_spawnRabbits) {
            var prng = std.rand.DefaultPrng.init(@as(u64, @bitCast(std.time.milliTimestamp())));
            const random = prng.random();

            var i: usize = 0;
            while (i < 10) : (i += 1) {
                const point = planet.transformedPoints[random.intRangeLessThanBiased(usize, 0, planet.temperature.len)];
                const lifeform = Lifeform.init(point, .Rabbit, self.gameTime);
                planet.addLifeform(lifeform) catch unreachable;
            }
            self.debug_spawnRabbits = false;
        }

        if (!self.paused) {
            var timer=std.time.Timer.start() catch unreachable;
            while(self.simulationStepsLastFrame<2 and self.simulationClock.take(simulation_step_seconds)) {
                // Bounded physical quantum; requested UI speed never disables a subsystem.
                planet.simulate(game.loop,.{.dt=simulation_step_seconds,.timeScale=1,
                    .solarConstant=self.solarConstant,.gameTime=self.gameTime,
                    .planetRotationTime=self.planetRotationTime,.solarVector=self.simulationSolarVector()});
                self.gameTime+=simulation_step_seconds;
                self.simulationStepsLastFrame+=1;
                // A single engine tick is indivisible; never start another after budget expires.
                if(timer.read()>=16_000_000)break;
            }
            if(self.simulationStepsLastFrame>0){const elapsed=@as(f32,@floatFromInt(timer.read()))/1e9;self.averageUpdateTime=self.averageUpdateTime*0.9+elapsed*0.1;@import("../performance_details.zig").metrics.physics(@as(f64,elapsed)*1000,self.simulationStepsLastFrame);}
        }
        self.simulationClock.finish();
        self.renderGameTime=self.gameTime;

        const targetMusicVolume: f32 = blk: {
            if (self.paused) {
                break :blk 0.1;
            } else {
                break :blk 0.4;
            }
        };

        const t = 0.6 * dt;
        game.audio.setMusicVolume(game.audio.getMusicVolume() * (1 - t) + targetMusicVolume * t);

        if (self.defer_saveGame) {
            self.saveGame() catch |err| {
                // TODO: handle error
                err catch {};
            };
            self.defer_saveGame = false;
        }
    }

    pub fn keyCallback(self: *PlayState, game: *Game, key: glfw.Key, scancode: i32, action: glfw.Action, mods: glfw.Mods) void {
        _ = scancode;
        _ = mods;
        if (action == .press) {
            if (key == .escape) {
                self.showEscapeMenu = !self.showEscapeMenu;
            }

            if (self.showEscapeMenu) return;
            if (key == .F3) {
                self.debug_showMoreInfo = !self.debug_showMoreInfo;
            }
            if (key == .F5) {
                const numEnumFields = @as(c_int, std.meta.fields(Planet.DisplayMode).len);
                self.displayMode = @as(Planet.DisplayMode, @enumFromInt(@mod(@intFromEnum(self.displayMode) + 1, numEnumFields)));
            }
            if (key == .F6) {
                if (self.freeCam) {
                    self.targetCameraDistance = self.cameraPos.length();
                }
                self.freeCam = !self.freeCam;

                game.renderer.window.setInputModeCursor(
                    if (self.freeCam) .disabled else .normal,
                );
            }
            if (key == .space) {
                self.paused = !self.paused;
            }

            if (key == .kp_add) {
                self.timeScale += 10;
            } else if (key == .kp_subtract) {
                self.timeScale -= 10;
            }
        }
    }

    pub fn mousePressed(self: *PlayState, game: *Game, button: MouseButton) void {
        if (self.showEscapeMenu) return;
        if (@import("builtin").target.cpu.arch == .wasm32 and self.mobilePointerOnUI(game)) return;

        if (button == .left and self.planet.worldMode == .origin and self.selectedTool == .PlaceVegetation) {
            if (self.cameraInputBlocked()) return;
            self.validateSeedTargetViewport(game);
            const cursor=game.window.getCursorPos();
            if (self.pickSeedTarget(@floatCast(cursor.xpos),@floatCast(cursor.ypos))) |cell| {
                self.selectedPoint=cell;self.pointerOnPlanet=true;
                if(self.planet.seedEligibility(cell)==.eligible) _=self.applySelectedTool(.PlaceVegetation,true,0);
            } else {
                self.mobileFeedback="Tap closer to a green + or use Seed colony";self.mobileFeedbackSeconds=3;
            }
            return;
        }

        if (button == .left and !self.pointerOnPlanet) {
            self.mobileFeedback = "Tap the planet, or use Land below";
            self.mobileFeedbackSeconds = 3;
            return;
        }
        if (button == .left) _ = self.applySelectedTool(self.selectedTool, true, 0);
        if (self.selectedTool == .PlaceLife and button == .left and self.planet.worldMode != .origin) {
            const planet = &self.planet;
            const point = self.selectedPoint;
            if (!guidance.rabbitWaterSafe(planet.waterMass[point] * planet.getKmPerWaterMass())) {
                self.mobileFeedback = "Too much water: choose dry land";
                self.mobileFeedbackSeconds = 3;
                return;
            }
            const pointPos = planet.transformedPoints[point];
            var lifeform = Lifeform.init(pointPos, .Rabbit, self.gameTime);
            if (@import("builtin").target.cpu.arch == .wasm32) {
                // Start a nearby mixed-sex pair, not an invisible single founder.
                // They still need suitable land, food and time to mature.
                lifeform.genome.gender = .Female;
                planet.addLifeform(lifeform) catch unreachable;
                const tangent = pointPos.cross(if (@abs(pointPos.norm().z()) < 0.9) Vec3.new(0, 0, 1) else Vec3.new(0, 1, 0)).norm();
                const nearby = pointPos.add(tangent.scale(35)).norm().scale(pointPos.length());
                var partner = Lifeform.init(nearby, .Rabbit, self.gameTime);
                partner.genome.gender = .Male;
                planet.addLifeform(partner) catch unreachable;
                self.mobileFeedback = if (planet.vegetation[point] <= 0.01) "Pair added. Plant food nearby" else if (self.paused) "Pair added. Press Play to watch them" else "Pair added. Watch them find food";
                self.mobileFeedbackSeconds = 3;
            } else {
                planet.addLifeform(lifeform) catch unreachable;
            }
        }

        if (self.selectedTool == .None and button == .left) {
            self.showPointDetails = true;
            self.clickedPoint = self.selectedPoint;
        }

        if (button == .right) {
            const cursorPos = game.window.getCursorPos();
            self.dragStart = Vec2.new(@as(f32, @floatCast(cursorPos.xpos)), @as(f32, @floatCast(cursorPos.ypos)));
        }
    }

    /// Shared implementation used by actual pointer editing and the test seam.
    fn applySelectedTool(self: *PlayState, tool: GameTool, tap: bool, elapsed: f32) bool {
        if (self.selectedPoint >= self.planet.vertices.len) return false;
        if (self.planet.worldMode == .origin and (tool == .PlaceVegetation or tool == .PlaceLife)) {
            // Seeding and nutrient input are deliberate taps, never automatic
            // repeated additions from frame rate or holding the pointer down.
            if (!tap) return false;
            const success = if (tool == .PlaceVegetation) self.planet.seedMicrobes(self.selectedPoint) else self.planet.addMicrobeNutrients(self.selectedPoint);
            self.mobileFeedback = if (tool == .PlaceVegetation) (if (success) "Colony seeded. Light and resources drive growth" else "Need shallow water, suitable temperature and space") else (if (success) "Nutrients added: an external resource input" else "This patch already has ample nutrients");
            self.mobileFeedbackSeconds = 3;
            return success;
        }
        if (tool == .None or tool == .PlaceLife) return false;
        const planet = &self.planet;
        if (tool == .EmitWater) {
            const kmPerWaterMass = planet.getKmPerWaterMass();
            if (planet.waterMass[self.selectedPoint] < 25 / kmPerWaterMass) {
                planet.waterMass[self.selectedPoint] = @min(25 / kmPerWaterMass, planet.waterMass[self.selectedPoint] + edit_rates.water(tap, elapsed) / kmPerWaterMass);
            }
        }
        if (tool == .PlaceVegetation) {
            planet.vegetation[self.selectedPoint] = @max(0.35, planet.vegetation[self.selectedPoint]);
            if (@import("builtin").target.cpu.arch == .wasm32) {
                // A phone brush paints a visible patch, not one tiny triangle.
                // Keep approximately the same physical brush footprint:
                // one ring on the lighter grid, three on existing dense saves.
                for (planet.getNeighbours(self.selectedPoint)) |first| {
                    planet.vegetation[first] = @max(0.35, planet.vegetation[first]);
                    if (planet.numSubdivisions >= 7) for (planet.getNeighbours(first)) |second| {
                        planet.vegetation[second] = @max(0.35, planet.vegetation[second]);
                        for (planet.getNeighbours(second)) |third| planet.vegetation[third] = @max(0.35, planet.vegetation[third]);
                    };
                }
            }
        }

        if (tool == .DrainWater) {
            planet.waterMass[self.selectedPoint] = 0;
            for (planet.getNeighbours(self.selectedPoint)) |idx| {
                planet.waterMass[idx] = 0;
            }
        }

        if (tool == .RaiseTerrain) {
            if (planet.elevation[self.selectedPoint] < planet.radius + 20) {
                planet.elevation[self.selectedPoint] = @min(planet.radius + 20, planet.elevation[self.selectedPoint] + edit_rates.terrain(tap, elapsed));
            }
            for (planet.getNeighbours(self.selectedPoint)) |idx| {
                if (planet.elevation[idx] < planet.radius + 20) {
                    planet.elevation[idx] = @min(planet.radius + 20, planet.elevation[idx] + edit_rates.terrain(tap, elapsed) * 0.5);
                }
            }
        }

        if (tool == .LowerTerrain) {
            if (planet.elevation[self.selectedPoint] > planet.radius - 20) {
                planet.elevation[self.selectedPoint] = @max(planet.radius - 20, planet.elevation[self.selectedPoint] - edit_rates.terrain(tap, elapsed));
            }
            for (planet.getNeighbours(self.selectedPoint)) |idx| {
                if (planet.elevation[idx] > planet.radius - 20) {
                    planet.elevation[idx] = @max(planet.radius - 20, planet.elevation[idx] - edit_rates.terrain(tap, elapsed) * 0.5);
                }
            }
        }

        self.mobileFeedback = switch (tool) {
            .PlaceVegetation => if (guidance.plantWarning(planet.waterMass[self.selectedPoint] * planet.getKmPerWaterMass())) |warning| warning else "Seedlings planted: let them grow",
            .EmitWater => "Water added: flooding can kill life",
            .DrainWater => "Water drained from this patch",
            .RaiseTerrain => "Land raised",
            .LowerTerrain => "Land lowered",
            else => "",
        };
        self.mobileFeedbackSeconds = 3;
        return true;
    }

    pub fn adjustSelectedWater(self:*PlayState, expected_point:u32, delta_m:f32) f32 {
        if(self.planet.worldMode!=.origin or expected_point!=self.selectedPoint or self.selectedPoint>=self.planet.waterMass.len or !std.math.isFinite(delta_m) or @abs(delta_m)>0.100001) return std.math.nan(f32);
        const changed=self.planet.adjustWaterDepth(self.selectedPoint,delta_m/1000);
        if(std.math.isFinite(changed)) {
            self.mobileFeedback=if(changed>0) "Fine water added to selected patch" else if(changed<0) "Fine water removed from selected patch" else "No water change";
            self.mobileFeedbackSeconds=3;
        }
        return changed;
    }

    pub fn setSelectedWaterTarget(self:*PlayState, expected_point:u32, target_m:f32) f32 {
        if(self.planet.worldMode!=.origin or expected_point!=self.selectedPoint or self.selectedPoint>=self.planet.waterMass.len or !std.math.isFinite(target_m) or target_m<0 or target_m>5) return std.math.nan(f32);
        const changed=self.planet.setWaterDepthMeters(self.selectedPoint,target_m);
        if(std.math.isFinite(changed)) {
            self.mobileFeedback=if(changed>0) "Water supplied to target depth" else if(changed<0) "Water removed to target depth" else "Target depth already reached";
            self.mobileFeedbackSeconds=3;
        }
        return changed;
    }

    pub fn applyGodAction(self:*PlayState,kind:@import("../god_actions.zig").Kind,expected:usize) @import("../god_actions.zig").Receipt {
        const Actions=@import("../god_actions.zig");
        const result=if(kind==.wave) Actions.wave(&self.planet,expected,self.selectedPoint) else Actions.lightning(&self.planet,expected,self.selectedPoint,self.planet.currentHeatCapacity(self.selectedPoint));
        self.godReceipt=if(result.success())result else null;
        self.godEffectSeconds=if(result.success())1.2 else 0;
        self.mobileFeedback=if(result.success()) (if(kind==.wave) "Wave moved existing water; watch flooding" else "Heat impulse added; ecology responds with time") else "Action blocked: refresh selected patch";
        self.mobileFeedbackSeconds=5;
        return result;
    }

    pub fn seedSelectedColony(self:*PlayState, expected_point:u32) i32 {
        if(self.planet.worldMode!=.origin or expected_point!=self.selectedPoint or self.selectedPoint>=self.planet.microbeCells.len) return -1;
        return @intFromBool(self.applySelectedTool(.PlaceVegetation,true,0));
    }

    pub fn makeSelectedNursery(self:*PlayState, expected_point:u32) i32 {
        const count=@import("../pond_action.zig").makeNursery(&self.planet,expected_point,self.selectedPoint);
        if(count>0) {
            self.mobileFeedback="Nursery shaped: 5 m center, 15 m reservoir; seed separately";
            self.mobileFeedbackSeconds=5;
        }
        return count;
    }

    pub fn makeSelectedPond(self:*PlayState, expected_point:u32) i32 {
        const count=@import("../pond_action.zig").makePond(&self.planet,expected_point,self.selectedPoint);
        if(count>0) {
            self.mobileFeedback="Basin shaped and filled; seed shallow floor";
            self.mobileFeedbackSeconds=5;
        }
        return count;
    }

    pub fn testAction(self: *PlayState, tool_id: i32) bool {
        if (!self.pointerOnPlanet or tool_id < 0 or tool_id > 6) return false;
        return self.applySelectedTool(@enumFromInt(tool_id), true, 0);
    }

    fn setOrbitDistance(self: *PlayState, distance: f32, snap: bool) void {
        self.freeCam = false;
        self.targetCameraDistance = distance;
        self.targetCameraPos = self.targetCameraPos.norm().scale(distance);
        if (snap) {
            self.cameraDistance = distance;
            self.cameraPos = self.targetCameraPos;
        }
    }

    pub fn zoom(self: *PlayState, steps: f32) void {
        if (!std.math.isFinite(steps)) return;
        const surface = self.planet.transformedPoints[self.planet.getNearestPointTo(self.targetCameraPos)].length();
        self.setOrbitDistance(camera_math.zoomDistance(self.targetCameraDistance, surface, steps), false);
    }

    pub fn resetView(self: *PlayState) void {
        self.setOrbitDistance(camera_math.globeDistance(self.planet.radius, self.viewportAspect), true);
    }

    /// Frame real live colonies or suitable existing shallow water; never create habitat.
    pub fn focusHabitat(self: *PlayState) bool {
        var chosen: ?usize = null;
        var best: f32 = -1;
        for (self.planet.transformedPoints, 0..) |point, i| {
            if (@abs(point.norm().z()) > 0.95) continue;
            const depth = self.planet.waterMass[i] * self.planet.getKmPerWaterMass();
            var neighbours: f32 = 0;
            for (self.planet.getNeighbours(i)) |n| { if (Microbes.habitable(self.planet.waterMass[n] * self.planet.getKmPerWaterMass(), self.planet.temperature[n])) neighbours += 1; }
            const biomass = if (self.planet.microbeCells.len > i) Microbes.biomass(self.planet.microbeCells[i]) else 0;
            const score = habitat_focus.score(biomass, point.norm().z(), depth, self.planet.temperature[i], Microbes.habitable(depth,self.planet.temperature[i]), neighbours);
            if (score > best) { chosen = i; best = score; }
        }
        const index = chosen orelse { self.mobileFeedback = "No shallow habitat: add water to a basin"; self.mobileFeedbackSeconds = 5; return false; };
        self.targetCameraPos = self.planet.transformedPoints[index].norm();
        self.selectedPoint = index; self.pointerOnPlanet = true;
        self.setOrbitDistance(self.planet.transformedPoints[index].length() + @as(f32, if (@import("builtin").target.cpu.arch == .wasm32) 900 else 300), true);
        return true;
    }

    pub fn focusSeedableHabitat(self:*PlayState) bool {
        self.selectedTool=.PlaceVegetation;
        var chosen:?usize=null;var best:f32=-1;
        for(self.planet.transformedPoints,0..)|point,i| {
            if(@abs(point.norm().z())>0.95 or self.planet.seedEligibility(i)!=.eligible)continue;
            var neighbors:f32=0;for(self.planet.getNeighbours(i))|n|{if(self.planet.seedEligibility(n)==.eligible)neighbors+=1;}
            // Placeable is not a survival guarantee: prefer existing shallow, low-latitude habitat.
            const score=habitat_focus.score(0,point.norm().z(),self.planet.waterMass[i]*self.planet.getKmPerWaterMass(),self.planet.temperature[i],true,neighbors);
            if(score>best){best=score;chosen=i;}
        }
        const i=chosen orelse {self.mobileFeedback="No seedable patch: inspect water, temperature and resources";self.mobileFeedbackSeconds=5;return false;};
        self.selectedTool=.PlaceVegetation;self.selectedPoint=i;self.pointerOnPlanet=true;self.targetCameraPos=self.planet.transformedPoints[i].norm();
        self.setOrbitDistance(self.planet.transformedPoints[i].length()+@as(f32,if(@import("builtin").target.cpu.arch==.wasm32)900 else 300),true);
        self.mobileFeedback="Can seed here: Seed colony adds existing life";self.mobileFeedbackSeconds=5;
        return true;
    }

    pub fn focusLand(self: *PlayState) bool {
        if (self.planet.worldMode == .origin) return self.focusSeedableHabitat();
        var best: usize = 0;
        var found = false;
        var bestElevation: f32 = -std.math.inf(f32);
        for (self.planet.transformedPoints, 0..) |point, index| {
            // Avoid the orbit camera's polar up-vector singularity.
            if (@abs(point.norm().z()) > 0.95) continue;
            const dry = self.planet.waterMass[index] < 0.1;
            if ((dry and !found) or (dry == found and self.planet.elevation[index] > bestElevation)) {
                best = index;
                found = dry;
                bestElevation = self.planet.elevation[index];
            }
        }
        self.targetCameraPos = self.planet.transformedPoints[best].norm();
        self.selectedPoint = best;
        self.pointerOnPlanet = true;
        self.setOrbitDistance(@max(self.planet.radius * 1.35, self.planet.transformedPoints[best].length() + 300), true);
        return found;
    }

    fn cameraInputBlocked(self: *const PlayState) bool {
        return self.showEscapeMenu or self.showPlanetControl or self.showPointDetails;
    }

    pub fn mouseScroll(self: *PlayState, _: *Game, yOffset: f64) void {
        if (self.cameraInputBlocked()) return;

        if (@import("builtin").target.cpu.arch == .wasm32) {
            self.zoom(@as(f32, @floatCast(yOffset)) * 0.5);
            return;
        }
        const zFar = self.planet.radius * 5;
        const zNear = zFar / 10000;

        const minDistance = self.planet.radius + zNear;
        const maxDistance = self.planet.radius * 5;
        self.targetCameraDistance = std.math.clamp(self.targetCameraDistance - (@as(f32, @floatCast(yOffset)) * self.cameraDistance / 50), minDistance, maxDistance);
    }

    fn validateSeedTargetViewport(self:*PlayState,game:*Game) void {
        const size=game.window.getFramebufferSize();
        if(self.seedTargetWidth!=@as(f32,@floatFromInt(size.width)) or self.seedTargetHeight!=@as(f32,@floatFromInt(size.height)))self.seedTargets.count=0;
    }
    /// Exact visible target, never redirected if ecology changed after rendering.
    /// The action separately rechecks eligibility before any state mutation.
    pub fn pickSeedTarget(self:*PlayState,x:f32,y:f32) ?usize {
        if(self.planet.worldMode!=.origin or self.selectedTool!=.PlaceVegetation or self.displayMode!=.Normal)return null;
        if(self.seedTargetWorld!=@intFromPtr(self.planet.waterMass.ptr))return null;
        return self.seedTargets.pick(x,y);
    }

    pub fn mouseMoved(self: *PlayState, game: *Game, x: f32, y: f32, dx: f32, dy: f32) void {
        if (self.cameraInputBlocked() or self.mobilePointerOnUI(game)) return;
        if (self.freeCam) {
            const mouseSensitivity = 0.1;
            self.cameraRotation.data[0] -= dx * mouseSensitivity;
            self.cameraRotation.data[1] -= dy * mouseSensitivity;
        }

        self.validateSeedTargetViewport(game);
        if (self.pickSeedTarget(x,y)) |cell| {
            if(std.mem.eql(u8,self.mobileFeedback,"Tap closer to a green + or use Seed colony")){self.mobileFeedback="";self.mobileFeedbackSeconds=0;}
            self.selectedPoint=cell;self.pointerOnPlanet=true;return;
        }
        const windowSize = game.window.getFramebufferSize();
        // Transform screen coordinates to Normalized Device Space coordinates
        const ndsX = 2 * x / @as(f32, @floatFromInt(windowSize.width)) - 1;
        const ndsY = 1 - 2 * y / @as(f32, @floatFromInt(windowSize.height));
        var cursorVector = za.Vec4.new(ndsX, ndsY, -1, 1);

        // 'unproject' the coordinates by using the inversed projection matrix
        const zFar = self.planet.radius * 5;
        const zNear = zFar / 10000;
        const projMatrix = Mat4.perspective(70, @as(f32, @floatFromInt(windowSize.width)) / @as(f32, @floatFromInt(windowSize.height)), zNear, zFar);
        cursorVector = projMatrix.inv().mulByVec4(cursorVector);

        // put to world space by multiplying by inverse of view matrix
        cursorVector.data[2] = -1;
        cursorVector.data[3] = 0; // we only want directions so set z and w
        const viewMatrix = Mat4.lookAt(self.cameraPos, self.getViewTarget(), Vec3.new(0, 0, 1));
        cursorVector = viewMatrix.inv().mulByVec4(cursorVector);
        const worldSpaceCursor = Vec3.new(cursorVector.x(), cursorVector.y(), cursorVector.z());
        //std.log.info("{d}", .{ worldSpaceCursor });

        const direction = worldSpaceCursor.norm();
        const distance = camera_math.sphereHit(self.cameraPos.data, direction.data, self.planet.radius) orelse {
            self.pointerOnPlanet = false;
            return;
        };
        self.pointerOnPlanet = true;
        const pos = self.cameraPos.add(direction.scale(distance));
        var closestPointDist: f32 = std.math.inf(f32);
        var closestPoint: usize = undefined;
        for (self.planet.transformedPoints, 0..) |point, i| {
            if (point.distance(pos) < closestPointDist) {
                closestPoint = i;
                closestPointDist = point.distance(pos);
            }
        }
        self.selectedPoint = closestPoint;
    }

    pub fn renderUI(self: *PlayState, game: *Game, renderer: *Renderer) void {
        const size = renderer.framebufferSize;
        const vg = renderer.vg;
        if (@import("builtin").target.cpu.arch == .wasm32) {
            self.renderMobileUI(game, renderer);
            return;
        }
        const pressed = game.window.getMouseButton(.left) == .press;
        const glfwCursorPos = game.window.getCursorPos();
        const cursorPos = Vec2.new(@as(f32, @floatCast(glfwCursorPos.xpos)), @as(f32, @floatCast(glfwCursorPos.ypos)));
        _ = cursorPos;

        {
            const barHeight = 50;
            vg.beginPath();
            vg.fillColor(nvg.rgbaf(1, 1, 1, 0.7));
            vg.rect(0, size.y() - barHeight, size.x(), barHeight);
            vg.fill();
        }

        {
            //var prng = std.rand.DefaultPrng.init(@bitCast(u64, std.time.milliTimestamp()));
            var prng = std.rand.DefaultPrng.init(0);
            const random = prng.random();
            if (!self.paused) {
                var meanTemperature: f32 = 0;
                var i: usize = 0;
                while (i < 1000) : (i += 1) {
                    const pointIdx = random.intRangeLessThanBiased(usize, 0, self.planet.temperature.len);
                    meanTemperature += self.planet.temperature[pointIdx];
                }
                meanTemperature /= 1000;
                self.meanTemperature = self.meanTemperature * 0.9 + meanTemperature * 0.1;
            }
            vg.textAlign(.{ .horizontal = .left, .vertical = .middle });
            vg.fontSize(20.0);
            if (ui.coloredLabel(vg, game, "mean-temperature", "{d:.1}°C", .{self.meanTemperature - 273.15}, 150, size.y() - 25, nvg.rgba(255, 255, 255, 255))) {
                if (pressed) {
                    self.showPlanetControl = true;
                }
            }

            ui.label(vg, game, "{d:.1} ups", .{1.0 / self.averageUpdateTime}, 250, size.y() - 25);

            vg.textAlign(.{ .horizontal = .center, .vertical = .middle });
            ui.label(vg, game, "Year {d:.1}", .{self.gameTime / 86400 / 365}, size.x() / 2, size.y() - 25);
        }

        if (self.showPlanetControl) {
            const panelWidth = 300;
            const panelHeight = 280;

            self.showPlanetControl = ui.window(vg, game, "planet-control-window", panelWidth, panelHeight);
            defer ui.endWindow(vg);

            vg.textAlign(.{ .horizontal = .center, .vertical = .top });
            ui.label(vg, game, "Solar Constant", .{}, 90, 0);
            ui.label(vg, game, "{d} W/m²", .{self.solarConstant}, 90, 30);
            if (ui.button(vg, game, "solar-constant-minus", 0, 30, 20, 20, "-")) {
                self.solarConstant = @max(0, self.solarConstant - 100);
            }
            if (ui.button(vg, game, "solar-constant-plus", 160, 30, 20, 20, "+")) {
                self.solarConstant = @min(self.solarConstant + 100, 5000);
            }

            if (ui.button(vg, game, "clear-water", panelWidth / 2 - (170 / 2), 130, 170, 40, "Clear all water")) {
                self.debug_clearWater = true;
            }
            if (ui.button(vg, game, "deluge", panelWidth / 2 - (170 / 2), 180, 170, 40, "Deluge")) {
                self.debug_deluge = true;
            }

            // if (pressed and !(cursorPos.x() >= panelX and cursorPos.x() < panelX + panelWidth and cursorPos.y() >= panelY and cursorPos.y() < panelY + panelHeight)) {
            //     self.showPlanetControl = false;
            // }
        }

        if (self.showPointDetails) {
            const panelWidth = 350;
            const panelHeight = 200;
            const selectedPoint = self.clickedPoint;
            const RH = Planet.getRelativeHumidity(self.planet.getSubstanceDivider(), self.planet.temperature[selectedPoint], self.planet.waterVaporMass[selectedPoint]);

            self.showPointDetails = ui.window(vg, game, "point-details", panelWidth, panelHeight);
            defer ui.endWindow(vg);
            vg.textAlign(.{ .horizontal = .left, .vertical = .top });
            ui.label(vg, game, "Altitude: {d:.2} km", .{self.planet.elevation[selectedPoint] - self.planet.radius}, 90, 0);
            ui.label(vg, game, "Temperature: {d:.1}°C", .{self.planet.temperature[selectedPoint] - 273.15}, 90, 20);
            ui.label(vg, game, "Humidity: {d:.0}%", .{RH * 100}, 90, 40);
        }

        if (self.showEscapeMenu) {
            vg.beginPath();
            vg.fillColor(nvg.rgbaf(0, 0, 0, 0.4));
            vg.rect(0, 0, size.x(), size.y());
            vg.fill();

            const panelWidth = 200;
            const panelHeight = 300;
            const panelX = size.x() / 2 - panelWidth / 2;
            const panelY = size.y() / 2 - panelHeight / 2;

            vg.beginPath();
            vg.fillColor(nvg.rgbf(0.8, 0.8, 0.8));
            vg.rect(panelX, panelY, panelWidth, panelHeight);
            vg.fill();

            if (ui.button(vg, game, "save-game", panelX + panelWidth / 2 - 170 / 2, panelY + 10, 170, 40, "Save")) {
                self.defer_saveGame = true;
            }
            if (ui.button(vg, game, "exit-game", panelX + panelWidth / 2 - 170 / 2, panelY + 80, 170, 40, "Exit")) {
                game.setState(MainMenuState);
            }
        }

        const renderHud = !self.showEscapeMenu;
        if (renderHud) {
            // TODO: in addition to that, for tool selection use a circle that spawns under the cursor when you click right mouse
            const panelWidth = 400;
            const panelHeight = 70;
            const panelX = 10;
            const panelY = 10;

            const colorGradBottom = nvg.lerpRGBA(nvg.rgba(255, 255, 255, 100), nvg.rgba(0, 0, 0, 100), 1 - 0.2);
            vg.beginPath();
            vg.fillPaint(vg.linearGradient(panelX - 5, panelY - 5, panelX + panelWidth + 10, panelY + panelHeight + 10, nvg.rgb(255, 255, 255), colorGradBottom));
            vg.roundedRect(panelX - 5, panelY - 5, panelWidth + 10, panelHeight + 10, 10);
            vg.fill();

            if (ui.toolButton(vg, game, "no-tool", panelX, panelY, 50, 50, renderer.textureCache.get("ui/no-tool"))) {
                self.selectedTool = .None;
            }
            if (ui.toolButton(vg, game, "emit-water", panelX + 70, panelY, 50, 50, renderer.textureCache.get("ui/emit-water"))) {
                self.selectedTool = .EmitWater;
            }
            if (ui.toolButton(vg, game, "drain-water", panelX + 140, panelY, 50, 50, renderer.textureCache.get("ui/drain-water"))) {
                self.selectedTool = .DrainWater;
            }
            if (ui.toolButton(vg, game, "place-vegetation", panelX + 210, panelY, 50, 50, renderer.textureCache.get("ui/place-vegetation"))) {
                self.selectedTool = .PlaceVegetation;
            }
            if (ui.toolButton(vg, game, "raise-terrain", panelX + 280, panelY, 50, 50, renderer.textureCache.get("ui/raise-terrain"))) {
                self.selectedTool = .RaiseTerrain;
            }
            if (ui.toolButton(vg, game, "lower-terrain", panelX + 350, panelY, 50, 50, renderer.textureCache.get("ui/lower-terrain"))) {
                self.selectedTool = .LowerTerrain;
            }
            if (ui.toolButton(vg, game, "place-vegetation", panelX + 420, panelY, 50, 50, renderer.textureCache.get("ui/place-vegetation"))) {
                self.selectedTool = .PlaceLife;
            }
        }

        if (self.debug_showMoreInfo) {
            if (ui.button(vg, game, "reload-shaders", 20, 210, 170, 40, "Reload shaders")) {
                renderer.reloadShaders() catch {};
            }

            vg.textAlign(.{ .horizontal = .left, .vertical = .top });
            const baseX = size.x() - 350;
            var baseY = size.y() - 290;
            const point = self.selectedPoint;
            const planet = self.planet;

            const RH = Planet.getRelativeHumidity(planet.getSubstanceDivider(), planet.temperature[point], planet.waterVaporMass[point]);
            const meanPointArea = planet.getMeanPointArea();

            ui.label(vg, game, "Point #{d}", .{point}, baseX, baseY);
            baseY += 30;

            ui.label(vg, game, "Point Area: {d}km²", .{@floor(planet.getMeanPointArea() / 1_000_000)}, baseX, baseY);
            baseY += 20;

            ui.label(vg, game, "Altitude: {d:.1} km", .{planet.elevation[point] - planet.radius}, baseX, baseY);
            baseY += 20;

            ui.label(vg, game, "Temperature: {d:.3}°C", .{planet.temperature[point] - 273.15}, baseX, baseY);
            baseY += 20;

            ui.label(vg, game, "Humidity: {d:.1}%", .{RH * 100}, baseX, baseY);
            baseY += 20;

            ui.label(vg, game, "Water Mass: {:.1} kg", .{planet.waterMass[point] * 1_000_000_000}, baseX, baseY);
            baseY += 20;

            // The units are given in centimeters, which is the equivalent amount of water that could be produced if all the water vapor in the column were to condense
            // similar to https://earthobservatory.nasa.gov/global-maps/MYDAL2_M_SKY_WV
            ui.label(vg, game, "Water Vapor: {d:.1} cm", .{planet.waterVaporMass[point] * 1_000_000_000 / planet.getMeanPointArea() * planet.getKmPerWaterMass() * 100_000}, baseX, baseY);
            baseY += 20;

            ui.label(vg, game, "Vapor Mass: {d:.1} kg/m²", .{planet.waterVaporMass[point] * 1_000_000_000 / planet.getMeanPointArea()}, baseX, baseY);
            baseY += 20;

            ui.label(vg, game, "Vapor Pressure: {d:.0} / {d:.0} Pa", .{
                Planet.getPartialPressure(planet.getSubstanceDivider(), planet.temperature[point], planet.waterVaporMass[point]),
                Planet.getEquilibriumVaporPressure(planet.temperature[point]),
            }, baseX, baseY);
            baseY += 20;

            ui.label(vg, game, "Air Speed: {d:.1} km/h", .{planet.airVelocity[point].length() * 3600}, baseX, baseY);
            baseY += 20;

            ui.label(vg, game, "Air Position Error: {d:.1}, {d:.1} km", .{ planet.airPositionError[point].x() * planet.radius, planet.airPositionError[point].y() * planet.radius }, baseX, baseY);
            baseY += 20;

            ui.label(vg, game, "Air Pressure: {d:.2} bar", .{planet.getAirPressureOfPoint(point) / 100_000}, baseX, baseY);
            baseY += 20;

            ui.label(vg, game, "CO2 Mass: {d:.1} kg/m²", .{planet.averageCarbonDioxideMass * 1_000_000_000 / meanPointArea}, baseX, baseY);
            baseY += 20;

            ui.label(vg, game, "O2 Mass: {d:.1} kg/m²", .{planet.averageOxygenMass * 1_000_000_000 / meanPointArea}, baseX, baseY);
            baseY += 20;
        }

        if (ui.button(vg, game, "game-pause", size.x() - 70, 30, 40, 40, if (self.paused) ">" else "||")) {
            self.paused = !self.paused;
        }

        {
            vg.textAlign(.{ .horizontal = .center, .vertical = .top });
            ui.label(vg, game, "{}", .{std.fmt.fmtDuration(@as(u64, @intFromFloat(self.gameTime)) * std.time.ns_per_s)}, size.x() / 2, 10);
        }

        {
            vg.textAlign(.{ .horizontal = .center, .vertical = .top });
            ui.label(vg, game, "Game Speed", .{}, size.x() - 80, 130);
            ui.label(vg, game, "{}/s", .{std.fmt.fmtDuration(@as(u64, @intFromFloat(self.timeScale)) * std.time.ns_per_s)}, size.x() - 90, 150);
            if (ui.button(vg, game, "game-speed-minus", size.x() - 150, 150, 20, 20, "-")) {
                self.timeScale = @max(1.0, self.timeScale - 3600 * 3);
            }
            if (ui.button(vg, game, "game-speed-plus", size.x() - 25, 150, 20, 20, "+")) {
                if (self.timeScale < 190000 or true) {
                    if (self.timeScale == 1) self.timeScale = 0;
                    self.timeScale = @min(200_000_000, self.timeScale + 3600 * 3);
                }
            }
        }
    }

    /// Explicit read-only local framing; never follows life automatically.
    pub fn fitLivingCluster(self:*PlayState,width:f32,height:f32) bool {
        return self.fitLivingClusterResult(width,height)==1;
    }

    /// Stable web result codes: 1 fit, 0 no nearby life; -2 mode, -3 viewport,
    /// -4 polar view, -5 invalid geometry, -6 cluster too wide. -1 is no world.
    pub fn fitLivingClusterResult(self:*PlayState,width:f32,height:f32) i32 {
        if(self.planet.worldMode!=.origin)return -2;
        const start=self.planet.getNearestPointTo(self.targetCameraPos);
        const fitted=@import("../life_camera.zig").fitDetailed(&self.planet,start,width,height) catch |err| {
            self.mobileFeedbackSeconds=4;
            self.mobileFeedback=switch(err){
                error.NoNearbyLife=>"No nearby connected life to fit",
                error.ViewportTooSmall=>"More canvas space needed to fit life",
                error.PolarView=>"Fit unavailable near the poles; navigate manually",
                error.InvalidGeometry=>"Fit unavailable for this view; camera unchanged",
                error.TooWide=>"Connected life too wide to fit; zoom out manually",
            };
            return switch(err){error.NoNearbyLife=>0,error.ViewportTooSmall=>-3,error.PolarView=>-4,error.InvalidGeometry=>-5,error.TooWide=>-6};
        };
        self.targetCameraPos=Vec3.new(fitted.direction[0],fitted.direction[1],fitted.direction[2]);
        self.setOrbitDistance(fitted.distance,true);
        self.cameraGroundPoint=self.planet.getNearestPointTo(self.cameraPos);
        self.mobileFeedback=if(fitted.truncated) "Fitted bounded nearby life; distant colonies excluded" else "Fitted nearby connected life";
        self.mobileFeedbackSeconds=4;
        return 1;
    }

    pub fn watchLife(self: *PlayState) void {
        self.watchLifeView = true;
        self.selectedTool = .None;
        self.seedTargets.count = 0;
        self.showEscapeMenu = false;
        self.showPlanetControl = false;
        self.showPointDetails = false;
    }

    fn mobileToolbarBottom(self: *const PlayState, width: f32) f32 {
        return if (self.watchLifeView) 56 else if (width >= 650) 112 else 166;
    }

    fn mobilePointerOnUI(self: *PlayState, game: *Game) bool {
        if (@import("builtin").target.cpu.arch != .wasm32) return false;
        if (self.showEscapeMenu or self.showPlanetControl or self.showPointDetails) return true;
        const p = game.window.getCursorPos();
        const size = game.renderer.framebufferSize;
        return p.ypos < self.mobileToolbarBottom(size.x()) or p.ypos > size.y() - 84;
    }

    /// Feedback depicts only cells changed by a successful explicit intervention.
    /// Real-time, monotonic fade: no repeated lightning flashes or full-screen flash.
    fn renderGodEffects(self: *PlayState, vg: nvg, vp: Mat4, width: f32, height: f32, toolBottom: f32) void {
        const receipt = self.godReceipt orelse return;
        const visuals = @import("../god_visuals.zig");
        if (!visuals.visible(receipt,self.godEffectSeconds)) return;
        const alpha = visuals.fade(self.godEffectSeconds);
        const progress = 1-alpha;
        for (receipt.affected[0..receipt.count]) |delta| {
            if (delta.cell>=self.planet.transformedPoints.len) continue;
            if (receipt.kind==.wave and delta.water_mass==0) continue;
            if (receipt.kind==.lightning and delta.temperature_k<=0) continue;
            const p=self.planet.transformedPoints[delta.cell];
            if (p.dot(self.cameraPos.sub(p))<=0) continue;
            const clip=vp.mulByVec4(za.Vec4.new(p.x(),p.y(),p.z(),1));
            if (clip.w()<=0) continue;
            const x=(clip.x()/clip.w()+1)*width/2;
            const y=(1-clip.y()/clip.w())*height/2;
            if (x<8 or x>width-8 or y<toolBottom+18 or y>height-100) continue;
            if (receipt.kind==.wave) {
                const radius=12+progress*30;
                vg.beginPath();vg.ellipse(x,y,radius,radius*0.55);
                vg.strokeColor(nvg.rgba(8,53,76,@intFromFloat(alpha*220)));vg.strokeWidth(6);vg.stroke();
                vg.strokeColor(nvg.rgba(117,238,255,@intFromFloat(alpha*240)));vg.strokeWidth(2.5);vg.stroke();
                vg.beginPath();vg.ellipse(x,y,radius*0.62,radius*0.34);
                vg.strokeColor(nvg.rgba(164,248,255,@intFromFloat(alpha*170)));vg.strokeWidth(1.5);vg.stroke();
            } else {
                vg.beginPath();vg.circle(x,y,14+progress*12);
                vg.fillColor(nvg.rgba(255,191,72,@intFromFloat(alpha*55)));vg.fill();
                // Fixed bolt geometry does not jitter or strobe between frames.
                const top=@max(toolBottom+4,y-64);
                vg.beginPath();vg.moveTo(x+9,top);vg.lineTo(x-7,y-37);vg.lineTo(x+6,y-32);vg.lineTo(x-3,y-12);vg.lineTo(x,y);
                vg.strokeColor(nvg.rgba(102,63,20,@intFromFloat(alpha*230)));vg.strokeWidth(7);vg.stroke();
                vg.strokeColor(nvg.rgba(255,245,169,@intFromFloat(alpha*255)));vg.strokeWidth(3);vg.stroke();
            }
        }
    }

    fn propaguleScreen(self:*PlayState,cell:usize,vp:Mat4,width:f32,height:f32,top:f32) ?Vec2 {
        if(cell>=self.planet.transformedPoints.len)return null;
        const p=self.planet.transformedPoints[cell];if(p.dot(self.cameraPos.sub(p))<=0)return null;
        const clip=vp.mulByVec4(Vec4.new(p.x(),p.y(),p.z(),1));if(clip.w()<=0)return null;
        const x=(clip.x()/clip.w()+1)*width/2;const y=(1-clip.y()/clip.w())*height/2;
        if(x<14 or x>width-14 or y<top+20 or y>height-116)return null;
        return Vec2.new(x,y);
    }
    /// Cyan diamonds are real arrivals, amber crosses actual tracked colony losses.
    /// Neither denotes established life; green + targets retain their own meaning.
    fn renderPropaguleFeedback(self:*PlayState,vg:nvg,vp:Mat4,width:f32,height:f32,top:f32) void {
        if(self.planet.worldMode!=.origin or self.displayMode!=.Normal)return;
        const tracker=&self.planet.propaguleFeedback;
        const latest=tracker.next_serial-1;
        if(latest<self.propaguleVisuals.last_serial)self.propaguleVisuals=.{};
        var serial=@max(self.propaguleVisuals.last_serial+1,if(latest>31)latest-31 else 1);
        while(serial<=latest):(serial+=1){
            const event=tracker.events[@intCast((serial-1)%tracker.events.len)];
            if(event.serial==serial and self.propaguleScreen(event.cell,vp,width,height,top)!=null)self.propaguleVisuals.take(event);
        }
        self.propaguleVisuals.last_serial=latest;
        var shown=false;
        for(self.propaguleVisuals.pulses)|pulse|{
            if(pulse.remaining<=0)continue;
            const pos=self.propaguleScreen(pulse.event.cell,vp,width,height,top) orelse continue;
            const x=pos.x();const y=pos.y();const alpha=pulse.remaining/@import("../propagule_visuals.zig").duration;
            const r=6+(1-alpha)*7;shown=true;
            if(pulse.event.kind==.arrival){
                if(self.propaguleScreen(pulse.event.from,vp,width,height,top))|from|{
                    if(from.distance(pos)<160){vg.beginPath();vg.moveTo(from.x(),from.y());vg.lineTo(x,y);vg.strokeColor(nvg.rgba(107,227,255,@intFromFloat(alpha*95)));vg.strokeWidth(1.5);vg.stroke();}
                }
                vg.beginPath();vg.moveTo(x,y-r);vg.lineTo(x+r,y);vg.lineTo(x,y+r);vg.lineTo(x-r,y);vg.closePath();
                vg.fillColor(nvg.rgba(15,59,78,@intFromFloat(alpha*180)));vg.fill();
                vg.strokeColor(nvg.rgba(117,237,255,@intFromFloat(alpha*255)));vg.strokeWidth(2.5);vg.stroke();
                vg.beginPath();vg.circle(x,y,2);vg.fillColor(nvg.rgba(210,255,255,@intFromFloat(alpha*255)));vg.fill();
            }else{
                vg.beginPath();vg.moveTo(x-r*0.6,y-r*0.6);vg.lineTo(x+r*0.6,y+r*0.6);vg.moveTo(x+r*0.6,y-r*0.6);vg.lineTo(x-r*0.6,y+r*0.6);
                vg.strokeColor(nvg.rgba(71,34,9,@intFromFloat(alpha*230)));vg.strokeWidth(6);vg.stroke();
                vg.strokeColor(nvg.rgba(255,185,93,@intFromFloat(alpha*255)));vg.strokeWidth(2.5);vg.stroke();
            }
        }
        if(shown){
            vg.beginPath();vg.roundedRect(8,height-113,@min(width-16,315),22,5);vg.fillColor(nvg.rgba(8,25,37,215));vg.fill();
            vg.fontFace("sans-serif");vg.fontSize(12);vg.textAlign(.{.horizontal=.left,.vertical=.middle});vg.fillColor(nvg.rgb(193,230,240));
            _=vg.text(15,height-102,"Diamond: arrival · X: tracked colony lost");
        }
    }

    /// Read-only Seed map: targets are actual cell centers where the engine can
    /// seed now, including slot/resource limits, not a water-color approximation.
    fn renderSeedZones(self: *PlayState, vg: nvg, vp: Mat4, width: f32, height: f32, toolBottom: f32) void {
        self.seedTargets.count=0;
        self.seedTargetWidth=width;self.seedTargetHeight=height;self.seedTargetWorld=@intFromPtr(self.planet.waterMass.ptr);
        if (self.planet.worldMode != .origin or self.selectedTool != .PlaceVegetation or self.displayMode != .Normal) return;
        for (self.planet.transformedPoints, 0..) |p, index| {
            if (self.seedTargets.count == 64) break;
            if (p.dot(self.cameraPos.sub(p)) <= 0) continue;
            const clip = vp.mulByVec4(za.Vec4.new(p.x(), p.y(), p.z(), 1));
            if (clip.w() <= 0) continue;
            const x = (clip.x() / clip.w() + 1) * width / 2;
            const y = (1 - clip.y() / clip.w()) * height / 2;
            if (x < 18 or x > width - 18 or y < toolBottom + 22 or y > height - 108) continue;
            if (self.planet.seedEligibility(index) != .eligible) continue;
            if (!self.seedTargets.add(.{.cell=index,.x=x,.y=y},true)) continue;
            // Dark rim keeps this actionable target visible on land and water.
            vg.beginPath(); vg.circle(x,y,13); vg.fillColor(nvg.rgba(18,94,67,125)); vg.fill();
            vg.strokeColor(nvg.rgba(3,24,26,235)); vg.strokeWidth(5); vg.stroke();
            vg.strokeColor(nvg.rgb(132,255,182)); vg.strokeWidth(2.5); vg.stroke();
            vg.beginPath(); vg.moveTo(x-4,y); vg.lineTo(x+4,y); vg.moveTo(x,y-4); vg.lineTo(x,y+4);
            vg.strokeColor(nvg.rgb(202,255,216)); vg.strokeWidth(2); vg.stroke();
        }
        if (self.selectedPoint >= self.planet.transformedPoints.len) return;
        const p = self.planet.transformedPoints[self.selectedPoint];
        if (p.dot(self.cameraPos.sub(p)) <= 0) return;
        const clip = vp.mulByVec4(za.Vec4.new(p.x(),p.y(),p.z(),1));
        if (clip.w() <= 0) return;
        const x = (clip.x()/clip.w()+1)*width/2;
        const y = (1-clip.y()/clip.w())*height/2;
        if (x<22 or x>width-22 or y<toolBottom+24 or y>height-110) return;
        const valid = self.planet.seedEligibility(self.selectedPoint)==.eligible;
        if(valid) _=self.seedTargets.add(.{.cell=self.selectedPoint,.x=x,.y=y},false);
        vg.beginPath(); vg.circle(x,y,20); vg.strokeColor(nvg.rgba(3,24,26,240)); vg.strokeWidth(6); vg.stroke();
        vg.strokeColor(if(valid) nvg.rgb(132,255,182) else nvg.rgb(255,143,126)); vg.strokeWidth(3); vg.stroke();
        if (!valid) {
            vg.beginPath(); vg.moveTo(x-6,y-6); vg.lineTo(x+6,y+6); vg.moveTo(x+6,y-6); vg.lineTo(x-6,y+6); vg.strokeWidth(3); vg.stroke();
        }
    }

    /// A sprout represents a real vegetated terrain population, not one plant.
    /// Close view scans <=512 neighbours; globe view scans real living cells.
    /// Allocation-free, de-cluttered, <=64 glyphs in either view.
    fn renderSprouts(self: *PlayState, vg: nvg, vp: Mat4, width: f32, height: f32, toolBottom: f32) void {
        self.visibleSprouts = 0;
        self.sproutCandidates = 0;
        if (!biology_visuals.showSprouts(self.cameraDistance, self.planet.radius, self.displayMode == .Normal)) return;
        var candidates: [512]usize = undefined;
        var screenPositions: [64]Vec2 = undefined;
        candidates[0] = self.cameraGroundPoint;
        const wide = self.cameraDistance >= self.planet.radius * 1.28;
        const lod = biology_visuals.markerScale(self.cameraDistance,self.planet.radius);
        var count: usize = if(wide) self.planet.transformedPoints.len else 1;
        var cursor: usize = 0;
        while (cursor < count and self.visibleSprouts < screenPositions.len) : (cursor += 1) {
            const index = if(wide) cursor else candidates[cursor];
            self.sproutCandidates += 1;
            if (!wide) for (self.planet.getNeighbours(index)) |neighbour| {
                if (count == candidates.len) break;
                var known = false;
                for (candidates[0..count]) |candidate| { if (candidate == neighbour) { known = true; break; } }
                if (!known) { candidates[count] = neighbour; count += 1; }
            };
            const origin = self.planet.worldMode == .origin;
            const biomass = if (origin) Microbes.biomass(self.planet.microbeCells[index]) else self.planet.vegetation[index];
            if (origin) { if (biomass < 0.001) continue; } else if (biomass < 0.08 or self.planet.waterMass[index] * self.planet.getKmPerWaterMass() > 0.0005) continue;
            const p = self.planet.transformedPoints[index];
            if (p.dot(self.cameraPos.sub(p)) <= 0) continue;
            const clip = vp.mulByVec4(za.Vec4.new(p.x(), p.y(), p.z(), 1));
            if (clip.w() <= 0) continue;
            const x = (clip.x() / clip.w() + 1) * width / 2;
            const y = (1 - clip.y() / clip.w()) * height / 2;
            const size = (if (origin) 13 + 10 * @sqrt(std.math.clamp(biomass, 0, 1)) else 12 + biology_visuals.sproutSize(biomass)) * lod;
            if (x < size + 4 or x > width - size - 4 or y < toolBottom + size * 2 or y > height - 90) continue;
            const screen = Vec2.new(x,y);
            // A living cell is an area, not a floating icon. Render its footprint
            // even when the nearby morphology glyph is suppressed by decluttering.
            // Adjacent occupied cells merge visually; empty terrain stays untouched.
            const cover = std.math.clamp(biomass, 0, 1);
            const patch = (10 + 13 * @sqrt(cover)) * lod;
            vg.beginPath(); vg.fillColor(nvg.rgba(50,160,112, @intFromFloat(35 + 35 * cover)));
            vg.ellipse(x,y+2*lod,patch,patch*0.57); vg.fill();
            vg.beginPath(); vg.fillColor(nvg.rgba(91,211,132, @intFromFloat(45 + 40 * cover)));
            vg.ellipse(x-4*lod,y,patch*0.65,patch*0.32);
            vg.ellipse(x+6*lod,y+3*lod,patch*0.55,patch*0.28); vg.fill();
            var crowded = false;
            for (screenPositions[0..self.visibleSprouts]) |prior| { if (screen.distance(prior) < @max(14,38*lod)) { crowded = true; break; } }
            if (crowded) continue;
            screenPositions[self.visibleSprouts] = screen;
            self.visibleSprouts += 1;
            vg.save(); vg.translate(x,y); vg.scale(lod,lod);
            // Soft contact shadow grounds the crisp silhouette in its living patch.
            vg.beginPath(); vg.fillColor(nvg.rgba(8,35,29,125)); vg.ellipse(0,2,13,4); vg.fill();
            if (origin) {
                var dominant: Microbes.Cohort = .{};
                for(self.planet.microbeCells[index].cohorts) |co| {
                    if(co.biomass>0 and (co.support_mass>dominant.support_mass or (co.support_mass==dominant.support_mass and co.biomass>dominant.biomass))) dominant=co;
                }
                const color=biology_visuals.lineageColor(dominant.optimum);
                const form = @tagName(Microbes.producerForm(dominant));
                // Dense real biomass reads as a colony rather than a single sticker.
                // Smaller shoots use the same inherited morphology, not extra species.
                if (biomass > 0.3 and lod > 0.75) {
                    vg.save(); vg.translate(-13,2); vg.scale(0.48,0.48); if(self.blenderAtlas) |atlas| renderBlenderForm(vg,form,color,atlas) else renderProducerGlyph(vg,form,color); vg.restore();
                    vg.save(); vg.translate(12,4); vg.scale(0.58,0.58); if(self.blenderAtlas) |atlas| renderBlenderForm(vg,form,color,atlas) else renderProducerGlyph(vg,form,color); vg.restore();
                }
                if(self.blenderAtlas) |atlas| renderBlenderForm(vg,form,color,atlas) else renderProducerGlyph(vg,form,color);
                if (biology_visuals.hasFed(self.planet.microbeCells[index].cohorts)) {
                    vg.beginPath(); vg.fillColor(nvg.rgb(255,191,89)); vg.circle(12,0,3); vg.fill();
                }
            } else {
                const color=biology_visuals.lineageColor(self.planet.plantTraits[index].optimum);
                renderProducerGlyph(vg,"branching",color);
            }
            vg.restore();
        }
    }

    // Only for a freshly created atlas, before cache insertion / NanoVG registration.
    // Cached or registered textures retain their existing renderer ownership.
    fn discardUnregisteredAtlas(texture:*Texture) void {
        std.debug.assert(texture.nvgHandle == null);
        gl.deleteTextures(1,&texture.texture);
        texture.texture=0;
    }

    fn loadAquaticAtlas(renderer:*Renderer,vg:nvg) ?nvg.Image {
        const key="aquatic-forms-atlas";
        if(renderer.textureCache.cache.getPtr(key)) |texture| return texture.tryToVgImage(vg) catch null;
        var texture=Texture.createFromPath(renderer.textureCache.cache.allocator,"assets/aquatic-forms-atlas.png") catch |err| {
            std.log.warn("Aquatic atlas unavailable ({s}); retaining vector forms",.{@errorName(err)});return null;
        };
        if(texture.width!=576 or texture.height!=384){discardUnregisteredAtlas(&texture);std.log.warn("Aquatic atlas dimensions invalid; retaining vector forms",.{});return null;}
        renderer.textureCache.cache.put(key,texture) catch {discardUnregisteredAtlas(&texture);return null;};
        return renderer.textureCache.cache.getPtr(key).?.tryToVgImage(vg) catch null;
    }

    fn renderBlenderForm(vg:nvg,form:[]const u8,color:[3]u8,atlas:nvg.Image) void {
        const names=[_][]const u8{"mat","cushion","rosette","ribbon","branching","canopy"};
        var id:usize=0;for(names,0..) |name,i|{if(std.mem.eql(u8,name,form)){id=i;break;}}
        const tile:f32=36;const left:f32=-18;const top:f32=-29;
        vg.beginPath();vg.rect(left,top,tile,tile);
        var paint=vg.imagePattern(left-@as(f32,@floatFromInt(id%3))*tile,top-@as(f32,@floatFromInt(id/3))*tile,tile*3,tile*2,0,atlas,1);
        // NanoVG image shader multiplies by inner_color; retain real thermal
        // lineage palette without extra textures or an invented form taxonomy.
        paint.inner_color=nvg.rgb(color[0],color[1],color[2]);paint.outer_color=paint.inner_color;
        vg.fillPaint(paint);vg.fill();
    }

    /// Crisp vector silhouettes for expressed population morphology, not individual trees.
    fn renderProducerGlyph(vg:nvg, form:[]const u8, color:[3]u8) void {
        const leaf=nvg.rgb(color[0],color[1],color[2]);
        const edge=nvg.rgb(12,49,44);
        vg.strokeColor(edge); vg.strokeWidth(2.2); vg.fillColor(leaf);
        if(std.mem.eql(u8,form,"mat")) {
            vg.beginPath();vg.ellipse(-5,-3,9,5);vg.ellipse(6,-6,8,5);vg.fill();vg.stroke();
            vg.beginPath();vg.fillColor(nvg.rgb(214,255,221));vg.circle(-6,-5,1.7);vg.circle(5,-8,1.7);vg.fill();return;
        }
        if(std.mem.eql(u8,form,"cushion")) {
            vg.beginPath();vg.circle(-8,-7,7);vg.circle(0,-12,9);vg.circle(9,-6,7);vg.fill();vg.stroke();
        } else if(std.mem.eql(u8,form,"rosette")) {
            var i:usize=0;while(i<7):(i+=1){const angle=@as(f32,@floatFromInt(i))*6.283185/7;
                vg.beginPath();vg.moveTo(0,-7);vg.lineTo(@cos(angle)*16-@sin(angle)*4,-7+@sin(angle)*14+@cos(angle)*4);vg.lineTo(@cos(angle)*18,-7+@sin(angle)*16);vg.closePath();vg.fill();vg.stroke();}
        } else if(std.mem.eql(u8,form,"ribbon")) {
            var i:i32=-1;while(i<=1):(i+=1){const x=@as(f32,@floatFromInt(i))*7;
                vg.beginPath();vg.moveTo(x,0);vg.bezierTo(x-9,-12,x+10,-20,x,-29);vg.bezierTo(x+17,-17,x+2,-8,x+4,0);vg.closePath();vg.fill();vg.stroke();}
        } else if(std.mem.eql(u8,form,"canopy")) {
            vg.beginPath();vg.moveTo(-2,0);vg.lineTo(-3,-24);vg.lineTo(3,-24);vg.lineTo(2,0);vg.closePath();vg.fillColor(nvg.rgb(178,139,87));vg.fill();vg.stroke();
            vg.fillColor(leaf);vg.beginPath();vg.circle(-9,-24,8);vg.circle(0,-30,10);vg.circle(10,-23,8);vg.fill();vg.stroke();
        } else {
            vg.beginPath();vg.moveTo(0,0);vg.lineTo(0,-32);vg.strokeColor(edge);vg.strokeWidth(4);vg.stroke();
            var i:usize=0;while(i<3):(i+=1){const y=-8-@as(f32,@floatFromInt(i))*8; const w=13-@as(f32,@floatFromInt(i))*3;
                vg.strokeWidth(2);vg.beginPath();vg.moveTo(0,y+4);vg.bezierTo(-w,y+5,-w-4,y-5,-w,y-7);vg.bezierTo(-3,y-9,-1,y,0,y+4);vg.moveTo(0,y);vg.bezierTo(w,y+1,w+3,y-9,w,y-11);vg.bezierTo(2,y-9,1,y-4,0,y);vg.fill();vg.stroke();}
        }
        // A small highlight preserves readability without blurred sprite textures.
        vg.beginPath();vg.fillColor(nvg.rgba(230,255,223,220));vg.circle(-3,-12,1.7);vg.fill();
    }

    fn mobileDetailLabel(vg: nvg, game: *Game, comptime fmt: []const u8, args: anytype, x: f32, y: f32, available: f32) void {
        _ = game;
        var buf: [240]u8 = undefined;
        const text = std.fmt.bufPrint(&buf, fmt, args) catch "";
        vg.textAlign(.{ .horizontal = .left, .vertical = .top });
        vg.fontSize(18); vg.fontFace("sans-serif"); vg.fillColor(nvg.rgb(235,242,250));
        var bounds: [4]f32 = undefined;
        _ = vg.textBounds(0, 0, text, &bounds);
        const textWidth = bounds[2] - bounds[0];
        if (textWidth > available) vg.fontSize(18 * available / textWidth);
        _ = vg.text(x, y, text);
    }

    fn renderWatchLegend(vg:nvg,width:f32,y:f32) void {
        vg.save();defer vg.restore();
        vg.fontFace("sans-serif");vg.fontSize(12);vg.textAlign(.{.horizontal=.left,.vertical=.middle});
        var a:[4]f32=undefined;var b:[4]f32=undefined;
        _=vg.textBounds(0,0,"paid arrival",&a);_=vg.textBounds(0,0,"tracked loss (not all deaths)",&b);
        const first=a[2]-a[0];const second=b[2]-b[0];const lossX=12+first+16;
        const total=lossX+12+second;
        const scale=@min(@as(f32,1),(width-20)/total);
        vg.translate(10,y);vg.scale(scale,scale);
        vg.beginPath();vg.moveTo(4,-4);vg.lineTo(8,0);vg.lineTo(4,4);vg.lineTo(0,0);vg.closePath();
        vg.strokeWidth(1.5);vg.strokeColor(nvg.rgb(117,237,255));vg.stroke();
        vg.fillColor(nvg.rgb(190,214,232));_=vg.text(12,0,"paid arrival");
        vg.beginPath();vg.moveTo(lossX,-4);vg.lineTo(lossX+8,4);vg.moveTo(lossX+8,-4);vg.lineTo(lossX,4);
        vg.strokeColor(nvg.rgb(255,185,91));vg.stroke();
        _=vg.text(lossX+12,0,"tracked loss (not all deaths)");
    }

    fn renderMobileUI(self: *PlayState, game: *Game, renderer: *Renderer) void {
        const vg = renderer.vg;
        if(!self.blenderAtlasAttempted){self.blenderAtlasAttempted=true;self.blenderAtlas=loadAquaticAtlas(renderer,vg);}
        const size = renderer.framebufferSize;
        const width = size.x();
        const height = size.y();
        const toolBottom = self.mobileToolbarBottom(width);
        // Map markers represent actual living rabbits, not decorative sprites.
        // The original 3D models are still drawn; markers remain legible at planetary scale.
        const projection = Mat4.perspective(70, width / height, self.planet.radius * 5 / 10000, self.planet.radius * 5);
        const view = Mat4.lookAt(self.cameraPos, self.getViewTarget(), Vec3.new(0, 0, 1));
        const vp = projection.mul(view);
        self.renderSeedZones(vg, vp, width, height, toolBottom);
        self.renderSprouts(vg, vp, width, height, toolBottom);
        self.renderPropaguleFeedback(vg,vp,width,height,toolBottom);
        self.renderGodEffects(vg, vp, width, height, toolBottom);
        // Screen-space selection only; not a representation of brush radius.
        if (self.pointerOnPlanet and !self.cameraInputBlocked() and !(self.planet.worldMode == .origin and self.selectedTool == .PlaceVegetation)) {
            const p = self.planet.transformedPoints[self.selectedPoint];
            const clip = vp.mulByVec4(za.Vec4.new(p.x(),p.y(),p.z(),1));
            if (clip.w()>0 and p.dot(self.cameraPos.sub(p))>0) {
                const x=(clip.x()/clip.w()+1)*width/2;
                const y=(1-clip.y()/clip.w())*height/2;
                if (x>18 and x<width-18 and y>toolBottom+18 and y<height-100) {
                    vg.beginPath(); vg.fillColor(nvg.rgba(230,252,255,220));
                    vg.roundedRect(x-16,y-16,9,2,1);vg.roundedRect(x-16,y-16,2,9,1);
                    vg.roundedRect(x+7,y-16,9,2,1);vg.roundedRect(x+14,y-16,2,9,1);
                    vg.roundedRect(x-16,y+14,9,2,1);vg.roundedRect(x-16,y+7,2,9,1);
                    vg.roundedRect(x+7,y+14,9,2,1);vg.roundedRect(x+14,y+7,2,9,1);vg.fill();
                }
            }
        }

        for (self.planet.lifeforms.items) |lifeform| {
            const p = lifeform.position;
            if (p.dot(self.cameraPos.sub(p)) <= 0) continue; // far hemisphere
            const clip = vp.mulByVec4(za.Vec4.new(p.x(), p.y(), p.z(), 1));
            if (clip.w() <= 0) continue;
            const x = (clip.x() / clip.w() + 1) * width / 2;
            const y = (1 - clip.y() / clip.w()) * height / 2;
            if (x < 6 or x > width - 6 or y < toolBottom + 6 or y > height - 90) continue;
            vg.beginPath();
            vg.fillColor(nvg.rgb(255, 178, 70));
            vg.roundedRect(x - 6, y - 6, 12, 12, 6);
            vg.fill();
            vg.beginPath();
            vg.fillColor(nvg.rgb(60, 30, 8));
            vg.roundedRect(x - 2, y - 2, 4, 4, 2);
            vg.fill();
        }
        vg.beginPath();
        vg.fillColor(nvg.rgba(8, 15, 28, 225));
        vg.rect(0, 0, width, toolBottom);
        vg.rect(0, height - 84, width, 84);
        vg.fill();
        const origin = self.planet.worldMode == .origin;
        if (self.watchLifeView) {
            const compactWidth = (width - 32) / 3;
            if (ui.button(vg, game, "watch-pause", 8, 6, compactWidth, 44, if (self.paused) "Play" else "Pause")) self.paused = !self.paused;
            if (ui.button(vg, game, "watch-tools", 16 + compactWidth, 6, compactWidth, 44, "Tools")) {
                self.watchLifeView = false;
                self.seedTargets.count = 0;
            }
            if (ui.button(vg, game, "watch-speed", 24 + 2 * compactWidth, 6, compactWidth, 44, guidance.speedLabel(self.timeScale))) {
                self.timeScale = guidance.nextSpeed(self.timeScale);
                self.mobileFeedback = guidance.speedHint(self.timeScale, self.paused);
                self.mobileFeedbackSeconds = 3;
            }
        } else {
        const topColumns: f32 = if (width >= 650) 4 else 3;
        const topW = (width - (topColumns + 1) * 8) / topColumns;
        if (ui.button(vg, game, "mobile-pause", 8, 6, topW, 44, if (self.paused) "Play" else "Pause")) self.paused = !self.paused;
        if (ui.button(vg, game, "mobile-climate", 16 + topW, 6, topW, 44, "Climate")) {
            self.showPlanetControl = !self.showPlanetControl;
            self.showPointDetails = false;
        }
        if (ui.button(vg, game, "mobile-menu", 24 + 2 * topW, 6, topW, 44, "Menu")) { self.showEscapeMenu = !self.showEscapeMenu; self.leavePlanetArmed = false; }
        const tools = [_]GameTool{ .None, .EmitWater, .DrainWater, .PlaceVegetation, .RaiseTerrain, .LowerTerrain, .PlaceLife };
        const names = [_][]const u8{ "Inspect", "Water +", "Water -", if (origin) "Seed" else "Plants", "Land +", "Land -", if (origin) "Nutr. +" else "Rabbits" };
        const columns: usize = if (width >= 650) 7 else 4;
        const bw = (width - 16 - @as(f32, @floatFromInt(columns - 1)) * 6) / @as(f32, @floatFromInt(columns));
        for (tools, names, 0..) |tool, name, i| {
            const x = 8 + @as(f32, @floatFromInt(i % columns)) * (bw + 6);
            const y = 58 + @as(f32, @floatFromInt(i / columns)) * 54;
            if (ui.button(vg, game, name, x, y, bw, 44, name)) self.selectedTool = tool;
            if (self.selectedTool == tool) {
                vg.beginPath();
                vg.fillColor(nvg.rgb(92, 214, 255));
                vg.roundedRect(x + 6, y + 46, bw - 12, 4, 2);
                vg.fill();
            }
        }
        var speedLabelBuffer: [40]u8 = undefined;
        const speedLabel = std.fmt.bufPrintZ(&speedLabelBuffer, "{s}", .{guidance.speedLabel(self.timeScale)}) catch "Pace";
        const speedX = if (width >= 650) 32 + 3 * topW else 8 + 3 * (bw + 6);
        const speedY: f32 = if (width >= 650) 6 else 112;
        if (ui.button(vg, game, "mobile-speed", speedX, speedY, if (width >= 650) topW else bw, 44, speedLabel)) {
            self.timeScale = guidance.nextSpeed(self.timeScale);
            self.mobileFeedback = guidance.speedHint(self.timeScale, self.paused);
            self.mobileFeedbackSeconds = 3;
        }
        }
        vg.textAlign(.{ .horizontal = .left, .vertical = .middle });
        if (origin) ui.label(vg, game, "Origin · Day {d:.1}", .{self.gameTime / 86400}, 10, height - 64) else ui.label(vg, game, "Day {d:.1} · {d} rabbits", .{ self.gameTime / 86400, self.planet.lifeforms.items.len }, 10, height - 64);
        vg.textAlign(.{ .horizontal = .right, .vertical = .middle });
        ui.label(vg, game, "{d:.1}°C", .{self.planet.temperature[self.selectedPoint] - 273.15}, width - 10, height - 64);

        vg.textAlign(.{ .horizontal = .left, .vertical = .middle });
        vg.fontSize(14);
        vg.fontFace("sans-serif");
        vg.fillColor(nvg.rgb(190, 214, 232));
        var ecologyText: [160]u8 = undefined;
        const ecologyLabel = if (origin and self.watchLifeView) @import("../watch_feedback.zig").line(&ecologyText,self.planet.propaguleArrivals,self.planet.propaguleTrackedLosses) else if (origin) std.fmt.bufPrint(&ecologyText, "Microbial births {d} · Inspect for traits", .{self.planet.microbeStats.births}) catch "Microbial habitat" else std.fmt.bufPrint(&ecologyText, "Born {d} · Lost {d} · Meals {d} · Gen {d}", .{ self.planet.rabbitBirths, self.planet.rabbitDeaths, self.planet.rabbitMeals, self.planet.plantGenerations }) catch "Ecosystem statistics";
        var ecologyBounds: [4]f32 = undefined;
        _ = vg.textBounds(0,0,ecologyLabel,&ecologyBounds);
        const ecologyWidth=ecologyBounds[2]-ecologyBounds[0];
        if(ecologyWidth>width-20)vg.fontSize(14*(width-20)/ecologyWidth);
        _ = vg.text(10, height - 40, ecologyLabel);
        vg.fontSize(14);
        const depth = self.planet.waterMass[self.selectedPoint] * self.planet.getKmPerWaterMass();
        const hint: []const u8 = if (origin and self.selectedTool == .PlaceVegetation)
            @import("../seed_eligibility.zig").seedHint(self.planet.seedEligibility(self.selectedPoint), if(self.mobileFeedbackSeconds>0) self.mobileFeedback else "")
        else if (self.mobileFeedbackSeconds > 0) self.mobileFeedback else if (origin and self.watchLifeView) @import("../watch_feedback.zig").legend else if (origin) switch (self.selectedTool) {
            .PlaceVegetation => if (depth < 0.0002) "Too dry: microbes need shallow water" else if (depth > 0.05) "Too deep: drain to 0.2–50m" else "Tap to seed existing simple life",
            .PlaceLife => "Tap to add nutrients (player supplied)",
            .None => "Inspect mats; Play to observe change",
            else => "Shape habitat; Inspect water and heat",
        } else switch (self.selectedTool) {
            .None => if (self.planet.lifeforms.items.len == 0) "Plant food, add rabbits, press Play" else if (self.paused) "Paused: press Play to watch your habitat" else if (self.planet.rabbitBirths == 0) "Watch grazing; births need food and time" else "Births recorded. Inspect or change climate",
            .EmitWater => "Paint mode: drag to add water",
            .DrainWater => "Paint mode: drag to drain water",
            .PlaceVegetation => guidance.plantWarning(depth) orelse "Paint mode: drag to plant food",
            .RaiseTerrain => "Paint mode: drag to raise land",
            .LowerTerrain => "Paint mode: drag to lower land",
            .PlaceLife => guidance.rabbitWarning(depth, self.planet.temperature[self.selectedPoint], self.planet.vegetation[self.selectedPoint]) orelse "Tap planted land to add a rabbit pair",
        };
        var hintBounds: [4]f32 = undefined;
        _ = vg.textBounds(0, 0, hint, &hintBounds);
        const hintWidth = hintBounds[2] - hintBounds[0];
        if (hintWidth > width - 20) vg.fontSize(14 * (width - 20) / hintWidth);
        if(origin and self.watchLifeView and self.mobileFeedbackSeconds<=0)renderWatchLegend(vg,width,height-16) else _ = vg.text(10, height - 16, hint);

        if (self.showEscapeMenu or self.showPlanetControl or self.showPointDetails) {
            const pw = @min(width - 24, 360);
            const ph: f32 = if (self.showPlanetControl) 280 else if (self.showEscapeMenu) 248 else 280;
            const px = (width - pw) / 2;
            const py = @max(6, (height - ph) / 2);
            vg.beginPath();
            vg.fillColor(nvg.rgba(0, 0, 0, 160));
            vg.rect(0, 0, width, height);
            vg.fill();
            vg.beginPath();
            vg.fillColor(nvg.rgb(20, 34, 53));
            vg.roundedRect(px, py, pw, ph, 12);
            vg.fill();
            vg.textAlign(.{ .horizontal = .left, .vertical = .top });
            ui.label(vg, game, "{s}", .{if (self.showEscapeMenu) "Planet menu" else if (self.showPlanetControl) "Climate" else "Surface details"}, px + 16, py + 14);
            if (ui.button(vg, game, "mobile-close", px + pw - 60, py + 6, 52, 44, "X")) {
                self.showEscapeMenu = false;
                self.showPlanetControl = false;
                self.showPointDetails = false;
                self.leavePlanetArmed = false;
                return;
            }
            if (self.showEscapeMenu) {
                const half = (pw - 40) / 2;
                if (ui.button(vg, game, "mobile-resume", px + 16, py + 58, half, 44, "Resume")) self.showEscapeMenu = false;
                if (ui.button(vg, game, "mobile-main-menu", px + 24 + half, py + 58, half, 44, if (self.leavePlanetArmed) "Discard & leave" else "Leave planet")) {
                    if (self.leavePlanetArmed) { game.setState(MainMenuState); return; }
                    self.leavePlanetArmed = true;
                }
                if (ui.button(vg, game, "mobile-daylight", px + 16, py + 110, half, 44, if (self.stableDaylight) "Daylight: on" else "Daylight: off")) self.stableDaylight = !self.stableDaylight;
                if (ui.button(vg, game, "mobile-map", px + 24 + half, py + 110, half, 44, if (self.displayMode == .Normal) "Surface" else "Heat map")) self.displayMode = if (self.displayMode == .Normal) .Temperature else .Normal;
                if (ui.button(vg, game, "mobile-slower", px + 16, py + 162, half, 44, "Slower")) self.timeScale = @max(1, self.timeScale / 2);
                if (ui.button(vg, game, "mobile-faster", px + 24 + half, py + 162, half, 44, "Faster")) self.timeScale = @min(86400, self.timeScale * 2);
                vg.textAlign(.{ .horizontal = .center, .vertical = .middle });
                vg.fontSize(14);
                vg.fontFace("sans-serif");
                vg.fillColor(nvg.rgb(190, 214, 232));
                var speedBuf: [100]u8 = undefined;
                const speed = if (self.leavePlanetArmed) "Unsaved progress lost. Close to cancel." else std.fmt.bufPrint(&speedBuf, "{d:.1} hours/sec · light affects view only", .{self.timeScale / 3600}) catch "";
                _ = vg.text(width / 2, py + 228, speed);
            } else if (self.showPlanetControl) {
                vg.textAlign(.{ .horizontal = .center, .vertical = .middle });
                ui.label(vg, game, "Sun: {d} W/m²", .{self.solarConstant}, width / 2, py + 76);
                if (ui.button(vg, game, "mobile-solar-minus", px + 16, py + 102, (pw - 40) / 2, 44, "Less sun")) self.solarConstant = @max(0, self.solarConstant - 100);
                if (ui.button(vg, game, "mobile-solar-plus", px + 24 + (pw - 40) / 2, py + 102, (pw - 40) / 2, 44, "More sun")) self.solarConstant = @min(5000, self.solarConstant + 100);
                if (ui.button(vg, game, "mobile-clear-water", px + 16, py + 158, pw - 32, 44, "Clear all water")) self.debug_clearWater = true;
                if (ui.button(vg, game, "mobile-deluge", px + 16, py + 214, pw - 32, 44, "Deluge")) self.debug_deluge = true;
            } else {
                const point = self.clickedPoint;
                if (origin) {
                    const cell = self.planet.microbeCells[point];
                    var c = cell.cohorts[0];
                    for (cell.cohorts[1..]) |cohort| { if (cohort.biomass > c.biomass) c = cohort; }
                    mobileDetailLabel(vg, game, "Microbial mat · {d:.3} kg C/m²", .{Microbes.biomass(cell)}, px+16, py+62, pw-32);
                    mobileDetailLabel(vg, game, "Water {d:.2}m · {d:.1}°C", .{self.planet.waterMass[point]*self.planet.getKmPerWaterMass()*1000,self.planet.temperature[point]-273.15}, px+16,py+94,pw-32);
                    mobileDetailLabel(vg, game, "Nutrients: {d:.3} kg/m²", .{cell.nutrient},px+16,py+126,pw-32);
                    if (c.biomass > 0) {
                        mobileDetailLabel(vg, game, "Dominant lineage {d} · Gen {d}", .{c.lineage,c.generation},px+16,py+158,pw-32);
                        mobileDetailLabel(vg, game, "Optimum {d:.1}°C · Light {d:.2}x", .{c.optimum-273.15,c.efficiency},px+16,py+190,pw-32);
                    } else mobileDetailLabel(vg, game, "No living colony at this point", .{},px+16,py+158,pw-32);
                    if (c.biomass > 0) mobileDetailLabel(vg, game, "Structure: {d:.0}% · drying protection", .{c.structure*100},px+16,py+232,pw-32) else mobileDetailLabel(vg, game, "Existing life seeded; not abiogenesis", .{},px+16,py+232,pw-32);
                } else {
                const half = (pw - 40) / 2;
                if (ui.button(vg, game, "inspect-surface", px + 16, py + 56, half, 44, if (!self.inspectAnimal) "Surface •" else "Surface")) self.inspectAnimal = false;
                if (ui.button(vg, game, "inspect-rabbit", px + 24 + half, py + 56, half, 44, if (self.inspectAnimal) "Rabbit •" else "Rabbit")) self.inspectAnimal = true;
                vg.textAlign(.{ .horizontal = .left, .vertical = .top });
                if (self.inspectAnimal) {
                    const nearby = habitat_feedback.nearestRabbit(self.planet, point);
                    const status = if (nearby) |i| habitat_feedback.inspectRabbit(self.planet, i, self.gameTime) else null;
                    if (status) |rabbit| {
                        mobileDetailLabel(vg, game, "Nearby: {s}", .{habitat_feedback.animalLabelText(rabbit.label)}, px + 16, py + 112, pw - 32);
                        mobileDetailLabel(vg, game, "Age: {d:.1} hours", .{rabbit.age_hours}, px + 16, py + 142, pw - 32);
                        mobileDetailLabel(vg, game, "Fullness: {d:.0}% (not health)", .{rabbit.fullness}, px + 16, py + 172, pw - 32);
                        if (rabbit.gestation_hours) |hours| {
                            mobileDetailLabel(vg, game, "Gestation: {d:.1}h minimum left", .{hours}, px + 16, py + 202, pw - 32);
                            mobileDetailLabel(vg, game, "Birth also needs food and space", .{}, px + 16, py + 232, pw - 32);
                        } else {
                            mobileDetailLabel(vg, game, "Breeding rest: {d:.1} hours", .{rabbit.cooldown_hours}, px + 16, py + 202, pw - 32);
                            mobileDetailLabel(vg, game, "Nearest now; not a tracked ID", .{}, px + 16, py + 232, pw - 32);
                        }
                    } else {
                        mobileDetailLabel(vg, game, "No nearby rabbit", .{}, px + 16, py + 112, pw - 32);
                        mobileDetailLabel(vg, game, "Inspect closer to an orange dot", .{}, px + 16, py + 150, pw - 32);
                        mobileDetailLabel(vg, game, "Animals move as time runs", .{}, px + 16, py + 190, pw - 32);
                    }
                } else {
                    mobileDetailLabel(vg, game, "Altitude: {d:.2} km", .{self.planet.elevation[point] - self.planet.radius}, px + 16, py + 112, pw - 32);
                    mobileDetailLabel(vg, game, "Temperature: {d:.1}°C", .{self.planet.temperature[point] - 273.15}, px + 16, py + 142, pw - 32);
                    mobileDetailLabel(vg, game, "Water depth: {d:.2} m", .{self.planet.waterMass[point] * self.planet.getKmPerWaterMass() * 1000}, px + 16, py + 172, pw - 32);
                    mobileDetailLabel(vg, game, "Plant cover: {d:.0}% · Gen {d}", .{ self.planet.vegetation[point] * 100, self.planet.plantTraits[point].generation }, px + 16, py + 202, pw - 32);
                    mobileDetailLabel(vg, game, "Adapted to: {d:.1}°C", .{self.planet.plantTraits[point].optimum - 273.15}, px + 16, py + 232, pw - 32);
                }
                }
            }
        }
    }

    pub fn saveGame(self: *PlayState) !void {
        try std.fs.cwd().makePath("saves/abc");

        const metadataFile = try std.fs.cwd().createFile("saves/abc/metadata.json", .{});
        defer metadataFile.close();
        const GameMetadata = struct {
            format_version: u32 = 0,
            game_time: f64,
            axial_tilt: f32,
            solar_constant: f32,
            planet_rotation_time: f32,
            time_scale: f32,
            radius: f32,
            subdivisions: u64,
            seed: u64,
        };
        try std.json.stringify(GameMetadata{
            .format_version = 0,
            .game_time = self.gameTime,
            .axial_tilt = self.axialTilt,
            .solar_constant = self.solarConstant,
            .planet_rotation_time = self.planetRotationTime,
            .time_scale = self.timeScale,
            .radius = self.planet.radius,
            .subdivisions = self.planet.numSubdivisions,
            .seed = self.planet.seed,
        }, .{ .whitespace = .indent_tab }, metadataFile.writer());

        const planetFile = try std.fs.cwd().createFile("saves/abc/planet.dat", .{});
        defer planetFile.close();

        var buffer = std.io.bufferedWriter(planetFile.writer());
        const writer = buffer.writer();
        const planet = self.planet;
        // planet.vertices can be re-generated using icosphere data, same for indices

        for (planet.elevation) |elevation| {
            try writer.writeInt(u32, @as(u32, @bitCast(elevation)), .little);
        }

        for (planet.temperature) |temperature| {
            try writer.writeInt(u32, @as(u32, @bitCast(temperature)), .little);
        }

        for (planet.vegetation) |vegetation| {
            try writer.writeInt(u32, @as(u32, @bitCast(vegetation)), .little);
        }

        for (planet.waterMass) |waterMass| {
            try writer.writeInt(u32, @as(u32, @bitCast(waterMass)), .little);
        }

        for (planet.waterVaporMass) |waterVaporMass| {
            try writer.writeInt(u32, @as(u32, @bitCast(waterVaporMass)), .little);
        }

        for (planet.airVelocity) |airVelocity| {
            try writer.writeInt(u32, @as(u32, @bitCast(airVelocity.x())), .little);
            try writer.writeInt(u32, @as(u32, @bitCast(airVelocity.y())), .little);
        }

        // TODO: save lifeforms

        try buffer.flush();
    }

    pub fn deinit(self: *PlayState, game: *Game) void {
        SunMesh.deinit(game.allocator);
        self.planet.deinit();
        self.framebuffer.deinit();
        self.blurFramebuffer.deinit();
        self.bloomFramebuffer.deinit();
    }
};

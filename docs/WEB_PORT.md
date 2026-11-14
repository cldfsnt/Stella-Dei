# Experimental browser port

Original upstream commit `006940ad6bf31d7d7dac9188d3bd8f26521268c2`, GPLv3.

The actual original game compiles to JavaScript/WebAssembly with Zig 0.13.0 and Emscripten 3.1.64. Build using `web/build.sh`; toolchains default to sibling `stella-toolchains`, override STELLA_TOOLCHAINS/ZIG/EMCC as needed.

Implemented: cooperative simulation job queue, persistent browser event loop, direct GL bindings, shared NanoVG/WebGL2 context, shader ES300 adapters, float/depth framebuffer formats, original assets in preloaded filesystem, and touch shell with orbit/zoom/menu controls. Native path retained.

The exact pinned mach-glfw source was recovered from the existing verified cache (contrary to the initial 404 diagnosis). Web copies of mach-glfw, zalgebra, zigimg, and GLFW header are vendored with their original licenses; mach-glfw init skips unavailable platform init hints under WASM.

Verified: Zig static-library compile, full Emscripten link, job unit test, shader-boundary unit tests, and HTML shell JS syntax. Cloud browser downloads/initializes WASM, but cannot create a WebGL2 context; an independent minimal WebGL2 test also returns null. Therefore actual rendering, new-game generation, simulation, audio, touch input and Android performance are NOT verified. This is an experimental test build, not a finished playable release.

Assets split into byte-identical 16 MB chunks for static-host file limits. Source and LICENSE must accompany deployed build. No purchases, credentials, or user data required.

## Startup repairs (v2)

Reproduced allocation failures independently in a Node/Emscripten probe:
- Missing `USE_OFFSET_CONVERTER` aborts Zig's allocation return-address lookup.
- Zig default WASM page allocator grows memory without updating Emscripten views; HEAPU8 length becomes zero. Overriding browser page_allocator to c_allocator preserves views and returns the expected test byte.
- Khronos glslangValidator identified desktop-only arithmetic and constant-expression usage in terrain/cloud/postprocess fragment shaders. Fixed: all 6 game shader pairs now compile/link in ES300 and desktop330, plus NanoVG both modes.

Starts main only after Play; audio initialization therefore happens in a trusted gesture. Visible persistent startup diagnostics report errors and aborts. Full Android gameplay still requires testing; the available cloud browser still lacks WebGL2.

## Audio startup exports (v3)
An Android diagnostic screenshot identifies `TypeError: Module._malloc is not a function`. The bundled miniaudio WebAudio backend calls Module._malloc/_free directly and ccall during audio callbacks. Explicitly exported malloc/free and ccall. Browser allocator self-test now completes before Play and logs `Audio memory bridge ready.`

## Phone interface (v4)
User confirmed v3 loads and runs. Mobile update replaces the fixed 1280x720 squeeze with viewport-matched canvas resizing, a responsive original-game HUD with 44px targets, 1–2 tool rows, large menu/intro controls and dismissible climate/menu panels. UI taps no longer apply planet tools underneath. Compact outer toolbar fits 390px without horizontal overflow, help is a dismissible overlay. Checked shell at 390x844 portrait and 844x390 landscape; landscape stage is 844x340, mode switch and help open/close pass. Game HUD geometry checked at 320/390/430 portrait and 800/844 landscape; full WASM compile/link passes. Actual new HUD rendering still relies on user device since cloud WebGL2 unavailable.

## Planet laboratory (v5)
Browser defaults to stable camera-facing daylight, while physical sun/climate time continues unchanged. Planet menu toggles Daylight and Surface/Heat map, with slower/faster controls (browser max one day/second so original rabbit AI is not bypassed). Default browser speed reduced to one hour/second.
Rabbits tool now names the actual supported organism and places a nearby mixed-sex pair. UI includes tool guidance and population count; Help explains land → plants → rabbits. Existing rabbit simulation includes vegetation consumption, movement, mating/gestation and deaths; no additional species or complete ecosystem is claimed.
Life safety repairs: reserve capacity before a population tick, iterate originals backwards so removals do not skip organisms/newborns are deferred, avoid recursive birth locking, unique RNG streams and opposite-sex mature partners/female gestation. Reverse-iteration mutation regression model passes; full browser archive/link passes. Actual v5 rendered gameplay remains untested in cloud due unavailable WebGL2.

## v6: navigation and gameplay test harness
- Diagnosed tiny per-tap mobile zoom: 120px synthetic wheel normalized to1.2 steps then only2.4% distance. Toolbar now invokes actual WASM zoom directly, scaling altitude by0.55 per tap with surface clearance.
- Land selects existing dry ground and frames it closely. Globe resets to aspect-aware whole-planet framing; startup faces dry land. No terrain is fabricated by navigation.
- Browser close-up camera and picking now share view target. Actual ray/sphere intersection replaces approximate selection; sky clicks no longer edit terrain.
- Mobile vegetation brush paints three topology rings, rather than a nearly invisible single tile.
- `web/gameplay-harness.js`, opt-in `?harness=1`, runs actual WASM camera/picking/tool methods and exports JSON plus canvas captures. This modifies a disposable current planet. It is not a visual-quality assertion, and captures may be blank on a cleared WebGL drawing buffer.
- Five tests against the production camera_math functions pass (zoom, bounds/fractional steps, portrait framing, ray hits/misses). Full WASM build/link and JavaScript syntax checks pass. Cloud WebGL2 remains unavailable, so rendered-game and physical touchscreen tests are NOT claimed passed; the harness makes this limitation explicit rather than substituting mocked rendering.

## v7 work in progress: actual graphics investigation
- Installed Mesa surfaceless EGL initializes successfully without window sockets or security changes: EGL1.5, desktop OpenGL4.5 llvmpipe; GLES3.2 also works.
- `web/tests/probe-gles-framebuffer.py` reproduced GL_INVALID_OPERATION0x502 for original drawBuffers([COLOR_ATTACHMENT1]) mapping. Valid attachment0 mapping returns0. This is an executed GLES3 test, not inferred from a compiler.
- Replaced unsafe same-FBO brightness extraction and attachment1 remapping with independent single-color scene/bloom/blur framebuffers. All pass outputs are attachment0 and no pass samples its own target. Full WASM build/link passed. Visual investigation ongoing; not yet a claim that the user's gray-surface symptom is resolved.
- Native original engine/renderer now actually executed under EGL llvmpipe. First native frame's misleading -244°C HUD was averaging from0K, not frozen simulation data; initialize meanTemperature to293.15K to match actual cells. Later real frames show20°C paused terrain, blue water and rocky continents.
- Actual scripted GLFW baseline inputs changed vegetation0→1 and rabbit count0→2; full original meshes rendered. Initial harness-only mobile guard transformation needed correction, so authoritative final run must transform both wasm equality and inequality branches.
- Browser Normal surface now explicitly cartographic: bare tan altitude shading, blue actual water, green actual vegetation, icy water nearfreezing, yellow selection ring. Haze/separate water layer are bypassed in this view, with physical fields unchanged. Actual living rabbit positions have orange UI markers alongside original3D models.
- Final actual-engine mobile-branch EGL interaction run: zoom distance10140→6321→5245; same selected tile16866 vegetation0→1; real pointer Rabbit action population0→2; terrain tool operated; Play advanced gameTime to7072.8seconds with2rabbits still present. Captured and visually inspected distinct tan/blue world, green planted patch, orange live markers and original rabbit meshes. Native test audio is offline and mobile compile branches explicitly selected; not an Android end-to-end claim. Native teardown reports an existing allocation leak, no run abort.

## v8 integration in progress
- Recovered v7 exact published source and assets after local workspace loss; rebuilt toolchains from official Zig0.13.0 and Emscripten3.1.64 releases. Original unused native remote dependencies are now lazy so web builds use vendored sources without fetching retired pins.
- Pinch controller is shared between real browser controls and deterministic regression tests. Two-finger pinch calls fractional actual WASM zoom; one-finger Navigate/ Paint modes, delayed frame-visible taps, cancel/blur/reset guards. Gesture tests and full WASM compilation passed before persistence integration.
- Ecology changes are under actual full-world playtest; controlled-core success alone is not a full climate/habitat assertion. Durable versioned browser saves are also under integration; not yet claimed completed here.
- v8 executed acceptance: real full-world, fixed-seed mobile-branch EGL run planted 37 cells at 0.35 coverage, placed two rabbits, then advanced climate/water/ecology for five simulated days. Vegetation reached 91 cells and 39.901 biomass (from12.95), peak coverage0.916; four rabbits, two births,24 meals, zero deaths. Inspected captured green expansion and grazing patches, not only counters. Plant thermal traits mutated/inherited to generation2; separate production selection test reached generation3.
- Actual-world save test serializes34,882,406bytes, clears live plants/rabbits/counters, restores, and recaptures byte-identical JSON. Found/fixed arena allocation ordering bug during this test. Separate real Chrome IDBFS fixture write→fresh page reload/read passed216bytes; this confirms browser storage mechanism, not full Android game restart. Saves remain browser-local and can be lost if site storage is cleared.
- Camera math5tests, schema/ecology4tests, production-core7day lifecycle and touch regressions pass. Native EGL captures use real engine/shaders and mobile branches; physical Android pinch and exact browser WebGL runtime remain separate device-verification gaps. Original native allocator shutdown leak persists. Five-day success is not long-term ecosystem balance or a claim all prototype features are complete.
- Stronger IDBFS acceptance executed: actual34,882,406-byte five-day world stored in real Chrome via Emscripten IDBFS, then fresh document/WASM read returned exact byte equality and SHA256c5159953f2552169bca23a6e22aa0637f3d9606169c5003b5db1158b8bd133ca. Local-only fixture/test directory excluded from published static site.
- Final carrying-capacity iteration: mating requires nearby food and limits local population, after a37-day test exposed overbreeding collapse. Controlled37-day soak now retains35 rabbits (peak35),39births1106meals6deaths and5.297848biomass. Final full-world5.007day rerun:91cells39.954biomass,4rabbits2births23meals0deaths; exact34,880,319-byte world restore passed. Earlier35MB browser storage test used preceding same-format world; final read/write implementation unchanged.

## v9 mobile playability and compatible lighter worlds
- New browser worlds use topology6 (40,962cells); existing topology7 saves retain all163,842cells and exact data, never resampled. Approximate physical plant brush footprint preserved using1ring on6 and3rings on7. Existing native defaults unchanged.
- Real native benchmark, two runs: update median9.0–9.2ms on6 vs36.8–37.0ms on7; render24.9–25.5ms vs54.7–54.9ms; gameplay memory~138MiB vs205.5MiB. These are software-rendered native measurements, not phoneFPS. Close-up grid is deliberately coarser.
- Topology6 actual five-day world passed:7 seeded cells/2.45biomass→37cells/8.864, plantgeneration2; rabbits2→4,2births23meals0deaths. Exact8,661,045-byte save restore passed. Topology-aware actual6→7→6 restore kept v8 high-resolution JSON exact; corrupted input and pending normal work rejected before mutation.
- Loading from main menu uses existing state transition then exact topology replacement; direct candidate-union assignment triggered Zig0.13 WASM compiler SIGTRAP, isolated/bisected and replaced. Existing live-world replacement remains failure-atomic. If menu load allocation fails, an empty new planet remains rather than discarding an existing user world.
- Native390px interaction verified speed1→6→24→1hours/sec, water-depth2.1m rabbit rejection with countunchanged, and successful dry-land pair placement with visible acknowledgement. Contextual footer reports actual food/water/temperature. More sheet puts Save/Load/Help/fullscreen behind a visible button rather than offscreen scrolling.
- Prior topology7 fullworld20-day soak also passed:37→200vegetatedcells, biomass130.868, rabbits2→16,14births209meals,plantgeneration8; no nonfinite primaryfields. This is a functioning sandbox, not evidence of a deep campaign or mandatory management challenge.

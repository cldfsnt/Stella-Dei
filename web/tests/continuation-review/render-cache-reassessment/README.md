# Read-only terrain cache reassessment at ec54ced / live v59

No implementation or new benchmark. Cloud Chrome currently cannot create WebGL; no browser runtime result is claimed.

## Current code and invalidation

`src/simulation/planet.zig:549–560` shares terrainPoint and synchronous refreshTransformedPoints. Geometry depends on vertices, elevation, radius and axial tilt, not water, biology or camera. `upload:564–659` still rebuilds all transformed points and streams six f32 geometry attributes each frame; queues computeAllNormals each tenth upload. At40962cells the geometry stream is983088bytes/frame. Dynamic map/water/vegetation uploads must remain live. Wind reuses bufData, so it cannot serve as persistent geometry cache storage.

Current mutation sites: initial Planet generation (elevation around390), applyImage(472), Play raise/lower selected+neighbors(947–962), both pond_action legacy mutation and checked apply(55–58,93), successful save apply elevation copy(71) and axial tilt(120), new Planet/mesh/VBO/topology/radius lifetime. Water brush alone does not change terrain. All need exact invalidation or snapshot keys.

Critical newer requirement: `save_game.zig:122` synchronously refreshes transformedPoints with restored tilt BEFORE subsequent physics; a cache must not defer this until render or retain prior-world geometry. Solar/microbial and atmospheric calculations read these points. Queued normal completion must dirty GPU normals even without another terrain edit. An old queued job across edits/load must not mark stale geometry clean. Existing native deinit waits for pending normal work; do not expand its cooperative-loop assumptions casually.

## Already tested, already held

See `geometry-integrated-v45/README.md`, not merely the earlier prototype. Integrated cache passed24 invalidation cases,30 settled pixel-identical captures,18 full-save hashes. It eliminated983088bytes/frame and periodic unchanged normal jobs, but did NOT show dependable total-frame benefit. Natural30day baseline→candidate frame medians were16.950→17.171ms paused,19.945→20.014 at Grow6,28.367→28.564 at24target. Snapshot storage~160KiB plus O(N) compare/invalidation complexity was therefore held. This remains negative evidence, not a new discovery ready to ship.

`browser-pump-profile/README.md` measured normals mean~.13–.23ms/frame, one job/10frames, max1.31–2.86ms. It included an obsolete extra native atmosphere upload in full-frame totals, explicitly documented; pump timings remain actual queued-job observations. Not the main measured bottleneck then.

## WASM distinctions and next decision

Both current web Zig and native EGL harness compile ReleaseSafe. Web additionally targets wasm32-emscripten, explicitly single-threaded, imports gl_web, and links Emscripten C/JS at-O2 through WebGL2; native uses desktop GL/EGL llvmpipe and hardware-native code. Browser callbacks cooperate via pump(16), while individual normal jobs remain synchronous. Native corrected cache tests deliberately used that browser policy and omitted the native-only atmosphereMesh upload, which production WASM already skips. Browser JIT, GL bridge/driver submission and async GPU scheduling can change costs; this is a reason to profile actual WASM, NOT evidence that the held cache now wins.

Do not repeat or promote the same cache without a concrete current WASM cost signal. No new normals-only or full-cache experiment is authorized by this audit. Await actual WASM harness attribution; retain load-before-physics, all invalidation and queued-job correctness requirements if that evidence justifies another gate.

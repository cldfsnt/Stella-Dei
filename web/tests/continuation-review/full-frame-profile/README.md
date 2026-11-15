# Full-frame native mobile-policy profile

Isolated fixture only; production source unchanged. `web/tests/egl-full-frame-profile-prepare.py` extends the actual nursery harness. Real generated 40,962-cell Origin world, normal nursery/seed APIs, unchanged coupled scheduler. Early snapshot has 1 occupied cell/1 cohort; established30d has 10 occupied cells/18 cohorts. This is not a dense biosphere stress test or evidence of completed ecological succession.

Three independent runs, each paused/6h-per-second/24h-per-second requested speed, each 12 warmup and60 measured full update + render + gl.finish + swap frames. Matched frozen independent JSON save restored before each speed and exactly afterward. No assigned biomass or changes to saved progress. Fixed1/60 input delta is a controlled workload, NOT measured achieved browser pace. Compute-throughput omits waiting/vsync/browser scheduling and is not a device-speed promise. Logging occurs outside timedframe. gl.finish ensures outstanding render completion, but stage telemetry is CPU submission time and stages are not GPU timings or necessarily additive.

Platform: llvmpipe LLVM19.1.7 256bits, OpenGL4.5 Mesa25.0.7 software renderer;390x700 canvas and scene. Existing mobile adapter substitutes WASM gates in copied PlayState only: no bloom,0 bloom passes, same default web policy. Copied loop.zig `is_web=true`: getParallelCount is1, matching cooperative WASM jobs rather than native worker pool. Native machine code, GLdriver, browser overhead, actual GPU and touch differ. Not Android/WebGL measurement.

## Three-run ranges (milliseconds)
|State/speed|Update mean|Render+finish mean|Full-frame mean|Full-frame p95|
|---|---:|---:|---:|---:|
|Early paused|0.0003–0.0007|6.809–7.571|6.809–7.572|8.224–9.207|
|Early6|2.706–4.205|7.313–8.618|10.018–12.823|18.843–31.679|
|Early24|10.502–11.225|7.146–7.995|17.904–18.912|19.708–21.828|
|30d paused|0.0004–0.0005|7.611–8.262|7.612–8.263|8.004–12.372|
|30d6|2.861–3.112|7.945–8.558|10.806–11.574|20.541–21.268|
|30d24|10.859–11.312|8.157–8.442|19.163–19.717|21.079–24.254|

6h workload executes15 physics ticks per60frames;24h executes60. Schedulerphysics telemetry almost exactly accounts for update cost. Full-frame cost at24h exceeds16.67ms despite tiny colony count. Large one-off outliers occur (first early6 physics tick89ms); three runs avoid treating that outlier as typical. The population comparison does not establish causality because climate/world state also advances.

### Next defensible investigation
Instrument copied `Planet.simulate` stage boundaries: (1) temperature initialization/jobs/wait/swap (planet.zig1582–1618), (2) water copies/jobs/wait/atmosphere transport (1620–1656), (3) animal+microbe/vegetation steps (1694–1720). All are inside measured ~11ms schedulerphysics; full-mesh thermal/hydrology work is plausible dominant cost but NOT isolated by this evidence. Do not claim that either is proven or optimize nearest-cell queries based solely on a microbenchmark. Render floor remains meaningful ~7–8ms on this software renderer; stage raw logs show terrain uploads and scene/post/UI submission separately. A proper shipping decision still needs real browser timing and a denser legitimate world.

## Reproduce
1. `python3 web/tests/egl-full-frame-profile-prepare.py <isolated-src>`
2. Zig0.13 build `web/tests/egl-propagule-visual-build.zig -Dsource=<isolated-src>/main.zig`, ReleaseSafe, standard native harness dependencies; use absolute prefix/cache paths.
3. Run stella-egl with STELLA_ORIGIN_COUPLED=1 STELLA_ORIGIN_FAST=1 STELLA_PRODUCER_LONG=1 STELLA_DIAGNOSTIC_DAYS=30 STELLA_FORMS_SINGLE=1 STELLA_ORIGIN_WIDTH=390, isolated STELLA_EGL_CAPTURE_PREFIX/STELLA_EGL_SAVE_PATH and Mesa cache. Repeat3times.

All3 runs exited0; early/established exact-save restores and final invalid-save rejection/exact restore passed. Existing native allocator leak still reported at shutdown. Raw sanitized logs and CSV contain all samples/context. No production edit, commit, push or deployment.

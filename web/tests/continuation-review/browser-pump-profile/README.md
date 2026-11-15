# Browser scheduling audit and cooperative full-frame proxy

## Decision
Deferred jobs are real unclassified work, but they are **not the main measured bottleneck here**. Do not rewrite scheduling or add broad new UI diagnostics on the strength of this one run. Renderer and actual physics remain the larger targets. No production changes.

## Source audit
- WASM builds single-threaded, with no pthread/OffscreenCanvas path. `Job.get()` executes queued jobs synchronously on the same thread. `web_frame` runs pollEvents, pump(16), update, pump(16), render, swap. A pump is bounded by job count, not wall time; one expensive job can still delay input.
- Physics ticks are1440 simulated seconds. At most2 per frame; the16ms budget is checked only AFTER each indivisible full-engine tick. Raising the target does not skip subsystems. Pending debt is capped at2ticks; background gaps over2seconds discard debt. A slow tick can therefore exceed the budget and reduce achievable pace. Input cannot run midway through synchronous physics/render.
- `gpuUpload` queues a whole-mesh normal recomputation every10uploads. It normally executes in the next pre-update pump, outside existing physics/render timing. Geometry does not change merely because biological/climate time advances; renderer worker investigates exact invalidation separately.
- Previous native full-frame fixture did not explicitly pump around update. In paused measurements this can leave a queued normals job unexecuted; this fixture follows the actual web order. It does not prove the older timings were browser-equivalent.
- Recurring JS work: world-mode DOM sync once/second; selected-cell snapshot plus full-cell goal-stage scan once/3seconds; gameplay-measure tick250ms; patch-watch200ms only while active. Finder work is explicitly batched via rAF. No periodic full-save serialization found. These calls are not timed by this native proxy and may still need actual-browser profiling.
- Resize passes CSS stage dimensions with no explicit devicePixelRatio multiplication. Scene framebuffer scale is1, so large desktop CSS dimensions still cost more pixels. Native desktop and WASM use different GL/shader paths; copied harness selects the web/mobile policy but is not WebGL.
- `Planet.deinit` contains a spin-wait unsafe for an unpumped cooperative caller. However ordinary exported save/load already pump1024 before the relevant operations; a user-facing load deadlock was NOT demonstrated. Do not report that guarded path as broken.

## Executed proxy
`egl-pump-profile-prepare.py` copies the current nursery harness and instruments only copied files. `pump-profile.zig.part` follows actual web-loop order, with separate poll/pre-pump/update/post-pump/draw/finish/swap timing. Job counters/max durations are isolated research instrumentation, not added to the game. Warmup12frames, measured60frames, paused/6/24hour targets, early seed and naturally grown30day world.40,962cells, one cooperative worker,1280×700 framebuffer, llvmpipe LLVM19.1.7. No assigned biomass. Each speed restores the same serialized starting state; final early/day30 saves restored exactly. Run exit0.

**Subsequent audit caveat:** inherited native preparation switches Play rendering policy but leaves Planet.gpuUpload native-only atmosphereMesh upload enabled. Actual WASM skips that unused upload. Thus the recorded full-frame/render totals include extra native work, not an exact browser workload. Pump timings still measure the queued normals path. No corrected rerun is claimed; renderer worker is correcting its separate A/B fixture.

Real browser render submission is asynchronous. This proxy adds explicit `gl.finish` AFTER draw and reports it separately, to expose completion cost. Draw CPU call time may already include driver waits; finish is not a pure GPU timer and the two cannot be interpreted as hardware-GPU stage profiling. Fixed1/60 input delta controls requested workload; it is not actual achieved laptop/browser pace. Logs are emitted outside timed frames. One run only, with outliers, not a device-FPS claim.

## Mean milliseconds per frame
|World/target hours per second|Pre-pump|Update|Draw call|Explicit finish|Whole proxy frame|
|---|---:|---:|---:|---:|---:|
|Early paused|.129|.001|10.906|5.311|16.351|
|Early6|.150|2.503|12.372|5.799|20.827|
|Early24|.144|9.948|13.845|5.863|29.801|
|30day paused|.231|.001|18.754|9.946|28.933|
|30day6|.159|3.441|17.352|9.292|30.246|
|30day24|.186|12.046|15.365|8.702|36.300|

Each60frame block executes6pre-pump jobs (periodic normals),0post-pump jobs. Update runs0/30/120 jobs at0/15/60physics ticks respectively, consistent with two queued physics tasks per tick. Max measured pre-pump job duration ranges1.31–2.86ms; outer pump wall includes scheduling noise and reaches4.74ms. This is visible work but small compared with render+physics. Early24 has a158ms draw outlier;30day24 has47.24ms update maximum. These outliers remain in logs, not removed. No causal attribution for scheduler/driver pauses is established by one sample.

## Next bounded action
Keep renderer's static geometry upload/normal invalidation experiment and physics workers' exact-result caching as priorities. Compare matched old/new full-frame proxy using the SAME pre/post pumps, legitimate save, view size, bloom configuration and warmups. Require saved-world equality and valid geometry changes, not faster timings produced by silently skipping climate or biology. Measure on-device with existing local gameplay sample before claiming laptop performance. If an unexplained browser long-frame residual remains, add opt-in pump/job timings with zero-clock overhead when disabled, not automatic uploads.

## Artifacts and reproduction
New preparer `web/tests/egl-pump-profile-prepare.py`; Zig fixture `web/tests/pump-profile.zig.part`. Build its generated main with existing `egl-propagule-visual-build.zig`, Zig0.13 ReleaseSafe. Environment: `STELLA_ORIGIN_COUPLED=1 STELLA_ORIGIN_FAST=1 STELLA_PRODUCER_LONG=1 STELLA_DIAGNOSTIC_DAYS=30 STELLA_FORMS_SINGLE=1 STELLA_ORIGIN_WIDTH=1280`, isolated save/capture/Mesa cache destinations. Existing shim fixes height700.

`input-hashes.json` pins actual production sources at copying. Logs are lossless deterministic gzip; uncompressed hashes retained. Known native allocator shutdown warning remains. No production edit, deployment, new user permissions or user telemetry transmission.

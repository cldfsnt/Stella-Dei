# Optional one-day advance: benchmark-only gate

No production changes, browser UI, new job controller or deployment. PLAN.md was saved before execution; it defines the proposed safety contract that still needs implementation/tests. This gate establishes only actual unchanged physics/state parity and a bounded native rendering-work opportunity.

## What ran

Actual natural60-day world,40,962 cells, native390×700 llvmpipe (LLVM19.1.7), cooperative loop parallelcount1. Each trial restores the same independently frozen serialized state.60×1440second production Planet.simulate calls, same per-tick events and pre/postpump16. Pausedflag and requestedpace stay unchanged: this is a proposed explicit advance job, not ordinary clock demand. Rendering on each callback vs hidden intervening rendering; each has initial and final actual redraw.100 unmeasured initial renders settle camera/warm shaders. Native-only atmosphere upload explicitly omitted to mirror existing browser branch. No physics skipped, simplified or enlarged.

Three paired trials with alternating order: normal/hidden, hidden/normal, normal/hidden. Other workers released the CPU window first. Saving/serialization excluded from timing; finalredraw included. `gl.finish` synchronizes software rendering, unlike an asynchronous real browser/GPU pipeline. No rAF waits or DOM progress updates in native loop.

## Measured results

|Trial|Hide globe?|Whole day +finalredraw ms|Physics ms|Draw during60ticks ms|Callback p95 ms|Maximum callback ms|
|---|---|---:|---:|---:|---:|---:|
|0|No|1375.487|572.818|783.339|25.918|52.698|
|1|Yes|498.867|486.175|0|8.751|9.475|
|2|Yes|565.583|548.714|0|8.408|75.511|
|3|No|1326.551|557.828|750.755|26.846|51.811|
|4|No|1312.536|530.430|763.917|24.868|29.692|
|5|Yes|514.616|502.583|0|9.024|9.346|

Median total1,326.551→514.616ms, about61.2% less tight-loop work. Paired reductions63.7%,57.4%,60.8%. Finalredraw11.38–16.84ms. All measurements, including hidden trial2's75.511ms callback outlier, retained. This does not establish a maximum cancellation latency or device-wide worst case.

**Not a half-second browser day.** Proposed one-tick-per-requestAnimationFrame still needs60 callbacks. At60Hz this imposes roughly a1second scheduling floor, before slow callbacks or overhead. At30Hz it is roughly2seconds. Native measurements omit browser event-loop/DOM/rAF waits and use software EGL rather than user's GPU. The opportunity is removing repeated expensive drawing while doing the same work, not a promised completion time or general laptop speedup.

## Exact-state checks

All six output saves byte-identical, including camera, full dense arrays, organisms, resources, RNG, history, time, pause and requestedpace. All progress exactly86,400 simulated seconds. Initial restoration and final original restoration independently byte-identical. Output hashes in provenance.json, full local snapshots not Git. Thus this specific hide/render schedule does not change model evolution. Existing transient visual caches are not serialized; freshdraw occurred before comparison.

No input or lifecycle safety tests were claimed: there is no active job controller yet. Implementation must preserve readonly status while blocking mutatingexports and native pointer/keyboard paths; reset stale held input before leaving overlay; cancel or suspend on visibility/context changes; token-check world/owner; never restore old-world pause into a newworld. Paused-only start/finish avoids pause restoration. Cancel retains completedticks and cannot interrupt an indivisible physics step. Fresh redraw and validpicktargets before interaction resumes. A DOM overlay alone is insufficient. Save/load must be explicitly blocked or safely cancel first. See PLAN.md.

## Decision

Evidence supports considering a deliberately optional **'Advance one day (hide globe)'** mode with opaque progress/cancel overlay, rather than silently degrading normal graphics or changing physics. It does not authorize shipping untested busy-state behavior. An actual browser acceptance pass remains necessary after controller implementation.

## Reproduce

Run egl-advance-day-prepare.py with an isolated source directory; build using egl-propagule-visual-build.zig and Zig0.13 ReleaseSafe. Execute from repository root with QA_PULSE_SAVE pointing at hashed natural60-day60.json, STELLA_ORIGIN_COUPLED=1, STELLA_ORIGIN_FAST=1, STELLA_PRODUCER_LONG=1, STELLA_FORMS_SINGLE=1, STELLA_ORIGIN_WIDTH=390 and software EGL. Do not run competing builds/benchmarks during trials.

Final build/run exit0; inherited native GPA teardown leak warnings remain. Initial unused inherited QA import compiler failure retained separately; no failed execution or parity sample discarded. Logs gzip mtime0 and lossless decompression verified. Sources/provenance/checksums retained; production untouched.

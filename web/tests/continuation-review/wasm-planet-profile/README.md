# Actual production Planet simulation under WASM, not a browser/GPU benchmark

## Result

All integrity gates passed. The actual wasm32 ReleaseSafe `Planet.simulate` calls temperature, liquid/wind, atmosphere and the final living-ecology branch. Actual production cooperative EventLoop runs one job partition; SIMD width4 and usize32. No GL constructor, renderer, DOM, rAF, canvas, or UI is called. The linked module has no GL/GLFW imports. Current production mathematics, schema6/model5 and RNG are unchanged. No experimental roots or replacement liquid solver enters these binaries.

Three frozen real 40,962-cell worlds and fixed18 alternating runs were retained, with no favorable repetitions. First tick is separately reported. Remaining59 ticks are still a short cold-process workload, not guaranteed fully optimized steady-state V8 execution.

| Input | Plain first tick median | Plain remaining tick median (range) | Instrumented temperature | Liquid + wind | Atmosphere | Ecology |
|---|---:|---:|---:|---:|---:|---:|---:|
| day30 |23.72ms|19.01ms (16.14–21.39)|2.16ms|3.63ms|10.28ms|0.85ms|
| day60 |21.37ms|16.32ms (15.73–19.23)|2.27ms|3.82ms|10.60ms|1.09ms|
| day90 |29.40ms|20.25ms (19.70–22.93)|2.63ms|4.45ms|12.51ms|0.91ms|

Stage columns are medians of instrumented remaining59 per-tick values, not components of the separate plain median. Atmospheric nested subtotals (already included above):

| Input | Wind cache | Edge-rate cache | Saturation + phase | Coefficient | Gather |
|---|---:|---:|---:|---:|---:|
| day30 |0.906ms|4.100ms|2.209ms|1.036ms|1.914ms|
| day60 |0.962ms|4.038ms|2.411ms|1.090ms|2.076ms|
| day90 |1.148ms|4.778ms|2.728ms|1.283ms|2.493ms|

Atmosphere is roughly60% of the instrumented step; rebuilding directed edge rates is its largest single measured subphase. This is a concrete code-generation/algorithm investigation target, **not authorization or proof for another cache or changed physics law**. Prior held geometry/basis/cache variants are not revived by this profile.

Instrumentation/plain total median differences were −11.0%, +9.4%, +4.3%, with substantial pair variability. The negative value cannot be a literal negative timer overhead: noise/JIT/code-layout effects are unresolved. Do not claim precise instrumentation overhead, exact cross-world cost scaling, or a speed improvement. Old native profiles used different target width/runtime and workload conditions; higher WASM numbers are not evidence of a production regression.

## Integrity and initialization

- Runtime checks every `getNeighbours` row against actual preserved graph. Storage order is FL,BL,L,FR,BR,R. No sendWater-order permutation is applied.
- Every world's zero-tick **complete parsed save equals the input**. Sparse cohort slots, RNG, stats, full atmospheric fields, buffers, game metadata and camera values remain intact.
- For every world, plain and instrumented WASM complete output files are byte-identical after1 and60ticks. All18 timing outputs equal their corresponding fixed60tick gate hash.
- Independent native headless counterpart uses the same loader, production math and cooperative scheduling, with native SIMD16. Its60tick output is **byte-identical to the preserved actual EGL-restored production complete save for all three worlds**. This supports omission of the GL constructor on these inputs, rather than relying only on instrumentation self-consistency.
- Geometry uses actual normalized vertices and production `refreshTransformedPoints`, with loaded elevation and axial tilt. Buffers use target SIMD alignment as production constructor requires. Exact plain/stage source diffs are saved.
- Cross-target native/WASM trajectory equality is not required: the current legacy SIMD liquid algorithm genuinely depends on target width. No cross-target equivalence is claimed.
- All captured endpoints pass production schema validation. Saves are only read; outputs remain separate QA files. This is not a save/load restart test or browser user journey.

## Scheduler relevance and limits

Actual PlayState consumes1440 simulated seconds per tick, starts at most two ticks per callback, and will not start another after its16ms budget is spent. A tick cannot be interrupted. The Node timings show meaningful simulation cost near or beyond that budget on this cloud host, before any rendering, but **do not measure a user's laptop/Android callback, display frame rate or GPU**. Six to seven simulated hours per real second would arithmetically mean15–17.5 such ticks per real second; this does not identify which device-side stage causes that reported speed. The actual cloud browser could not create independent WebGL contexts; this harness does not remove or conceal that blocker.

## Reproduction and provenance

1. `bash web/tests/build-wasm-planet-profile.sh` prepares isolated source trees from current checkout and builds both plain/stage executables. Uses pinned Zig0.13.0, wasm32-emscripten, ReleaseSafe, single-threaded; emcc-O2/ASSERTIONS/USE_OFFSET_CONVERTER/NODERAWFS,128MiB initial growable memory,8MiB stack. Exact versions/host are in `environment.txt`.
2. `bash web/tests/build-native-planet-control.sh` builds same loader with native target and explicit cooperative Loop branch. Native comparator is correctness only, not a timing competitor.
3. `python3 web/tests/run-wasm-planet-profile.py` first runs all integrity gates, then the fixed18 trials. Existing frozen inputs/graph/EGL reference endpoints are required; hashes are saved. One process invokes `qa_run` once, so retained allocations/counters have process lifetime rather than a repeated-call API guarantee.

Clocked region excludes parse/restore/geometry/validation/serialization. Includes first lazy scratch allocation and V8 warmup. Phase markers add timing calls only; nested timings must not be added twice. Full logs/results and hashes are committed; large complete JSON snapshots and binaries remain local with hashes.

Initial fixture failures are retained: relative module path, default non-null pointer initialization, timer inserted in wrong function, then actual first-tick unaligned QA buffers. These were corrected without changing production math. The topology-order draft was corrected before execution. Native linking needed bundled Zig compiler runtime and quadmath; final build passed. No failed test was relabeled as a production defect or silently discarded.

**Recommendation:** use this as measured WASM stage attribution. Keep all three liquid-gather variants held and live game unchanged. Inspect actual edge-rate WASM code generation before proposing any optimization.

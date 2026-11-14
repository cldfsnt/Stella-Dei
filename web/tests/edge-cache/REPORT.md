# Directed atmospheric edge-rate cache (isolated prototype)

No production/main files edited. Requires integrator acceptance, current-tree smoke and WASM verification before deployment.

## Mechanism and scope
Atmospheric transport previously recalculated each directed edge rate three times per tick: coefficient total, donor subtraction total, and inbound gather. The candidate owns a lazy [6]f64 scratch row per cell and refreshes all six rates after wind updates every tick. Donor sums use their original neighbor order. Inbound gather uses a bounded six-neighbor reverse lookup, retaining its original accumulation order; missing reverse adjacency falls back to the original calculation. Duplicate neighbor slots have equal rates and preserve original repeated contributions.

This reduces rate calculations from 18 to 6 per cell. A lookup is bounded/O(1), but the whole simulation remains O(N). Neither physics resolution nor tick count changes. It does not statically cache changing terrain or velocity. Nothing is serialized.

Extra allocation: 1,966,176 bytes at 40,962 cells; 7,864,416 bytes at 163,842 cells. No reverse-index table. Resize allocates replacement before freeing old scratch; failure retains original calculations whenever scratch length mismatches. New-world construction remains lazy and cannot fail because of this cache. Deinit frees owned scratch.

## Correctness so far
- All three rate targets retain six-tick physical save hash d523353839672a4, cached and forced-failure baseline.
- Paired 1800-tick / 30-day full serialized state hash 3138eaaced1f785 is exactly equal, including all saved fields.
- Forced edge allocation failure keeps the pre-existing wind cache, exercises the uncached edge path, and completes. Cache poisoning with NaNs followed by load/step is fully refreshed.
- Independent generated/simulated/deinitialized Planet: 32,231,576 allocated bytes = freed bytes.
- Two actual replaceWorld cycles grid6→7→6 allocate fresh 163,842 / 40,962 cell scratch and validate saves.
- Pause callbacks, invalid rates, background gap, menu/load reset, rejected invalid saves and exact restore pass.
- Native shutdown still emits the existing unrelated allocator warning. The tracked Planet lifecycle is balanced.
- Dedicated terrain/velocity mutation paired 1800-tick run passes exact hash 2aa1307c66b4a2a7 after identical edits at ticks 300 and 900.
- Canonical Raise/LowerTerrain actions plus normal geometry upload pass a 20-tick paired hash f72797c449ed2c61. Every outgoing cached rate and reverse-gather lookup is asserted exactly equal to original calculation immediately after rebuild, on each tick.

## First paired native timing, not a phone promise
Both enabled/disabled runs use the same binary and wind cache; baseline forces only edge allocation failure. At Fast, atmospheric stage was 10.02→6.23 ms per tick; actual throughput 17.69→18.79 simulated h/s. Median frame was 36.20→21.77 ms, but p95 worsened 41.69→47.51 ms and maximum 247.48→268.30 ms. Synthetic two-render-frame pause was 17.33→15.94 ms, not OS/touchscreen latency.

This is native llvmpipe/software GL on a shared machine, not Android/WebGL. Do not promise tail improvement or universal smoothness. Long correctness runs overlap builds and their durations are not controlled benchmarks. Instrumented render_cpu/gpu_wait values of zero are unhooked counters, not measurements. See raw logs and QA instructions.

## Artifacts
edge-cache.patch is narrow production-only code, with no profiling hooks. planet-baseline.zig and planet-candidate.zig retain exact compared source. qa/prepare.py reconstructs isolated checks from current source plus patch; successful preparation was verified byte-identical for Planet. Do not copy an entire older source tree into main.

## Investigated failed fixture (retained evidence)
The first dynamic test produced unequal final hashes. It directly edited transformedPoints, but save.apply restores saved elevation and wind, not this derived geometry. The second pass therefore began with geometry left over from the first run. Restoring the same initial geometry before both passes resolved the 30-day mismatch without a production change. Both failed and corrected logs are retained. The canonical-action direct test independently verifies rate lookup equivalence. This is not a claim to have fixed or changed production loading.

The final candidate patch adds explanatory comments beyond the instrumented source; executable statements are unchanged. QA-SOURCE-HASHES.txt identifies actual tested sources; HASHES.txt identifies clean patch and source artifacts.

## Reverse-order repeat and recommendation
After the correctness runs finished, repeated cached first then baseline (five-second target windows, same binary): Fast atmosphere 9.86 → 5.75 ms/tick, actual throughput 18.95 → 22.25 simulated h/s. Median frame 36.49 → 21.81 ms, p95 45.13 → 34.94 ms, maximum 118.70 → 88.43 ms. Synthetic two-frame pause 20.11 → 15.15 ms. Both passes exit 0 with identical model hashes and callback checks. This repeat supports reduced average atmospheric CPU work and lower median frame cost; it does not erase the first run's worse tail. Shared-machine variance remains substantial.

Recommendation: worth a staged deployment at the normal 40,962-cell grid after integrated/WASM checks. An extra 1.97 MB buys an approximately 38–42% reduction in measured native atmospheric-stage time while preserving exact results and graceful allocation failure. This is a measured CPU-work reduction, not a claim that phone FPS or worst-case latency will improve. The high grid adds 7.86 MB; weigh that explicitly against existing WASM heap/device pressure. Do not increase default grid resolution on the strength of this optimization. Actual device diagnostics remain necessary to evaluate throughput and long frames. If memory is tight, retain the uncached fallback rather than skipping simulation work.

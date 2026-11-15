# Ordered transient activity index: exact-state gates and performance limits

## Result and scope
The candidate removes two repeated whole-cell scans in sparse Origin worlds without changing traversal order, physiology, births, movement, randomness or saved data. Parent reviewed/applied the proposed production helper and Planet patch; this worker changed copied research sources and test/evidence files only. Publication is the parent's responsibility.

Large-grid native coupled-simulation gains are demonstrated in the clean paired sample below. Small-grid timing is too variable to claim an Android gain. Dense parity passes, with a small +1.24% regression in the second measured pair; do not claim faster for every population. No browser FPS, GPU, or touch-latency measurement is made here.

## Mechanism and lifetime
Existing growth/decay still scans all cells in ascending order and builds bits for cells containing living biomass OR detritus. Movement and reproduction enumerate marked indices in ascending order. Successful relocation marks `moved.to`; successful exploratory/neighbor births mark the actual destination. Every iterator call reloads its word, so later arrivals in the same word are visible in the current phase. Lower indices are not revisited. Reproduction starts its own cursor at zero, preserving moves into lower-index cells before the birth phase. Empty/depleted marked cells merely follow existing no-biomass guards; they do not get invented growth or credit.

The bitset is rebuilt for every tick and freed with the same owning Planet allocator on every return. It is20,488bytes for163,842 cells and5,128bytes for40,962 cells. Allocation failure falls back to the complete original ascending scans. No persistent cache, save field, load invalidation protocol, resampling or stale world pointer is introduced. Complexity remains O(N + active work), NOT O(1). Actual Planet generation initializes its allocator; old synthetic fixtures constructing undefined Planet objects must initialize that field too, as the parent corrected separately.

`proposed/planet.patch` and `proposed/active_cell_index.zig` retain the reviewed proposal. Parent also corrected the obsolete comment claiming no world-sized scratch. The copied final fixtures import the exact applied `src/active_cell_index.zig` (hash493573880318b287d52b10dc1dd1c84d8fee252807ee1c96a9d56d4d751a05c4), not a second iterator implementation.

## Correctness gates
- Three focused production-helper tests: dynamically added future same-word cells, skipped prior cells, empty/word-boundary/padding/dense order, allocation refusal, complete linear fallback.
- Seven controlled180-day scheduler runs, each10,800ticks. Three seeds ×stable/depth mosaic, plus forced allocation failure on EVERY tick for seed42 stable. Every tick compares complete cohort arrays (all traits/RNG/history), gas pools, stats, arrival/failure feedback and counters against baseline. Original carbon/nutrient tolerance0.001 retained. All pass.
- Controlled runs exercise13,678–36,548 funded births,6–40 relocations and13,289–35,859 propagule arrivals, not just a silent sparse snapshot. Forced-OOM run reproduces36,548 births and24 relocations exactly.
- Natural163,842-cell replay: four alternating60-tick complete coupled-physics arms give identical full saved JSON, including every cell RNG and all serialized climate fields, SHA256 `51286afe3bbc86f7f7420502fc14df012e8348aad985fd809b49a29c0bef8b7d`. Exact original save restored.
- Natural40,962-cell replay: full JSON SHA256 `6a3eeb0bf0f458c88b18629b0dacfe11c784af1e53a35abc5556024fa2d43d4e`, all four arms identical, exact original restored.
- Dense40,962-cell stress fixture: **40,962 occupied cells and40,970 cohorts initially**. Starting from the legitimate saved mesh, temperature is deliberately set303K and water to1m;40,952 empty patches are seeded using the actual resource-paid seed API. This is an explicitly manipulated stress fixture, NOT natural dense evolution. Four result JSONs match `f51e3bf6741c82f2303568f27c7b3f673651b805a57258ffa41074a35ac8cbf9`. The original pre-intervention save is restored exactly.

These tests use native ReleaseSafe code and real production physiology, not Android/WebGL. The two research paths differ in copied scheduling only; phase timers are observation. The applied helper is exercised, but the timed binary retains a runtime baseline/candidate switch and phase instrumentation rather than being the final release binary.

## Clean large-grid timings
No other worker build/benchmark ran during `clean7.log`. Two sequential baseline/candidate pairs, each60 coupled1440-second ticks, no rendering inside the interval:

|Pair|Baseline coupled ms|Candidate coupled ms|Reduction|
|---|---:|---:|---:|
|1|2542.310|2077.690|18.27%|
|2|2541.518|2018.815|20.57%|

Baseline movement+birth loops total303.806/292.684ms per60ticks; candidate .599/.583ms. The existing full growth scan remains173–186ms. The change avoids reading all empty cohort records two more times; it does not skip climate, hydrology, detritus recycling or active organisms. End-to-end gain also reflects ordinary cache/timing effects, not exclusively the sum of these two phase measurements.

Earlier `run7.log` overlapped a reviewer compiler and is explicitly diagnostic, not the clean performance claim. Full saved-state parity still holds there.

## Dense and small-grid caveats
Dense two pairs:1348.317→1212.061ms and1240.532→1255.936ms. The second pair is +1.24%; first baseline has larger unrelated growth/movement time, so do not market dense improvement. There is no observed major regression in this bounded test; many repeated runs and a163k dense world were not tested.

Natural small-grid two pairs:667.370→557.974ms and561.357→642.667ms. The unchanged full growth scan itself ranges30.693–110.296ms across arms, showing substantial noise not explained by bit iteration. **No reliable40k/Android speedup established.** Correctness and removal of sparse movement/birth scans hold, but the large-grid18–21% figure must not be projected onto this grid or a user's laptop/browser.

All sampled worlds are QA fixtures, not user saves. Sparse large world has7 occupied patches/12cohorts; small has10/18. Complete saved-state equality is stronger than comparing counts, but it excludes transient render caches. The replay applies the same saved nursery mesh before physics, without an explicit fresh render before each timed arm. Existing generated nursery geometry matches the intended source fixture; arbitrary different-geometry/tilt load replay would need pre-timing transform refresh. This comparison is not an arbitrary-load rendering test. Subsequent integrated release acceptance should refresh those caches explicitly.

## Reproduction and source ownership
- `web/tests/prepare-microbe-active-profile.py <copied-v42-profile-source> <fresh-output>` creates research scheduling/timers only in the new source copy, importing current applied helper.
- `web/tests/microbe-active-profile.zig.part` is the loaded-save replay routine; `src/qa_active_parity.zig` is compiled ONLY inside that generated source because it imports research metrics.
- Build generated main with existing `egl-propagule-visual-build.zig`, Zig0.13 ReleaseSafe. `STELLA_CPU_LEVEL=7` plus `QA_MICRO_REPLAY=<large QA save>` for large; level6 and the natural30day QA save for small; add `QA_MICRO_DENSE=1` for the explicit dense stress setup.
- Saved inputs: large `cpu-v42/save7.json`; small `watch-natural-30day.json` with provenance manifest. Input hashes, copied source snapshots and exact helper hash accompany results. Source baseline came from review worker's already-instrumented CPU-v42 tree; existing phase instrumentation does not change model state.
- Baseline reference remains the untouched full ascending loops; the candidate uses real dynamically updated words. OOM fallback tests force real allocator refusal, not a mocked iterator alone.

Raw logs are losslessly gzip-compressed with deterministicmtime0; original hashes retained. No source save or failed result is silently discarded. Known native shutdown allocator warning remains. Parent owns integrated WASM/JS gates and deployment; this evidence does not claim browser playback was tested.

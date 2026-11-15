# Exact latitude cache, current-v52 isolated experiment: HOLD

Production source was not changed. Current source checkpoint c5b50a4 copied through existing CPU phase/replay preparers. The previously unfinished latitude preparer is reused, not a new discovery: it had one old unit-test log but no accepted whole-world timing. It replaces repeated acos(vertex.z), hemisphere sign, sin(latitude) with exactly the same computed f32 value keyed by the exact f32 z bits. Spin rate, radius, dt and multiply order remain per-step. Eight bytes per vertex,327696 bytes at40962 cells. Allocation failure uses the original expression, and cached values update if z bits change. No geometry/visual simplification or approximate sqrt identity.

## Workload and proof

Native EGL llvmpipe at390×700 using browser render policy/cooperative scheduler1. Not an actual phone, browser WASM or Todd's hardware measurement. Two existing actual QA worlds run through the current engine: early after a prior short profile (2 patches/2 cohorts), and naturally evolved30d (10 patches/18 cohorts). Each arm restores the same world independently. Three alternating pairs each; pair1 has no warmup (cold cache), pairs2/3 have12 warmup frames, then60 measured frames/60 ticks of1440 simulated seconds at requested24h/sec. Input1/60s is synthetic workload control, not promised real achieved speed. No biology updates were disabled.

All12 runs exit0; all6 paired full serialized state hashes match byte-for-byte. Helper test checks100004 exact inputs,100000 repeated reads, changed keys and signedzero. These are state/numerical proofs, not new settled-image parity or standalone WASM proof. Existing allocator teardown warnings remain in full logs. Invalidations beyond z-bit unit coverage (newworld/load/tilt/tool sequences) were not added for this experiment, so it is not release-ready acceptance.

## Results

Median of three per-run means, baseline→candidate, milliseconds:

| World | update | liquid/wind substage | full frame |
|---|---:|---:|---:|
| Early |9.6322→8.8008|1.872965→1.299985|16.6163→16.4460|
|30d |10.8312→10.7139|1.976435→1.390902|19.4170→19.1990|

Every liquid/wind substage is lower, consistent with removal of repeated transcendental work. Total results are mixed: early pair2 update is slower; established cold pair10.6114→10.7139 and warmed pair2 10.8312→11.0025 are slower, while warmed pair3 11.1688→9.5598 is faster. Full means similarly mixed. Established max frame reaches186.2449ms and unrelated organism/renderer phases vary substantially despite a coordinated window without known sibling builds. Do not discard those runs or present the favorable median as a robust universal gain.

Median process peakRSS: early233888→234392KiB (+504);30d236808→237428KiB (+620). This includes native software graphics and fixture JSON allocations, not browser memory footprint.

**Recommendation: HOLD.** The targeted work reduction is real, but whole-frame median savings~1% and inconsistent pairs do not justify another production cache/performance promise yet. Largest measured full-frame problem remains rendering plus broader atmosphere/temperature work. No production commit or deploy is implied.

## Reproduction

From the current pinned production tree, run egl-cpu-resolution-prepare.py into isolated `profile`, egl-cpu-coefficient-replay-prepare.py profile base, and egl-cpu-latitude-prepare.py base candidate. Build both main.zig files with existing egl-propagule-visual-build.zig, Zig0.13 ReleaseSafe and separate cache/prefix directories named base-build/candidate-build. `run.py` expects its directory to contain those builds and sibling cpu-v44/cold-base-early.json + cpu-v44/save.json (prior actual QA worlds). It alternates runs and checks full-state hashes; input fixtures are not user saves. Source and result hashes are archived; logs sanitized and losslessly gzipped. Full summary.json includes all conditions, not just medians.

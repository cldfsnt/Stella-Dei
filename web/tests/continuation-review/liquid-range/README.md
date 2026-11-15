# Contiguous liquid SIMD membership: HOLD

Isolated current-v54 copied-source experiment only. No production edit.

## Hypothesis and scope

`sendWater` suppresses a transfer into its own SIMD source batch by comparing the target against every source lane. The sole caller supplies contiguous iota indices. Replace only membership with `target >= origin[0] and target-origin[0] < VECTOR_SIZE`; preserve every floating-point operation, scatter/addition order, water donor remainder, and other solver path. No cache, allocation, persistent memory, graphics or schema change. Integer boundary checks cover widths4/8/16/32 and low/high addresses. This is not a generalized replacement for arbitrary noncontiguous vectors.

## Actual engine method

Current production copied through the existing natural60 native EGL fixture. Real40,962-cell early/day30/day60 saves; each arm independently restores the same owned save.30 untimed1440-second coupled steps, then300 timed coupled steps. Order baseline/candidate/candidate/baseline/baseline/candidate. Serialization/render/UI outside timer. No other workers compiling or executing heavy jobs during timings. No shadow instrumentation.18 endpoints match complete serialized state byte-for-byte including model/RNG fields; original save restored. This is native coupled CPU time, NOT laptop/Android/browser/full-frame timing.

| Input | Baseline ms/tick | Candidate | Median change | Paired changes |
|---|---:|---:|---:|---|
| Early |8.319|8.153|-2.00%|+4.87%, -2.67%, -5.99%|
| Day30 |7.975|7.979|+0.05%|-3.48%, +0.60%, +1.23%|
| Day60 |8.137|7.714|-5.19%|-8.55%, -5.19%, -4.41%|

## Decision and limitations

HOLD. All correctness endpoints pass, but the representative timing benefit is inconsistent. The predicate's workload is not colony-density dependent, so one favorable late-world result cannot establish a broad speedup. No production integration, no browser speed claim, no extra memory cost. Do not repeat this as a fresh optimization without acknowledging these results.

Targeted WASM32 semantics and Sandbox execution gates were not run because representative performance did not justify promotion. They remain mandatory before any future integration. No targeted liquid-stage instrumentation or final-image comparison was run; full model parity does not alone measure graphics.

Source/input hashes and actual start times are preserved. Large saves remain local, not duplicated in Git. Logs retain the existing native GPA teardown diagnostics; this assay makes no memory-leak claim. Reproduce with `egl-liquid-range-prepare.py`, existing `egl-propagule-visual-build.zig`, and `run.py` using STELLA_WORKSPACE. The preparer introduces only a QA selector and candidate branch into the copied solver; production is untouched.

### Coordination timestamp check

A sibling later warned of possible delayed-message compiler overlap. Checked file creation timestamps resolved it: this run was06:11:53–06:12:47UTC; that sibling's first compiler log was created06:13:43.280520UTC (later retry06:14:11UTC). Thus that reported compiler did not overlap. Timing variability still remains and the HOLD decision is unchanged.

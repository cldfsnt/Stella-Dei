# Actual-world phase-coefficient cache comparison

Production candidate avoids recomputing invariant per-tick relaxation coefficients for each cell. No skipped cells, ecological equations, water exchange, timestep, visual quality or precision reductions. Prepared coefficients use the exact timestep; no persisted world/geometry cache or new save fields.

## Matched frozen binary, three alternating baseline/candidate pairs
Real generated 40,962-cell Origin nursery,30 days normal coupled evolution,10 occupied cells/18 cohorts. Fixed1/60 workload,24h/sec target,12 warmups+60 timed update/render/finish frames.60 actual1440-second physics ticks measured. Software llvmpipe native mobile-policy390x700,no bloom,cooperative schedulerparallel1. All limits from full-frame-profile apply: no Android/WebGL timing claim or dense-biosphere guarantee.

All six runs' complete serialized world captured immediately AFTER measured ticks and BEFORE restoring saves are byte-identical:
`03374f92d0fd9dbc458a6a1b14119a461074486e304ea1f51024745013fa5993`.
This includes actual30-day preparation plus warmups+60 measured ticks, not merely a saved pre-test snapshot. Original save restored exactly afterward. No fuel/biomass fixture assignments. All6 runs exited0, existing native shutdown allocator leak persists.

|Paired run|Baseline update mean ms|Candidate update mean ms|Baseline full-frame mean ms|Candidate full-frame mean ms|
|---|---:|---:|---:|---:|
|1|11.7158|10.5661|21.4389|19.8098|
|2|11.9051|9.8678|20.6168|18.2805|
|3|11.1000|10.5866|21.0533|19.6319|

Median update11.7158→10.5661ms (9.8% lower); median fullframe21.0533→19.6319ms (6.75% lower). Paired update reduction ranges4.6–17.1%, reflecting machine noise/outliers. These are native workload results, not promised phone speedups. Candidate does not yet reach16.67ms fullframe on this software renderer.

Median phase loop including unchanged saturation-pressure computation108.167→52.0126ms per60ticks (~51.9% lower). Thus the isolated helper's~4× microbenchmark gain becomes~2× for actual phase loop and~10% whole update; do not advertise4× game speed. Render cost is unaffected algorithmically and varies betweenruns.

Both paths in the frozen comparison initialize3 per-tick coefficients; baseline then ignores them and uses original per-cell phase. This adds a tiny constant3calls/tick to baseline versus ~100k per-cell calls; explicitly not an uninstrumented production baseline. Timers/counters common to both; all per-frame logging after timed interval. Larger one-off baseline outliers retained rather than filtered.

## Reproduction and production verification
`egl-phase-cache-compare-prepare.py` now composes atmospheric/fullframe instrumentation and adapts current production Planet: STELLA_PHASE_CACHE=1 chooses actual production PhaseStep; unset chooses independent frozen experimental/phase_reference.zig. This avoids accidentally comparing the newly cached wrapper against itself. STELLA_PHASE_MEASURED_PATH writes full postmeasurement state. Build with existing native EGL ReleaseSafe Zig0.13 harness and nursery flags/repeated command. Initial6 results used equivalent experimental Cache in an already-built frozen binary while production integration proceeded; final actual-production verification is recorded separately.

New profiling files only owned by this worker. Parent owns production integration, tests, publishing. No commit/push/deploy here.

### Final production path verification
Actual integrated PhaseStep run exited0. Full postmeasurement state hash again03374f92d0fd9dbc458a6a1b14119a461074486e304ea1f51024745013fa5993, identical to all6 old/reference/candidate runs. Exact original save restore passed. Single finalrun update9.7214ms/fullframe17.6051ms; validation only, not substituted into matched3-pair medians.

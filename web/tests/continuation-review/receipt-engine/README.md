# Actual coupled-engine realized-receipt gate (research only)

The known exact tiny-N funding failure is NOT fixed: at dt=0.01 seconds/light=0.5, biomass can gain 1.862645149e-9 while f32 nutrient 0.02 does not change. This is bounded drift-reduction research, not exact conservation or production approval.

## Frozen mechanism and real inputs

Candidate a1c48d7, realized_receipt_core SHA256 `9efae4e34a4588413fe59bd2395a19fdcc795a994980bea89e451f5b917898e3`. The preparer transplants only its arithmetic step body and two helpers into a copy of the current production module, retaining production types, all reproductive/movement/mutation behavior, and the original step as the baseline. The experimental pace multiplier is removed, not added to the engine. No schema or production source changes.

Actual preserved 40,962-cell natural30 and natural60 saves each run 10 more simulated days with full coupled climate/water/atmosphere/biology, at 1,440 and 720-second steps, baseline and candidate. `runs.json` pins input hashes, actual game_time, exits, and wall time. Wall time includes validation, duplicate shadow physiology, serialization, rendering/setup and is NOT a performance benchmark.

## Gates and accounting semantics

Every tick checks production validCell (including finite/nonnegative tissue, nutrient, support bounds and lineage range) and finite nonnegative atmospheric O2/CO2. These do not constitute an exact conservation test. Whole-world C/N residuals are reported without invented tolerances, corrective topups, or forced winner. C uses biomass+detritus plus atmospheric CO2-carbon, normalized by mean patch area. N uses free nutrient plus biomass-bound N, summed in f64; no second detrital N pool.

For each real pre-step occupied cell, independent by-value copies run baseline and candidate on the exact SAME Environment and elapsed input. The actual chosen arm then executes independently. The shadow records signed, accumulated absolute, and maximum absolute residuals:
- N: precise after total minus precise before total.
- C: precise biomass+detritus change minus reported fixation plus reported recycling (which already includes grazing/support respiration).
- fixed_over / recycled_over: maximum returned transfer receipt above original CO2/O2 carbon capacity. These are receipt bounds, NOT proof every represented tissue transfer was exactly funded; the C residual and known tiny-N case expose the remaining mismatch.

Shadow includes occupied-cell physiology only, not empty-detritus-only decay, reproduction or relocation. Within each arm both shadows have identical inputs; different actual arms diverge, so their shadow totals must not be compared as identical trajectories. Signed residual can cancel; lower accumulated absolute error does not guarantee a better signed endpoint or smaller worst case.

At each final endpoint: capture→apply→capture must be exactly equal. Two separately restored copies then execute 10 coupled ticks and their complete serialized outcomes must match. This proves restored-state repeatability, NOT uninterrupted-vs-restored cache equivalence. Each actual arm begins from identical independently parsed frozen initial bytes; original world is restored at end. No cross-model trajectory parity is expected.

`ENGINE_PASS` means these structural/save assertions passed, not a numeric conservation threshold. Existing allocator teardown leak diagnostics are retained in logs; they are not interpreted as candidate-specific allocation defects.

## Reproduction

Run `python3 web/tests/egl-receipt-engine-prepare.py "$STELLA_WORKSPACE/site-tmp/receipt-engine/src"`, build with `web/tests/egl-origin-build.zig`, `-Dsource=<generated main.zig>`, ReleaseSafe Zig 0.13, output prefix `site-tmp/receipt-engine/build`, then this directory's `run.py` with STELLA_WORKSPACE set. Input saves must exist at site-tmp/natural60-day30.json and natural60-day60.json with recorded hashes. Native EGL/llvmpipe correctness only, not browser/device validation.

## Measured result

All four processes / eight 10-day arms exited 0. All eight exact save roundtrips, restored continuation repeatability checks, and final original-world restores passed. `endpoints.json` retains full signed/absolute/max paired diagnostics and whole-world residuals.

On identical occupied-cell inputs, accumulated absolute C residual decreased 23.8–24.5% on day30 scenarios and 12.0–13.3% on day60 scenarios. N decreased 1.6–2.7% and 27.6–32.0%, respectively. All returned fixation/recycling capacity-overspend maxima were zero in both models.

This is NOT uniformly improved worst-case error: day60/720s on baseline trajectory had maximum per-step N residual 8.50e-9 baseline versus 1.01e-8 candidate; on candidate trajectory 8.45e-9 versus 1.04e-8. Several C maxima also slightly increase. Whole-world signed endpoints are mixed: day60/720s N magnitude increases from 1.09e-7 to 2.19e-7, while day60/1440s decreases from 2.15e-7 to 9.77e-8. Final colony counts differ (day30/1440: 62→60; day30/720:71→72; day60/1440:56→56; day60/720:50→51). Such differences are reported, not framed as ecological improvements.

Recommendation: evidence supports a bounded average numerical drift reduction, not exact local funding, uniformly improved worst case, or gameplay benefit. No automatic production promotion. Missing uninterrupted-vs-restored equivalence and clean performance profiling remain explicit; neither is implied by these assertions. Native and separate sibling WASM arithmetic tests do not substitute for an actual browser coupled-world gate.

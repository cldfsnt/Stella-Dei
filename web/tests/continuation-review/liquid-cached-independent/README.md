# Independent cached liquid-gather audit

Experimental only. No production changes or device performance claim.

## Executed gate

`zig test src/qa_liquid_cached_independent.zig -O ReleaseSafe`: **2/2 passed**.

Five mixed-scale mass fixtures, three timesteps (0, 1440, 15000), both traversal orders on a reciprocal graph containing duplicate/self slots and a fifth-cell tail. Cached outputs and outgoing edges match naive gather byte-for-byte; both rounding-ledger values match exactly. A changed topology at the same address/count is explicitly re-prepared and matches. Nonreciprocal prepare and offset source/output and elevation/output aliases refuse.

This is a focused finite fixture, not an exhaustive proof. Prepared neighbor/reverse arrays must remain immutable. The fast step intentionally does not revalidate malformed/stale reverse slots. Preparation may partially write scratch on refusal; callers must not use it after failure.

## Lifecycle audit

`prepare-liquid-cached-world.py` owns copied neighbor and reverse arrays in the Planet simulation arena. Count change reallocates/rebuilds; topology pointer change rebuilds; computeNeighbours and successful save.apply explicitly invalidate even at unchanged pointer/count. Arena deinit frees storage. Current graph mutations occur through construction/computeNeighbours. A future in-place topology mutation must call invalidation. Repeated count-changing geometry within one arena can retain prior scratch until arena teardown; existing world construction gives fresh lifetime. No new save fields.

Reverse mapping takes the first matching reciprocal slot; later duplicate edges are zero in the naive law. Self and repeated source-neighbor slots use sentinel255. Gather order of nonzero additions is retained. Read-only arrays may alias each other, but scratch/output byte-range overlap with them is rejected.

## Preserved naive timing failure

Independently read all18 logs and result records and inspected timing scripts. Same-version prior endpoint and uninterrupted/restored comparisons are enforced before recording each result. Three alternating pairs per natural day30/60/90,60 actual simulation ticks, first scratch allocation included; startup/render/saves/scans excluded. Median baseline→naive candidate ms/tick:

- day30:8.2549811→9.3982541 (+13.8495%)
- day60:7.66616097→9.5919551 (+25.1207%)
- day90:8.3738115→10.28841958 (+22.8642%)

Every paired candidate was slower (+8.50% to+46.87%). HOLD that naive version. Cached timing not yet reviewed. Discarded return ledgers may be optimized away, so source arithmetic presence does not prove diagnostic overhead was measured.

Residual reduction alone does not establish acceptable whole-world water closure. The solver changes actual lineage trajectories; no retrospective tolerance or production approval follows from this audit.

# Copied-Planet physics phase profile

Isolated native fixture only, no production source changes. `egl-physics-phase-profile-prepare.py` composes full-frame nursery fixture and instruments only its copied Planet.simulate. One representative established30d workload, 40,962 cells,10 occupied cells/18 cohorts, actual coupled physiology/climate,24 simulated hours/sec requested.12 full-frame warmups then60 measured frames with60 actual1440-second scheduler ticks. Cooperative parallel count measured1. Native mobile-policy390x700 rendering, llvmpipe, no bloom. Same limitations as full-frame-profile: not actual browser/Android performance, not dense biosphere. Initial two-line fixture syntax error fixed before successful run; no engine fix required.

## Measured cost
|Phase|60-tick total ms|Mean per tick ms|Share of classified physics|
|---|---:|---:|---:|
|Temperature initialization + jobs/wait + swap|146.3109|2.4385|20.90%|
|Water inclusive|459.1237|7.6521|65.58%|
|Atmospheric water, nested in water|341.1326|5.6855|48.72%|
|Water excluding atmosphere|117.9911|1.9665|16.85%|
|Organisms plus disabled geology bookkeeping|94.7064|1.5784|13.53%|

Water-inclusive and atmosphere MUST NOT be added: atmosphere is nested. Disjoint totals sum700.141ms; existing scheduler physics reports700.212ms, leaving~.071ms for timer/control overhead. Full update11.6715ms/frame, renderer+finish9.4983ms, total21.1703ms, p9527.9918ms. Timer instrumentation and normal machine variability mean do not compare this one run's total against older means as regression. Exact save restore and final invalid-save rejection/exact restoration pass. Run exit0, existing native allocator leak at shutdown.

## Actionable next experiment, not a proven fix
Atmospheric transport is the strongest measured target (~49% of physics) on this sparse scene. Split its internal wind-cache construction, outgoing edge-rate construction, phase relaxation, donor coefficient, and gather passes before deciding. Current `cachedAtmosphericEdgeRate(n,i)` searches the donor's up-to6 neighbors for every gathered edge; repeated reciprocal-slot lookup is a concrete candidate. An isolated topology-derived reverse-slot cache could avoid those repeated scans without changing edge arithmetic or accumulation order. It must rebuild/validate on mesh topology changes and save replacement, handle pentagonal/degenerate cases, maintain fallback behavior, and demonstrate bit-identical atmosphere output plus meaningful end-to-end timing reduction before production. Do not simply skip dry cells, moisture exchange or ecology to manufacture faster simulation. Geometry-rate caching across ticks requires additional geometry/velocity invalidation and is NOT justified by this profile alone.

## Reproduce
`python3 web/tests/egl-physics-phase-profile-prepare.py <isolated-source>`; build with existing egl-propagule-visual-build.zig ReleaseSafe Zig0.13. Run with same30-day nursery environment flags documented in full-frame-profile README. Isolated copied source gets qa_phase_metrics.zig counters; production Planet remains unchanged. Counters collected only during timed frames, no per-tick I/O. Raw log contains metadata, every frame, phase totals and save checks. Hashes pin production inputs, preparers and copied instrumented Planet to prevent comparison against a different engine unnoticed.

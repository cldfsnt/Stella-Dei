# Protective inactivity: conditional recovery, not a general survival upgrade

One prospective, uncalibrated game law; production and every saved world untouched. Whole-cohort transient state in a copied law3 core, no second biomass pool, schema, inheritance, UI or full-world scheduler. All 12 fixed seven-day arms retained (six conditions, two slot orders). Shared cell/soil/C/N/O2, two actual paid-founder phenotypes; cloned competitor lineage is explicitly experimental, not another player payment. No resource refill. Local prescribed weather, not global hydrology or climate prediction. No bare soil evaporation/rain/transport in this local fixture.

## Day7 living carbon, kgC/m²
|Condition|Protective-capable|Always active|
|---|---:|---:|
|Stable warm, no entry|.07086336|.07086336|
|One dry day then rewet|.03829442|.10697118|
|One263K day then warm|.13609546|0|
|Permanent240K|0|0|
|Permanent400K|0|0|
|Forced paid entry in stable warmth|.06825356|.07403344|

The cold treatment has actual post-stress recovery: .01862538 at end of cold day2, .02723383 day3, .13609546 day7. Entry spent .000605328C; wake occurred only after five1440s favorable intervals. Sixty cold ticks plus five recovery ticks inactive. Existing .0025 extinction cutoff unchanged. Permanent extremes killed both without revival. Forced warm entry spent .000399999C and lost acquisition time, ending below active competitor. In dry weather the active rooted competitor could still use finite soil, whereas inactivity withheld root uptake; inactivity lost. This is a real tradeoff, not an all-weather multiplier.

Original first run caught a copied integration omission: shared_soil computes its own demand independently of Microbes.rootDemand, so suppressing only the latter still delivered water. Assertion failed on the first dry inactive tick. first-run.log is retained. Fixed copied shared_soil to skip inactive demand, no rate/parameter/condition changes. Stable neutral results already exact. Final matrix enforces zero inactive root credits every step.

Local C/N conservation checks remain1e-5 absolute, finite gas/soil bounds each step. Existing core f32 rounding remains, not exact global closure. Slot reversal differences are tiny (dry active endpoint ~6e-9); not claimed bitwise slot equivalence. Unit tests exercise zero-O2 atomic entry refusal, no inactive fixation/root demand/offspring, actual predation on inactive tissue, interrupted recovery timer and no resurrection. Final run passes all38 tests (three local plus imported core tests). Final matrix daily rows exactly match the successful pre-extra-assertion run. No cost/timing claim.

## Why this differs from old rejected pace work
Prior quiescence imposed identical thermal/dry hazard and therefore did not protect against those stresses. Later accounting-fixed slow-pace assays still lost competitive advantage after full recovery. Here reduced stress hazard is an EXPLICIT new phenomenological assumption, not a consequence proved by lower maintenance. It is bounded to253–333K; old hazard applies outside. This demonstrates engineering/game-design feasibility, not biological calibration or evolved selection.

## Integration requirements before any full-engine feature
Persistent per-lineage inactive/recovery state and explicit opt-in law/save identity; legacy state must remain exact. Activity must reach BOTH soil demand paths, physiology, grazing and every birth/transport path. Timers must track lineage and simulation seconds, survive restart and reset on death; no slot-owned stale timer. Current fixture assigns capability and uses one external timer, so it is NOT an inheritance implementation. Define a genuine inherited entry propensity separately, with funded offspring and no trait injection. Keep inactive mass in occupancy, predation and geometry unless a separately funded retraction law is designed. Existing near-cutoff juveniles can still die; no hidden sporebank. Entry/respiration use finite resources, and lack of O2 must never grant free entry.

Next decision: only if desired, a source-reviewed actual-scheduler integration with save/restart and one fixed stress/recovery path. Do not alter parameters to force the dry arm to win. Reviewer owns separate full-world climate calibration. No production deployment or new ecology search authorized by this result.

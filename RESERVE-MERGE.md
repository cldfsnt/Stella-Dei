Isolated candidate, not deployed. Preserves current production sized propagules and all feedback/events, Watch/trend, reset/cache hooks. Adds reserve physiology, proportional paid child water transfer, numeric carries, schema7, paused action normalization. No 25% neighbor-first policy merged.
Base production planet SHA256: 29edccb158b7dd7da6400467fbb0928f3a716262d8880526db6fe631e96a6d5d

Tests: schema/model57, pond6, god45, bridge/model41 all pass.
Native paired acceptance pending. The model changes existing evolution RNG by
adding retention mutation, so old live lineage outcomes are not promised.

Review patches are against the captured working production source at candidate
creation, not just remote master. They preserve new small-propagule logic and
its carbon/support/credit semantics. Child water is funded proportionally at
f64 precision. Parent and child share neither duplicated water nor free carbon.
No old 25%-neighbor-first policy was carried into this candidate.

Atmospheric-water solver itself remains unchanged. The biological bridge reads
actual surface mass plus numeric carry and writes through water_precision.apply;
direct paused water edits call reconcileWaterPrecision. Rebase the narrow
Planet patch onto later atmospheric fixes rather than replacing Planet wholesale.

## First integrated native run caught and fixed a numeric edge
With the new exploratory reproduction trajectory, enabled native reached day99
with a genuine protected shore cohort, then correctly rejected an invalid water
transfer. Four proportional uptake shares summed one f64 ulp above a carry-only
liquid budget: available9.480795576247094e-7, requested9.480795576247095e-7kg/m².
Shares now use the accumulated Flux as their budget, not a separately decremented
remaining variable, and round down if addition would exceed the supply. Ten
thousand carry-only distributions test no overdraft and water accounting.

A separate randomized full-depletion test found cancellation in unit conversion.
An exact debit equal to the public represented available balance now returns
zero directly. This is exact equality, not a tolerance for excessive withdrawals.
One hundred thousand bulk/carry full-depletion cases pass. Bridge/model suite43
and model36 pass; fixed native rerun pending. Reserve-disabled native100d passed
all save/paused-action checks and ended with no shore biomass.

## Fixed integrated native acceptance completed
Current production small-propagule policy + reserve/carry physiology:
- Reserve enabled, world1337 expanded eight explicit Seeds, one basin plus one
  diagnostic shelf edit day20, no subsequent irrigation: one protected shore
  cohort remains at day100; biomass0.016930306kgC/m², water0.43957729824kg/m²,
  measured protection0.98905. Thus integrated reproduction retains genuine
  shoreline survival; this is not universal one-founder land progression.
- Matched reserve-disabled100d control: no shore biomass/reserve.
- Both native runs pass invalid-save rejection, unchanged state after rejection,
  exactv7 restoration and immediate paused fine-drain/pond/wave canonical saves.
- Existing native teardown allocation warnings remain.
- Final unit counts: model36, schema59, bridge43, pond7, god47, all passing.

No live deployment performed. Candidate source is frozen for review. Active
production is unchanged. Atmospheric cycle fixes must be merged independently
using the narrow Planet patch and rerun native acceptance. The shelf action is
still diagnostic-only; a clearly disclosed accessible player habitat pathway
and reserve/retention UI explanation remain release/product work.

## Pentagon mesh padding edge fix
After native acceptance, the isolated candidate additionally skips sampled
self-neighbours before propagule attempt/arrival counters or paid propagation.
A self draw simply does not disperse; no retry bias or extra births are added.

Wave gathers unique nonself neighbours, retaining out-of-bounds/invalid-water
atomic validation, the same donor budget and once-per-affected-cell carry hooks.
Pentagon five-neighbour + self filler, duplicate IDs, self-only rejection and
invalid-index atomic behavior are covered; god/helper/model48/48 pass.
Narrow post-acceptance diffs are pentagon-propagule-only.patch and
pentagon-wave-only.patch. These small mesh edge fixes have not rerun the full
native100d acceptance; the previously measured ordinary basin is not a pentagon.

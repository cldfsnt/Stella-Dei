# Directed-daughter precision experiment (research only)

No production code, UI, save schema or scheduler wiring changed. `src/experimental/directed_sample.zig` and `src/qa_directed_sample.zig` are isolated. This validates a candidate transfer transaction, NOT ecological establishment, natural availability of donor credit, player usability or a shipped feature.

## Actual finding
Across10,000 parent masses0.03 through approximately0.99 with35% support and0.2 credit, existing production `M.reproduce(...,false)` transfers the fixed f32 child amount independently from the rounded parent subtraction. Measured represented total carbon can increase by up to9.313225746154785e−9 or decrease by up to5.587935447692871e−9 kg C/m² per transaction. These are small real representation mismatches, not a new source of significant gameplay resources demonstrated here.

The isolated candidate accepted all10,000 cases with exact f64 sums of represented f32 carbon and support before/after. Free nutrient stores and donor/target RNG were unchanged. Four new test cases plus32 imported core tests pass (36 total). A separate97-transfer sequence retained every daughter in another empty cell and conserved represented carbon/support after EACH withdrawal, with no donor/credit/resource refill.

## Narrow conservative transaction
- Existing production nonmutating reproduction runs on temporary source/target/stats copies, preserving eligibility and child ancestry/history semantics. No live state is committed on refusal.
- Compute a representable parent remainder. If its actual f64 decrement exceeds the requested0.01 f32 tissue amount, move the remainder one representable step upward. The child receives the actual represented decrement, not the original independently assigned0.01. Thus no extra mass can be copied into a child.
- Proportional support uses the same actual withdrawal rule. Both total support and total biomass are conserved; support remains a subset of biomass, not additional carbon. Source and child support bounds are revalidated.
- Earned-credit charge rounds the opposite way: never less than the requested0.04 f32 charge. Receipt states actual debit. A conservative1e−5 relative deviation cap rejects events whose representation is too coarse. This is an explicit numerical-policy bound, not a biological parameter; it was not raised after a failed case. No global correction, residual array or hidden resource top-up.
- Refuse if actual decrement cannot itself be represented exactly as the child f32 amount. This is safe failure rather than pretending exact conservation. Extremely large finite credit, e.g.1e8, fails the narrow charge-precision test atomically.
- Carbon-associated nutrient is implicit in living biomass. Exact represented total biomass and unchanged free nutrient preserve that mathematical ledger. Existing f32 `M.nutrientTotal` aggregate rounding and subsequent physiology drift are NOT repaired here. No claim that every rounded aggregate helper is bit-identical is made.

## Guard coverage
Stale colony ID/world token, bad source/target/slot, same-cell/nonneighbor destination, insufficient credit or tissue, invalid/NaN state, full or near-capacity target, lineage/birth overflow, and unresolved precision all leave source/target/RNG/stats unchanged. Zero, tiny,35%, near-full and fully supported tissue pass. Full inherited phenotype fields and offspring histories are compared with exact expected nonmutating ancestry; child generation increments, earned credit/feeding/movement histories reset as in production. Receipt does not label this as autonomous relocation.

The `neighbors` slice and world tokens are supplied by the caller in this primitive. A future real Planet/player wrapper must derive them from the actual current world and recheck donor selection/ID at execution; the primitive is NOT evidence that an eventual UI already does so. Current production natural reproduction remains untouched. If this is promoted, assess whether a narrowly shared transfer primitive should replace both paths rather than maintaining subtly different accounting.

## Reproduction and limits
`zig test src/qa_directed_sample.zig -O ReleaseSafe --cache-dir /absolute/cache --global-cache-dir /absolute/global-cache` with Zig0.13.0. Initial test compile failed due a helper name shadowing a parameter; corrected test-only names. Failure and passing outputs preserved losslessly. No heavy frame benchmark, browser launcher, actual generated-world assay, survival comparison or performance claim was performed.

Next gate, not done: actual-scheduler donor/target wrapper with current adjacency and owner invalidation, naturally earned eligible donor, matched wet/shallow branches and offspring fate tracing under unchanged physiology. Do not make the feature available by inventing donor credit or claiming a persistent strategy from this transaction proof.

## Deferred research inspiration
Lower maintenance combined with a paid dormancy/recovery lag remains a possible later gameplay hypothesis, not a calibrated biological model or evidence of coexistence. It is not implemented or validated by this transfer experiment. Real-scheduler integration, whole-world gas/carbon/nutrient ledgers over time, and naturally funded descendant establishment remain unresolved gates; exact local transfer bookkeeping does not settle them.

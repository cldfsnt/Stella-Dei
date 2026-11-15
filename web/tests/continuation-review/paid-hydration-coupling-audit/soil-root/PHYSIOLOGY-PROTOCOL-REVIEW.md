# Independent pre-outcome physiology protocol review

Reviewed ec512e1. The36-run fixed actual-full-cell local design is suitable for an isolated hypothesis test after the following semantic details are frozen, without changing proposed rates to favor survival.

1. Specify the exact common aerial water-demand formula and units (including frond mass, light factor, exposure and elapsed seconds). Root and optional storage receipts share that one demand. Do not infer it from a generic phrase or run both old reserve evaporation and new throughflow.
2. Specify the operator split. Kernel changes surface liquid through infiltration/drainage internally, so caller-provided depth/exposure is a start-of-kernel snapshot unless physical phases are explicitly separated. Do not label it post-infiltration geometry. Actual core physiology should receive the resulting surface depth; snapshot differences remain timestep-sensitive and must be retained in1440/720/360s comparisons.
3. Root0 parity means unchanged copied physiology/RNG given the SAME soil-enabled physical path/environment. It cannot mean whole-world parity against no-soil physics, because soil exchanges occur even with no roots. Duplicate root0 conductance arms should match exactly.
4. The held compartment is an external accounted reservoir when recharge can return it, not literally destroyed water. Surface removal/return and setup infiltration require actual represented receipts; total includes held water, with no later silent topup.

Full-cell fixed lineage478, root0/.25 prescription, unchanged total-support maintenance/frond cost, all canopy-support uses audited, no reproduction/dispersal, finite gases/nutrients and no favorable target search are appropriate safeguards. The six-hour preparation is explicitly nonbiological laboratory setup, not elapsed natural evolution. Capacity1kg/m² and the proposed finite rates are hypotheses, not calibrated soil or game defaults. Keep all outcomes and skip/refusal observations; no positive root benefit is required to pass correctness.

A later positive result would establish only usefulness of prescribed paid roots under these finite controlled conditions. Inheritance, from-zero establishment, whole-Planet soil exchange and native f32 receiving precision remain separate gates.

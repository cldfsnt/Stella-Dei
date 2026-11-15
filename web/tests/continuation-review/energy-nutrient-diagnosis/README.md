# Exact diagnosis of four failed nutrient audits

Read-only investigation of production/current research. New isolated probe/core copy only; original energy-cycles assay, experimental core and production unchanged. No tolerance widening, resource correction, refill or intended winner.

## Result: real stored-state rounding drift, overwhelmingly in the core
A f64 audit sums each represented cohort biomass independently times the exact existing f32 nutrient-per-carbon constant, plus represented free nutrient. This avoids the original f32 total's final rounding. It confirms the losses are not merely display/ledger summation error.

|48-day neutral stable control|Sparse|Crowded|
|---|---:|---:|
|Exact stored N drift|−1.8651222136e−5|−1.9557600167e−5|
|Original f32 reported drift|−1.8641352654e−5|−1.9565224648e−5|
|External maintenance contribution|−6.8998904423e−8|−1.7547167719e−8|
|Actual copied-core contribution|−1.8582223232e−5|−1.9540052999e−5|
|Mortality nutrient-store rounding|−8.1156126702e−6|−8.5529197128e−6|
|Mortality biomass rounding|−6.8395019408e−6|−7.1465737320e−6|
|Growth nutrient-store rounding|+3.2437819837e−6|+3.3355138206e−6|
|Growth biomass rounding|−6.8708906043e−6|−7.1760733750e−6|

Both slot orders give identical figures. Four core components sum to core delta within1.39e−16; maintenance+core exactly reconstruct total drift within1e−12. No unexplained biological sink remains in these controls. Maintenance is <0.4% of loss, so fixing its nutrient addition alone will NOT resolve the failure. Core mortality/growth update represented biomass and nutrient with independently rounded planned transfer quantities; their discrepancies accumulate with repeated equilibrium-like transfers. Nutrient-store category includes product/add/subtract quantization. Biomass category is actual represented tissue delta minus intended transfer, multiplied by the same stoichiometric constant.

These are actual f32 storage losses, not a new conceptual nutrient-use pathway. The core code is shared with actual production physiology, but this magnitude was reproduced in a48-day fixed two-cohort experimental maintenance scenario, not measured in the released game. Do not claim a shipped-world catastrophe or a completed production fix.

## Experimental implications
Maximum loss is about0.0109% of initial0.18 nutrient, but about1.96× the declared1e−5 tolerance, so the original audit correctly fails. Neutral controls retain exact slot symmetry; numerical failure does not manufacture a slow-trait advantage in these four cases. Selected unequal-trait plots met their existing ledgers and have much larger biomass separations than this residual, so this diagnosis is not evidence that their qualitative reversal is a numerical artifact. However nonlinear competition can amplify small perturbations: only a corrected, matched rerun can establish how much endpoints change. Do not retroactively mark the72-run sweep passed or assert conclusions invariant under correction.

## Safe next experiment (not implemented)
1. In an isolated accounting-corrected core, base each local transfer receipt on actual represented biomass removed/added, not intended f32 `dead`/`growth`. Use bounded representable changes so receivers cannot gain more than admitted resources; align reported carbon fixation/respiration/reproduction credit with actual transfers. This touches C as well as N, so audit both together.
2. Carry exact local nutrient rounding residual in a compensated f64 pool/ledger or use a declared higher-precision authoritative pool. Residual must come from real local transactions, never a global target-total top-up. A compensated sidecar becomes part of logical resources and must survive movement, copying, save/load and reset correctly; dropping it silently recreates loss. A production representation change needs explicit migration/tests, not a quick hidden refill.
3. Re-run all72 original scenarios with unchanged thresholds, fixed totals, slot swaps, no-resurrection and C/N/O2 accounting; retain old evidence. Add long-run cycling/equilibrium tests and tests at very small/large pools. Then reassess competitive conclusions without requiring any phenotype to win.

## Reproduce and interpretation
`zig test src/qa_energy_nutrient_diagnosis.zig -O ReleaseSafe --test-filter 'diagnosis only'` runs only the four known failing controls. A diagnostic PASS means attribution closes AND exactly4 original-budget failures are observed; it does NOT mean conservation passed. New energy_nutrient_probe_core is the existing research core with additive observation counters only. Separate `--test-filter 'instrumented core at activity'` compares instrumented outputs to actual production scalar fields through240 light/dark steps, proving observation does not change that control.

`run.log` retains all daily values and explicit within_original_tolerances=false outcomes. `core-parity.log` records independent parity. No original evidence overwritten, production edits, commit or deployment.

# Bounded fixed-cohort accounting candidate (research only)

New isolated `experimental/energy_accounted_fixed.zig` and `qa_energy_accounted_cycles.zig`. Production, save schema, original experimental core and original failed evidence are unchanged. This is NOT a corrected general production core. It supports only this wet303K fixed-founder assay: no structure/support/organization/grazing/motility, offspring, relocation, mutation or save/load. A scope predicate rejects unsupported temperature/depth/features/invalid activity; ReleaseSafe entry asserts it. Do not run as unrestricted gameplay.

## Local accounting, not resource creation
- Mortality removes bounded representable f32 tissue. Actual removed carbon, not intended rounded transfer, funds dead carbon and released nutrient.
- Growth admissions are bounded by the finite available carbon/nutrient and shared requested growth budget. Each actual represented biomass increase determines fixed-carbon debit, nutrient debit and reproduction-credit receipt. Rounding cannot overspend the admitted request.
- Free nutrient and dead carbon retain their exact local f32 storage residual in f64. Authoritative amount is represented value+residual; subsequent transfers use it. No global initial-total correction or unexplained top-up exists. Dead-carbon accounting is necessary too: fixing N alone would leave C drift.
- Fixed/recycled gas receipts use f64 actual transfers; respiration remains oxygen-limited. The same existing mortality/uptake/relaxation rates are used for the supported scenario, but transfer representation and rounding are deliberately changed. This is not claimed bitwise-equivalent physiology.
- Credit residual is per slot ONLY because this assay has fixed cohort ownership and no births/movement. It clears when the cohort dies. It is NOT a proposed inherited sidecar; generalizing requires identity-safe transfer and persistent representation/migration.
- The external maintenance assumption remains the prior uncalibrated rate0.2/0.6 experiment, not a newly validated biological law.

## Results under unchanged original audit limits
All72 scenarios (same initial totals, rate/activity/light/density/slot matrix,40days cycles+8days recovery) complete with zero budget failures. Maximum absolute C error7.81597e−14; N error1.05471e−15. Original tolerances remain C1e−4/N1e−5. Gas pools nonnegative, valid cells, no resurrection and slot comparisons pass. The original four baseline failures remain failures in original evidence; this candidate does not retroactively green that run.

Additional local tests cover54 timestep/light/finite-C/finite-O2 combinations including zero/tiny resources; receipts stay within finite funding, C/N ledgers close≤1e−12, and credit equals actual growth. A10,000-cycle tiny transfer/reversal check retains only the local rounding residual. Unsupported grazing/dry/NaN-activity scope is rejected by predicate tests. Four tests total pass with the72-run matrix included. The earlier neutral observation-only instrumented-core parity test remains independently preserved in energy-nutrient-diagnosis; the accounting candidate is intentionally NOT bitwise equivalent, and its behavioral difference is quantified below.

## Matched trajectory comparison
All3456 daily rows match by scenario/day. Maximum fast-cohort biomass difference1.16e−5kgC/m²; slow6.55e−6. Maximum accumulated paid-maintenance difference0.000133537; dead-carbon pool difference3.51e−5; gas difference0.000118579. Values compare logged9-decimal daily observations, not an unlogged exact-state replay. No daily extinction-status disagreements across either cohort.

Slow advantage counts among24 unequal-activity settings (one slotorder): baseline AND candidate2atday20,0atday40,0atday48. Thus correcting these transfer losses does not rescue lasting slow dominance in this matrix. Lower demand still buffers some dark intervals, but faster acquisition recaptures resources. No future phenotype/fitness conclusion is forced, and no offspring/succession/adaptation claim follows.

## Reproduce and next decision
Zig0.13.0 `zig test src/qa_energy_accounted_cycles.zig -O ReleaseSafe --test-filter 'accounted'` runs full matrix and local tests. `compare.py` compares its archived run with baseline energy-cycles/run.log.gz. Logs are losslessly gzip-compressed with deterministicmtime0; uncompressed hashes retained. Source hashes pin this exact candidate and its imported historical functions.

A general core correction would still need funded support, predation, dispersal, reproduction, mixed traits, authoritative gas receipts, save/migration, invalid-state handling and long-run parity/behavior tests. This small candidate demonstrates local conservative bookkeeping feasibility, not production readiness. No deployment or commit by this worker.

# Shared-resource metabolic pace: experimental negative/conditional result

Not production, inherited trait, full scheduler, new species, or shipped mechanic. This follows the prior isolated maintenance-quiescence hypothesis with actual co-resident competitors. No production/schema files changed.

## Model and controls
`prepare-shared-pace.py` copies the current real microbial core and adds only a per-slot multiplier on photosynthetic acquisition potential before the existing shared light/space/resource allocation. The ordinary step wrapper retains pace1. `shared_pace.zig` adds explicit basal maintenance proportional to the SAME pace, then calls this core once for the whole cell: shared finite CO2/O2/nutrient, original mortality, light/space competition, support and grazing/decay code. Assay organisms have no support, grazing or mobility. Lower uptake is not a free lower-maintenance mutation. No resting pool or programmed environmental response.

Maintenance uses analytic finite demand, proportional shared O2 funding, actual represented biomass debit to CO2 and bound nutrient. Unfunded demand gives the same fractional stress hazard to both competitors, inherited from the prior uncalibrated hypothesis (0.5/day maximum); not calibrated ATP biology. Dead carbon becomes detritus, bound nutrient released once. New photosynthetic O2 helps only later maintenance. Remainder rounds upward so represented tissue is not overcharged; retained rounding is reported, not concealed as delivered metabolism.

72 conditions, each run twice with reversed slots: rates0/.05/.2/.6 perday × slowpace1/.5/.25 versusfast1 × stablelight/alternatingdark/limitedalternating × sparse(.1 each)/crowded(.4 each). Full24days at1440s steps. Darkness days2–4,6–8,10–12,14–16,18–20; days20–24 light recovery. Initial shared nutrient .1,CO2/O2 10; limited .005/.05/.01. No replenishment. Outputs days2,4,20,24. All288 endpoints retained. Rate0 is no-added-maintenance control, pace1 no-pace-difference control. No growth-rate or trait substitution during runs; no reproduction or mutation yet.

## Findings
No slow competitor leads atday2 in the36 unequal-pace positive-maintenance conditions. Slow leads12/36 after the FIRST dark interval(day4), only2/36 atday20, and0/36 afterday24 recovery. Thus the isolated-population slow-survival result does NOT translate into general competitive dominance; early dark-endpoint sampling can mislead.

Example rate.2,slow.5,sparse:
- Stable day2 slow.24166/fast.62393; day24 .17049/.74442.
- Cyclic day20 .14320/.44541; after recovery .17107/.74378.
- Limited cyclic day20 .05119/.06826; after recovery .06176/.11685.
The slow competitor actually spends less maintenance, but fast acquisition usually regains the shared budget after light returns. These outcomes are conditional on the model and chosen regimes, not evidence that real dormant organisms cannot compete. No parameters tuned to create a slow winner.

## Validation and limitations
All67 ReleaseSafe Zig tests pass (includes imported core suites). Per-step carbon and nutrient checks, nonnegative shared gases, biomass cap, reversed-slot comparison. Maximum observed absolute carbon drift4.43103e-5, nutrient8.82149e-6, swapped-slot biomass difference5.96046e-8. Maximum cumulative retained-tissue maintenance rounding7.73072e-5. Tolerances1e-4 carbon/1e-5 nutrient/1e-5 slot biomass: not exact arbitrary-duration closure. Generated pace1 control compared production core nutrient and cohort biomass for an identical step; not a full-field production-equivalence proof. Invalid pace refuses atomically; zeroO2 darkness yields zero paid respiration and full deficit, no free resource creation. Initial compile-time cross-module test conversion error retained separately, then corrected without changing physiology.

No inheritance, reproduction funding, dispersal, climate scheduler, natural phenotype derivation, invasion-from-rare, or long-run coexistence tested. Existing efficiency is NOT renamed metabolic pace. Recommendation: do not ship this parameter yet. Next useful test would be invasion-from-rare over repeated full cycles and physiological calibration, rather than changing thresholds to force succession. The more immediate natural-world bottleneck still needs event-time establishment-loss measurement.

Reproduce: run `python3 web/tests/prepare-shared-pace.py`, then `zig test src/qa_shared_pace.zig -O ReleaseSafe`. Generated source pinned with production source hash. Full log losslessly compressed.

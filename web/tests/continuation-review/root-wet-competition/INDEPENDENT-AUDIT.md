# Independent wet competition audit

Reviewed committed experiment 071a85e without rerunning its simulation or changing sources. Read the preregistration and complete fixture before execution; then independently parsed all 252 daily records and 36 endpoints from the retained compressed results.

## Checks performed

- Recomputed SHA256 for all three entries in `pre-run-hashes.json`; the fixture, experimental physiology core, and donor input match exactly.
- All 252 records have unique pair/slot-swap/ID-swap/timestep/day keys.
- Every ID-swapped daily result is identical after removing only the ID-swap flag and cohort lineage labels.
- Both equal-allocation controls remain exactly 50/50 every observed day. Their per-cohort biomass is identical between root0/root0 and root.25/root.25 at matching timestep, day and permutations.
- Root0 is the sole surviving comparison cohort at all 12 unequal-pair endpoints.
- Maximum slot-swap biomass difference across daily observations is **2.0116567611694336e-7 kg C/m²**. Maximum at endpoints alone is **1.4901161193847656e-8**. Trajectories are not slot-bit-identical; the observed fate/direction is unchanged.
- All recorded maximum carbon and nutrient residuals remain within the original 1e-4 limits; water residual is zero throughout.

The fixture asserts exact initial biomass/nutrient totals, half-donor support/credit/feeding history and original RNG; each core step validates cohorts and finite nonnegative gas pools. These are laboratory accounting checks, not exact conservation of all f32 biological transfers.

## Interpretation

The initial measured light asymmetry is real in the implemented shared-resource core. Feeding was deliberately retained, so subsequent grazing and nutrient feedback can amplify the asymmetry; this experiment cannot identify the direct cause of disappearance or isolate a grazing-free canopy effect. Identical equal-allocation controls support a relative interception cost, not a general absolute productivity penalty.

The source phenotype is fixed, synthetic comparison IDs are not genuine offspring, environmental light/temperature are prescribed, water is held unchanged, and there is no reproduction or movement. This is not evolution, whole-world ecology, device performance, or production-enablement evidence. No blocking reporting defect was found.

# Shared-pool metabolic pace: actual fixed-cohort competition, experimental only

Production unchanged. `prepare-energy-community.py` creates an isolated copy of the current actual microbial core, recording its source hash. Only step signature/wrapper and a multiplication of each cohort's uptake potential by its assigned activity are changed. The ordinary step wrapper uses all1activities. `qa_energy_community.zig` adds common maintenance before that copied actual step. Neutral-activity copied core matches actual production cohort/flux/nutrient/detritus/RNG fields exactly over240ticks. All66tests pass, including both copies' original32tests.

## What this tests
Two genuinely co-located cohorts compete in ONE actual Cell with shared CO2, oxygen, nutrient, light and space. Not two isolated runs joined afterward. Fixed assigned phenotypes: fast activity1, slow0.25/0.5/1. The same activity factor scales both real tissue-funded basal maintenance and actual acquisition potential. All other traits identical. No dormant compartment in this narrower assay; no descendants, mutation, spatial dispersal or claim of evolved/inherited metabolic pace.

Uncalibrated assumptions: basal rates0.05/0.2/0.6perday, common unmet-O2 stress hazard0.5/day. Existing core baseline mortality remains. No fire/dry bonus. O2 allocated proportional to demand; actual represented debit drives gas receipts. Unfunded demand creates equal fractional stress for both cohorts. Decay subsequently receives remaining O2; new fixation helps next maintenance step. Directed-down f32 capacities avoid prior upward-rounding overdraft. Per-cohort activity is not secretly equated to existing inherited light-efficiency.

## Grid and controls
108runs =3basal rates ×3slowactivities ×3environments ×2startingdensities ×2slotorders. Each20days at1440s. Stablelight; alternating2days light/2days dark starting day2; same darkschedule with low shared resources. Low-density begins0.02percohort, crowded0.4each. Normal free nutrient0.1, CO2/O2=10each; limited0.005nutrient, CO2=.05,O2=.01. No refills. Within each competitive pair initial biomass/resources are equal, slots swapped. Across density settings total initial boundcarbon/nutrient intentionally differ: density results are NOT a pure fixed-total-resource manipulation. No runtime transfers create the competitor or help a prescribed winner.

## Results: isolated persistence does NOT establish competitive superiority
Only2of54parameter/environment/density settings give slow greater day20biomass (excluding slot duplicate): both at high basal0.6, initiallycrowded, alternatingdark, slowactivity0.25or0.5. Fast is otherwise larger or equal. This is a sampled finite-time comparison, not extinction/invasion fitness or universal winner.

Example basal0.6/activity0.5/initiallycrowded:
- Stablelight fast0.47371 vs slow0.29696living. Maintenance spent5.11192 vs2.05046kgC/m².
- Alternatingdark fast0.11702 vs slow0.14967. Maintenance3.08590 vs1.58581; stressdeath0forboth. Here slower resource use preserves more living tissue through the dark endpoint, without a stress-immunity bonus.
- Limiteddark fast0.07337 vs slow0.01329. Maintenance1.43098 vs0.46638; stressdeath0.60940 vs0.39813. Shared shortages and reacquisition change the outcome: low expenditure is not automatic dominance.

At basal0.2/activity0.5, slow trails fast in EVERY shared setting, even though prior isolated physiology runs favored its persistence under dark/limited conditions. For crowded alternatingdark fast0.35280 vs slow0.25321. This directly guards against turning isolated survival into a selection claim. Day20 ends in darkness; recoveries and full-cycle trajectories require further tests.

## Accounting and order tests
All steps validate finite nonnegative gases/cells and C/N totals with unchanged1e-4/1e-5bounds. Observed snapshot maxima3.775e-5C and7.034e-6N. Extinct identities remain zero. No resurrection.

Initial exact whole-state slot assertion failed on unchanged core's one-ULP detritus accumulation; failure log preserved. Final declared1e-5comparison measures actual differences, NOT bitwise invariance: maxliving1.863e-8, maintenance4.750e-8, stress5.960e-8, detritus5.960e-8, gas4.981e-8. No observed swap changes qualitative result. No production rounding change was made.

## Meaning for playable strategy
A coupled slow-growth/lower-demand strategy can yield a conditional shared-resource advantage under these assumptions, but limited to2testedsettings and NOT evolved. It is worth an explicit experimental mode only after parameter calibration, full-cycle/spatial lineage tests and complete accounting/schema work. It is not grounds for silently changing all saved organisms or naming existing light-efficiency metabolic pace. Reusing that existing trait would require a distinct hypothesis: link its actual respiration demand to its existing uptake behavior, test costs and inherited descendants, and explain changed meaning. Current experiment does not establish whether a new schema field is necessary.

Next bounded step: maintain total initial C/N across density comparisons, follow whole light/dark cycles longer, and add genuine donor-funded offspring/inheritance in the copied scheduler. Then check whether low-demand descendants establish rather than merely preserve larger founders. Resting-pool integration, predation and movement remain separate.

## Files and reproduction
`src/qa_energy_community.zig`, generated `src/experimental/energy_community_core.zig`, `web/tests/prepare-energy-community.py`. Recreate copy with preparer; run `zig test src/qa_energy_community.zig -O ReleaseSafe` (Zig0.13.0). Logs/results.json/source hashes saved here. No production edits, commits, pushes or deploys.

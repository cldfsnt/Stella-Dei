# Proposed finite handling cost from paid Origin structure

Read-only design after live Wind artifact099bd74/releasea629e6e; no model edit or experiment. Builds on c3ff7d3, not a claim that aerial allocation increases growth. Source: isolated released Wind simulation/microbes.zig graze/step/reproduce, Planet.applyMicrobeFlux and environment. Existing single-founder failure and broader seven-day results remain unchanged.

## One minimal mechanism

At the existing simultaneous grazing snapshot, for a valid living prey with carbon B and paid support S, define d = structure * (S/B). Proposed predator-to-prey request = OLD request / (1+d). Retain an explicit old arithmetic path when structure==0 or S==0 and for the disabled historical law. Do not renormalize the reduced requests across other prey. This models finite handling effort spent on defended food, not perfect preference or free recovery of lost feeding time. Keep old oxygen scaling, simultaneous source caps, gains/waste and support-removal rules initially unchanged, subject to ledger tests.

No new trait, biomass floor, resistance reservoir or assigned genotype. All valid d are in[0,1]; handling remains[0.5,1], so even maximally defended tissue remains edible and local extinction possible. Small paid support gives a proportionally small benefit, continuously approaching zero. The coefficient1 is an explicit illustrative one-extra-unit handling cost at d1, not calibrated biology and not selected from outcomes. Do not adjust it to obtain coexistence.

## Existing costs and exact meanings

B and S are kg carbon/m²; S is a subset of B, not extra mass. Structure, organization, feeding and d are dimensionless. Existing grazer request is min(other biomass, predator B*3*feeding*days), distributed among prey by biomass. Thus3 is a per-day ingestion coefficient, not new energy. Half consumed carbon becomes predator biomass/reproductive credit; one quarter is respired and one quarter detritus. With nutrient_per_carbon=.1, half the bound N is retained in predator growth and half returned locally. Oxygen is capped using the respiration carbon requirement. Atmospheric conversion uses C:CO2:O2=12:44:32 and actual mesh area; native gas inventories are average10^9kg per point.

Structure already multiplies positive photosynthetic input by(1-.5*structure) and adds .10*structure/day wet mortality. Actual growth allocates organization fraction to support, reducing active frond B-S. Support consumes up to .12*S*(1+.4*max(0,efficiency-1)) carbon/day with oxygen-limited respiration. Support is inherited as a paid subset at division; ordinary founders have none. Grazing proportionally removes support with prey biomass and can fund predator support via its organization. No extra arbitrary cost is needed merely to balance a desired result.

## Boundaries and possible failures

- Oxygen-limited consumption can erase the handling benefit when enough total request remains to use all oxygen. Report this interaction rather than forcing protection.
- A predator is also edible prey. This is not a plant-only or species defense rule; mixotrophs may benefit too. No label-based exemption.
- Sparse real support and small structure may give negligible practical benefit. Do not amplify based on a disappointing trial.
- Reduced feeding can starve grazers, reduce nutrient recycling or favor tender competitors elsewhere. No guaranteed succession/winner.
- Existing birth-slot capacity, thermal match, shared gases and local light can dominate. No occupied-patch replacement change.
- Large timesteps saturate food caps and need refinement checks; a finite factor is not timestep independence.
- Current grazing uses f32 accumulated gains/losses, not the stronger downward-rounded growth ledger. Preserve and measure represented source/receiver residuals; adding a demand factor cannot justify exact-real conservation claims. Any material new over-credit is a blocker, not permission to widen tolerance.

## Compatibility and bounded gate proposal

Use a separately persisted explicit handling law in an isolated copy. Existing schema11 Wind loads historical handling, schema7 classic remains untouched. A new save identity must require a recognized new-law field, reject unknown/missing identities atomically, preserve every existing trait/RNG/serial and keep new-world defaults historical until explicit opt-in. Do not repurpose wind_dispersal.law (routing) to silently change feeding. No production schema number chosen yet.

First gate: actual graze/step with fixed four-slot fixtures, not another long world search. Include empty; no feeding; zero oxygen; one prey/predator; two competing predators; mixed tender/defended prey with swapped slots; fully occupied four cohorts; dt0/360/720/1440 and one-day cap case. Defense dimensions: structure0, support0, finite tiny S, and S/B .25/1 with structure .5/1. Keep all carbon/N/oxygen/detritus/support/reproductive-credit endpoints and actual represented debit/credit. Test invalid input refusal at validated API boundary, no NaN or fabricated floor. Explicit legacy-disabled and d0 trajectories/RNG must be exact.

Then, only after review, one fixed14-day local actual-core control set: paired grazed/ungrazed supported and unsupported cohorts with matched total initial carbon/N/thermal traits, and a fixed mixed established four-slot cell versus an initially vacant recipient in actual paid reproduction controls. These prescribed phenotypes are mechanism tests, not evolved-world proof. Record costs without grazing, paid gains/losses with grazing, births/refusals, starvation/extinction and timestep refinement; no extra horizons or favorable parameter search. A full-world player trial, inheritance/save continuation and runtime screen would be a later gate, not implied by passing local controls.

## Player-facing interpretation

If supported by tests, describe it as paid structural tissue making grazing slower. Do not call Pioneer a fast-growing weed or promise forest succession. Real visible support/structure, actual grazing receipts and retained costs should explain the decision; no new cosmetic species or forced winner is needed.

## Actual saved-population scale check: likely too subtle for the immediate Wind goal

Read-only census of every living cohort in the fixed endpoints, reproducible with web/tests/structure-handling-census.py; complete positive rows/source hashes in structure-handling-census.json.gz. Percentages below are hypothetical request reductions d/(1+d), NOT measured feeding or survival effects.

| Existing endpoint | Living / positive d | Positive d with another feeding cohort | Maximum reduction | Biomass-weighted reduction | Cohorts at least1% |
|---|---:|---:|---:|---:|---:|
| Wind ordinary day7 |239 /8|3|0.36036%|0.003712%|0|
| Wind Pioneer day7 |246 /8|4|0.24503%|0.001475%|0|
| Wetlands law3 day21 |1140 /562|511|2.68377%|0.085648%|12|
| Historical beta law1 day30 |1015 /606|497|3.51386%|0.218347%|97|

The later two worlds are different saved biological laws, not longer Wind replicates. Co-location with positive feeding means potential exposure only, not proof of realized grazing in that interval. Oxygen limitation/source caps may further reduce actual differences. The Wind maximum d values are .00361664 (ordinary) and .00245629 (Pioneer); the later maxima are .0275778/.0364183.

Recommendation: do NOT sell this coefficient-one proposal as a visibly meaningful immediate Wind defense strategy. Existing day7 tissue and structure multiply to a very small effect; the later populations still show modest average changes. The law is coherent and testable but presently a poor candidate for the requested tangible gameplay milestone. Do not tune its coefficient until a winner appears, and do not manufacture defended founders to claim natural accessibility. Any reconsidered biological scaling requires a separately declared mechanism and controls, not reinterpretation of this census. No model changes or new ecological runs occurred.

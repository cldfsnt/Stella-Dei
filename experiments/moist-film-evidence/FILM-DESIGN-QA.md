# Experimental moist-film physiology (not deployed)

NOTE: The completed30/100-day evidence below uses preserved `variants/abrupt/microbes.zig`. Current candidate contains approved smooth15–20cm fixation/exposure transitions, tested against paired1337/1338 worlds below. Do not mix variant evidence.

Baseline: release/v26-render-work `d97624d7931f4d8a02e6d5457ea8c14c7aca1e03`.
Isolated candidate, schema 6 unchanged. Frozen previous UI and ecology evidence are untouched.

## Mechanism and scope

Actual support fraction `s = support_mass / biomass` and inherited structure `t` jointly provide film protection `P = s/(s+.005) * t/(t+.02)`. Without either real paid support or structure, P=0. These constants are phenomenological game parameters, not measured plant biology.

Between zero and 20cm of actual surface liquid, photosynthetic habitat fitness is `P * sqrt(depth / .2m)`. The response does not give a free trait, tissue, carbon or reproduction credit. Support remains part of existing carbon, costs respiration, displaces photosynthetic fronds, and structure retains its existing growth penalty. Photosynthesis is strictly zero with no liquid, or temperature <=273.15K; the latter also closes the preexisting aquatic frozen-fixation loophole. Seed eligibility remains aquatic-only. Ordinary paid propagules may still reach hostile cells and die.

Film mortality includes existing thermal/trait costs plus `4*(1-hydration)*(1-P)^2` daily drying stress. Exposed-height damage is reduced by `(1-P)` only when a nonfrozen film exists. Fully dry mortality remains unchanged. No new stored water, soil water, automatic irrigation, freeze immunity, animal evolution or vascular plants.

Water is an environmental prerequisite only, as in schema6 baseline. This candidate does not implement chemical water uptake/transpiration. It never modifies liquid/vapor arrays and adds no hidden reservoir. Local carbon/nutrient fluxes remain accounted; climate water numerical error must be reported separately in coupled tests rather than claimed exactly conserved.

## Current verification

- Final model28/28 tests pass. Includes zero-liquid/frozen fixation, no-support and no-structure counterfactuals, carbon/nutrient accounting, real paid propagule transfer, and existing inherited-form evolution tests.
- Final schema43/43 tests pass.
- Synthetic four-day controls start at0.1kgC/m²,4% support,structure0.1,303K,half-day daylight. Supported phenotype reaches0.1604kgC/m² in5cm; no-support/no-structure controls die. In1cm it declines to0.0511 despite some fixation;1mm declines with no fixation;dry all die. At1m aquatic depth, unsupported control0.9238 exceeds supported0.8812, an actual construction/maintenance tradeoff. These assigned-phenotype controls do NOT prove natural evolutionary emergence.
- Coupled one-seed Continents nursery pairs completed below. Film-on/off arms use same serialized initial state, fixed1440s physical quantum, existing nursery/seed callbacks and no subsequent care. Release gates remain unresolved.

## Integration boundary

Only `src/simulation/microbes.zig` changes production physiology. All toggles, diagnostics, selected experimental nursery location and deterministic fixtures belong only to generated harness source. No schema change; no production UI edits. Existing labels still describe aquatic-only growth and would require coordinated truthful updates before release. This is not yet a release candidate.

## Independent review and remaining boundaries

Independent reviewer reproduced26 model passes and found no new carbon/nutrient transfer defect. Existing20cm aquatic habitat boundary remains: just below it fitness is protection-limited; at20cm it becomes1 even for unprotected ancestors. An explicit epsilon-boundary and240 alternating-depth update test records this discontinuity and resource conservation. It is NOT claimed continuous across the inherited aquatic cutoff. This should be revisited for smooth player feedback before release, without disguising loss of an ecological constraint.

Grazing and whole-cohort relocation still require the existing aquatic habitat. This is a producer-specific film experiment, not a general shoreline foodweb. Support respiration is oxygen-limited (baseline behavior), so a zero-oxygen environment suspends that cost; frond allocation and structure efficiency costs remain. Save bytes remain compatible, but loaded worlds intentionally obey changed physiology, particularly the newly strict frozen-fixation guard.

## Actual coupled30-day pair (completed)

Both arms start from byte-identical actual schema6 world after one ordinary nursery action and one simple seed at30114 in deterministic Continents world1337. The preexisting harness repeats the idempotent nursery callback once before simulation, but does not repeat care after time begins; no traits, biomass or carbon are assigned. Actual fixed1440s physics quantum. Film-off only disables the new thin-film physiology, retaining the strict frozen guard inboth arms. Native render/save engine, not browser or Android verification.

Final serialized results (daily reports run just before last tick, so slightly differ):

|Metric|Film on|Film off|
|---|---:|---:|
|Living cohorts|29|15|
|Summed biomass kgC/m² across cells|0.3117265|0.1804180|
|Cohorts below20cm|9|1|
|Below20cm biomass sum|0.0970348|0.0033485|
|Cumulative shallow fixation by last daily report|0.0131533|0|
|Strict zero-liquid fixation|0|0|
|Frozen fixation|0|0|

Natural shallow descendants generation2–3 occur at13–18cm, descended from ordinary seeded ancestor; no assigned phenotype. No outgoing paid birth from a film source recorded byday30. This establishes some naturally reached shallow fixation/survival, not yet self-sustaining independent shore lineages. The unchanged100-day extension completed below.

Both exact saved-state restore and invalid-save atomic rejection pass. Both retain known shutdown allocator-leak warning. Whole climate water loses~2.45375e-5 ofinitialwater in30days, almost identical acrossarms; not exact conservation. Compact fixture/ledger summaries inresults/paired30-summary.json; full local initial/final JSON retained. No chemical water uptake added.

## Abrupt-boundary variant100-day pair (completed, NOT release-ready)

Preserved source:`variants/abrupt/microbes.zig`; exact generatednative source remains`tmp/source`. Initial byteidentical acrossarms. Compact results:`results/paired100-summary.json`.

|Metric|Film on|Film off|
|---|---:|---:|
|Occupied cells|99|73|
|Living cohorts|142|112|
|Biomass density sum|6.8930057|3.5317766|
|Cohorts in<20cm|28|6|
|Biomass in<20cm|0.5942204|0.0211955|
|Shallow fixation (last daily report)|3.7999632|0|
|Paid outward births from<20cm|235|1|
|Zero-liquid/frozen fixation|0/0|0/0|

The off-arm's single shallow-source birth proves event depth alone does not establish shallow-funded reproduction: previously earned credit can be carried across changing water depth. On-arm minimum birth-source depth13.575cm; do not call this dryland evolution or1cm establishment. More biomass/cohorts in this particular pair, not universal advantage or validated realplant physiology.

Coupled carbon residualon+128266kg/off+30196kg; nutrients−2835kg/+2346kg; climate water loss~1.0053e17kg/~0.32m globalequivalent, preexisting climate conservation limitation. Local tests remain conservative within f32 tolerances; do not conflate those with exact wholeplanet accounting. Final schema6 restore exact; known native shutdown leak remains.

## Follow-up smooth-fixation variant (paired evidence completed below)

Parent approved blending shallow-film response with smoothstep aquatic submergence over15–20cm. At<=15cm unsupported/no-structure ancestors still have zero photosynthetic habitat; actual supported+tough descendants can exploit thinner liquid. Both converge continuously to fitness1 at20cm. An epsilon boundary/oscillation regression passes; full model27/27. This changes behavior in15–20cm even for unprotected ancestors, intentionally disclosed rather than mislabeled a purely inherited ability.

The next pair repeated deterministic1337 and a second1338 world, one nursery/one seed, without subsequent care. Added diagnostic conservative lineage credit lowerbound: accumulate actual credit increases only atdepth<15cm, subtract *every* paid reproduction creditcost, and log only when sufficient such remaining credit funds a subsequent propagule. This distinguishes newly earned thin-film production from wet-earned reproductivecredit. Diagnostics live only in copied harness source, do not alter model/RNG/save.

## Smooth-fixation paired100-day worlds (completed)

One initial nursery and ordinary simple seed, no later care or assigned traits, seeds1337 and1338. Same saved initial state within each pair;1337 initial also matches earlier abrupt fixture. Both control arms share the frozen-fixation correction. Model differs only by experimental film response in on/off comparison. Reproducible compact results in`results/smooth-1337/summary.json` and`results/smooth-1338/summary.json`.

|Seed/arm|Occupied|Living cohorts|Biomass sum|<20cm cohorts|<20cm biomass|
|---|---:|---:|---:|---:|---:|
|1337 on|104|153|5.672069|30|0.501216|
|1337 off|73|112|3.531777|6|0.021196|
|1338 on|73|138|3.710333|20|0.211037|
|1338 off|55|77|2.907847|0|0|

Strict dry and frozen fixation remain0 inall four runs. Last-report shallow fixation3.910428(1337on),1.218170(1338on),0 controls. Outward births from<20cm286/1 and59/0; these alone do not establish funding origin.

Conservative new-credit tracker establishes3 births funded by >=.01 credit actually earned while<15cm in1337,4 in1338,none controls. Two of1337's births occurred at14.58cm and13.43cm (third15.75cm). All four1338 events occurred at13.05–14.88cm. Each consumes existing parent biomass/credit with standard mutation; no new propagation rate or gift. Tracked parents persist today100:1337 parents at12.6–13.2cm,generation4;1338 parents at11.32cm,generation5/8. **All seven specifically tracked offspring were absent byday100.** This is evidence of persistent natural thin-water producers and exploratory paid reproduction, not proven establishment of those descendants, drought growth, species diversification, land plants or a self-sustaining terrestrial foodweb.

QA tracker is copied-harness-only, no biological/RNG/save effect. It excludes inherited newborn credit and subtracts every successful reproduction cost before attributing remaining shallow credit. It assumes one advancing world perprocess (true ofthese separate invocations); globals are not suitable for cross-load/rewind analysis. Lineage IDs>=65536 would undercount. f64 .01/.04 bookkeeping differs by tinyrounding fromf32 production costs; counted events have margins>.002 above the threshold, so none is a threshold-rounding claim. It tracks<15cm photosynthetic credit only; grazing cannot operate there inthis producer-limited experiment.

All four schema6 full-save equality/invalidsave checks pass. Whole-world accounting remains approximate:carbon residuals1337on+205539kg/off+30196kg;1338on+46271kg/off+73273kg. Nutrient residuals−7094/+2346kg and−7811/−2803kg respectively. Climatewater losses~0.320/0.343m globalequivalent, present incontrols. Do not represent these worlds as numerically closed to biological precision.

## Final tall-form exposure fix and remaining release gates

The smooth-fixation variant could still abruptly lose protection against exposed-height damage at20cm for unusually tallforms. Current source now blends that protection tozero using the same15–20cm smoothstep. Added tall-form epsilon comparison passes; full model28/28. Actual paired trajectories have maxorganization.22919/.30123; all initial support=0 and every tissue allocation is bounded by this historical max, so maximum possible heights are7.73cm/11.21cm, below15cm. The final fix is therefore inactive in these actual pairs. Final native replays ofboth on-arms pass exact entire saved-world byte equality with their respective smooth-fixation results (results/final-equivalence.log). Thus both complete100-day measured outcomes hold on final model, not merely by inference from the height bound.

Mandatory before any deployment: coordinate honest seeding/guidance with strict273.15K fixation floor (current eligibility uses260K); update waterline UI toactual producer suitability rather than old20cm blanket block; retain grazing/movement scope warnings; run current-master merge/WASM/UI tests. Existing savebytes need no migration, but simulation rules deliberately change. No production edits or deployment have occurred.

Final verification: model28/28, schema43/43, native full-engine paired100-day tests inboth seeds and final exposure-smoothed on-arm exact replay pass. WASM/current-master merge and hosted/mobile UX testing have NOT been run for this experimental biology patch. No deployment claim.

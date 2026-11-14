# Reserve v7 acceptance status

**Experimental, not integrated into the deployed game.** No seedbank or fire behavior is implemented.

## Passing model/schema checks

- 33 microbe tests and full50 schema/model tests passed.
- Exact water ledger through real uptake, evaporation, water-limited growth, maintenance/capacity overflow, death, reproduction, grazing and relocation.
- Limited water shared proportionally, frozen water cannot fund fixation, zero liquid+reserve cannot fund fixation; finite drought ultimately kills.
- Independent retention reduces water demand/loss but slows wet photosynthetic uptake. In the dry fixture high retention fixes roughly twice as much carbon from its finite initial reserve; low retention grows faster while water is ample.
- Version7 exact sparse save roundtrip, legacy≤6 zero defaults, and finite/range/capacity rejection pass.

## Actual coupled world: local-first comparison

Reserve enabled and disabled, identical new retention-mutation schedule, original local-first reproduction, one ordinary founder, actual basin and one diagnostic shelf action, 100 days each. Both passed native invalid-save rejection and exact restoration. Neither produced a lasting shore population. Only one shelf propagule arrived on this new RNG path; it had no inherited toughness, so it was not evidence of a reservoir-enabled protected shore strategy.

This is a genuine incomplete emergence result, not proof of unavailable water or reservoir failure. Completed bounded neighbor-first and expanded-seeding comparisons are reported below; no extra births, forced mutations or biomass were introduced.

## Measured environmental trace replay

Sixty actual 24-minute samples from a coupled-world day supply depth, light and temperature. A protected fixture matching the recorded descendant's known traits (unknown efficiency/mobility defaulted, so not an exact genotype reconstruction) grows from0.01 to0.04486 after30cycles with reserves; naked control dies. The same recorded-trait fixture previously failed without a reserve. Carbon/nutrient accounting passes; frozen fixation is zero. This is controlled physiological evidence, not a substitute for natural mutation/dispersal acceptance.

Parameters (20kg water/kgC biomass plus60kg water/kgC support capacity, finite carbon-water demand and retention tradeoff) are phenomenological game ecology, not measured species-specific physiology. The fine shelf is still a diagnostic intervention, not an exposed player tool.


## Completed natural-path comparisons

All runs use production mutation/reproduction, no assigned biological traits, one explicit basin action and a diagnostic-only shelf action on day20, with no later irrigation. Expanded cases use **eight explicit Seed actions across seven cells** (initial center seed plus seven more, including center again).

| World/path | Reserve on, shore at day100 | Reserve off, shore at day100 |
|---|---|---|
|1337, one Seed, local-first | extinct | extinct |
|1337, one Seed,25% neighbor-first | extinct | extinct |
|1337, expanded seeding,25% neighbor-first | four protected cohorts, biomass0.06266361, stored water1.4209771kg/m² | extinct |
|1338, expanded seeding,25% neighbor-first | extinct (aquatic system still has18 supported cohorts) | extinct |

For the successful1337 path, lineage26 naturally arrived before shelf conversion and bred shore children96 and202. More importantly lineage149 naturally dispersed into the already exposed shore on day61.37, at only1.8mm external water, and grew from0.01 to0.02095 by day100. No hidden irrigation or genotype assignment. Four cohorts remained at day100 with actual paid support and water.

The disabled control receives genuinely generated protected arrivals as well, but no sustained shore population. The measured trace replay supplies a more tightly controlled physiological comparison; whole-world trajectories can diverge as biological outcomes change RNG eligibility.

Every completed native run passed invalid-save rejection and exact restoration. Native teardown still reports the pre-existing allocation warning. Whole-world water accounting includes tissue reserve, but climate simulation float error and the explicit shelf edit prevent calling that a closed precision ledger; isolated ledger tests are the exact conservation check.

World1338's shelf was only roughly1.6–3.2mm at daily sampling, compared with~22mm in successful1337. This is a measured difference, not a proven sole cause of failure. Natural shore emergence is habitat/founder dependent, not universally reliable from one Seed. The reserve mechanism is demonstrated; a user-facing accessible shore tool, reserve readout, habitat guidance and integration playtest remain necessary. These are shoreline producers, not vascular land plants or evolved animals.


## Independent review: numerical bridge is not yet integration-ready

The current Planet bridge stores bulk liquid/vapor as f32. A requested0.0001kg/m² uptake from a15m cell can round to zero bulk debit while a cohort receives reserve. Isolated f64 reservoir tests do not cover that loss of significance. Before production integration, quantify biological-scale error across step sizes and implement/review approved nonnegative f64 precision carries with old-save defaults0. Native save acceptance above is real, but it does not imply exact coupled water conservation.

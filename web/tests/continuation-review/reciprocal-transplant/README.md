# Reciprocal transplant of naturally evolved phenotypes

## Provenance and execution
Production code unchanged. Rerun actual Planet depth-only180-day evolution, seeds42/1337/2027, then select largest living cohort from wet13-cell background and shallow6-cell patches. Full donor traits and lineage printed in donor.csv. These donors evolved through real funded mutation/reproduction; the subsequent transplants are controlled fixtures, NOT a natural-world simulation.

Build exit0 after one fixture correction. All3 actual scheduler evolutions,48 monoculture assays,24 co-cultures and imported tests pass. Every assay tick checks valid cell, nonnegative gases and carbon/nutrient closure within0.0001. Evolution checks tolerance0.001. Original failed run preserved in first-fixture-failure.log: initialized daughter holding cells inadvertently carried default0.02 nutrient, caught by ledger. Corrected to0. This was probe bookkeeping, not production ecology; no production fix made.

## Design and terminology
Each transplanted cohort starts biomass0.1, zero reproduction credit/grazing history. Tissue0 preserves actual evolved support:biomass ratio. Tissue1 assigns both the mean of the pair's support fractions; inherited organization, structure, feeding, mobility, efficiency and optimum stay unchanged. This is tissue normalization, NOT normalization of all inherited traits. Support is paid from fixed total biomass, never added on top. Tissue-normalized states may depart temporarily from trait equilibrium; physiology can adjust them.

Wet=habitat0 (1m); shallow=habitat1 (8cm), both303K. Finite CO2/O2 pools10 carbon equivalents each, nutrient0.12, actual M.step1440s,30-day day/night at light1/0. Same resources within each comparison. Pair has total initial biomass0.2; monoculture0.1, so pair and single absolute totals are not resource-matched comparisons. Pair assays have no reproduction; swapped0/1 switches donor slots. They test equal-abundance competition/grazing and survival, NOT rare invader establishment.

Monoculture breed0 has no reproduction. Breed1 uses real funded nonmutating M.reproduce at most once per tick, then exports each0.01 daughter to an inert accounting ledger. Exported carbon/nutrient remain in conservation checks, never recycled or simulated. `held_daughters` is exported biomass; `total_living_produced` is parent plus exported accounting mass, NOT demonstrated surviving descendants. Counts measure funded parental offspring output, not multigenerational populations. Production Planet scheduler is only used to evolve donors; assays use M.step directly. No winner is hardcoded.

## Main result: consistent habitat reversal
With original tissue ratios,30-day co-culture outcomes:

|seed|wet habitat wet/shallow-origin biomass|shallow habitat wet/shallow-origin biomass|
|---|---|---|
|42|.9311 /0|0 /.4583|
|1337|.9437 /0|0 /.3086|
|2027|.9320 /0|0 /.4060|

Both slot orders yield same winners and displayed masses. Equalized support fractions yield same reversal for all3 seeds; wet winners .9308/.9436/.9317, shallow winners .4584/.3078/.4060. This rejects a simple explanation based only on original occupied patch, initial total biomass, or initial tissue fraction. It supports habitat-dependent performance of these inherited phenotype packages, not causality of any single trait.

Wet pair grazing totals are .241/.794/.386 (original tissue); shallow pair grazing is0. Thus wet outcomes involve trophic removal, not just light/growth competition. Existing structure provides shallow survival, not grazing armor. Lower wet endpoints for shallow-origin colonies alone (.841/.873/.882) do not by themselves imply they reproduce slower.

## Monoculture and offspring nuance
In original-tissue no-reproduction assays, wet-origin survives1m at .931/.944/.932; shallow-origin also survives there at .841/.873/.882. At8cm wet-origin dies by day3.30/1.08/1.13, while shallow-origin ends .458/.309/.406. Initial tissue equalization does not reverse final viability.

Funded exported offspring in1m are64/61/64 for wet-origin versus82/81/76 for shallow-origin. At8cm wet-origin produces0, shallow-origin67/44/66. Therefore DO NOT label wet winner a generally faster breeder: offspring count, retained biomass, respiration and direct predation differ. Endpoint parent+exported mass in wet is close (.1 initial plus resource uptake), and daughters are not survival-tested here.

## Limits and next useful test
Only largest resident genotype per habitat per seed, not representative distributions; inherited traits correlated. Same source seed does not make genotype identities matched. Equal-abundance30-day fixture is not natural succession, no rare invasion, no spatial refuge or migration, no evolved animal/fire behavior and no mobile gameplay proof. The stable uniform late-daughter bottleneck remains unresolved. These results do justify exposing contrasting real habitat strategies in gameplay, rather than manufacturing universal stronger successors.

Next: low-frequency reciprocal invasions with matched total biomass and explicitly funded invading propagules, plus nonfeeding counterfactual copies to separate trophic exclusion from abiotic tolerance. Keep original phenotype performance as primary result; counterfactuals must be labeled.

## Reproduce
`zig build --build-file web/tests/lifecycle-build.zig -Dsource=src/qa_reciprocal_transplant.zig --cache-dir <absolute-cache> --global-cache-dir <absolute-global-cache>`
Zig0.13. results.log retains full telemetry; donor.csv,pair.csv,transplant.csv are exact parsed tables. Existing evidence unchanged.

# Habitat-factorial establishment experiment

Actual production `Planet.simulateMicrobes`; no production changes. All 12 180-day runs and imported tests completed with build exit 0. Cell validity, nonnegative atmospheric gases, carbon and nutrient ledgers pass each tick (absolute tolerance 0.001).

## Controlled design
Same 19-cell six-neighbor ring, ordinary founder in wet/warm cell0, finite atmospheric pools and nutrient ledger as the establishment probe. Three seeds42/1337/2027. 1440-second scheduling, imposed half-day light/night. Four treatments: 0 uniform1m/303K; 4 depth-only mosaic (six fixed cells at8cm/303K); 5 temperature-only (same six cells1m/293K); 3 combined (same six cells8cm/293K). Other13 cells stay1m/303K. No automatic climate/water simulation.

TRAITS zone0=whole world, zone1=13 background cells, zone2=six focal cells (same labels even in uniform controls). Snapshots day30,60,63,100,180 report biomass-weighted inherited organization, structure, feeding, optimum and generation; actual support tissue fraction; largest living cohort's lineage/parent/traits. Zero-valued traits in empty zones are missing observations, NOT zero-trait organisms. Maximum generation records ever observed ancestry; it does not mean all extant organisms have that generation. Lineage IDs are identifiers only within a run, not comparable genomes across treatments. `became_parent` counts post-day30 newborns observed having offspring. Existing fate-observation limitations remain (end-of-step sampling, right censoring).

## Results: depth is the strongest reproducible niche contrast
At day180 depth-only focal shallow colonies have higher organization/structure and lower feeding than wet background in all three seeds:

|seed|shallow vs wet structure|organization|feeding|
|---|---|---|---|
|42|.337 vs .046|.218 vs .017|.022 vs .180|
|1337|.202 vs .047|.118 vs .018|.036 vs .158|
|2027|.224 vs .033|.102 vs .013|.044 vs .118|

Shallow biomass increases from day30 to180: .034→.544, .046→.331, .091→.352. Focal dominant cohort changes from generation3 to generation5/6/6; dominant structure rises .122→.351, .163→.330, .135→.250. These are actual inherited traits in funded living cohorts, not visual taxonomy. They support phenotype/environment associations consistent with existing support/shallow-survival tradeoffs; they do NOT isolate which trait alone causes success.

|seed|uniform maxgen / late parents|depth-only|temperature-only|combined|
|---|---|---|---|---|
|42|5 / 19|9 / 31|7 / 31|9 / 48|
|1337|6 / 18|8 / 36|7 / 18|5 / 14|
|2027|5 / 0|7 / 14|8 / 44|5 / 8|

## Cooler patches and the negative combined result
Temperature-only focal patches show lower weighted preferred temperature than background in all seeds:298.52 vs302.66K;301.46 vs302.80K;298.28 vs303.83K. Feeding is higher (.250 vs .103; .158 vs .091; .237 vs .120). The293K patch temperature is not fully matched by optimum, and weighted structure does not show one consistent direction.

Combined treatment is NOT uniformly better: seed42 shallow+cold population persists and reaches greater ancestry, but focal patches are empty at day180 in seeds1337 and2027. Seed2027 is already empty there at day30;1337 has only .0055 biomass at30 then none at180. Combined world biomass ends .933 for2027 versus14+ uniform, showing harsh pockets can impair outcomes rather than automatically enrich them. Single-seed earlier mosaic result must not be generalized.

## What this does not establish
No full stable-habitat pioneer displacement claim. Homogeneous controls retain poor late establishment. No proof of complete ecological succession, animals, drought on truly dry land, fire adaptation or browser/mobile fun. Paired seeds control initial randomness, but treatments alter later random paths through population dynamics; identities cannot be paired as counterfactual clones. Different light, shallow stress and resource competition interact. Only three seeds and one fixed topology. Dominant cohort replacement need not be direct parent-child replacement or competitive displacement; no lineage tree inference is made.

Next discriminating experiment: reciprocal transplant copied established focal/background phenotypes into matched shallow/wet environments with identical biomass, paid tissue, food and nutrients, comparing growth/survival/offspring while preserving accounting. That separates habitat tolerance from altered encounter histories without scripting winners.

## Reproduce
From repository root, Zig0.13:
`zig build --build-file web/tests/lifecycle-build.zig -Dsource=src/qa_habitat_factorial.zig --cache-dir <absolute-cache> --global-cache-dir <absolute-global-cache>`
Raw stdout/stderr retained in results.log. traits.csv and trajectories.csv are exact parsed telemetry. Existing establishment/succession evidence unchanged.

# Actual fullscheduler thermal buffering: positive paid land progression

Fixed preregistration ddff2a2 executed once. Both binaries built; all four48h arms and their fresh-process24h→48h continuations PASS complete serialized state/RNG byte equality. Root, mortality, growth, patch and birth trace rows after the midpoint also match exactly. Initial complete paid worlds match byte-for-byte across thermal variants. No extra runs or parameter changes.

## Outcomes

All start with the real public-action paid standard rooted founder .02kgC/m², rootallocation.5, support.005, organization.25, structure0. No gene assignment to existing organisms, water/nutrient additions, temperature clamps, care or retargeting.

|Ground effective layer / site|Final founder C|Actual direct children born/alive48h|Founder+children density sum|Actual T range K|Cold intervals≤273.15K|
|---|---:|---:|---:|---:|---:|
|0.1m /126|.00822366|0/0|.00822366|272.10–321.26|8|
|0.5m /126|.03182659|3/3|.04656707|296.24–306.99|0|
|0.1m /1845|.00492416|0/0|.00492416|267.99–304.08|23|
|0.5m /1845|.01628339|1/1|.02022089|294.29–304.98|0|

Density sums across patches are not new organisms/species or absolute mass; the common engine mean area can convert them. The1845 founder itself declines despite producing one child: retain that tradeoff, not universal success. All children inherit actual paid support/rootallocation.5; these are descendants of an explicitly chosen rooted founder, NOT independent natural evolution of roots. Their complete IDs, phenotypes and final locations/depth/soil are in child-fates.json.

Site126 candidate is genuine exposed terrestrial growth in the modeled world: surface depth stays0 at all120 endpoints, root hydration is used on120ticks, cumulative credited water .00248346kg/m², founder fixation .03079253C versus mortality .00546475 and upkeep .00150119 plus paid offspring. Soil spans .69935 down to .09955, so warming also dries the land; this is not free/guaranteed permanent water supply. Control126 receives some root hydration but loses substantially more biomass under49K temperature swings.

Site1845 candidate shifts from a thin-water margin toward exposure (depth0–15.89mm), root hydration used119ticks, creditedwater .00153555. Its fixation .01798630 nearly balances mortality .01665737 and upkeep .00104554 before a paid .004 propagule. Soil drops to .35342. Control1845 remains wetter (2.97–73.02mm), crosses the cold gate23times and fixes only .00433924C.

## What changed and what did not

Exactly one runtime physics constant changes: existing Origin heat capacity uses an effective ground reservoir0.5m rather than0.1m. No new arrays, scans, per-step branch, resource, genotype, growth/mortality/demand coefficient, day length or solar input. The same cached heat capacity governs CPU solar heating, radiation cooling and neighbor heat exchange; existing OpenCL upload also calls the same capacity helper. Sandbox path is unchanged.

This is a NEW illustrative game-design thermal assumption, not empirically calibrated soil physics. Same initial temperature plus fivefold ground heat capacity assumes greater initial stored internal energy. No recurring heat is injected. Radiative equilibration near300K slows roughly18h→89h on dry ground;48h results demonstrate buffering and real reproduction, NOT long-term equilibrium or indefinite establishment. Existing water phase model lacks explicit ice/latent heat and enthalpy advection, and this test does not fix those omissions.

The independent local test7a75ef6 already showed capacity for growth in stable climates. This comparison now confirms the full climate/water/root/biology/dispersal engine can deliver it, including genuine paid offspring, without reducing biological mortality. The cold gate and .0025 cleanup cutoff remain phenomenological game choices, not sacred biological truths. Their separate calibration/dormancy review remains justified; no need to mix changes into this successful isolated test.

## Save and deployment limits

Both variants are private labelled QA binaries. Test fixtures serialize current wire10 and are meaningful only with the matching external control/candidate source identity. There is NO public save migration or silently reinterpreted old saved world. A product implementation would need explicit model identity/default policy and historical exact behavior before exposure. Current live games and saved worlds are untouched. No performance benchmark or browser/deviceFPS claim; arithmetic work is unchanged, but final runtime gates would still be needed.

## Evidence

Complete initial/midpoint/end saves, main/resume logs, original source hashes and exact constant delta retained. All compressed files individually below8MiB. Control source is the frozen real paid natural-site QA adapter; output path prefixes and midpoint60 are the only other copy differences. Reproduce with prepare-thermal-reservoir.py and run-thermal-reservoir.py using the documented EGL native build. No failed runtime attempt or discarded ecology outcome in this comparison. The child-fate read-only analysis first attempted to save under read-only permissions; it was repeated with authorized write permissions, without re-running any simulation.

Checkpoint compactness: tracked snapshots retain all four complete48h endpoints. Initial/midpoint compressed copies remain local, with their hashes in artifact-hashes.json and deterministic reconstruction/restart in the runner, but are not duplicated in the current checkpoint tree. Full uncompressed local inputs/midpoints are preserved. This does not erase any result or require rerunning ecology to inspect the retained endpoint.

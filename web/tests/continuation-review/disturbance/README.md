# v35 evolved cohorts under disturbance and recovery

## Scope and execution
`src/qa_disturbance_transplant.zig`, pinned Zig 0.13.0 via lifecycle-build.zig. Exit 0. Production ecology unmodified. Three real Planet scheduler evolutions of 180 days (seeds 42, 1337, 2027) supply largest living wet-zone and shallow-zone donors. Includes current v35 rare mutations, not cached v34 donors. Then 48 controlled two-cohort assays: 3 seeds × 4 shocks × 2 habitats × 2 slot orders, 60 days each. All ticks verify valid state, nonnegative atmospheric inventories and carbon/nutrient closure within 0.0001. 192 observation records saved. Slot-swapped final outcomes match to printed precision.

Each donor starts 0.1 biomass with its actual inherited traits and proportionally preserved paid structural tissue; credits/grazing/movement counters reset. Finite identical resources: nutrient .12, CO2/O2 each 10 carbon-equivalents. Normal M.step every 1440s, alternating 12h light/dark. No reproduction, arrival, dormant seed bank or mutations during assay. Donor evolution is genuinely multigenerational; assay is not. Baseline habitats are 1m and 8cm water, 303K. On days 10–13 only, treatment 1 imposes 2cm depth; 2 holds temperature at 343K; 3 combines both; 0 remains untreated. At day13 restore baseline climate, follow to day60.

This is a controlled exposure, NOT a real wave/lightning action or coupled hydrology. Imposed temperature does not have an externally accounted heat budget, so it cannot be described as a conserved-energy god-tool experiment. Carbon and nutrient accounting are explicit. Sustained heat is not combustion; no fire ecology is implemented by this probe.

## Findings (not hardcoded assertions)
- Heat reduces wet-habitat winner biomass substantially at day13 (seed42 .8785→.0799; 1337 .9394→.0988; 2027 .9414→.0983). Surviving winners regrow by day60.
- Three-day drying wipes out the wet-habitat winners in seeds1337/2027. Their rival already died during competition. Restoring water does not resurrect either lineage: both remain zero at day60. There is no dormant pool or immigration in these assays.
- Seed42's shallow-derived winner survives drying (.3002), heat (.0799), and combined (.0380), then recovers in wet habitat. In baseline shallow habitat, shallow-derived survivors recover in all three seeds after all treatments.
- Crucially v35 donor evolution is not identical to v34. Seed42 shallow-origin now wins both habitats, whereas seeds1337/2027 still reverse winners between habitats. Do not reuse the prior all-three reversal claim for v35. Rare mutations change whole evolutionary trajectories; this small set cannot establish their population-level benefit.
- No universal strong successor or guaranteed beneficial disturbance. No continuous invasions, offspring establishment, fire-adapted seeds, rabbits or physical Android performance demonstrated here.

## Reproduce
`zig build --build-file web/tests/lifecycle-build.zig -Dsource=src/qa_disturbance_transplant.zig --cache-dir <absolute-cache> --global-cache-dir <absolute-global-cache>`

Next useful experiment: disturbance before competitive exclusion and low-frequency arrivals, using normal funded offspring, to distinguish surviving resilience from recolonization. Do not add invisible care or fake resurrection to make recovery look good.

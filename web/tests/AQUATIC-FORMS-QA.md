# Aquatic producer forms

Six map-visible growth forms are derived from living cohorts' existing inherited traits and actual tissue: microbial mat, cushion, rosette, ribbon, branching and canopy. These are aquatic functional forms, not taxonomic species or full land plants. A dead cohort or one without both real support and collecting tissue cannot show an organized form. Form labels are not timer unlocks, assigned rewards or additional biomass.

Continuous architecture links inherited light efficiency/toughness to height, collector spread and upkeep. Slender low-efficiency forms gain height per support; high-efficiency collectors spread wider but pay greater support maintenance; tougher forms grow lower. These affect relative competition for the existing finite photosynthetic budget. Display classification thresholds cause no growth jump. Carbon and nutrients remain conserved; no save fields/schema changed.

## Automated checks

- 22/22 production microbe tests pass.
- 37/37 save-schema/model tests pass, including existing legacy migrations, conservation, grazing, movement, support and exact sparse preservation.
- 128 initially simple seeded colonies, each run for 60 simulated days in a controlled suitable environment using production growth/reproduction/mutation, produced all six forms. No traits were assigned. Across hourly observations: mat331104, cushion92535, rosette69575, ribbon32423, branching587, canopy20094. These are repeated observations, not unique organisms. This is not a full-world or universal diversity guarantee.

## Full coupled-world failure found

Generated world seed1337, ordinary initial Seed, then explicit3m targets at selected+6neighbor patches and actual Seed actions. No biological values assigned and no subsequent water care. Four forms coexisted atday5 (12living cohorts), but terrain flow left shallow habitat dry or deep. All cohorts extinct byday17; remained extinct atday100. Exact save restoration and invalid-save rejection passed. Native mean update10.35ms; no Android FPS claim. Existing GPA teardown leak warning persists.

This demonstrates that uniform depth targets are not a contained pond on high-relief terrain. The release needs either explicit care or a genuine basin tool; do not claim sustained flourishing from this failed run.

Reproducer: `egl-forms-world-prepare.py` extends existing full-engine diagnostic harness; current version uses production Make Pond with optional explicit5day refills. The initial unmaintained run used equivalent selected-patch3m target calls before the new area callback existed. Subsequent results must identify any new basin semantics.

## Explicit care comparator (prior uniform-depth area tool)

Repeating the same real seven-patch3m water action once per5simulated days,20actions total, retained three living support-bearing lineages atday100: cushion, rosette and canopy. Total biomass-density sum0.240403, support-density sum0.008410; four real relocations occurred. Save/restore exactness passed. This is player intervention scripted by the harness, not game auto-care. It demonstrates a reproducible playable management path but not a contained basin or carefree ecosystem. Later19cell basin behavior is evaluated separately.

## Three-metre contained basin comparator

The first19cell basin implementation (7flatfloor patches,12dryrim,3m initial water) created28living cohorts byday6 and fourforms byday3, but without care it dried and was extinct byday19. With20explicit5day refill actions, it retained8cohorts across fourforms atday100 (mat1,cushion3,rosette3,canopy1), total biomass1.314062 and support0.012328. Exact save restore passed. These are comparison runs, not the final deeper basin behavior.


## Final fifteen-metre basin: no further care

The final production basin edits at most 19 cells: seven flat aquatic floor cells with 15 m water, surrounded by a dry rim at least 17 m above the floor. It performs an explicit player terrain/water intervention, not automatic maintenance, seeding, or trait assignment. The real production fine-depth editor remains capped at 5 m; the basin uses validated direct water mass for its documented 15 m action. The harness asserts actual depth on all seven floor cells before simulation.

World generator seed 1337, real initial Seed plus seven additional Seed clicks across the basin, one basin action, no refills: after 100 simulated days, 18 living cohorts remained across four forms (mat 5, cushion 10, rosette 2, canopy 1). Five forms coexisted earlier, including ribbon; this run did not demonstrate branching. First differentiated descendants appeared by day 7. At day 61 there were 26 living cohorts across five forms. At day 100 biomass-density sum was 1.24153357, support-density sum 0.00421416, with 13 support-bearing cohorts. The selected patch retained 4.14 m water. Invalid-save rejection, unchanged state after rejection, and exact restoration passed. Native mean update 9.71 ms; this is not measured mobile FPS. Existing native teardown allocation warning remains.

### One Seed is sufficient

A separate 30-day run used just the ordinary initial center Seed and the same explicit basin action, with no extra seeds, refills, or assigned traits. The first descendant cushion appeared on day 7, rosette on day 14, ribbon on day 19. Four forms coexisted during days 19–26. At day 30 six support-bearing cohorts remained (four cushions and two ribbons), biomass-density sum 0.17421773, support-density sum 0.00326958, and one real relocation. The selected patch retained 13.72 m water. Save rejection and exact restoration passed. This validates the single-Seed onboarding path, not a requirement for seven precise taps.

At the displayed Fast setting of 24 simulated hours per real second, days 7, 19, 30 and 100 correspond nominally to 7, 19, 30 and 100 seconds of simulation time. Actual wall time depends on device throughput and the simulation's work cap. The harness advances the same production model but is not proof of touch usability or Android frame rate.

Reproduce the one-Seed branch with `STELLA_FORMS_SINGLE=1 STELLA_DIAGNOSTIC_DAYS=30`; omit the former for the expanded-seed case and use 100 days. Do not set `STELLA_FORMS_CARE` for either final acceptance scenario. Filtered evidence is in `evidence/forms/`. These results establish aquatic ecological diversification, not land-plant evolution, rabbits, or all possible-world stability.

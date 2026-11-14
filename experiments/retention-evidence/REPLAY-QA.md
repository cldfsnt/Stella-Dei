# Actual Continents environment replay: reserve mechanism, not evolution

Isolated investigation only. Current game remains schema6 and unchanged. No warming, vapor deletion, hidden refill, trait assignment in a game world, deployment or save migration.

## Inputs
Fresh deterministic Continents world, ordinary actual Focus/Nursery/one Seed actions, production1440-second physics quantum,30days. Read-only instrumentation records the exact environment entering microbial simulation at cells35503,6787,30111: time, dt, temperature, water depth, solar-vector-derived light, atmospheric carbon and oxygen capacities. 1800rows/site,5400rows total. Recording occurs before microbial updates, not an inferred day/night approximation.

Production ecology hash6224eb3a2ce81699d3296ee255eb38cd91b579a263a736841d2816fdb98164e1; Planet hash01092032cbb7aa63eaf8025133c89b41ae6fd3004bf78bcc46c440da43cef6d7. Replay reserve model hash0f507e33035fef4e8530dcbc4a4839961f1a8133412d12a7e5ec3a40f2db6ed8, retained from the saved experimental precision candidate, not production.

## Controlled contrasts
Each replay starts with a SYNTHETIC supported cohort:0.1kgC/m² total biomass,0.004support included within biomass, organization.04, structure.15, optimum285or303K, retention0/.5/1. Initial stored water ZERO. Reserve enabled versus disabled. Thirty-six contrasts total. These traits were deliberately assigned for mechanism isolation; none are evidence of natural evolution or ordinary-player establishment. No reproduction or external arrivals are simulated in replay.

Every step uses measured liquid supply, debits real uptake, credits evaporation/returns and explicitly accounts the exchange required to match the next measured environment. Thus the replay is an OPEN prescribed environment, not a claim of closed full-world water conservation. Biology cannot change subsequent recorded weather. Carbon fixation/recycling and nutrient totals are independently checked. Frozen steps and steps with zero external AND zero stored water must fix zero carbon.

## Results
-35503:1545/1800dry steps (85.8%),371frozen steps,630warm/dry/lit steps. No-reserve controls die aroundday21.2. Low-retention reserve controls remain alive atday30 but shrink from.1 to.007735(optimum285) or.005934(optimum303). Dry-period fixation.021747/.024499kgC/m². This is finite survival extension, NOT thriving establishment. Retention1 dies byday24–25; costs outweigh slower water loss here.
-6787: all controls die without meaningful fixation. Reserves do not create suitable habitat or universal cold tolerance.
-30111:680dry steps (37.8%),163frozen,267warm/dry/lit. Optimum303,retention0: reserve-on finalbiomass.25804 versus off.18989; cumulative fixed1.1707versus.6620; paid dry-period fixation.0795. Optimum285 reaches~.292 with either setting, indicating thermal matching is an independent strategy and reserve benefit is conditional. Retention1 is worse; no “many equally good strategies” claim is supported.

All36model unit tests pass. All36replay contrasts pass finite/valid-cell, zero-water/frozen fixation, carbon/nutrient and explicit water-ledger assertions. Maximum water discrepancy is approximately1.7e−13kg/m²; this applies only to the replay's f64 biological ledger, not the whole climate solver.

## Concrete next playable experiment
Worth testing naturally evolved, donor-funded arrivals from an ordinary nursery bordering30111, with reserve on/off matched saved ancestors and current climate. Do not seed an already adapted synthetic land organism into the game. Preserve the actual warmer/cooler optimum differences and expose habitat condition/lineage outcomes. Require visible establishment and paid reproduction before calling it a playable shoreline path. The harsh35503site should remain a survival challenge, not be made friendly by removing frost. Strong retention currently has no winning niche in these traces; do not market it as a distinct successful strategy or retune it just to force a winner.

This does not establish terrestrial plants, roots, seedbanks, fire recovery or naturally evolved water retention. No live migration is warranted solely by these results.

## Reproduce
`web/tests/egl-retention-trace-prepare.py` instruments an isolated generated source copy. Use standard egl-origin-build with actual nursery flags QA_CONTINENTS=1, STELLA_FORMS_SINGLE=1, STELLA_ORIGIN_COUPLED=1, STELLA_ORIGIN_FAST=1, STELLA_PRODUCER_LONG=1, STELLA_DIAGNOSTIC_DAYS=30. Filter RETENTION_TRACE records. Compile replay/run.zig with Zig0.13 and pass the trace file. Exact trace, all results and hashes are under replay/results. Use workspace-local TMPDIR for future runs.

# Independent actual coupled candidate source review (pre-result)

Read-only review of web/tests/egl-hydration-coupled-prepare.py and copied candidate Planet. This is source wiring review, not acceptance of ecology outcomes. Candidate full run was not yet claimed when reviewed. No production changes by reviewer.

## Confirmed wiring

- Copied Planet is restored from current production before applying exactly the two narrow hydration changes, so inherited profiling/QA physics rewrites are removed.
- Physiology remains after climate/hydrology. The adapter receives current waterMass and waterVaporMass, not newWaterMass or newWaterVaporMass scratch.
- Actual mean point area is passed, not the isolated fixed area constant. The real microbeEnvironment provides current temperature, atmosphere budgets and actual daylight-derived light. Adapter replaces nominal environment depth with depth derived from the represented liquid remaining after uptake.
- The owned-water branch calls exchange.step once; exchange.step calls the biological core once. Planet applies the returned microbe flux once through its existing applyMicrobeFlux. No isolated State atmosphere bookkeeping is layered on top.
- Cells with no biomass/detritus but outstanding liquid/vapor escrow flush to the current matching pool, then continue before active-bit marking. They do not enter movement/reproduction and consume no extra reproduction RNG. Unrepresentable returns remain escrow for a future tick, not lost or credited as live hydration.
- Same core owns water through birth/grazing/death/movement. The planned final daily inventory includes current physical liquid+vapor plus waterTotal(cell) converted using actual area. It does not count scratch pools.
- Zero-trait parity comparator first asserts every new field zero, then permits only schema/model revision normalization and removal of those zero fields; all remaining saved values must match. It does not broadly ignore numerical differences.

## Required result gates / gaps called out before run

Daily global totals alone cannot separate new biological numerical error from inherited physical hydrology drift. Requested per-exchange-call total before/after (physical liquid+vapor+owned stores+escrows), maximum absolute and signed residual accumulation, plus an end-of-microbial-scheduler ledger including births/moves/deaths and escrow-only flushes. State the chosen tolerance before observing outcomes; no global mass correction. Compare biological-stage residual separately from whole coupled tick water change. A natural god-tool edit has its own external receipt and must not be folded into numerical error.

Global carbon accounting must convert the stored average CO2 mass using Npatches×1e9×12/44 and add area×sum(living+detritus). Do not add raw average atmosphere units to per-area biology. Global nutrient is area×sum(free nutrient+living×nutrient_per_carbon), consistent with existing mortality/recycling convention. O2 remains a separate physical mass ledger. Report existing f32/core residuals honestly.

The current fixed-root active experiment compares two seven-day drained runs (allocation0/.25); its arm0 is a ten-tick disabled parity gate, NOT an undrained seven-day treatment. Therefore outcomes cannot establish a full wet-versus-dry ecological tradeoff in this coupled world without a separately specified matched undrained arm. Both drained arms use the same one-time actual Water− action after one day and natural refill thereafter; no repeated irrigation or world search. Do not generalize from one root/world.

Thermal phase model remains phenomenological with no latent-heat coupling, as agreed. This source review establishes neither thermodynamic closure, actual browser/mobile behavior, production schema readiness, nor a universal evolutionary benefit.

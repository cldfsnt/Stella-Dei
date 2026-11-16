# Cleanup cutoff scale audit (existing evidence only)

Scope: frozen combined00502c4 source and all four preregistered day7→21 logs6474993. No simulation, new fate, model edit or horizon extension. Source: Microbes.step first charges support upkeep and analytic mortality, then, if biomass<.0025kg C/m², sends **all remaining biomass** to detritus and boundN to nutrient, clears the cohort and increments failed_patches. Growth and grazing occur afterward. This is a finite-resolution cleanup rule, not continuous biological mortality or lost carbon.

The old comment describes25% of a.01propagule. Current paid wind and local exploratory packets are.004, so the same threshold is62.5% of their initial carbon. Of5,670 new births in this follow-on,5,602 were.004 and68 were.01. Lowering a global threshold to.001 would be25% of the smallpacket and10% of the largepacket; it would affect weak older organisms too, not only wind.

|Arm|Observed losses = failed_patches|New wind deaths / within1day|New nonwind deaths / within1day|
|---|---:|---:|---:|
|42 ordinary|1242|0 /0|1090 /983|
|42 Pioneer|1101|510 /470|444 /395|
|1337 ordinary|563|0 /0|493 /458|
|1337 Pioneer|687|343 /335|272 /252|

New means born afterday7; pre-existing organisms are included only in all-loss totals. Nonwind includes actual local exploratory and large births, not assumed neighboring wind arrivals. Ages use exact recorded tick identities,24min intervals. Across arms,853 wind-arrival deaths include805 within1day;2,299 new nonwind deaths include2,088 within1day. These are existing outcomes, not a claim that all early deaths are caused only by packet size or would recover under another cutoff.

## What the trace proves, and what it does not

Every observed loss is accounted for by the failed_patches delta. Source has one such increment, at cleanup. Whole-cohort relocation preserves identity and does not contribute to these counts. Thus all3,593 disappearances crossed the cleanup rule. Continuous mortality/grazing may be the reason they became weak; cleanup is the final discrete removal, not an alternative ecological cause.

Logs retain the complete previous-tick living cohort, not the exact post-mortality residual at the cleanup line. Last-live biomass spans.00193812–.00267233. Some were already below.0025 after the previous tick's grazing, which is permitted until the next mortality/cleanup stage. Do not mistake last-live biomass for the quantity recycled.

A conservative single-stage bound is possible without inventing an environment. Valid trait bounds give support upkeep≤.1344×B/day. Film mortality≤4.99/day, dry mortality≤4/day, and extra height exposure≤3/day; hydration/immersion blends cannot increase these maxima. At1440s (1/60day), using exp(−x)≥1−x gives remaining B≥(1−.1344/60)(1−7.99/60)B≈.86489B before floating rounding. We deliberately use the looser .86B bound, whose margin vastly exceeds f32 rounding at these normal .002-scale values. All physiology precedes movement/dispersal in separate loops, so a recorded prior-tick cohort receives one such mortality stage, not repeated cell-order updates.

Therefore each of the3,593 recorded cleanup inputs would still have **more than.001** after that same unchanged continuous mortality/upkeep stage. The summed residual lower bound is7.7151kg C/m² summed over events/cells; the true residual is unlogged and below.0025 per event. This is not carbon newly available or an exact flux ledger. A .001 comparison on those identical stage inputs would defer their immediate cleanup. It does NOT imply3,593 additional living colonies atday21: changing occupancy changes later competition, grazing, nutrient recycling, successful births and RNG paths.

## Likely gameplay and performance consequences

The rule currently destroys a small propagule after losing only about37.5% of initial biomass, while an old.01packet can lose75%. A lower finite cutoff would give weak seedlings more time to experience changing light/weather without making them immortal. Under a hypothetical constant4/day decay with no growth/grazing, changing.0025→.001 adds ln(2.5)/4≈5.50hours; under milder decay it can add much longer. These are analytic examples, not observed survival predictions. Growth rescue is possible, never guaranteed.

More simultaneous occupied slots are likely, especially around successful wind deposition. Fixed cell/cohort arrays do not grow, but active physiology, competition, serialized living records, and capacity refusals may increase. Existing traces cannot quantify that workload or lasting occupancy under a changed rule. Do not infer an FPS cost from cumulative delayed deaths. Four slots per cell remain the fixed capacity.

A separate relocation preflight also requires a post-cost fragment≥.0025 (microbes line364). Changing mortality cleanup alone does not automatically make a weak organism mobile. Keep that scope explicit rather than accidentally replacing every literal. No new per-cell state or immortal floor is needed for the cutoff proposal.

## Proposed next discriminating gate (not executed)

Before any full-world change, copy only the cleanup threshold into a private pure actual-Microbes.step comparison: legacy.0025 versus candidate.001; frozen real support-free dry root213 birth phenotype/environment as the harsh example, plus a fixed warm/wet growth-capable control and exact boundary witnesses. Keep packet sizes, mortality, light, paid resources and every other trait unchanged. Record continuous mortality separately from residual cleanup, C/N recycling, actual growth, death time and finite loss; validate identical outputs until a cleanup divergence, old branch exact, and dt refinement. This is an illustrative mechanism test, not calibrated ecology.

If that supports the desired weak-colony window, request one fixed fullscheduler comparison with explicit saved-law identity and restart/performance checks. Do not silently alter historical saves or rerun until a winner appears. The existing evidence already identifies a tangible scale mismatch worth testing, without claiming stable land life or forest succession.

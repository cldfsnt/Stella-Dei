# Read-only climate/terrain diagnosis on the v21 QA world

No production or climate parameters were altered.

## Initial conditions and terrain
Generation explicitly initializes vapor and rainfall to zero. The reproducible
QA world chooses sea level +4.838867 km with the original random ±5 km rule.
On its retained terrain, about89.8% is below that level; roughly4171/40962 cells
are above it. Nineteen nursery-edited cells slightly affect these estimates.
This is one QA world, not a claim that every randomly generated world has that
coverage. Current browser generation still selects a random world seed.

Initial water is about5.24km global-equivalent depth. At30days, only5 cells have
exactlyzero water;25≤1mm,88≤1cm,557≤10cm,1284≤20cm globally. Among original-land
heights, median surface depth is about0.305m. The simple aquatic ancestor's
minimum depth is0.2m, while moist-shore fitness uses a0.02m hydration scale.
Thus water-depth categories, not just a strictzero test, also show that most
exposed land is puddled rather than persistently dry.

## Column mechanism
getSubstanceDivider uses cell area×12000m, and the saturation calculation uses
the current surface temperature throughout that whole column. Calculating the
code's ideal-gas/Tetens expression gives saturation equivalents:
280K92mm;285K127mm;293.15K207mm;303.15K364mm;310K522mm.
These are model calculations, not claimed observed meteorology.

Ocean evaporation supplies that vapor from real liquid, then wind advection and
cooler columns condense it. The prior exact per-edge stress accounting recorded
349mm condensation,86mm evaporation,41mm outflow and zero liquid inflow in one
day. Starting vapor was not fabricated; the large capacity and water-rich world
make very wet land plausible in this simplified model.

## Accounted design options, not implemented
1. New-world Continents preset: choose initial sea level from a terrain quantile
(e.g.70% ocean coverage), then initialize water from that declared inventory.
On this terrain the70% level is about+1.913km, global water2.865km, versus
current~5.24km. This changes a NEW world's initial conditions, not an unannounced
deletion from an existing saved world.
2. If water-cycle calibration is needed, separate a vertically varying vapor
saturation capacity from the shared gas-pressure divider. Simply replacing12km
everywhere would also alter air pressure. Any new profile must conserve existing
liquid+vapor and document its approximate physics; do not erase atmospheric water.
3. Surface runoff/soil retention remain distinct from organism reserves. A
draining land geometry or conserved soil-water compartment would be different
mechanics, not justification for inventing water or plant survival.

Whole-world water falls by about145mm global-equivalent over this30day run
(relative2.78e-5 of the large ocean inventory). This is separate from the tested
biological bridge's tiny error; its exact source was not isolated here. Do not
claim exact conservation for the entire preexisting climate/liquid solver.

A broader saved per-cell exposure survey is pending, to distinguish truly
persistent dry habitats from transient zeros or unusually cold/hot sites.

## Completed exposure survey
1800 actual1440-second ticks:825cells dry≥5% oftime,231≥10%,7≥50%,0≥80%. None ofthe7≥50% have mean285–325K. Driest cell27014 is dry64.78%, with260.38–306.29K range and283.43K mean. Best classifiedwarmmean candidate31264 is onlydry20.83%,262.22–317.88K. A warm, sustaineddryhabitat was not found. No physiology changes are justified by these data alone. Summary+rawCSVhash preserved in web/tests/results/v21-climate-summary.json.

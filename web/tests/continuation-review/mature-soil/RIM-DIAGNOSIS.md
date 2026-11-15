# Rim flooding diagnosis: condensation, not immediate overtopping

Read-only source/previous trace analysis; no new engine runs or parameter changes.

Current nursery code (`src/pond_action.zig`, both action and shared plan) raises rim to max(existing elevation, base+17m). Base includes all adjacent outside water surfaces. Deep/Sunlit floor water surface is approximately base+15m, so newly made rim has approximately2m clearance above the inside water and17m above outside water. Finite f32 rounding exists, but does not explain millimetre rain accumulation. It sets rim water zero once; it does not promise dry drainage capacity.

Existing actual mature trial proves cause at the tested location after one day of conditioning:
- First post-drain liquid transport delivers exactly0 water to target3121.
- Atmospheric vapor1363.8982586 native exceeds saturation1232.7419910 at288.865K.
- Condensation adds43.239589691 native; infiltration removes0.010837555; ending43.228752136 native=5.636mm.
- Second tick transport actually reduces43.228752→42.398762, then condensation adds70.509563.
- Across24h rootless arm, net liquid transport exports510.130367native, while local column phases add2064.921627native; ending1554.791260native. Exact dyadic telescoping passes. This is local represented inventory attribution, not global conservation.

Current atmospheric source uses one-hour relaxation of vapor above saturation into local liquid, independent of terrain height (`simulation/atmosphere_water.zig:17–27`). Rain can accumulate on raised terrain while slow lateral runoff removes some. Raising the rim again or removing water continuously would mask this process, not fix its cause. No evidence here warrants a solver change or new draining rule. The experiment uses archived widened-vapor candidate weather, so its exact rainfall is not a forecast for current production worlds.

## Minimal honest current behavior
`web/habitat-plan.js` currently says “Rim: dry (0m), raised above the floor”, followed after apply by “Water may redistribute after you resume.” Receipt already disclaims survival. Smallest accurate wording: “Rim: water cleared to0m now; raised above the floor. Rain and flowing water can wet it after resume.” This is a clarity correction, not a promise of new land gameplay. No code change in this audit.

## Habitat selection, not artificial drainage
A future bounded finder may report *currently* dry, warm, empty patches adjacent to the selected living colony, additionally exposing current rain and vapor/saturation status. Excluding currently supersaturated/raining targets is a reasonable pre-action suitability filter, not a durability guarantee; daily cooling/advection can change it. A real stable-coast claim requires observed wetness through a full weather/daylight cycle, not altitude or initial zero water alone. Do not call tiny residual water dry by changing the threshold to win. No additional survival trial is justified until this distinction is explicit.

This result corrects the earlier shorthand “rim refills”: in this fixture rainfall wets the rim, while transport drains it. The finite soil mechanism itself did receive funded water; persistent land exposure is a different ecological/weather condition.

## Fixed existing snapshot census
Read natural days30/40/50/60 only. Approximately6,584/6,587/6,596/6,599 of40,962 columns are supersaturated under the current source saturation formula. This is not globally condensing weather. Formula is an offline Python table/interpolation approximation, not a native bit-exact threshold proof.

Three patches8483,27014,27026 are exactly dry, warm, empty and undersaturated at all four archived snapshots. Day60 vapor/saturation ratios approximately.257/.125/.135 respectively, far from the classification boundary. Their saved smoothed rain-rate proxies are58.36/14.57/9.81mm/day, so even the least-rainy one is NOT rain-free.27026 is the deterministic lowest-rain candidate among this fixed intersection, not a favorable biological outcome selection. No adjacent patch has living cohorts, blocking current legal one-hop transplant. These snapshots repeat essentially the same daily phase and do not prove dryness through nighttime or all intervening days. A future habitat test would need weather observation and actual reachable seeding/transport, not another founder survival run now.

# Grazing integration candidate (v13 rollback retained)

Candidate-only changes add heritable feeding allocation0–1 and actual recorded
resident-cohort intake (`lifetime_grazed`,kgC/m²,reset on daughter establishment).
World consumed/respired carbon ledgers use kgC. This is mixotrophic grazing
capability, not an animal/species unlock. Other living cohorts supply real food;
there is no invented prey and no automatic success.

Simultaneous feeding demands avoid iteration-order advantage. Consumed carbon
is50%assimilated,25%respired with oxygen,25%detritus. Nutrient in both waste
streams recycles. Grazing respiration and detritus decay share one finite oxygen
budget. Feeding reduces photosynthetic capacity and raises maintenance costs.
No grazing outside habitable wet conditions. New model v4saves default oldfeeding
fields0; old saved values preserved, future trajectories explicitly upgraded.

Eight model tests pass: genuine donor-funded inherited grazing daughter .01→
.03207 in18darkdays, while feeding-disabled .00419 and prey-free .00362. Actual
.08250prey carbon consumed; inherited gen2 funded from assimilation. Oxygen,
photosynthetic cost, conservation, order independence and prior biological
invariants pass.120day foodweb48births/gen2,livebiomass.19444. Real Planet100day
integration passes with naturally arising grazers,407births/gen5,sixoccupied
cells,carbonrelativeerror1.20e-6,nutrienterror1.04e-7.

Full generated-world20day ordinary and mechanistic dark/feeding-disabled tests
are running; do not claim fullworld acceptance until fresh results recorded.
Harnesses: egl-grazing-world-prepare.py, egl-grazing-selection-prepare.py.

Ordinary generated-world20day fullclimate acceptance passed at390and320px:
biomass.18631,3births/gen1,one naturally grazing lineage feeding.01311; actual
consumption220,948,527kgC,respiration55,237,132kgC. Exact39,443,848-bytev4restore
and corrupt rejection pass. Seed screenshot has no amber; day20 actual recorded
intake adds amber. Native peakRSS~355–358MB is a mobile-memory caveat, not a
physical-device/browser guarantee. Wholewaterdrift1.00675e-5. Model step-size
controls60/1440/3600simseconds remain conservative and prey-supported.

First mechanistic test branched too late: after14constant-lightdays the lineage
had consumed competing prey.18subsequentdarkdays produced zero new feeding and
starvation; feeding-disabled control declined less due lower costs. Preserve
this useful negative result (prey-depleted14day-control.log). Earlier branch
with real remaining prey is being tested, without adding organisms/resources.

Normal60-simulation-second steps also pass fullworldfive-day stability and
exact39,319,606-byte save restoration:biomass.03536,one daughter/gen1. This
particular lineage acquired structure but NO feeding trait; actual feeding
counters correctly remainzero. No guaranteed innovation is claimed. Totalwater
drift3.984e-5. An earlier four-day establishment followed by18darkdays showed
real consumption573MkgC in enabledbranch vszero disabled, but both ultimately
extinguished. This is a real long-blackout limit, not hidden by forced survival.

## Final actual player-tool food-web acceptance

The isolated starter can overgraze its offspring. Rather than silently retune
biology or grant organisms, the test uses real shared Drain/Water+ handlers to
make seven2m wet patches (explicit water editing), leaving just the original
seed. It spreads itself into them. With temperature held at the generated293K
and controlled12h light/12h dark,120days yields sevenoccupiedcells,1.25949biomass,
1,025births,eight living observed-feeding cohorts throughgeneration3; peak
observedfeeding generation4. Actual consumption82.37BkgC,respiration20.59BkgC.
Matched feeding-disabled control consumeszero,has59births and1.29628biomass.
No taxonomic claim; actual inherited trophic function is demonstrated.

Fullworld organic-carbon ledger and nutrient checks pass: density-sum carbon
error within a few millionths kgC/m² and nutrient error below1e-7kg/m². Both
exactv4save restorations/corrupt rejection pass. This is controlled climate,
not evidence that the engineered wetland survives120days of fullhydrology.
Ordinary unedited20day fullclimate proof is documented separately above.

Sandbox37day regression remains35livingrabbits,39births,1106meals,6deaths,
plantbiomass5.297848. Model/Planet production source frozen for integration.

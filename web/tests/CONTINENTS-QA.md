# Experimental new-world Continents preset

Candidate only. No production changes, deployment, save migration or reserve physiology.

## Scope
`GenerationOptions.water_preset = .continents` selects the 70th percentile of freshly generated terrain as initial sea level. Terrain is not modified; initial surface inventory is computed from positive sea-level minus terrain height. Initial vapor remains zero. Original `.random` is the default and retains its existing random ±5 km sea-level draw. Preset use without new terrain is rejected; existing saved worlds are never drained.

The native QA fixture uses a deterministic planet seed. Its original random sea level gives approximately 89.8% ocean. This is NOT universal browser behavior: ordinary browser worlds use random seeds and sea levels. Continents is an explicit planet configuration, not a claim to fix every default world.

## Actual engine test
Production v21 fixed 1440-second physical quantum, effective timeScale 1, schema6 and production ecology. One explicit Focus, Make Nursery and Seed action; no biological assignments, ongoing irrigation, hidden rewards or free births. 1,800 physical ticks / 30 days / 120 seconds of Grow simulation time.

Initial Continents coverage 69.9941409%, sea level +1.9130859 km; stored initial liquid inventory 899,988,744,561.8809 engine mass units (one unit = 10^9 kg). Vapor zero. Requested and achieved fractions are both reported because tied heights and finite cells need not give exactly 70%.

The existing guide selected an eligible site (cell228) and the actual nursery callback created its normal 5m center. Stale selection rejection and off-canvas seed rejection passed. By day2: three occupied patches and two paid arrivals. By day30: ten occupied patches, thirteen living cohorts, biomass-density sum0.16334095 from0.02, seventy propagule attempts, forty-seven arrivals and thirty-four tracked colony losses. Living producer forms: mat4, cushion3, rosette3, ribbon2, branching0, canopy1. These are aquatic microbial producer morphologies, NOT vascular land plants or animals.

Native invalid-save rejection, no mutation from invalid load, and exact schema6 restore passed. A pre-existing native shutdown allocation-leak diagnostic remains; do not describe this as a wholly clean sanitizer run.

## Dry-land measurement
All40,962 cells measured each physical tick:

| Metric | Continents | Original water-rich QA fixture |
|---|---:|---:|
| Dry at least5% of ticks |3705|825|
| Dry at least10% |1244|231|
| Dry at least50% |56|7|
| Dry at least80% |2|0|
| Exactly dry at day30 |31|5|
| Day30 water≤1mm |157|25|
| Day30 water≤1cm |464|88|
| Day30 water≤10cm |2270|557|
| Day30 water≤20cm |4303|1284|

The original-fixture climate survey used the isolated reserve candidate, not a perfectly matched reserve-free control. These are descriptive climate contrasts, not a controlled biological performance comparison. No physiological reserve conclusion follows.

A promising dry site,35503, was dry85.83% of ticks but ranged266.50–317.38K (mean288.64K). No site met both dry≥80% and temperature never below280K. More dry land exists, but this does NOT establish accessible frost-free drought evolution. Rain still wets most nominal land; the simplified atmospheric column remains unchanged.

## Reproduction
Run `web/tests/egl-continents-prepare.py <generated-copy>`, then build that copy with `web/tests/egl-origin-build.zig` and Zig0.13. Native flags: `QA_CONTINENTS=1 STELLA_FORMS_SINGLE=1 STELLA_ORIGIN_COUPLED=1 STELLA_ORIGIN_FAST=1 STELLA_PRODUCER_LONG=1 STELLA_DIAGNOSTIC_DAYS=30`. Optional `QA_CLIMATE_SCAN_PATH` writes per-cell CSV. World-water planner unit tests pass3/3. Native build succeeds.

## User-facing next step, not implemented
Offer a new-world-only choice “Random” / “Continents · about70% ocean” beside the Origin/Sandbox start flow, retaining Random. Explain that aquatic life still starts in water, and existing saved worlds are unchanged. Do not add a live ocean-drain slider. Menu layout/mobile validation and independent review are required before shipping.

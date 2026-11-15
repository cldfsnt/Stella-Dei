# Natural player-world progression from day30 to day60

One preserved natural30-day QA world continued in current coupled Planet.simulate:1800ticks ×1440seconds, no care, resource inputs, imported organisms or assigned traits. This is30 additional simulated days, not measured browser pace. An unrelated nursery setup precedes loading in the shared harness; loading completely replaces its saved model. Exact source and local-only saved checkpoints are hashed in provenance.json. Full saves remain local, not Git. Screenshot framing explicitly invokes existing Find life at each checkpoint; no automatic following is proposed. Native390×700 EGL llvmpipe with browser-policy branches, NOT Android/WebGL gameplay evidence.

|Sim day|Living colonies|Occupied patches|Biomass density sum|Max generation|Forms mat/cushion/rosette/ribbon/branching/canopy|
|---|---:|---:|---:|---:|---|
|30|18|10|.200586|3|12/2/1/2/0/1|
|40|62|28|1.176769|5|20/13/13/8/0/8|
|50|70|37|2.484558|7|17/16/14/9/1/13|
|60|64|37|2.591618|7|12/16/13/8/1/14|

Biomass is sum of per-cell kg C/m² values, NOT planet kilograms or a species count. Forms classify actual inherited traits plus actual support tissue; these are aquatic microbial growth forms, not terrestrial plants or animals. All6forms appear naturally byday50. Maxstructure expands .0892→.1483 atday50, organization .0629→.2605 atday60; feedingmax .1875→.3774 atday50. Detailed all6trait ranges and habitat histories retained in checkpoints.txt. Tracked arrivals/losses are transient since-load counters; births cumulative.

Births48→1560; arrivals since load1505; tracked colony losses1205; relocation count0→23. Living population levels off fromday50 to60 but births/deaths continue, so do not describe it as frozen. Whole-world ID intersection between checkpoints: day30→40 keeps16, adds46, loses2;40→50 keeps36, adds34, loses26;50→60 keeps43, adds21, loses27. Intermediate births/deaths are not reconstructed from endpoints.

No-care patch13594 biomass .030954→.033233→.030473→0: this initially diverse local community disappears while the wider world progresses. Its nutrient rises to .02509 atday60; no cause isolated. Original nursery patch13596 persists around .030, nutrient remains low .00018–.00024. Temperature/depth evolve naturally. This is evidence against universal extinction/stall in this one world, NOT proof every seed succeeds or of deterministic succession.

## Safety / oracle checks
Every checkpoint asserts valid cells (finite/nonnegative resources, valid trait/tissue invariants), unique living IDs and parentID<childID; finite nonnegative atmospheric reservoirs checked by the model and gas nonnegative assertions. These are validity/inheritance-order checks, not complete parent-child trait delta validation or a new global conservation proof. Current resource accounts and full stats retained; no conservation claim from unrelated summed nutrient/biomass alone. Snapshots immediately serialize capture before future ticks, avoiding borrowed dense-array aliases. No observer-parity comparison was needed for this progression question; existing separate observer tests retain that role.

## Visual / gameplay conclusion
Actual captured checkpoint contact sheet shows visible expansion and varied forms after explicit framing. This suggests the next major playability problem is helping a player reach and see long progression and understand real turnover, not forcing faster winners or adding untested traits. The fixed-step replay does not establish comfortable real-time waiting, browser throughput, automatic visibility, or fun for all users. Onlyone starting world was tested, as requested.

Build/run exit0, inherited GPA teardown leaks remain. Initial compile-only unused QA imports corrected; failed log preserved. No production changes. Reproduce with egl-natural60-prepare.py +egl-propagule-visual-build.zig, then QA_PULSE_SAVE=<preservedworld>, STELLA_ORIGIN_COUPLED=1 STELLA_ORIGIN_FAST=1 STELLA_PRODUCER_LONG=1 STELLA_FORMS_SINGLE=1 STELLA_ORIGIN_WIDTH=390 LIBGL_ALWAYS_SOFTWARE=1. Screenshot/save paths are QA scratch outputs.

## Baseline identity follow-up
Of18 living day30 baseline IDs (not necessarily founders),16/12/10 remain living atday40/50/60. Living cohorts with recorded prior grazing total42/56/57 atthose checkpoints; this is history, not eating now. Exact recomputed counts in baseline-survival.json.

# Actual habitat engineering: one natural world, three retained outcomes

Research only; no production change. Native EGL/llvmpipe, not browser or Android acceptance. See PREREG.md and the exact copied-source provenance. Input is the actual naturally evolved day-60 save, SHA256 `76d5f4af52b9b26272381e220d899a0ff6f780479b7164709c8d09b1fde97dd7`.

## Result

An initially empty patch colonized naturally in **all three arms**. A single nursery intervention increased standing biomass at that patch, but harmed the surrounding community initially and left fewer colonies globally. It was not an unconditional improvement.

| 14-day outcome | Untouched | One pond | One nursery |
|---|---:|---:|---:|
| Initial selected depth, m | 17.819 | 15 | 5 |
| Final selected depth, m | 17.822 | 17.261 | 7.400 |
| Selected biomass, kg C/m² | .013828 | .015391 | .023396 |
| First sampled occupation, hours | 6.4 | 7.2 | 7.2 |
| Occupied post-tick samples / 840 | 802 | 823 | 823 |
| Original root + new descendants alive | 3 | 1 | 1 |
| Original root + new descendants biomass | .140697 | .079086 | .084476 |
| Globally occupied patches | 38 | 36 | 37 |
| Global living colonies | 60 | 52 | 49 |
| Natural births since start | 725 | 636 | 642 |

Both tools dried **12 initially occupied rim patches** immediately. At day 1 only six of those patches remained occupied, versus all 12 in control. All 12 were occupied again at day 14; this does not prove the original colony identities survived. The initial root was ID55 at source3106. Target13594's first observed new colonies descended from ID120, not ID55; later colonies also descended from ID328. No seed, transplant, assigned traits, repeated care, water clamp or forced survival was used.

The selected patch is a hole in the existing community, not an outward habitat bridge. The present-day production habitat graph contains 2,581 eligible patches in 347 components, but only one component contains currently occupied eligible patches, and that component has only **one reachable empty eligible patch**. Eligibility is not a growth/survival guarantee, and the graph is not an absolute dispersal barrier: actual propagules can enter harsh neighbors and thin-film organisms can persist outside its predicate.

## Accounting and limits

Each arm restores the same independently serialized world, performs zero or one actual public export, then runs 840 unchanged coupled 1,440-second ticks. Every cell is validated each tick. Immediate oracle permits only the planned elevation/water footprint; all biological resources, identities, RNG and histories remain byte-identical. Immediate save/load roundtrip and final restoration pass. Root-family tracking includes the root plus only new descendants born after the assay starts, not pre-existing relatives. Counts are sampled at tick boundaries.

Pond and nursery remove respectively 261,032.6312 and 337,727.9242 units of 10^9 kg water as explicit god-tool intervention. Absolute terrain displacement proxies are 6.99096e13 and 6.99845e13 m³, not conserved excavation mass/energy. The patch width is about 87.6 km; a 19-patch footprint is roughly 145,721 km². These are coarse planetary cells, not literal garden ponds.

After 14 days, carbon residuals relative to post-action baseline are +18,920 / −5,212 / −14,456 kg; nutrient residuals +343.84 / −289.37 / −480.62 kg. Coupled water residuals are approximately −31.88 million units of 10^9 kg in every arm. Existing model numerical/global-water drift is retained, not hidden or attributed to the immediate tool. Exact fluxes, traits, IDs and intermediate outcomes are in results.json. No trait-specific adaptation, universal fitness or closed global conservation claim follows from this one world.

## Validity correction and evidence

The first run was invalid as a pond comparison: an inherited QA preparer globally replaced `makeSelectedPond` with `makeSelectedNursery`. Both treatment arms therefore began at 5 m. This was caught before accepting results. Its full log is retained as invalid-duplicated-nursery.log.gz, and local full saves are hashed. It is not used in the table above.

The corrected preparer restores the production public pond body and verifies both public action bodies, both PlayState methods and the entire pond_action module. The reusable all-export audit additionally checks **all 51 exports**, with zero unexplained differences and no named exceptions. Native availability bridging changes only the private web-state accessor. Assertions require the expected 15 m pond versus 5 m nursery center. Corrected run exits 0; inherited GPA teardown leak messages remain, so this is not leak-free acceptance.

comparison.png shows actual day-74 native frames after explicit Fit life in each arm. They visibly differ in community arrangement, but glyph appearance alone is not a physiological or ancestry measurement.

## Reproduction

Run `python3 web/tests/egl-habitat-engineering-prepare.py <absolute copied-source directory>` then the standard Zig 0.13 native `web/tests/egl-propagule-visual-build.zig` build with `-Dsource=<copy>/main.zig`. Run with `QA_PULSE_SAVE=<natural60-day60.json>`, `STELLA_ORIGIN_WIDTH=390`, `STELLA_ORIGIN_COUPLED=1`, `STELLA_ORIGIN_FAST=1`, `STELLA_PRODUCER_LONG=1`, `STELLA_FORMS_SINGLE=1`, software EGL and a dedicated capture prefix. The preparer records source provenance and all three deterministic arms. Full logs are deterministic-mtime gzip archives, verified losslessly against originals before archival; full saves remain local with hashes.

## Next useful player-facing change (proposal only)

Before a pond/nursery action, show its actual bounded footprint and occupied floor/rim counts, water added/removed, and a clear warning that the rim becomes dry. A shared pure plan must reproduce current ordered writes exactly, with checked world/selection/input freshness before explicit confirmation. Do not silently choose a supposedly beneficial site or alter biology. A later boundary-habitat experiment would be more informative about outward expansion than repeating this central-hole intervention.

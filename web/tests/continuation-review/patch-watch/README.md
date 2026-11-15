# Selected-patch observation, v42 candidate

## Feature
Explicit **Watch this patch · 10 seconds** closes Life snapshot and observes the selected Origin patch while the simulation already runs. It never starts, unpauses, speeds up or cares for the world. A compact HUD reports actual simulated hours and actual grazing intake in kg C/m², with Stop/Dismiss. Results are local and transient, not save fields.

The accumulator takes the actual `Microbes.step` flux before relocation, never differences lifetime lineage counters. It owns one selected planet/patch only, uses no scans or allocations, and changes no biology/RNG/resources. Empty/no-intake observations are explicit; historical feeding is not described as current eating. The observer checks its ten-second deadline at active tick boundaries; an already running engine tick is indivisible. JS also has a deadline timer. Pause, menu, world/load, changed selection, pointer/keyboard navigation, hiding/leaving the page, or explicit cancel stop observation. Results are patch-level, not attributed to specific organisms or the whole world.

## Passed
- Five deterministic Zig observer tests: exact selected-cell accumulation, empty/no-step interval, pause/world/selection/manual stop, owner isolation, deadline and invalid/overflow guards.
- Entire JS test suite: 12 tests, including bounded timers, blocked start, stale callback protection, exact supplied values, hard stop, and invalid results.
- Root reran 47 save-schema tests; no schema changes.
- Actual native coupled engine: genuine 30-day seeded nursery, seed 8156589452691600790, subdivisions6, normal Grow target21600; no assigned evolved biology or later auto-care.
- Natural patch3420 had recorded historical feeding but only one resident at day30. Both 8-tick/3.2-hour and 60-tick/24-hour watches correctly recorded **zero** new intake, matching independent flux oracle.
- QA-only selection of first naturally coexisting feeder and another resident found patch3421. Over 60 actual engine ticks / 86,400 simulated seconds it recorded **0.0014814876212767558 kg C/m²**, exactly equal to the independent selected-patch `Flux.grazed` sum. No food, feeding histories, traits, oxygen or light were assigned.
- Positive and zero tests restored the same immutable baseline before both observer-on and observer-off arms. Resulting serialized worlds were byte-identical, including saved resources/cohorts/RNG/stats. This demonstrates observation purity, not a guarantee about every save/reload future trajectory.
- Actual native pause, selection change and successful load canceled observation. Browser shell/HUD testing is documented separately in ui-fixture.md; mocked data there are not biological evidence.

## Reproduction and evidence
Use `web/tests/egl-patch-watch-prepare.py OUT`, build the generated main with `egl-propagule-visual-build.zig`, then run with STELLA_ORIGIN_COUPLED=1, STELLA_ORIGIN_FAST=1, STELLA_PRODUCER_LONG=1, STELLA_DIAGNOSTIC_DAYS=30, STELLA_FORMS_SINGLE=1 and LIBGL_ALWAYS_SOFTWARE=1. Captures should use a writable STELLA_EGL_CAPTURE_PREFIX. Final preparer selects the naturally coexisting patch; earlier zero-run source differs only in QA selection/window. Its code writes a local natural-30day checkpoint beside OUT, not to git.

Native logs are losslessly gzip-compressed with mtime0; DECOMPRESSED_SHA256SUMS records their original bytes. `native-positive.log.gz` is final positive acceptance; `native-day.log.gz` and `native-controlled.log.gz` are natural zero controls. Failed logs remain: `native.log.gz` caught a test-only borrowed save array restore alias; `native-final.log.gz` caught the fixture trying to start an old patch after load correctly reset selection to0. The following `native-proof.log.gz` diagnosed and passed after reselecting; later controlled tests symmetrically restored both arms. No production biological change was made to fix these fixtures.

## Limits
Native offscreen rendering and control-flow evidence are not Android/WebGL gameplay verification. Native acceptance bypasses real-time frame pacing to exercise a known count of real full-engine ticks, but keeps the observer's real deadline enabled. Browser timer behavior is separately unit/fixture tested. Harness exits0 after acceptance, but reports a GPA allocation leak during teardown; this is not a clean leak-check claim. Watcher itself allocates no heap. No new organism, armor, succession or fire-adaptation model is shipped here.

# Selected-patch ecology pulse

Candidate extending the existing ten-second local watch, not a new biological model. Actual `Microbes.step` receipts accumulate fixed carbon, biological carbon returned to air, and grazing intake. Start/end living biomass sums finite positive tissue across the selected patch's four slots; colony counts are resident positive-biomass cohorts, not species or cumulative births. End snapshots occur after movement and reproduction. Thus changing occupancy and donor transfers are included in **net patch change**, never labeled growth, death or adaptation.

The return-to-air receipt combines support upkeep, grazing respiration and dead-carbon recycling in the biological update. It explicitly excludes later movement respiration, god tools and physical gas redistribution. It is not a complete patch carbon budget and is not a mortality count. Observing changes no resources, RNG, time, pause/pace, saved fields or physiology. No extra full-world scan or allocation: selected four-slot population snapshot only, plus the existing active observer guard/flux hook. The 10-second deadline is checked at tick boundaries; an admitted indivisible tick may finish afterward.

Controller renders four newline-separated lines (<350 characters in the typical unit fixture), leads with net biomass and fixation rather than absence of grazing, and retains explicit zero/no-step output. Main's shell integration owns HUD white-space and detailed explanation. Native gameplay acceptance and browser layout are separate claims.

## Focused verification
- Eight Zig observer tests passed: existing guards/deadlines/owner isolation, exact selected flux sums, atomic invalid-flux refusal, finite bounded population, stopped snapshot freeze, empty-to-occupied end snapshot and invalid time handling.
- Eight controller tests passed: old interruption/replacement behavior, missing fields refused, fixation with declining biomass not called growth, compact four-line text.
- Entire currently checked JavaScript suite:20 tests passed. Concurrent main UI changes may require a later final aggregate rerun.
- Actual native acceptance passed, exit0: naturally evolved patch3421,60 real coupled ticks /86400 simulated seconds. Fixed carbon0.001978155396955117; biological return0.003281266806880012; grazing intake0.0014814876212767558 kg C/m². All equal independent per-step receipt sums exactly.
- Start/end living biomass0.009361055446788669→0.006635898724198341 kg C/m²; resident colonies2→1, exactly matching final post-scheduler state. This demonstrates photosynthesis occurring alongside net decline, not an inferred cause or death count.
- Complete saved worlds observer-on/off are byte-identical. Pause, selection change and load cancellation pass; final original restore/save validation passes.
- Known inherited GPA teardown leak warning remains despite exit0; this is not a clean memory-leak certification. Observer adds no heap allocation. Earlier printed generation-history diagnostics belong to the skipped fresh-world lead-in, before loading the natural save; its mean-update value is NaN because zero history frames were measured. No performance claim uses it.

## Native reproduction
`python3 web/tests/egl-ecology-pulse-prepare.py /absolute/new/src`

Build using Zig0.13.0 and `web/tests/egl-propagule-visual-build.zig`, `-Dsource=/absolute/new/src/main.zig`, dedicated prefix/cache. Run with `STELLA_ORIGIN_COUPLED=1 STELLA_ORIGIN_FAST=1 STELLA_PRODUCER_LONG=1 STELLA_FORMS_SINGLE=1 STELLA_ORIGIN_WIDTH=390`, `LIBGL_ALWAYS_SOFTWARE=1`, a writable capture prefix, and optional `QA_PULSE_SAVE=/absolute/watch-natural-30day.json`.

The optional input reuses the previously preserved genuinely evolved30-day nursery rather than regenerating history. No traits, tissue, food or gases are assigned. Test-only selection locates a naturally coexisting feeding patch. Independent copied Planet instrumentation sums actual step fluxes. Start/end state checks use actual selected cell; complete observer-on/off arms restore the same immutable save and compare final serialized worlds. Previous obsolete numeric-ID finder assertions are not rerun by this harness; the separate feeding-finder evidence remains preserved. Source/current binary provenance and input SHA256 are recorded separately.

This is native engine/control-flow acceptance, not proof of Android/WebGL performance, touch behavior or complete game functionality. No browser speed claim. No new immunity, dormant pool, fire adaptation or forced ecological winner.

## Additional controlled actual-scheduler arrival gate
`src/qa_patch_pulse_arrival.zig` passes through the real current `Planet.simulateMicrobes` scheduler (lifecycle build, exit0). Two deliberately arranged patches, finite gases, assigned donor tissue0.1 and earned-credit field0.02; these initial values are a test fixture, NOT natural evolution. All six source adjacency entries target the initially empty watched patch. Actual production propagation debits donor tissue/credit and creates one child after the growth phase. Watch reports starting biomass0/count0 and end biomass0.004000000189989805/count1, zero target growth-phase flux, one simulated second. This specifically verifies the population snapshot is after reproduction rather than before it. Observer-off repetition exactly matches cohort/RNG state, stats, propagule feedback and gases. This is not an additional natural-world or movement-arrival claim.

Reproduce with Zig0.13: `zig build --build-file web/tests/lifecycle-build.zig -Dsource=/absolute/repo/src/qa_patch_pulse_arrival.zig --cache-dir /absolute/cache --global-cache-dir /absolute/global-cache`. Imported core tests also execute; the captured run exits0.

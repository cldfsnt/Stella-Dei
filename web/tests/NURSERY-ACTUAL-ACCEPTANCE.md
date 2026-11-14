# Explicit nursery actual-engine acceptance

The guarded `makeSelectedNursery` API was run on the generated browser-resolution world, ordinary Find habitat cell13596. Source includes the bounded water-cycle correction. One real seed, normal Grow6h/s,30 simulated days (120 nominal play seconds), no automatic refilling, temperature changes, trait gifts or forced reproduction. Nursery initial action repeated before time starts to test repeatability. The old15m action remains separate.

Final:11 occupied patches,26 living cohorts,53 accepted paid propagule arrivals,24 tracked colony losses. Actual form counts:17mats,3cushions,3rosettes,1ribbon,0branching,2canopy. Biomass final0.2029309, selected depth8.544176m/temp295.47995K. Six inhabited patches visible in correctly centered camera. This matches the prior same-world/same-location shallow experiment exactly, validating the actual API rather than only a test-specific geometry hook.

Save10,455,262bytes: invalid input rejected without mutation, exact restore passes, transient arrival/loss counters/visual observers cleared. World water+vapor drift0.006882% over30days measured, not exact floating-point conservation. Existing native shutdown allocator warnings remain; full simulation process exits0. Native replay of saved state was manually stopped after images rendered because cleanup waited; it is not a second simulation or clean-exit claim.

`results/nursery-actual-api/nursery-inspect-002.png` is the real final saved state, paused in Inspect mode, with six visible life patches.The initial003 capture is not valid selected-colony proof: the test opened details without updating clickedPoint. Replay has been corrected; use002 overview until the corrected capture is present. Saved-state load clears transient arrivals/loss marks; none were fabricated for these pictures. This is an aquatic producer demonstration, not proof of full land-plant/rabbit evolution, every starting location thriving or mobile device FPS.

Reproduce from repo:
```
python3 web/tests/egl-nursery-prepare.py /tmp/nursery-qa
# Build with web/tests/egl-origin-build.zig and -Dsource=/tmp/nursery-qa/main.zig
STELLA_ORIGIN_COUPLED=1 STELLA_ORIGIN_FAST=1 STELLA_FORMS_SINGLE=1 STELLA_PRODUCER_LONG=1 STELLA_DIAGNOSTIC_DAYS=30 STELLA_EGL_SAVE_PATH=/tmp/nursery-final.json <binary>
```
Inherited FAST flag selects the long-run harness branch; actual pace is21600sec/sec. The new preparer uses unchanged production pond/planet source, no QA_NURSERY geometry substitutions. Source root override:STELLA_SOURCE_ROOT. `--replay` adds saved-state-only rendering, with `QA_REPLAY_SAVE` and `STELLA_EGL_CAPTURE_PREFIX`. Its fixed13596 selection is only for this documented world fixture.

The first run log's inherited `production_15m=true` string is inaccurate. Actual API, center5m assertions/source and startup water volume establish this was the shallow nursery. New preparer labels it`actual_nursery_api=true`.

## Compact Watch visual acceptance

`results/nursery-actual-api/nursery-watch-mobile-002.png` was visually reviewed after loading the actual final save through normal save code, activating Watch, and rendering with the native harness's browser/mobile substitutions. It shows the compact one-row Play/Tools/Grow toolbar, seven actual occupied patches, distinct canopy/rosette/mat silhouettes, day 30 and 53 recorded births. No life, traits or feedback events were added for the screenshot. Current `nursery-replay.zig.part` also fixes clickedPoint for future detailed inspection; the original003 detail screenshot is excluded.

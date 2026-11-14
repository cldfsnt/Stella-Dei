# Explicit Fit nearby life camera candidate

Integrated into v22 after isolated review. New API `stella_fit_life()` returns1 success,0 no nearby Origin cluster,-1 no active world. Isolated shell has More→Fit nearby life, reachable during compact Watch. It resets touch state and closes the sheet before calling the action. Missing capability/world and no nearby life have visible actionable messages. No new cramped native header button.

## Scope
Read-only, explicit framing, not continuous camera following. Find an actual living anchor within at most3 adjacency steps of the current viewing direction, then follow only adjacent occupied patches. Bound to128cells and ~11.5° from that anchor. Disconnected or distant colonists are excluded; no global mean/jump. Fits actual3D points using70° FOV, screen aspect and mobile toolbar/footer/glyph margins; minimum100km above local surface. Polar singular regions and invalid geometry fail without changing camera. Does not seed, terraform, modify climate/life/resources, advance time, alter pace or unpause. Existing selection remains; user can inspect actual patches afterward.

## Six actual saved-world comparisons
Saved day30 worlds from the preselected42/2027 playtest, no injected organisms or events. Native renderer uses browser/mobile substitutions.

| Saved world | Viewport | Visible patches before→after | Connected cluster | Glyph size change |
|---|---|---|---|---|
|42|320×700|6→8|8|−2.78%|
|42|390×700|6→8|8|−1.60%|
|42|800×400|8→8|8|−0.63%|
|2027|320×700|3→5|5|−1.54%|
|2027|390×700|4→5|5|−0.74%|
|2027|800×400|3→5|5|−1.16%|

Glyph changes are computed from actual renderer LOD formula and logged camera distances; not guesses from screenshot. Reviewed320portrait,390portrait and landscape after-images: silhouettes remain distinct/readable, no toolbar/footer clipping, and additional nursery rim/terrain context appears. Images in results end002 before/003 after. These are native screenshots, not Android performance claims.

## Guard and selection proof
All6cases pass no-world rejection, empty-world no-life failure with unchanged camera, repeated-action idempotence within0.01km numerical tolerance, pause/pace/time preservation and full saved-state equality after normalizing only the four camera fields. Same world/resource hash across viewports:42=c957a0149e8f9813,2027=d5cab3d03314df03.

Every occupied cluster centroid was projected and exercised through the real native pointer/Inspect handler after fitting:8/8targets for42,5/5for2027 at every viewport. Correct selectedPoint and clickedPoint asserted, UI guard retained. No model writes. All native cases exit0; existing allocator shutdown warnings remain. The harness bypasses only browser availability check for native exported callback testing.

Pure helper3tests pass (local/distant separation, portrait geometry/safe altitude, empty/polar/invalid nonmutation). Isolated production shell test passes including success, no-life, missing-world/API and failure feedback. The integrated production shell tests, three helper tests and WASM build passed; no browser runtime or Android performance claim.

## Reproduce
After integration, `STELLA_SOURCE_ROOT=<repo> python3 qa/prepare.py /tmp/fit-qa` creates isolated source and build/shim. Build `/tmp/fit-qa/build.zig` with `-Dsource=/tmp/fit-qa/main.zig`. Run from repo asset cwd with `QA_REPLAY_WORLD=42` or2027, `QA_REPLAY_SAVE=<actual saved world JSON>`, `STELLA_ORIGIN_WIDTH=320|390|800`, `STELLA_ORIGIN_HEIGHT=700|400`, and `STELLA_EGL_CAPTURE_PREFIX`. The original fixture saves are /tmp/v20-seed-42.json and /tmp/v20-seed-2027.json. Native source hashes retained under qa.

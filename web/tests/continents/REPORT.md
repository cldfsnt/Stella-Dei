# Continents isolated v23 integration acceptance

Base: b73cf9c10692b1dfad70452ab819c713347d9d46. Originally isolated; integrated in v24 after the additional current-main checks under integrated/.
Tracked-file git-object comparisons matched this base except four intended source patches: main, main_menu, play, planet. New world_setup and inventory planner files are additions. Latest v23 atmospheric wind cache is retained; microbial physiology and schema6 remain unchanged. No reserve feature is included.

The explicit Random/Continents selection affects only fresh Origin/Sandbox creation. The saved-world replacement uses generate_terrain=false with defaultRandom, and copies the complete saved inventory. initWithTopology also deliberately ignores menu selection. No new save provenance is fabricated.

## Tests
- World setup/layout2/2 and initial inventory planner3/3 pass.
- Full WASM build plus packaging succeeds. Artifact index.wasm SHA256: 6da80e5d3d585986b2d4383bc631cba75aaafe893b561ffa45581429a4e553a5.
- Actual native menu pointer tests select Continents, Random, Continents, then start Origin or Sandbox (including its Create my planet button).
- Save test captures the newly created mode, restores an existing30-day schema6 Origin fixture while Continents remains selected, compares complete canonical JSON, then restores the newly created mode and compares its complete JSON. This includes all resources, terrain, traits, organisms, counters, RNG and serialized view/time fields.

Initial desktop-threaded harness exposed a test race: background simulation changed water/vapor during Sandbox restore. It was not a preset inventory recalculation. Corrected harness uses the browser-equivalent cooperative EventLoop and a quiescent frame boundary, as the established Origin native harness does. No production physics/save changes were made to hide this race.

Corrected cooperative native results: BOTH modes pass. Origin390×700 and Sandbox640×360 each completed the real pointer menu path, existing30-day Origin restore and created-mode restore with full canonical JSON byte equality; selected Continents was ignored by both loads. All stayed at schema6. Native rendering is not a substitute for actual Android WebGL/device testing. Pre-existing shutdown allocator-leak report persists and is not described as clean sanitizer acceptance.

## Reproduce
Generate native source with web/tests/egl-world-menu-prepare.py, compile using egl-world-menu-build.zig. Run with QA_SANDBOX=1 to select Sandbox; omit for Origin. QA_EXISTING_SAVE selects an existing schema6 Origin fixture; default local QA fixture is not bundled. STELLA_ORIGIN_WIDTH/HEIGHT controls viewport. Pointer-generated actions, not direct preset assignment, drive menu choices. Fixture data is loaded via actual save_game.replaceWorld.

Use continents-v23.patch for integration, never wholesale replace current production files. No deployment is authorized by this test report.

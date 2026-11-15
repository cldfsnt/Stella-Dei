# Independent actual-native Advance-one-day acceptance

This uses a copied actual current game, actual exports and shared production `advanceFrame` callback, real Planet physics, real OpenGL rendering and native GLFW shim input. The only platform bridge makes webPlayState available in native QA; the save adapter's `/saves` destination is redirected to a dedicated QA directory. No production/source ecology changes and no real user's saved file are overwritten.

Actual preserved natural60 world, deliberately paused and framed on existing life before freezing the fixture. A reference runs60 ordinary1440-second coupled ticks with final real render. The exported job must produce byte-for-byte identical complete saved state, preserve pause/pace, render no intermediate frames, and render exactly once before terminal status. Its rendered glyph/pick caches are deliberately emptied immediately before tick60 and must refill with targets whose real cells contain living biomass.

Other actual API/callback gates:
- stale world and running-world start refusal without mutation;
- save/load, speed, water, seed, tool, zoom, mouse movement/scroll/press blocked during active job;
- wrong-token cancellation rejected;
- held physical left mouse button remains latched after explicit terminal dismissal, neutral release clears it;
- final one-shot cursor baseline tested in controlled free camera: first event zero delta, second normal delta; restored afterward;
- cancellation after7ticks preserves partial simulation, waits for tab visibility, then redraws once;
- context loss permanently blocks further ticks/draws even after context-restored signal; correct paused current partial world can be saved, exact file bytes checked; changed pause/time/world denies safe save; load/mutations/dismiss remain blocked;
- long frame gap, world change and direct save-apply cancellation do not execute an extra tick;
- original paused fixture restored exactly.

This does NOT create actual WebGL context loss or test browser IndexedDB durability, touch input, keyboard W/S physical shim release, browser scheduling, or a real user's device. Those limits remain explicit. Recovery tests invoke real production environment-state transitions on a still-valid native EGL context, verifying that no subsequent render is dispatched.

## Preserved fixture failures

Initial complete60tick/guard acceptance passed, but partial-cancel save equality compared a pre-render snapshot to a post-render snapshot. Diagnostics found ONLY `camera_target` changed through existing render normalization: [-3441.7158203125,4535.79833984375,1384.090576171875] → [-3441.71630859375,4535.798828125,1384.0906982421875]. No physics/biology/other serialized field differed. The corrected oracle independently restores the partial state, performs an ordinary real final draw, and compares COMPLETE serialized state, without stripping/normalizing resource fields. Failure logs/snapshots preserved.

A later QA linking failure used a shim without qa_capture. Switched to existing egl-propagule-visual-build.zig, whose shim is the same as origin plus the screenshot function. No production fix was needed.

## Reproduce

Run `python3 web/tests/egl-advance-acceptance-prepare.py <workspace>/site-tmp/advance-acceptance/src`, then Zig0.13 build with `--build-file web/tests/egl-propagule-visual-build.zig -Dsource=<copied main> --prefix <workspace>/site-tmp/advance-acceptance/build`. Run from repository cwd with STELLA_ORIGIN_COUPLED=1, STELLA_ORIGIN_FAST=1, QA_PULSE_SAVE pointing at recorded natural60 save, LIBGL_ALWAYS_SOFTWARE=1, EGL_PLATFORM=surfaceless, and a capture prefix inside the fixture directory. This is ReleaseSafe native correctness, not a wall-clock speed benchmark.

An optional cursor check initially supplied callback coordinates while the GLFW physical cursor remained over the mobile toolbar, so both events correctly returned without rotation. Corrected fixture uses actual shim pointer moves on the canvas. Final first event preserves free-camera rotation exactly; next event changes it normally. The inherited native fixture uses browser-style mobile UI predicates at390×700, not an Android browser. Source checksums distinguish the fixture copy from production.

## Final result

Final process exits0. All gates in result.txt pass on the final cursor-baseline source.34 live glyphs and34 live-cell pick targets regenerated after deliberately clearing their caches before tick60. final.png is the actual passive final redraw; independently visually inspected by reviewer and coordinator. It contains clear green/cyan life forms and real event marks, with no active tool controls. No fabricated plants or injected ecology.

source-sha256.json pins production main/controller/play/save/performance/Planet/atmosphere plus actual compiled-copy and natural60 input. All those production and copied hashes were rechecked unchanged after final execution. Recovery save file is an exact partial snapshot; browser IndexedDB sync remains outside this native gate. Final fixture also passes existing save validation/rejection/restore check. Allocator teardown diagnostic retained in log; this work does not claim to fix it or establish a device memory budget.

Full camera before/after JSONs remain local; only their hashes and exact differing camera coordinates are committed. No large world snapshots are duplicated in this evidence checkpoint.

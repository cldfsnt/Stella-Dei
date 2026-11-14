# Selected-only Water− correction

Previously one tap unconditionally zeroed selected patch and all neighbors, despite single-patch feedback. Now the real DrainWater tool delegates to water_brush.remove: up to1m selected depth per tap,5m/second held using same real-time bounded edit_rates.water as Water+. Never touches neighbors, organisms, temperature, game time or pace; no automatic hydrology claim. Deletion is explicit external removal, not modeled evaporation/drought chemistry. Fine±0.1m and target-depth APIs unchanged.

Helper returns actual removed depth and status. Negative/nonfinite mass, conversion or hold elapsed and invalidindex refuse unchanged. Zero depth is a dry no-op. Zero elapsed no-op; stalledelapsed bounded. Transfers below float resolution or rounded above requested tolerance refuse without changing water. Existing terrain/hydrology can later move water when simulation advances; unchanged-neighbor assertion applies to the intervention instant only.

Five model/edit-rate tests pass: tap and partial-depth clamp, no neighboring writes,15/30/60/120Hz two-second gestures, stalled/invalidelapsed, badindices/nonfiniteinputs and huge-depth precision refusal. Shell tests pass updated explanatory copy. Native harness now uses actual testAction(2), checks all other watercells and biological save unchanged, checks .25m temporary fixture clamps0 and drytapno-op, then restores exact preintervention save before final existing savechecks. It does not leave altered water in the natural acceptance world. Existing egl-prepare tool logging updated to require actual water decrease instead of obsolete totaldrain semantics.

No new evolution rule, fire trait, water creation, save schema, cloudbackup or background action. Parent owns publication.

## Native result
Final isolated native build/run exit0. Actual30-day nursery,10occupied patches/48arrivals, all10rendered roots correctly picked, godpreview exactsaveunchanged. On real living selected patch12349, actual Water− tool removed exactly1m; every other watercell unchanged; biological data/time/pace/pause unchanged. Temporary selected0.25m fixture clamped0; repeat drytapno-op. Original world restored exactly from independently parsed original JSON; usual invalidsave rejection and exactrestore also pass (schema6,10452383bytes). Native/EGL adapter is not Android/WebGL; preexisting shutdown allocator leak persists.

First native attempt reached30days but fixture restore passed capture's aliased live slices directly to saves.apply, causing @memcpy alias panic. Corrected harness restore parses frozen JSON into independent allocations, then exactserializedworld comparison. Production save/action code was not changed for this fixture error. Both sanitized failed and successful logs retained.

Release integration: pinned Zig0.13/Emscripten3.1.64 WASM compilation passed; all seven JS suites and generated JavaScript syntax passed. Final native acceptance passed after fixing test-only aliasing during restoration (serialized frozen JSON now parsed to independent save). No live user save was used. Build v37 contains this water correction; fire-candidate code is deliberately unimported and not playable.

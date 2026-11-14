# v29: lighter bloom and measurement during gameplay

This checkpoint targets render work and clearer performance evidence, not a completed ecosystem or a proven Android speed gain. Biology remains unchanged while separate moist-film experiments address dry-boundary behavior and undergo renewed paired testing.

## Full-resolution seven-tap blur

The symmetric kernel combines adjacent linearly sampled weights into seven fetches instead of nine. The existing kernel sum, full-size HDR render targets, four blur passes, extraction, tone-map composite, atmosphere and effects are retained. This is22% fewer blur fetches, not22% faster gameplay.

Native actual-game paired framebuffers at390×700 and920×700 are exact across ten map/atmosphere combinations, a visibly rendered rabbit and bright sun/day-night transitions. Two paired native timing sequences favor the candidate's median but tails vary. Native llvmpipe is not Android hardware, a GPU timer or a smooth-frame guarantee.

Shader arithmetic is NOT bit-exact. Desktop GL and OpenGL ES3 synthetic HDR textures expose intermediate rounding differences; their final displayed channel differences are bounded by1/255 in the executed144 cases per backend. ES3 changes more components than desktop GL. These synthetic tests and representative-image review do not prove identical results on every phone GPU. Preserve the detailed report and failed/unavailable validation records rather than presenting exact desktop images as WebGL evidence.

## Gameplay measurement

An explicit local measurement closes the Speed panel for approximately10 seconds of ordinary play, then retains results for later review without automatically reopening it. The achieved simulated-hours/second rate covers actual elapsed run time. Frame timings are the last block of up to60 frames, not a whole-run average. No data is transmitted or persisted. Pause, menus, backgrounding, world replacement or speed changes cancel the run rather than mix incompatible states; prior completed results remain visibly labeled.

Final integration evidence is appended after the final source passes its checks. Actual Android layout, gesture behavior and performance acceptance are not verified by this environment.

## Final executed gates
All seven JavaScript suites pass on the integrated source, including queued modal events and repeated/interrupted measurement flows. Final full WASM build/package passes with the new helper present. Native measurement callback code is byte-identical to the integrated engine files: enable/read/disable preserves the complete8,867,927-byte world save and simulation clock; extreme finite metadata yields valid1126-byte JSON in2048-byte capacity. No telemetry or serialized state was added.

The separately captured v28-plus-shader native gate passes paired pixels/model and actual pause/rate/background/menu/load/save tests; physical hashd523353839672a4 at all three target rates,8,734,640-byte exact save restoration. This shader gate predates diagnostic hooks, so it is not mislabeled a full combined native gameplay run. Combined source passes WASM and JS gates, and diagnostic engine files exactly match their independent native invariance test. Native teardown's pre-existing allocator warning remains; it is not a clean-memory claim. Static glslangValidator was unavailable; actual GL and ES3 shader compilation tests ran instead.

Supplemental actual-game ESSL300/browser-format shader runs at390 and920 also pass: displayed channel differences never exceed1/255, including bright-sun48components at390 and46at920; night is exact. Model remains unchanged and reviewed sun images show no discernible halo artifact. This uses desktop GL with browser shader adaptation, not a real browser/WebGL gameplay test. Final evidence includes the initial QA-only link failure and corrected successful runs.

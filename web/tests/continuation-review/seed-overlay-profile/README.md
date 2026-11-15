# Green seed-target overlay: bounded native attribution

No production changes. One fixed shown→hidden→hidden→shown sequence,12warmup frames and30timed frames per block. Actual evolved Sunlit day14 world and fitted390×700 camera, paused; no Play.update or simulation ticks. Timed interval is complete render→gl.finish→swap, not browser rAF, input latency or device FPS. Only copied NanoVG per-draw debug=false is forced to match shipped diagnostic policy; existing native host uses browser-policy render gates. Actual context reports no bloom/0passes. Renderer is software llvmpipe LLVM19.1.7/Mesa25.0.7. Shader/setup validation retained.

Source per-block:

| block | hints | targets | colony glyphs | full render mean ms | median ms | p95 ms | seed CPU mean ms |
|---|---|---:|---:|---:|---:|---:|---:|
|0|shown|4|16|9.440|9.176|10.647|0.12353|
|1|hidden|0|16|10.334|9.519|15.365|0.000253|
|2|hidden|0|16|9.617|9.392|13.079|0.000217|
|3|shown|4|16|10.532|9.187|21.229|0.11618|

Hide removes roughly0.12ms of seed-target CPU submission/scanning in this native view. Full render medians did NOT improve; driver/system variability spans both conditions and is larger than that removed CPU work. Do not claim an FPS improvement, especially on a laptop/Android or actual WebGL. No sweep or extra favorable repeats. User benefit remains the verified visual decluttering/control, not a promised speed gain.

All4blocks preserve complete saved model/time/RNG bytes exactly. Real colony glyphs remain16, same513sprout candidates, and seed targets4→0→0→4. No biology or camera change. Existing metrics additionally report terrain/scene/post/UI timing in results.json; seed time is nested within UI and these diagnostics must not be added blindly to full render time. Timing counters are copied QA-only. Hidden seed timer is mostly instrumentation floor. Session-only visibility flag is intentionally absent from saves.

Clean window13:37:20–13:37:24UTC2026-11-15 coordinated after rabbit compiler completion and before rabbit outcome runs. Fixed stdout records occur outside timed loops. Reproduce egl-seed-overlay-profile-prepare.py + egl-propagule-visual-build.zig with the existing actual-toggle fixture environment and hashed day14 input. No GPU/browser workaround, no device claim, no performance-driven production patch follows this negative/full-frame result.

# Actual saved-world renderer regression: meaningful close-view cost

Native EGL/software,390×700, paused presentation frames only. Three paired repetitions for each natural-day60 mixed/dominant patch and close/default-globe view. Protocol and all observations are retained; no simulation/device/browser speed claim. Exact released renderSprouts bodies b308b37(v57) and be1abc8(v58), renamed only, run in the same existing frozen browser-policy QA host. This is a narrow function-change comparison, not whole-release build comparison. Source/body/input/binary hashes are recorded.

| View / selected history | v57 median ms/frame | v58 median ms/frame | Median change | All paired changes |
|---|---:|---:|---:|---|
| Close mixed |11.103|13.833|+24.59%|+16.92%,+36.11%,+8.11%|
| Close dominant |10.646|11.586|+8.83%|+9.41%,−0.01%,+15.75%|
| Globe mixed |13.443|13.831|+2.88%|+8.54%,−0.50%,+2.88%|
| Globe dominant |14.085|12.663|−10.10%|−13.09%,−7.47%,−5.66%|

**Do not claim regression-free.** Close mixed is slower in every pair with roughly2.73ms median added time in this proxy. Close dominant is also slower overall, with variability. Globe differences are mixed and cannot justify a global speed claim. Actual emitted glyph counts change intentionally with selected readability: close mixed32→29,close dominant31→27,globe mixed5→1,globe dominant5→3. Fewer glyphs do not guarantee cheaper NanoVG work: the new history band adds several filled/stroked paths, a plausible next controlled attribution experiment rather than a proved cause.

Both runs exit0; all six arms per patch maintain exact complete serialized state after equal render counts, selected body/root checks pass for candidate, hidden back-face has no target, cap64 holds and original input is restored. Known inherited GPA teardown diagnostics remain in unabridged compressed logs. No biology/water/save/production changes were made. First12 shim image captures, all screenshot capture, JSON, assertions and logs are outside timed loops. Every measured frame includes cooperative pump, real render, gl.finish and swap; no PlayState.update or running physics is included. Native diagnostic policy and other rendering are held constant. Native software rendering is not a mobile/laptop/WebGL result.

Timing window2026-11-15T09:26:17Z through recorded window.txt end; both siblings confirmed no heavy jobs. Only three pairs and two selected actual patches: no confidence interval or broad scene generalization. Recommendation: preserve readability and investigate lower-command-count truthful history glyphs with exact state and visual/picking acceptance before claiming this visual improvement is cheap. Do not silently revert or remove ecology, selected legibility, or safeguards from this evidence alone.

Reproduce: run web/tests/egl-feeding-regression-prepare.py into an isolated src; build with existing egl-propagule-visual-build.zig, same pinned Zig0.13 toolchain. Run with LIBGL_ALWAYS_SOFTWARE=1,EGL_PLATFORM=surfaceless,STELLA_ORIGIN_COUPLED=1,STELLA_ORIGIN_FAST=1,STELLA_ORIGIN_WIDTH=390,QA_PULSE_SAVE=<hashed natural60-day60.json>,STELLA_EGL_CAPTURE_PREFIX=<writable prefix>; unset QA_MARKER_GLOBE for close and set1 for globe. Input/large artifacts remain locally in site-tmp; exact source extraction and hashes provide provenance.

# v30 integrated native guidance/save gate

Passed on the current working production source after the corrected moist-film patch was merged atop v29. No production code edited by this gate. Complete src and shell hashes are in source-hashes.json; all still matched after both runs.

- Origin portrait390×700 and Sandbox landscape640×360 actual menu press/release, Random/Continents selection and world creation exercised.
- A real previous schema6 Origin save loaded after Continents selection without changing any serialized state; each newly created Origin/Sandbox world restored exactly too.
- Actual Life snapshot export and read-only producer-habitat observation left full saved resources/RNG unchanged.
- Test-only four living cohorts stress produced valid JSON with producer_habitat,2681bytes in8192-byte buffer. The cell was restored exactly before gameplay gates. This synthetic serialization fixture is not evolution evidence.
- Actual warm focus/seed/targets succeeded. QA-only all-world273.15K override rejected seed and focus, changed no resources, and rendered zero green seed targets. Original temperatures restored before warm test.
- Both native processes exit0. Known shutdown allocator warning remains; no memory-clean claim. Native Linux rendering and shell tests are not hosted browser/mobile visual QA.

## Reproduction

Create an isolated tree with current production src, assets and deps. Copy the five included egl-* harness files to its web/tests. Run egl-film-guidance-prepare.py with an absolute destination tmp/native-src. Build with Zig0.13:

```
TMPDIR=$PWD/tmp /path/to/zig build --build-file $PWD/web/tests/egl-world-menu-build.zig -Dsource=$PWD/tmp/native-src/main.zig --prefix $PWD/tmp/native --cache-dir $PWD/tmp/cache --global-cache-dir /path/to/zig-cache
QA_EXISTING_SAVE=/absolute/old-schema6.json QA_GUIDANCE_OUTPUT=$PWD/results STELLA_EGL_CAPTURE_PREFIX=$PWD/tmp/origin LIBGL_ALWAYS_SOFTWARE=1 EGL_PLATFORM=surfaceless ./tmp/native/bin/stella-egl
QA_SANDBOX=1 STELLA_ORIGIN_WIDTH=640 STELLA_ORIGIN_HEIGHT=360 QA_EXISTING_SAVE=/absolute/old-schema6.json QA_GUIDANCE_OUTPUT=$PWD/results STELLA_EGL_CAPTURE_PREFIX=$PWD/tmp/sandbox LIBGL_ALWAYS_SOFTWARE=1 EGL_PLATFORM=surfaceless ./tmp/native/bin/stella-egl
```

Old fixture hash is in proof.json; local original retained at stella-shore-visibility/tmp/schema6-world.json, not duplicated here. Generated native harness deliberately substitutes cooperative browser-like scheduling, offline audio and initialized snapshot export gate only. It does not alter production biology.

Initial build used relative cache paths and failed with duplicated web/tests/options.zig lookup; absolute build/cache paths corrected this tooling-only failure. Initial attempted launch before compilation finished returned127; final two runs used successfully built binary. Build failure/final logs retained. Snapshot newline marker appears as literal\n in log, not a failed check.

This gate does not rerun100-day evolution; corrected paired evidence remains separately frozen under ../evidence. Full binary and native captures remain in the isolated stella-film-v30-native workspace. Parent owns deployment and hosted review.

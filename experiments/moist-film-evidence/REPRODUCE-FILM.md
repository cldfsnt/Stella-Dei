# Reproduce isolated film experiment

Start from `d97624d7931f4d8a02e6d5457ea8c14c7aca1e03` with project's existing dependencies/assets. Overlay current `src/simulation/microbes.zig` and new `web/tests/egl-film-{prepare.py,build.zig,shim.c}`, `web/tests/film-summary.py`. Do not overlay on a newer live checkout wholesale. No publishing/deployment steps here.

Use installed Zig0.13.0 and Python3, EGL/Mesa native libraries. Commands from repo root (`ZIG` is the actual executable path):

```
mkdir -p tmp results
export TMPDIR="$PWD/tmp"
"$ZIG" test src/simulation/microbes.zig
"$ZIG" test src/save_schema.zig
python3 web/tests/egl-film-prepare.py "$PWD/tmp/source"
"$ZIG" build --build-file web/tests/egl-film-build.zig -Dsource="$PWD/tmp/source/main.zig" --prefix "$PWD/tmp/native"
```

For each deterministic worldseed1337 and1338, run `on` before `off`, separate processes with unique resultdirectory:

```
export STELLA_PRODUCER_SEED=1337
export STELLA_ORIGIN_COUPLED=1 STELLA_ORIGIN_FAST=1 STELLA_PRODUCER_LONG=1
export STELLA_DIAGNOSTIC_DAYS=100 STELLA_FORMS_SINGLE=1
export QA_SCREENSHOT_DIR="$PWD/tmp" MESA_SHADER_CACHE_DIR="$PWD/tmp/mesa"
export QA_INITIAL="$PWD/results/initial100.json"
STELLA_EGL_SAVE_PATH="$PWD/results/on-100-final.json" ./tmp/native/bin/stella-egl >results/on-100.log 2>&1
QA_FILM_OFF=1 STELLA_EGL_SAVE_PATH="$PWD/results/off-100-final.json" ./tmp/native/bin/stella-egl >results/off-100.log 2>&1
python3 web/tests/film-summary.py results -100 >results/summary.json
```

No `STELLA_FORMS_CARE` or irrigation flags. Harness uses actual initial nursery/seed actions (idempotent nursery repeat beforetime starts), existing fullengine scheduler at1440s/tick, no biological injection, no latercare. Process starts one freshworld; QA creditglobals are NOT valid across a rewind/load followed by furthermeasurement. Final save/loadcheck occurs aftermeasurements. Expected shutdown allocatorwarning is separately retained, not a cleanmemory result.

The portable shim differs from actual measured shim only in screenshot outputdirectory; no input/render/biology changes. Fullserialized fixtures remain local; compact summaries carry theirSHA256. Native output is not proof of browser/mobile execution or UI quality.

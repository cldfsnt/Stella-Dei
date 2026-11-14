#!/usr/bin/env bash
# Experimental native fire assay, not a playable feature or Android validation.
set -euo pipefail
cd "$(dirname "$0")/../.."
ROOT=$PWD
unset STELLA_FORMS_CARE STELLA_PRODUCER_IRRIGATE STELLA_MIGRATE_V5 STELLA_PRODUCER_EXPAND QA_REPLAY_SAVE
OUT=${1:?Provide an absolute artifact directory}
[[ "$OUT" = /* ]] || { echo 'Artifact directory must be absolute' >&2; exit 2; }
TOOLS=${STELLA_TOOLCHAINS:-$ROOT/../stella-toolchains}
ZIG=${ZIG:-$TOOLS/zig-linux-x86_64-0.13.0/zig}
mkdir -p "$OUT"
git rev-parse HEAD > "$OUT/source-commit.txt"
git status --porcelain > "$OUT/source-status.txt"
sha256sum src/simulation/microbes.zig src/simulation/planet.zig src/states/play.zig src/experimental/detritus_ignition.zig src/experimental/planet_ignition.zig web/tests/egl-fire-candidate-prepare.py > "$OUT/source-hashes.txt"
python3 web/tests/egl-fire-candidate-prepare.py "$OUT/native-src"
"$ZIG" build --build-file web/tests/egl-propagule-visual-build.zig \
 -Dsource="$OUT/native-src/main.zig" --prefix "$OUT/build" \
 --cache-dir "$OUT/compiler-cache" --global-cache-dir "$TOOLS/zig-cache" > "$OUT/build.log" 2>&1
MESA_SHADER_CACHE_DIR="$OUT/mesa-cache" STELLA_ORIGIN_COUPLED=1 \
 STELLA_ORIGIN_FAST=1 STELLA_PRODUCER_LONG=1 STELLA_DIAGNOSTIC_DAYS=30 \
 STELLA_FORMS_SINGLE=1 STELLA_ORIGIN_WIDTH=390 \
 STELLA_EGL_CAPTURE_PREFIX="$OUT/frame" STELLA_EGL_SAVE_PATH="$OUT/test-save.json" \
 "$OUT/build/bin/stella-egl" > "$OUT/run.log" 2>&1
grep 'FIRE_RESTORE exact_original=true' "$OUT/run.log"
grep 'ORIGIN_SAVE .*exact_restore=true' "$OUT/run.log"
echo 'Experimental fire controls completed. Not wired into the game. Inspect captured PPM frames and run.log. This is not Android/WebGL acceptance; known shutdown allocation warning may remain.'

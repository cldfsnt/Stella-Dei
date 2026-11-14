#!/usr/bin/env bash
# Native fire assay. Optional --player-flow uses shared production action path; never Android validation.
set -euo pipefail
cd "$(dirname "$0")/../.."
ROOT=$PWD
unset STELLA_FORMS_CARE STELLA_PRODUCER_IRRIGATE STELLA_MIGRATE_V5 STELLA_PRODUCER_EXPAND QA_REPLAY_SAVE
OUT=${1:?Provide an absolute artifact directory}
[[ "$OUT" = /* ]] || { echo 'Artifact directory must be absolute' >&2; exit 2; }
TOOLS=${STELLA_TOOLCHAINS:-$ROOT/../stella-toolchains}
ZIG=${ZIG:-$TOOLS/zig-linux-x86_64-0.13.0/zig}
MODE=${2:-research}
[[ "$MODE" = research || "$MODE" = --player-flow ]] || { echo 'Use optional --player-flow or research' >&2; exit 2; }
mkdir -p "$OUT"
printf '%s\n' "$MODE" > "$OUT/assay-mode.txt"
git rev-parse HEAD > "$OUT/source-commit.txt"
git status --porcelain > "$OUT/source-status.txt"
sha256sum src/main.zig src/simulation/microbes.zig src/simulation/planet.zig src/states/play.zig src/experimental/detritus_ignition.zig src/experimental/planet_ignition.zig web/tests/egl-fire-candidate-prepare.py > "$OUT/source-hashes.txt"
if [[ "$MODE" = --player-flow ]]; then
 python3 web/tests/egl-fire-candidate-prepare.py "$OUT/native-src" --player-flow
else
 python3 web/tests/egl-fire-candidate-prepare.py "$OUT/native-src"
fi
"$ZIG" build --build-file web/tests/egl-propagule-visual-build.zig \
 -Dsource="$OUT/native-src/main.zig" --prefix "$OUT/build" \
 --cache-dir "$OUT/compiler-cache" --global-cache-dir "$TOOLS/zig-cache" > "$OUT/build.log" 2>&1
MESA_SHADER_CACHE_DIR="$OUT/mesa-cache" STELLA_ORIGIN_COUPLED=1 \
 STELLA_ORIGIN_FAST=1 STELLA_PRODUCER_LONG=1 STELLA_DIAGNOSTIC_DAYS=30 \
 STELLA_FORMS_SINGLE=1 STELLA_ORIGIN_WIDTH=390 \
 STELLA_EGL_CAPTURE_PREFIX="$OUT/frame" STELLA_EGL_SAVE_PATH="$OUT/test-save.json" \
 "$OUT/build/bin/stella-egl" > "$OUT/run.log" 2>&1
grep -E 'FIRE_RESTORE (player_flow=true )?exact_original=true' "$OUT/run.log"
grep 'ORIGIN_SAVE .*exact_restore=true' "$OUT/run.log"
if [[ "$MODE" = --player-flow ]]; then
 grep 'FIRE_PLAYER_APPLIED shared_export_action=true' "$OUT/run.log"
 grep 'FIRE_PLAYER_REPEAT no_fuel=true' "$OUT/run.log"
fi
echo 'Native fire assay completed; see assay-mode.txt for direct research versus shared production action coverage. Inspect captured PPM frames and run.log. Not Android/WebGL acceptance; known shutdown allocation warning may remain.'

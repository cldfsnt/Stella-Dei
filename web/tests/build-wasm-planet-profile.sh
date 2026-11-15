#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../.."
T=${STELLA_TOOLCHAINS:-../stella-review-tools};T=$(realpath "$T")
O=$(realpath ../site-tmp/wasm-planet-profile)
python3 web/tests/prepare-wasm-planet-profile.py
for M in plain stages; do
 "$T/zig-linux-x86_64-0.13.0/zig" build --build-file web/tests/wasm-planet-build.zig -Dsource="$O/$M/src/qa_wasm_planet.zig" -Dsysroot="$T/emsdk/upstream/emscripten/cache/sysroot" --cache-dir "$O/$M/cache" --prefix "$O/$M/build" > "$O/$M/build.log" 2>&1
 "$T/emsdk/upstream/emscripten/emcc" "$O/$M/build/lib/libstella.a" web/tests/wasm-planet-profile-main.c -O2 -sENVIRONMENT=node -sASSERTIONS=1 -sUSE_OFFSET_CONVERTER=1 -sNODERAWFS=1 -sALLOW_MEMORY_GROWTH=1 -sINITIAL_MEMORY=134217728 -sSTACK_SIZE=8388608 -o "$O/$M/profile.js" > "$O/$M/link.log" 2>&1
 echo BUILD_OK:$M
done

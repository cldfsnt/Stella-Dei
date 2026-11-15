#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../.."
T=${STELLA_TOOLCHAINS:-/workspace/scratch/f67c3ac60ca3/stella-review-tools}
O=${NEAREST_QA_OUT:-/workspace/scratch/f67c3ac60ca3/site-tmp/nearest-target}
mkdir -p "$O"
Z="$T/zig-linux-x86_64-0.13.0/zig"
"$Z" build-obj -O ReleaseSafe --dep zalgebra -Mroot=src/qa_nearest_wasm.zig -O ReleaseSafe -Mzalgebra=deps/web-vendor/zalgebra/src/main.zig -femit-bin="$O/native.o"
"$Z" build-exe "$O/native.o" web/tests/nearest-wasm-main.c -lc -O ReleaseSafe -femit-bin="$O/native"
"$O/native" > "$O/native.log"
"$Z" build-obj -target wasm32-emscripten -O ReleaseSafe -fsingle-threaded -lc -isystem "$T/emsdk/upstream/emscripten/cache/sysroot/include" --dep zalgebra -Mroot=src/qa_nearest_wasm.zig -target wasm32-emscripten -O ReleaseSafe -Mzalgebra=deps/web-vendor/zalgebra/src/main.zig -femit-bin="$O/wasm.o"
"$T/emsdk/upstream/emscripten/emcc" "$O/wasm.o" web/tests/nearest-wasm-main.c -O2 -sENVIRONMENT=node -sASSERTIONS=1 -sALLOW_MEMORY_GROWTH=1 -sUSE_OFFSET_CONVERTER=1 -o "$O/wasm.js"
node "$O/wasm.js" > "$O/wasm.log"
cmp "$O/native.log" "$O/wasm.log"
cat "$O/native.log" "$O/wasm.log"

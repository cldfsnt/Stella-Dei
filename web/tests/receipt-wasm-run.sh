#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../.."
TOOLS=${STELLA_TOOLCHAINS:-../stella-toolchains}
OUT=${RECEIPT_QA_OUT:-../site-tmp/receipt-qa}
"$TOOLS/zig-linux-x86_64-0.13.0/zig" build-obj src/qa_receipt_wasm.zig -target wasm32-emscripten -O ReleaseSafe -fsingle-threaded -lc -isystem "$TOOLS/emsdk/upstream/emscripten/cache/sysroot/include" -femit-bin="$OUT.o" --global-cache-dir "$TOOLS/zig-cache"
"$TOOLS/emsdk/upstream/emscripten/emcc" "$OUT.o" web/tests/receipt-wasm-main.c -O2 -sENVIRONMENT=node -sASSERTIONS=1 -sALLOW_MEMORY_GROWTH=1 -sINITIAL_MEMORY=134217728 -sSTACK_SIZE=8388608 -o "$OUT.js"
node "$OUT.js"

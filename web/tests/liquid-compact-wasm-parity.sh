#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../.."
TOOLS=${STELLA_TOOLCHAINS:-../stella-toolchains}
OUT=${LIQUID_COMPACT_WASM_OUT:-../site-tmp/liquid-compact-wasm-parity}
mkdir -p "$OUT"
"$TOOLS/zig-linux-x86_64-0.13.0/zig" build-exe src/qa_liquid_compact_wasm_parity.zig -O ReleaseSafe -lc -femit-bin="$OUT/native"
"$TOOLS/zig-linux-x86_64-0.13.0/zig" build-obj src/qa_liquid_compact_wasm_parity.zig -target wasm32-emscripten -O ReleaseSafe -fsingle-threaded -lc -isystem "$TOOLS/emsdk/upstream/emscripten/cache/sysroot/include" -femit-bin="$OUT/parity.o" --global-cache-dir "$TOOLS/zig-cache"
"$TOOLS/emsdk/upstream/emscripten/emcc" "$OUT/parity.o" web/tests/liquid-wasm-main.c -O2 -sENVIRONMENT=node -sASSERTIONS=1 -sUSE_OFFSET_CONVERTER=1 -sNODERAWFS=1 -sALLOW_MEMORY_GROWTH=1 -sINITIAL_MEMORY=134217728 -sSTACK_SIZE=8388608 -o "$OUT/parity.js"
for day in 30 60 90; do
 INPUT="../site-tmp/liquid-transport-order/day$day.json"
 "$OUT/native" "$INPUT" "$OUT/native-day$day.bin"
 node "$OUT/parity.js" "$INPUT" "$OUT/wasm-day$day.bin"
 cmp "$OUT/native-day$day.bin" "$OUT/wasm-day$day.bin"
 sha256sum "$OUT/native-day$day.bin" "$OUT/wasm-day$day.bin"
done

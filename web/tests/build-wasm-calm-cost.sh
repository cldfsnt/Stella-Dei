set -e
ROOT=/workspace/scratch/f67c3ac60ca3
cd "$ROOT/stella-independent-review"
for ARM in legacy small; do
 O="$ROOT/site-tmp/wasm-calm-cost/$ARM"
 "$ROOT/stella-review-tools/zig-linux-x86_64-0.13.0/zig" build --build-file web/tests/wasm-planet-build.zig -Dsource="$O/src/qa_wasm_land.zig" -Dsysroot="$ROOT/stella-toolchains/emsdk/upstream/emscripten/cache/sysroot" --prefix "$O/install" --cache-dir "$O/cache" --global-cache-dir "$ROOT/stella-review-tools/zig-cache"
 "$ROOT/stella-toolchains/emsdk/upstream/emscripten/emcc" web/tests/wasm-law3-canonical-main.c "$O/install/lib/libstella.a" -O2 -sALLOW_MEMORY_GROWTH=1 -sSTACK_SIZE=16777216 -sENVIRONMENT=node -sNODERAWFS=1 -sASSERTIONS=1 -sUSE_OFFSET_CONVERTER=1 -sINITIAL_MEMORY=134217728 -o "$O/profile.js"
done

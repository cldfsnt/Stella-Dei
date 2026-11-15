#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../.."
T=$(realpath "${STELLA_TOOLCHAINS:-../stella-review-tools}");O=$(realpath ../site-tmp/wasm-planet-profile)
python3 - <<'PY'
from pathlib import Path
import shutil
r=Path.cwd();o=r.parent/'site-tmp/wasm-planet-profile';shutil.copytree(o/'plain/src',o/'native/src',dirs_exist_ok=True)
p=o/'native/src/loop.zig';p.write_text(p.read_text().replace('const is_web = @import("builtin").target.cpu.arch == .wasm32;','const is_web = true; // QA cooperative browser scheduling, native arithmetic.'))
PY
"$T/zig-linux-x86_64-0.13.0/zig" build --build-file web/tests/native-planet-profile-build.zig -Dsource="$O/native/src/qa_wasm_planet.zig" --cache-dir "$O/native/cache" --prefix "$O/native/build" > "$O/native/build.log" 2>&1
cc web/tests/wasm-planet-profile-main.c web/tests/native-profile-clock.c "$O/native/build/lib/libstella.a" -lm -lquadmath -ldl -lpthread -o "$O/native/profile"
echo NATIVE_BUILD_OK

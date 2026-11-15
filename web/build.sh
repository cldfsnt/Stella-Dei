#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
TOOLS=${STELLA_TOOLCHAINS:-../stella-toolchains}
ZIG=${ZIG:-$TOOLS/zig-linux-x86_64-0.13.0/zig}
EMCC=${EMCC:-$TOOLS/emsdk/upstream/emscripten/emcc}
WEB_GL_DEBUG=${STELLA_WEB_GL_DEBUG:-false}
case "$WEB_GL_DEBUG" in true|false) ;; *) echo 'STELLA_WEB_GL_DEBUG must be true or false' >&2; exit 2 ;; esac
"$ZIG" build --build-file web-build.zig -Dweb-gl-debug="$WEB_GL_DEBUG" --cache-dir "${STELLA_WEB_CACHE:-.zig-cache-web}" --global-cache-dir "$TOOLS/zig-cache"
mkdir -p web/dist
"$EMCC" zig-out/lib/libstella.a deps/miniaudio.c deps/nanovg/src/fontstash.c deps/nanovg/src/stb_image.c \
 -Ideps -Ideps/nanovg/src -DFONS_NO_STDIO -DSTBI_NO_STDIO -O2 \
 -sUSE_GLFW=3 -sMIN_WEBGL_VERSION=2 -sMAX_WEBGL_VERSION=2 -sFULL_ES3=1 \
 -sALLOW_MEMORY_GROWTH=1 -sINITIAL_MEMORY=134217728 -sSTACK_SIZE=8388608 \
 -sEXPORTED_FUNCTIONS=_stella_auto_seed_start,_stella_auto_seed_step,_stella_auto_seed_status,_stella_auto_seed_apply,_stella_auto_seed_cancel,_stella_habitat_prepare,_stella_habitat_execute,_stella_habitat_cancel,_stella_habitat_status,_stella_advance_start,_stella_advance_status,_stella_advance_cancel,_stella_advance_environment,_stella_advance_dismiss,_stella_scene_resolution_get,_stella_scene_resolution_set,_stella_patch_watch_start,_stella_patch_watch_start_checked,_stella_transport_options,_stella_transport_prepare,_stella_transport_execute,_stella_transport_cancel,_stella_transport_status,_stella_transport_inspect,_stella_patch_watch_stop,_stella_patch_watch_snapshot,_main,_malloc,_free,_stella_resize,_stella_zoom,_stella_focus_land,_stella_reset_view,_stella_camera_distance,_stella_target_distance,_stella_life_snapshot,_stella_adjust_water,_stella_set_water_target,_stella_make_pond,_stella_make_nursery,_stella_seed_colony,_stella_seed_targets,_stella_arrival_effects,_stella_world_ecology,_stella_watch_life,_stella_fit_life,_stella_find_life,_stella_find_detritus,_stella_find_feeding,_stella_find_offspring,_stella_set_speed,_stella_speed_snapshot,_stella_performance_enable,_stella_performance_snapshot,_stella_god_action,_stella_god_target,_stella_world_mode,_stella_goal_stage,_stella_selected_point,_stella_selected_water,_stella_selected_vegetation,_stella_selected_elevation,_stella_test_action,_stella_test_pick,_stella_save,_stella_load -lidbfs.js -sEXPORTED_RUNTIME_METHODS=callMain,ccall,FS,IDBFS -sASSERTIONS=1 -sUSE_OFFSET_CONVERTER=1 -sEXIT_RUNTIME=0 --preload-file assets --shell-file web/shell.html -o web/dist/index.html
python3 web/package.py
cp LICENSE web/dist/LICENSE
cp web/gameplay-harness.js web/dist/gameplay-harness.js

cp web/touch-controls.js web/dist/touch-controls.js

cp web/stella-storage.js web/dist/stella-storage.js

cp web/life-trend.js web/dist/life-trend.js

cp web/copy-report.js web/dist/copy-report.js
cp web/renderer-info.js web/dist/renderer-info.js
cp web/gameplay-measure.js web/dist/gameplay-measure.js

cp web/patch-watch.js web/dist/patch-watch.js

cp web/colony-watch-details.js web/dist/colony-watch-details.js
cp web/colony-transport.js web/dist/colony-transport.js
cp web/advance-day.js web/dist/advance-day.js

cp web/habitat-plan.js web/dist/habitat-plan.js

cp web/auto-seed.js web/dist/
cp web/world-ecology.js web/dist/
cp web/offspring-search.js web/dist/offspring-search.js

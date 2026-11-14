# Topology performance experiment, 2026-11-13

No production topology or save-loader change. Existing level-7 saves remain unchanged.
Actual native game code, cooperative single-thread job scheduling, Mesa llvmpipe
software GL, portrait 390x700. One binary selects level with STELLA_BENCH_LEVEL.
Same PRNG seed1337, 5000km radius, fixed-angular green patch, zero initial rabbits.
65 full update/render cycles, first5 excluded; dt1/60 and timeScale60, fixed
physical game time per iteration. glFinish includes software raster completion.
Two independent process runs per level in order7,6,6,7. Offline audio and direct
PlayState are explicit test adaptations. Native timings are **not phone FPS**.

| Measurement | Level7 | Level6 |
|---|---:|---:|
| Cells |163,842|40,962|
| Startup incl renderer/assets/planet |365–393ms|248–257ms|
| Full update median |36.75–37.04ms|9.01–9.23ms|
| Full update p95 |47.06–47.47ms|13.14–15.29ms|
| Render+glFinish median |54.68–54.87ms|24.89–25.48ms|
| Gameplay peak process RSS |205.4–205.6MiB|138.2–138.3MiB|
| JSON save size |34,736,979 bytes|8,621,996 bytes|
| Streamed save write |194–250ms|51–60ms|
| Read/parse |240–407ms|53–69ms|
| Apply parsed state |2.4–4.1ms|0.55–0.59ms|
| Process peak after parse |259.2MiB|158.7–158.9MiB|

JSON loading raised native high-water memory by ~54MiB for level7 versus ~20MiB
for level6. Browser WASM heap growth, MEMFS/IndexedDB copies, JS and GPU memory
are not represented by this native RSS number. Save timing uses native files,
not IndexedDB. Raw structured measurements are in evidence/performance/.

Visual review of both globe screenshots at390x700: both have readable blue
coastlines, tan terrain and a visible green planted patch; differences are
minor at whole-globe scale. Close-up brush/model resolution was not benchmarked.
Level6 has four times fewer faces/cells, so equal adjacency-ring brushes cover
a larger physical area, and existing level7 saves cannot simply load into6.

Recommendation: retain7 and its save compatibility. First target interruptible
simulation phases/chunks and decouple simulation cadence from render frames;
a37ms uninterrupted update alone exceeds a16.7ms frame budget on this native
host. Do not claim a higher browser FPS until actual device measurements exist.
An opt-in lightweight world preset6 could be worthwhile later, with topology-aware
load and consistent physical brush radius; do not silently downgrade existing worlds.
Native shutdown still reports a pre-existing allocator leak.

Reproduce from repo root:
```sh
python3 web/tests/egl-bench-prepare.py
../stella-toolchains/zig-linux-x86_64-0.13.0/zig build \
 --build-file web/tests/egl-bench-build.zig -Dsource=/tmp/stella-egl-bench-src/main.zig \
 --prefix /tmp/stella-egl-bench-out --global-cache-dir ../stella-toolchains/zig-cache \
 --cache-dir /tmp/stella-egl-bench-cache
MESA_SHADER_CACHE_DIR=/tmp/stella-mesa-cache STELLA_BENCH_LEVEL=7 STELLA_BENCH_SAVE=1 \
 /tmp/stella-egl-bench-out/bin/stella-egl
```
Repeat level6. Captures /tmp/stella-bench-LEVEL-NNN.ppm; test-only saves
/tmp/stella-bench-saves/world.json. Production /saves is not touched.

## Brush scale and repeat variance

At radius5000km, average cell area is ~1917km² (level7) versus7670km²
(level6), corresponding to ~44km versus88km linear spacing. A hex-like
three-ring37-cell vegetation brush has equivalent-area radius~150km on7
but~301km on6. Do not keep that unchanged. A one-ring7-cell brush on6 is
~131km equivalent radius (~24%less area than the old37-cell brush); two
rings19cells are~215km. Prefer a shared physical radius~150km and filter
local neighbor candidates by angular/distance threshold, rather than sweeping
all cells on each pointer event. About9–10level6 cells cover the old patch area.

Update medians varied0.8%(level7) and2.4%(level6) across repeats; render medians
varied<0.4% and2.4%. Tail outliers were large (maximum full updates up to186ms,
render195ms), so these host measurements are not guaranteed frame budgets.
Save/parse timings varied more, especially level7 parse240–407ms. Use repeat
ranges and high-water memory instead of claiming a single deterministic cost.

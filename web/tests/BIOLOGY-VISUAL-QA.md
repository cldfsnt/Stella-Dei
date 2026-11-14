# Biology visual QA (v10 candidate)

Rendering only: `biology_visuals.zig` changes the existing Y-up rabbit model's
basis/foot offset. It never changes lifeform state/count. Close-view sprout
symbols use actual vegetation density at actual mesh cells; these are biomass
indicators, **not individual plant counts or new species**. Hidden in globe view
and climate overlays; max 512 candidates and 64 symbols, 20px spacing.

## Evidence

- `zig test src/biology_visuals.zig`: 2/2 pass. Foot-plane position/radial basis
  checked at six axis/oblique points. Biomass size and zoom/overlay gates checked.
- Actual engine/EGL static fixture: four locations (X+, Y+, near-pole,
  oblique south), topology 6, identical seed 20261113. Before uses original
  unrotated model and no sprouts; after uses production rendering. One real
  rabbit and fixed 0.7 vegetation in a small patch, paused. This is visual
  regression evidence, not growth/breeding evidence.
- `evidence/biology/{before,after}-{025,050,075,100}.png`: after captures show
  radial upright models and sparse sprouts on the actual occupied patch.
  Logs show one rabbit throughout and 2, 1, 4, 4 visible symbols, max512
  candidates. Rabbit grounding helper is topology-independent; this fixture
  does not independently prove topology7 rendering.
- Actual non-fixture ecology/intervention evidence lives separately in
  `evidence/intervention`: grown habitat, flooded habitat, recovered habitat.
  The gameplay worker observed sprouts disappearing on flood and returning
  after real growth, alongside actual rabbits/counters.
- Instrumented isolated `renderSprouts` CPU timing: 105 calls,
  median282µs, p95401µs, maximum694µs. Includes local BFS/projection/NanoVG
  command creation, **not GPU completion or whole-frame timing**. This is
  container-native EGL, not an Android performance guarantee.

## Reproduce

From repo root, prepare (never edits production):

```
python web/tests/egl-bio-visual-prepare.py /tmp/stella-bio-visual-src
../stella-toolchains/zig-linux-x86_64-0.13.0/zig build --build-file web/tests/egl-bio-visual-build.zig -Dsource=/tmp/stella-bio-visual-src/main.zig --cache-dir /tmp/stella-bio-visual-cache --global-cache-dir ../stella-toolchains/zig-cache --prefix /tmp/stella-bio-visual-out
STELLA_VISUAL_BASELINE=1 /tmp/stella-bio-visual-out/bin/stella-egl
/tmp/stella-bio-visual-out/bin/stella-egl
```

Captured PPMs: `/tmp/stella-bio-{before,after}-NNN.ppm`.
Latest UI source adds actual `Lost` count and Inspect water depth, so fixture
screenshots taken earlier in the build show the previous footer wording.
No claim of physical-device touch/WebGL verification is made by these tests.

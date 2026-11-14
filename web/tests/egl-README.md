# Actual-engine offscreen graphics/input harness

This is a QA harness, not a replacement game or browser deployment. It compiles
Stella Dei's real engine, simulation, shaders, NanoVG UI and models, replacing
only GLFW window creation with a socket-free EGL surfaceless pbuffer.

Requirements: Zig 0.13, Mesa libEGL.so.1 with surfaceless OpenGL, vendored deps.
From the repository directory:

```sh
python3 web/tests/egl-prepare.py --mobile --paused
../stella-toolchains/zig-linux-x86_64-0.13.0/zig build \
  --build-file web/tests/egl-build.zig \
  -Dsource=/tmp/stella-egl-src/main.zig \
  --global-cache-dir ../stella-toolchains/zig-cache \
  --cache-dir /tmp/stella-egl-cache
MESA_SHADER_CACHE_DIR=/tmp/stella-mesa-cache STELLA_EGL_INTERACT=1 \
  web/tests/zig-out/bin/stella-egl > /tmp/stella-egl-actions.log 2>&1
```

`egl-prepare.py` makes an isolated source copy in `/tmp`. Explicit test adaptations:
- Skip intro/menu and start the real PlayState directly.
- Use miniaudio's offline/noDevice configuration (no audio device required).
- `--mobile`: select the real mobile UI/camera/input branches on native.
- `--paused`: begin paused to isolate graphics and tools; input script presses Play later.
- Add a trace export reporting actual selected-point values and rabbit count.

No assets are copied. Run from the repo so original assets load normally.
The original renderer is native desktop GL, not WebGL; these checks do not
validate Android browser lifecycle, touch/pointer JS plumbing, mobile GPU
capabilities or WebGL API restrictions. Separate shader/WebGL tests are needed.

The shim supplies real GLFW cursor/button/scroll callbacks and queried button
states. With STELLA_EGL_INTERACT it zooms in, selects Plants, paints the planet,
selects Rabbits and adds a pair, raises land, presses Play, and zooms out.
Frames 1/25/55/75/105/150 are captured as `/tmp/stella-egl-NNN.ppm` and actual
CPU state is printed alongside. It closes after 160 frames.

A leaked allocation was reported by the original native allocator on shutdown;
this harness does not claim a memory-clean run or audio playback verification.

## Verified run (2026-11-13)

With the current cartographic browser branch, final scripted execution rendered
land/oceans and actual mobile toolbar, painted visible green vegetation, added
exactly two original rabbit entities (models + map markers), resumed simulation,
and zoomed out. CPU trace showed:

- Frame 1: 0 rabbits, paused, game time 0, selected vegetation 0.
- Frame 55: selected point 16866, vegetation 1, 0 rabbits, paused.
- Frame 75: same selected point 16866, vegetation 1, 2 rabbits, paused.
- Frame 150: 2 rabbits retained, game time 7072.7976 seconds, running.

Screenshots were inspected at globe and close-up scale. Selection changed after
camera movement, so later per-point vegetation/elevation values must not be
compared as if they described the same vertex. This run does not prove breeding,
long-term ecosystem stability, mobile GPU compatibility, or memory-clean exit.

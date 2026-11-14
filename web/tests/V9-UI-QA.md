# v9 mobile guidance checks (2026-11-13)

Passed pure `zig test src/mobile_guidance.zig` (2 cases) and Node gesture,
storage and production-shell DOM-handler tests. The shell DOM test uses a VM
DOM stub: it verifies wiring/state transitions, not browser layout.

Actual-engine EGL portrait test, 390×700, production mobile UI/input branches:
- Genuine button callbacks cycle 3600→21600→86400→3600 seconds/second.
- Rabbit tool selected through toolbar.
- Fixture changes selected habitat water to 0.0021km, then actual cursor/button
  callback attempts placement. Population stays zero; warning is rendered.
- Fixture drains same clicked point and seeds food; callback adds two rabbits,
  with rendered acknowledgement and markers. No substitution simulation.
- Screenshots at frame55/70 inspected: speed control and footer text fit.

Reproduce from repo:
```
python3 web/tests/egl-v9-ui-prepare.py
../stella-toolchains/zig-linux-x86_64-0.13.0/zig build --build-file web/tests/egl-v9-ui-build.zig -Dsource=/tmp/stella-v9-ui-src/main.zig --cache-dir /tmp/stella-v9-ui-cache --global-cache-dir ../stella-toolchains/zig-cache --prefix /tmp/stella-v9-ui-out
MESA_SHADER_CACHE_DIR=/tmp/stella-mesa-cache /tmp/stella-v9-ui-out/bin/stella-egl
```

Native EGL proof does not verify physical Android gestures or WebGL. New More
sheet browser visual verification is separate from these native screenshots.

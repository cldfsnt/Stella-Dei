# Local WebGL startup diagnosis (pending browser execution)

Production and runtime are unchanged. `web/tests/webgl-startup-diagnostic.html` is copied only to the existing ignored `web/dist` directory for the coordinator's local server. It is not included by `web/build.sh` and must not be packaged/deployed as part of a release.

## Source findings

- `src/main.zig:main_web` returns `WindowCreationFailed` from `glfw.Window.create`, before `gl.load`, `Renderer.init`, loop and `Game.init`. This error does not establish shader, ecology, or hardware failure.
- `web/build.sh` pins MIN/MAX_WEBGL_VERSION=2 and FULL_ES3. Built `web/dist/index.js` calls `canvas.getContext("webgl2", attributes)`.
- `deps/web-vendor/mach-glfw/src/Window.zig` defaults alpha/depth/stencil bits to 8/24/8 and samples to 0. Main overrides only OpenGL profile/version. Generated GLFW translates these to alpha:true, depth:true, stencil:true, antialias:false. Browser.createContext adds majorVersion:2.
- The diagnostic's first case reproduces these context-creation attributes at 1280×720. Additional fresh-canvas default WebGL2, default WebGL1 and minimum-buffer WebGL2 cases separate API availability from buffer-option failure. WebGL1 is diagnostic only, not a supported engine fallback.

## Safety and interpretation

Click-driven, at most four contexts per page load; no game startup, save access, flags, permissions, external dependencies or network requests. CSP explicitly denies connections. No unmasked renderer/fingerprint query. Results show creation status, actual context attributes, exceptions and browser creation-error text. No upload occurs.

If all WebGL2 cases fail, that establishes creation failure in this browser/page, not its hardware cause. If the matching case succeeds, compare the real engine canvas/runtime path next; that alone does not prove game initialization. Context creation can depend on browser resource pressure, so run matching first and preserve test order.

Node syntax check passed; source and local dist copies match byte-for-byte. Actual browser results are pending the coordinator's supported CUA execution. Provenance hashes identify the source and built JS inspected.

## Subsequent executed result

Coordinator executed all four tests once through cloud Chromium CUA. All failed independently with disabled renderer/context creation errors. See ../v59-local-browser-startup/observed-context-results.json and its README for exact observations and limits. This supersedes the preparation-time pending status above, not the game's live deployment.

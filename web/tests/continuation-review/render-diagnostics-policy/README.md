# Web per-draw diagnostics: explicit build opt-in

Production candidate, not a measured laptop-speed claim. Default web builds no longer ask NanoVG to query the GL error flag after each draw/uniform setup. Native builds preserve the historical debug=true behavior. Diagnostic web builds can explicitly opt in with:

```
STELLA_WEB_GL_DEBUG=true bash web/build.sh
```

Direct Zig web builds use `-Dweb-gl-debug=true`. Default false; shell accepts only true/false. No runtime setting, telemetry, save field or persistent state is added.

## Rationale and scope

Emscripten's primary [WebGL optimization guidance](https://emscripten.org/docs/optimizing/Optimizing-WebGL.html#avoid-gpu-cpu-sync-points), checked2026-11-15, warns that render-time GL error queries may create GPU/CPU synchronization points and recommends keeping such checks out of rendering. This supports conservative web production hygiene even though our native llvmpipe timing showed no consistent improvement.

Audit found `options.debug` is read only by NanoVG checkError, which polls glGetError and prints diagnostics. No physics, assets, transparency, drawing order, blend calls or quality setting changes. Shader compile/link status checks remain unconditional; Emscripten assertions, ReleaseSafe, and setup validation are untouched. This does not suppress browser context-loss handling or make recovery safe after GL context loss.

## Verification

- Pure policy test covers native false/true opt-in (both keep checks) and web false/true (only explicit true enables).
- Aggregate JS suite:56checks pass; focused build/source policy tests pass.
- Shell syntax passes; invalid option exits2 before compilation.
- `../nvg-attribution/` contains current-source actual native backend debug-on/off proof:16 exact complete saved-state endpoints and16 exact final pixel comparisons on early/day60, paused/coupled real worlds. The boolean toggled there is precisely the option now selected by this policy. Actual living screenshot inspected. That gate predates the small selection wrapper; it is not a new whole-application run of the final build-option integration.
- Final integrated WASM build and publication remain coordinator gates, not claimed completed by this checkpoint.

No measured laptop, Android, browser-rAF or consistent native speedup claimed. Prior mixed results remain immutable. Diagnostic query counts (about78early/512established per frame in that fixture) demonstrate eliminated calls, not saved milliseconds on the user's device.

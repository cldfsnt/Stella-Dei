# Gameplay regression harness

## Real production-core tests (no graphics needed)

From repository root:

```
../stella-toolchains/zig-linux-x86_64-0.13.0/zig test src/camera_math.zig --global-cache-dir ../stella-toolchains/zig-cache --cache-dir /tmp/stella-camera-test
```

This tests the camera/picking functions imported by the real game, not a reimplementation. Five tests cover meaningful zoom, saturation, fractional wheel steps, portrait globe framing, near/oblique sphere intersections and sky rejection.

## Actual WASM game

Open the deployed game with `?harness=1`, press Play and create a disposable planet. Click **Run gameplay tests**. It changes that planet's vegetation and elevation; no saves are uploaded. **Download test report** exports JSON containing exact state transitions, assertions and PNG captures. It works with the actual game exports, shared input ray picking, and shared held-pointer tool handler.

Run at portrait and landscape dimensions. Tests cover live WebGL surface, dry land focus, center-screen land picking, meaningful in/out zoom, planting, raising, whole-globe reset and sky input rejection. The harness does not claim rendered quality from a non-null context or snapshot alone. Images require visual review; browser drawing-buffer clearing may yield blank captures. Physical touchscreen translation is still a separate device test.

A page without a running planet returns `blocked`, not success. This implementation's cloud browser has failed WebGL2 creation; therefore rendered gameplay tests have not been claimed as passed there. The native production-core tests are executable independently.

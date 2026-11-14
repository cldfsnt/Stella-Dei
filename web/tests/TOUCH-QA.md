# Touch-input verification (2026-11-13)

`node web/tests/touch-controls.test.cjs` passes:
- pinch spread and inward zoom with continuous fractional steps
- no mouse/tool action from pinch, including Paint mode
- remaining-finger drag after pinch cannot paint/click
- navigation uses right-drag, painting uses left-drag
- tap holds across at least two rendered frames and 120 ms (500 ms safety cap)
- cancelled/lost/blurred gestures release all input
- repeated taps, third finger, mouse pass-through
- frame-scheduler cancellation cleans all timers and animation-frame callbacks

The production shell uses this exact controller; no mocked replacement simulation.
`StellaHarness.run()` now includes `touch-pinch-camera-and-input-isolation`, which
runs production gesture logic against the live WASM camera and records distances.
This is a live integration test when run in a WebGL2-capable browser, not a claim
that an Android device has passed. Keep failed/unrun cases explicit.

Manual mobile acceptance:
1. Start a planet and use Land. Pinch smoothly inward/outward, avoiding sudden jumps.
2. Drag with Navigate. Select Plants, tap land; switch Paint and drag a green patch.
3. Pinch in Paint. No unintended patch or rabbits should appear from finger lift.
4. Open/close Climate/Menu, pause/resume, rotate screen, background/foreground.
5. Repeat gestures near toolbar/edge. Confirm button labels and habitat remain visible.
6. Check day, rabbit births, grazing meals and plant generation against engine state.

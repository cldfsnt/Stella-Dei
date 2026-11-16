# Pending real graphics-capable device gate

Status2026-11-16: NOT RUN. Environment inventory shows only cloud connected; PowerPC desktop offline. Latest single-dock build-info separately reports cloud WebGL2 unavailable and mocked-native browser DOM checks. Those checks, native/EGL pointer/render tests and screenshots do not satisfy this gate.

Before testing, record exact deployed build/source and device/browser/viewport. Preserve a verified duplicate/export of the player's current save through supported existing save/recovery tools; never clear site data or replace an unsaved player world without authorization. Prefer an isolated test world/save copy. Keep canonical and legacy import/recovery safeguards intact.

## Gestures and panels
- Actual two-finger pinch in/out and one-finger pan with dock visible, portrait and landscape, near dock edges. Verify no unintended Seed/God action, stuck gesture, pointer capture or scroll; release returns to normal control.
- Start gesture on canvas, move toward/over dock; start on dock and move toward canvas; interrupt with panel opening/closing, second finger, pointer cancellation, background/foreground and orientation change.
- For Seed, God, Stats and World panels, plus Speed and native secondary dialogs: verify intended modal blocking. Pinching/dragging within a panel must scroll/operate panel only, never pan/paint behind it. After dismissal canvas control resumes immediately without stale touches or accidental taps.
- Verify selected tool highlighting, readable target feedback and accurate hit location after zoom/pan, at all explicit3Dresolution choices. Keep touch hit testing full canvas resolution.

## Saved-world interaction
- Load a supported existing save copy, including legacy save when available. Verify time, pause, requested speed, selected world mode, actual existing colonies/resources and camera/selection preservation per documented save contract.
- Repeat gesture/panel tests after load and after a save/reload round trip. Verify no duplicate planting, model conversion or misplaced pointer action, and that relevant stale selection/receipts are rejected rather than targeting a different world/organism.
- Check failure/cancel/repeated-load paths and recovery availability without deleting the player's canonical save. Record exact actions and screenshots/video plus observed issues.

Report separately: actual device pass/fail, native harness pass/fail, DOM mock pass/fail, and unsearched/unrun cases. No real-device claim or complete-game claim until the relevant observations exist. If actual multitouch cannot be generated through the available supported controls, mark it unverified and request a bounded device-side test rather than simulate mouse input as proof.

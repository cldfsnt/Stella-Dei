# Sandbox guidance / inspection UI QA

## Implemented
- Optional first-run hint; dismissal stored locally with safe blocked-storage fallback.
- More → Sandbox guide: truthful on-demand habitat stage, Check habitat, First steps,
  Find land, and collapsed field manual. No full-world scan on animation frames.
- Explicit sandbox label: current vegetation/rabbits are not a simple-life-to-animal
  evolutionary progression. Stage5 is not a resilience or completion badge.
- Surface / Rabbit tabs in existing280px Inspect panel. Recomputed nearest current
  rabbit, no persisted array index; age, fullness (not health), breeding rest or
  gestation minimum, with food/space caveat.
- Leave planet requires a separate second click after unsaved-progress warning.
  Closing cancels it. Long footer hints and Inspect labels fit real font bounds.

## Executed tests
- Production inline shell VM test passes: repeated More/Guide open/close, Check,
  First steps, missing export/not started, changed goal after new world, persisted
  dismiss, blocked localStorage, absent/present dry land, Save/Load confirmation.
  This is DOM/control logic evidence, not a visual browser screenshot.
- `habitat_feedback.zig`: 2/2 tests pass (real-state stage regression, animal facts).
- Actual native game + EGL callbacks at320x640,390x700,800x360. Surface opens,
  Rabbit tab opens with no nearby animal, actual fixture rabbit appears, Leave
  arms warning but keeps planet alive, Close cancels. Trace at85 menu=true,
  armed=true;95 menu=false, armed=false at all three resolutions.
- Visually inspected320 rabbit detail,390 surface detail and short-landscape
  Leave warning. Tabs44px high, labels contained, dialog contained. Evidence:
  `evidence/v11-ui/stella-v11-WIDTHxHEIGHT-NNN.png`.
- The static UI fixture inserts one actual rabbit at frame45 to exercise status
  presentation, not to prove reproduction. Actual biological regression is a
  separate gameplay-worker test. Native EGL does not verify Android WebGL.
- Camera modal-guard regression is a separate web_gl worker patch/test.

## Reproduce native UI
```
python web/tests/egl-v11-ui-prepare.py /tmp/stella-v11-ui-src
../stella-toolchains/zig-linux-x86_64-0.13.0/zig build --build-file web/tests/egl-v11-ui-build.zig -Dsource=/tmp/stella-v11-ui-src/main.zig --prefix /tmp/stella-v11-ui-out --cache-dir /tmp/stella-v11-ui-cache --global-cache-dir ../stella-toolchains/zig-cache
QA_WIDTH=320 QA_HEIGHT=640 /tmp/stella-v11-ui-out/bin/stella-egl
```
Change width/height to390/700 or800/360. PPMs saved to `/tmp/stella-v11-*`.
Actual HTML Guide visual review is assigned to integration worker's preview.

Integrator actual CUA Chrome preview: More → Sandbox guide opened; pre-Play correctly said Start or load a planet. Check, First steps, Close and reopen passed. Screenshot reviewed readable guide and manual layout. Live game-state changes are covered by the native engine test, not this GPU-unavailable browser.

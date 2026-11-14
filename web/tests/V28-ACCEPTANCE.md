# v28 render targets and mobile controls

Bounded checkpoint: remove unused depth attachments from bloom/blur targets while preserving full-resolution HDR color, real scene depth and all effects; keep the Speed dialog Close control reachable during long diagnostic scrolling.

Release gates: actual framebuffer attachment/cleanup/resize and error-path checks, exact paired pixels across maps and HDR/animal scenes, save/clock invariance, repeated dialog lifecycle tests, final current-tree build. Native software GL and structural shell tests do not substitute for Android visual/performance acceptance. No physical-VRAM or universal phone-speed claims. Biology changes remain isolated until independently verified.

## Mobile Speed sheet
Speed now uses the same opaque sticky-heading pattern as Life/God, with a nonshrinking Close target of at least64×44 CSS pixels. Reopening resets scroll and stops/collapses stale diagnostics. Copy is shorter but measurement/stage/context formatters are unchanged. Production shell tests cover repeated open, Close, close-event handling and hidden-page reset; CSS structure preserves bounded responsive scrolling. Actual browser layout/hit-test verification was blocked by the environment's socket restriction before page load, including one reviewed retry; no actual Android sticky-position screenshot or native Escape event is claimed. The existing user screenshots motivated this narrow fix, not a claim that visual acceptance passed.

## Executed framebuffer evidence
Native and browser-format desktop GL checks pass all eight attachment/resize/liveness/error-unwind cases at four sizes. Real scene depth remains attached. Paired pixels remain exact across ten map/atmosphere combinations, a visibly rendered rabbit, HDR sun and lighting transitions at390×700 and920×700; world and clock/save invariants hold. Error-path tests inject incompleteness, not actual GPU out-of-memory. Two unused texture objects are removed. Logical WebGL DEPTH_COMPONENT32F storage avoided is2×4×width×height bytes (2,184,000 at390×700), not measured physical VRAM. Native timing gains were inconsistent; no phone-speed promise.

## Final integrated gate
Actual current-tree native browser-format390 test passes all attachment/error cleanup and exact image/model cases. Clock/pause/rate/background/menu/load and8,734,640-byte exact save restore pass; full physical hash remains d523353839672a4 at all three targets. Final full WASM packaging and root JavaScript suites pass. Actual Android visual/performance verification remains outside this environment.

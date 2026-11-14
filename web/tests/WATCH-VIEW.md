# Compact Watch view QA

Explicit Watch life enters Inspect and clears stale placement targets/modal panels.
It does not change camera, pause, simulation pace, or ecology. Watch header is
56 logical pixels high, with three 44-pixel buttons: Pause/Play, Tools, current
pace. Tools returns the existing full toolbar (166px portrait /112px wide).
The same height helper is used for rendering, marker clipping and pointer UI
exclusion. Native Seed tapping does not enter Watch. Save/load clears the
transient flag; no schema change or persisted gameplay change.

390x400 test: actual EGL game render with phone UI paths and actual pointer
callbacks. It seeds through the real action, enters Watch, asserts camera/pause/
pace preservation; then clicks Pause, Pause, Pace, Tools, asserting no unintended
Inspect popup, no selected-patch drift from UI pointer motion, and expected state. Captures show compact and full view. These
native rendered/callback checks are not Android browser conformance claims.

Integrated into production v20 source. Native captures are not browser screenshots.

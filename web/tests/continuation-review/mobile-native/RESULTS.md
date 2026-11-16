# Mobile native bridge acceptance

Frozen implementation: e8b4793 (preceded by 6d743de and Peek framing correction c203e63). Isolated `site-tmp/mobile-ux/src`; all 273 Zig hashes checked. Only main.zig, states/play.zig, life_camera.zig and new web_shell.zig differ from unified-game. No simulation, save schema, generation law, coefficient, persistent field or ecology horizon changed.

## Actual native result

Final ReleaseSafe EGL software-rendered native adapter passed (session 60121, EXIT0). It runs browser Play presentation branches with the existing cooperative task pump and scratch-only save namespace. This is a native interaction proxy, not browser/device performance evidence.

- Actual ready menu click creates the existing integrated15 world; busy refusal remains intact.
- Shell ownership/snapshot and refused operations preserve complete serialized state and RNG. Ownership is a module-session flag, not a save field; old13 load preserves it and resets selection to None as before.
- Native mobile top/footer controls are suppressed independently of living glyphs, seed/effect overlays and Peek. Fresh ordinary selection becomes None. Repeated enabled/inset updates preserve the explicitly selected brush and target cache.
- Stale/invalid/modal tool and pause requests refuse; enabling ownership does not close an implicit-pause menu or resume it. Existing speed action has the same shell-only modal/busy guard.
- Shell Escape never opens the legacy menu; explicit Advanced settings opens that existing menu, clears its discard arm, preserves pause, and refuses stale/repeated modal requests. Standalone/mobile fallback Escape behavior remains unchanged.
- Pointer hit bounds change consistently: at390x700, old166px top+84px bottom becomes28px top+0px bottom with no Peek (222px more usable height). A real visible Peek retains84px bottom exclusion. Cluster framing anticipates this actual panel rather than reserving invisible old chrome.
- Actual default tap selects a patch/Peek without changing biology/RNG. Same actual raycast target yields byte-identical complete saves for Water+ via the existing explicit tool method versus pointer tap.
- Actual Sandbox tool3 plants cover and tool4 creates the existing rabbit pair; cancel selects None. Origin Seed/Nutrients retain their original mode-specific methods; this bridge changes only selection access, not those methods.
- Final populated-world image visibly retains the real living mat glyph, Peek composition bar, Details and Dismiss. Paired fallback/shell frames use the same390x700 viewport and world. No performance/FPS claim.

## Retained failures and corrections

The first expanded brush comparison incorrectly forced cell334 for the helper but moved the real cursor before pointer activation, which legitimately raycast cell29254. Exact JSON difference was only the corresponding one-metre water addition at those two cells. Corrected QA uses the same actual raycast target for both routes; no engine fix or resource tolerance was introduced. Original failing logs retained. A later QA-only import typo (gameplay_guidance instead of mobile_guidance) was corrected and its compiler failure retained.

A genuine integration review fixed repeated shell-set calls cancelling brushes: only the false-to-true ownership transition clears tools. Another review reserved the retained84px Peek during explicit life framing. Final acceptance includes both corrections.

## Reproduction and remaining boundary

`python web/tests/prepare-mobile-native.py NEW_SOURCE_DIR` copies frozen unified-game and applies the narrow patch. `prepare-mobile-bridge-native.py` creates the separate host QA tree (choose a new output path if already present); build using `web/tests/egl-propagule-visual-build.zig` with Zig0.13 ReleaseSafe, then run `EGL_PLATFORM=surfaceless LIBGL_ALWAYS_SOFTWARE=1 .../bin/stella-egl` from repository root. The script records the scratch path/platform/pump adapters; final QA hashes are retained separately from owner hashes.

Browser gesture classification remains the existing touch-controls.js: an initial tap waits until release, pinch starts no new brush, remaining finger stays inert, and cancellation releases held input. A brush stroke already performed before a second finger arrives is not rolled back. Actual JS gesture/DOM and linked-WASM checks belong to the frontend gates; this report does not replace them. Desktop native rendering was not re-baselined visually; its ownership flag defaults false and legacy render branches/model source are unchanged.

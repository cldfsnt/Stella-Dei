# Isolated toughness silhouette prototype, not shipped

Actual existing native Sandbox `renderSprouts` route, 390×700, frozen warm day14 world with 82 rabbits. No simulation ticks. All patch traits were prescribed uniformly as 0, .25 or .5 for visual QA; these are not naturally evolved plants or a test of defense fitness. The copied renderer contains the only visual change. Production renderer, biology and save schema remain untouched.

Comparison PNG columns: original d0, prescribed d.25, prescribed d.5. Close view uses terrain altitude +200; globe uses radius×2. Same camera and unchanged optimum colors. The positive trait changes paired leaf contours, illustrating handling resistance rather than literal thorns, poison or botanical species. Zero delegates the exact original branching glyph.

## Gates and actual review
- Actual zero-trait candidate versus original path pixels byte-identical in both views.
- Same visible glyph count across all four cases: 3 close, 10 globe; existing ≤64 cap and culling/declutter unchanged.
- Complete serialized state/RNG unchanged by each render except the four existing camera fields explicitly normalized: camera, camera_target, camera_distance, target_distance. Trait fields are included. Original complete input restored exactly.
- Same per-glyph submission budget: five beginPath, four fill, four stroke; paired-leaf loop still four Bezier calls per tier, no extra particles, rings, animation, texture or global scan. Different contours may tessellate differently; no runtime/performance equivalence claim.
- Actual PNGs inspected. Close-view .25 and .5 silhouettes are visibly narrower versus broader angular leaves. At globe distance the distinction is subtle and many plants are occluded by real rabbit markers. **This does not establish reliable distant trait identification.** No change to rabbit rendering was attempted.
- First invocation omitted inherited STELLA_ORIGIN_COUPLED entry flag and never reached this test. Its diagnostic is retained separately, not counted as acceptance. Correct invocation passes TOUGH_VISUAL_PASS and exits0.

## Reproduce
`python3 web/tests/egl-toughness-visual-prepare.py <absolute output>/src`

Build using `web/tests/egl-propagule-visual-build.zig`, Zig0.13 ReleaseSafe, absolute cache/prefix, `-Dsource=<output>/src/main.zig`. Run from repository root with `STELLA_ORIGIN_COUPLED=1 STELLA_ORIGIN_FAST=1 QA_PULSE_SAVE=<absolute site-tmp/foraging-production/warm-actual-end.json>`. The existing EGL shim defaults to390×700. Raw pixels and binary remain in `site-tmp/toughness-visual`; hashes are in results.json. PNGs are pixel-preserving conversions/compositions of actual captures, not generated illustrations. No WebGL/mobile-device performance or rendering claim.

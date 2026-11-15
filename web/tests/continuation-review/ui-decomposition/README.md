# v44 UI draw-submission decomposition (research)

Status: isolated harness compiled; measurements pending coordinated clean window.

Source: v44 `5f52002`. Native EGL llvmpipe, browser-policy UI/loop, corrected browser-only atmosphere-upload policy, no production changes. This is NOT browser, Android or hardware-laptop performance. The actual old natural-30-day QA save is loaded into current source, not regenerated; provenance explicitly accepts only source hashes reviewed as label-only Play and parity-tested sparse traversal Planet. Other engine changes fail preparation.

Plan: early and cached30d, 40,962 cells, 1366×768, identical fresh restore per pace (paused/6/24 target), 12 warmups and 60 measured frames. Actual pre/post cooperative pumps retained. NanoVG cancellation is research-only, after full UI construction: biology, targeting and receipt ingestion are retained, but no UI draw submission occurs. Compare complete saved-world hashes. Do not propose removing controls/glyphs based on this experiment.

UI_PART mappings: 0 seed-zone construction; 1 living sprout/glyph construction; 2 propagule receipt construction; 3 god-effect construction; 4 NanoVG endFrame submission (or cancelFrame in control). These are CPU elapsed calls, not independent GPU measurements; driver waits may shift between calls/finish. Existing scene/post/UI metrics are retained. Full render+finish and whole-frame costs determine whether any isolated cost is material.

## Completed measurements

Three paired ON/OFF runs completed, all 18 complete saved-world hashes match. The default actual UI is ON; OFF builds the same commands and then cancels NanoVG submission. No benchmark code is applied to production.

Median total frame ms, ON → OFF:
- Early paused: 14.827 → 12.321; Grow: 18.297 → 15.289; target24: 26.063 → 22.067.
- Cached30d paused: 16.878 → 12.957; Grow: 19.932 → 16.083; target24: 28.965 → 23.625.

Cached30d render+finish median: 16.730 → 12.811ms paused, 17.281 → 13.666ms Grow, 19.073 → 14.388ms target24. Full UI submission is a measurable part of this software renderer's cost, but this is all controls, text, living glyphs and effects together, not the arrival/death cues alone. Those previously showed no consistent major cost in their own paired test.

Living glyph construction itself is about 0.34–0.53ms/frame across these medians. Receipt construction is about 0.001–0.019ms. Seed-zone/god-effect values are effectively zero here because those features are inactive; this does not establish their active cost. NanoVG endFrame call is ~0.47–1.51ms ON, while cancellation is ~0.001–0.003ms. Remaining render differences include downstream software raster work and synchronization; do not add stage values as independent GPU timings.

The ON run has 66–79 early draws/frame and about 177–248 cached30d draws/frame. OFF retains 11 scene/postprocess draws/frame and unchanged terrain uploads (1,474,632 subdata bytes/frame); no NanoVG bufferData submission. Most living-world incremental draw calls therefore originate in the UI/overlay path, not thousands of individually meshed species.

This establishes a research direction, NOT authorization/recommendation to hide the UI or reduce graphics: investigate batching repeated glyph paths, opaque/convex primitives where visually equivalent, and avoid redundant driver state changes while preserving order and hit targets. Any candidate requires screenshot equivalence and separate measured acceptance. Scene/postprocess still costs roughly 12–14ms with UI submission disabled in this proxy, so UI alone is not the whole problem. Existing native GPA teardown leak warning remains.

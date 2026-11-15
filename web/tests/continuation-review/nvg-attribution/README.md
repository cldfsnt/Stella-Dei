# Current-source NanoVG attribution and debug-query gate

Isolated QA only. No production changes. Native EGL software renderer with explicit browser-policy clearSurface/mapContext/bloom/UI and native-only atmosphere-upload disabled.390×700. Not Android/WebGL/hardware laptop evidence.

## Method

Load real40,962-cell early/day60 worlds. Explicitly frame existing life and settle60renders, freeze owned save. Each paused/coupled arm restores independently;12warmup renders,60measured frames. Coupled frames invoke one unchanged1440-second actual Planet tick then real render/finish/swap. This is fixed-work throughput, not browser-rAF achieved pace. Debug order off/on/on/off, two pairs. Counters present in both arms. Only copied NanoVG context options.debug toggled, all original GL draw/uniform/blend/texture calls retained. It only controls checkError glGetError polling/printing. Shader compile/link checks and runtime safety remain unchanged. No transparency reorder, graphics simplification, gameplay/event removal, new cache, or resource adjustment.

16 complete saved-state endpoints and all16 final pixel images match within each corresponding world/pace. Original saves restored. Actual day60 screenshot inspected: distinct living glyphs, amber marks, arrival/loss cues and controls visible. Logs preserve existing allocator teardown diagnostics; no leak claim. Input/source hashes and start times recorded. Other workers' heavy tasks finished before measured execution.

## Counts: actual per measured frame

Early:36 NanoVG calls,66 drawArrays,39 uniform uploads,17 image requests (15 repeat previous image),36 blend calls (35 repeat previous blend),78 error queries with debug on.

Day60 coupled averages:228.93 calls,544.88 drawArrays,265.18 uniform uploads,50.97 image requests (48.97 repeated),228.93 blend calls (227.93 repeated),511.58 error queries. Debug off removes only those queries. Image repetition describes nonzero image requests; it is not a guarantee of safe texture-call suppression in all unrelated state paths. Blend comparisons are exact field comparisons within flush. Counts are read-only; draw calls are not batched.

## Full-frame medians (debug ON → OFF)

- Early paused:7.587→8.493ms; coupled16.791→16.393ms.
- Day60 paused:11.582→11.683ms; coupled20.177→21.080ms.

Variability is substantial. No consistent native benefit; no laptop speed claim. Render+finish and flush call-time logs are retained; flush elapsed is not independent GPU time and must not be added to total rendering. Normal simulation+render, not mere microbenchmarks, is measured. Counters/timers add instrumentation to both arms.

## Decision

HOLD any production performance change on this evidence alone. Hundreds of diagnostic error queries per living frame and redundant per-call blend state are concrete browser API-crossing hypotheses; native driver/llvmpipe results do not demonstrate their browser cost. If pursued, preserve opt-in diagnostic checks and independently validate WebGL semantics and images. Do not disable shader validation or alter ecology. This gate does not establish that event cues are expensive: prior receipt-construction/effects-only results remain small/mixed.

Reproduce with egl-nvg-attribution-prepare.py, egl-nvg-attribution-build.zig (`-Dnvg-source` points to copied qa-nanovg/nanovg.zig), run.py with STELLA_WORKSPACE. Large input saves/PPMs retained locally; hashes and one losslessly converted PNG committed.

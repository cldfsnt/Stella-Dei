# Existing bloom path audit; no redundant optimization

No production edit, new setting or timed run. Current `src/empty_bloom.zig` already skips the bright extraction and four blur passes for browser Origin Normal map, stable radial daylight, orbit camera, zero animals and finite camera radius0..250000. The final shader enableBloom flag suppresses stale glow sampling. Unsupported HDR scenes retain bloom. Prior `web/tests/empty-bloom/REPORT.md` includes exact eligible pixel comparisons and unsupported-scene regression evidence.

The initial suspicion that scene-scale benchmarks used native canSkip(false) was WRONG. Inspection of preserved site-tmp/scene-scale-src/states/play.zig shows canSkip(true,...). The nested preparer chain includes egl-prepare.py replacing the spaced wasm architecture predicate with true. Newer unspaced architecture checks require individual audit, so blanket native/browser equivalence is not claimed.

All18 preserved scene-scale benchmark logs (two viewports ×three scales ×three repeats) contain six actual FRAME_RENDER_CONTEXT rows each: early/cached30d ×pause/Grow/24h-target. All108 rows explicitly report bloom=false, bloom_passes=0. Canvas1366×768 and390×700 include Sharp100%,75%,50%. contexts.json preserves each actual line plus compressed-log hash. Therefore previous scene-resolution benefits did not result from accidentally including five bloom passes, and forcing bloom off in these observed scenes cannot remove additional bloom passes.

No user-facing bloom toggle is justified by this evidence. An active-HDR scene experiment would be a different visual-quality tradeoff, not an optimization of this already-empty default path. All prior timing remains native llvmpipe proxy, not hardware laptop/Android/WebGL performance proof.

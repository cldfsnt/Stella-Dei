# Standalone native / WASM liquid-helper parity: PASS

Existing supported Zig0.13 wasm32-emscripten ReleaseSafe single-threaded object, linked by emcc-O2 using Node24 runtime. Effective production-style vector suggestion/fallback is16 native and4 WASM; usize64 versus32. No full browser rendering, authentication, device timing or FPS test.

All three frozen40,962cell direction-remapped inputs (days30/60/90) pass four fixed dt0/360/1440/15000. Scalar reference versus cached helper forward/reverse match output f32 bits, every per-edge f64 receipt and both ledger values internally. The native executable and actual WASM module export8,520,184bytes perworld; host cmp and SHA256 verify all bytes identical, not merely matching printed summaries.

First standalone link omitted USE_OFFSET_CONVERTER, which the actual project already enables; runtime aborted requesting it. First log preserved. Adding this existing project flag, without solver changes, produced the passing second run. Full command is liquid-wasm-parity.sh; executable/object/WASM/input/exported-data hashes and imported/exported symbols are recorded. Large binary outputs remain workspace research artifacts, not repository payload.

This establishes a practical standalone target parity gate for THESE frozen scalar/cached helpers. It does not assert the old width-dependent SIMD update matches across targets, validate the later compact helper, establish a browser full-scheduler result, or erase the measured native slowdown. No microbenchmark was performed. Future performance work must retain target-specific semantics and separately verify any changed solver.

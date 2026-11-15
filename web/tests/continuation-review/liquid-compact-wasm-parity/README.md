# Compact standalone WASM parity: PASS

The distinct new Zig fixture verifies compact f32-edge/head-cache helper against cached f64-edge reference for all40,962cells, all six widened edge receipts and both ledger fields, at dt0/360/1440/15000 and both source traversal orders. All tests passed native and Node/WASM; each world's8,520,184 serialized reference bytes compare exactly across targets. The output hashes also equal the prior cached-only platform proof.

Native effective SIMD suggestion16/usize64; WASM4/usize32. Helpers under test are scalar routines: this is not equivalence to the legacy width-dependent scatter or a performance test. No actual Planet fixture, rendering, FPS, browser or device claim. The reviewer owns separate actual-coupled-engine tests.

Reproduction: `bash web/tests/liquid-compact-wasm-parity.sh`. Source/import/toolchain/input/binary/output hashes in provenance.json; complete successful log gzipmtime0. No failed run or helper edit.

The reused C IO wrapper's static stdout label still says `scalar_cached_reverse_exact`; this is historical wording, not the executed assertion. The linked `qa_run` is the new fixture `qa_liquid_compact_wasm_parity.zig`, whose code explicitly calls compact.step and compares it to cached.step. Native log correctly names compact/cached/bothorders. No prior cached-only result was substituted for this run.

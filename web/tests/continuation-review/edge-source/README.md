# Centralized production EdgeSource parity

Native ReleaseSafe: 100000 random f64 cases,81 invalid/extreme/signedzero cases and one zero-length case pass exact output-bit equality with the frozen pre-hoist scalar formula. The six existing atmospheric tests also pass (7tests total). Actual wasm32-emscripten ReleaseSafe/singlethreaded, emcc-O2, Node execution passes the same100082 cases with failures0. Not browser/full-world performance.

`src/qa_edge_source.zig` imports the actual staged production helper. `web/tests/edge-source-wasm-run.sh` reproduces the WASM check. The experimental helper was tested before production staging; final logs here are production-helper runs. EdgeSource is rebuilt once per source per atmospheric edge scratch refresh, not retained across ticks. Wind scratch failure computes original wind once; edge scratch failure keeps original fallback API. No allocations/schema changes/approximation. Source validity is checked before pure destination arithmetic; finite value arithmetic order is unchanged.

Whole-engine exact serialized-state and timings belong to prior edge-hoist evidence (a7f8975), whose copied candidate had the same arithmetic inline. Centralized integrated full-game build remains coordinator's release gate. No deployment performed here.

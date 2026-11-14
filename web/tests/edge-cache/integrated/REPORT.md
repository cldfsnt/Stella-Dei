# Integrated directed-edge correctness smoke

PASS: native build and both runs exit 0. Prepared independently from current main using web/tests/edge-cache/qa/prepare-direct.py, with isolated test-only exact edge assertions. No main source edits or deployment.

Tested production Planet SHA256: 8ce15fcb8c2beb62eb38b9d968cf9dd1e6cb872e946d5b00e61aee3d98c0899d, byte-identical to reviewed clean candidate. SOURCE-HASHES.txt records other core files and all still matched after testing. QA-HASHES.txt records the instrumented source. Only tracked main difference observed is expected Planet patch (23 insertions, 3 deletions); untracked other workers' artifacts were not changed.

- Canonical Raise/LowerTerrain plus geometry upload: all outgoing and reverse-gather cached rates exactly equal original calculations after rebuilding each tick.
- Paired 20-tick serialized state hash f72797c449ed2c61, cached versus forced edge allocation failure.
- Poisoned edge cache after load is refreshed.
- Clock targets 3600/21600/86400 yield equal six-tick physical save hash d523353839672a4.
- Actual synthetic pointer pause prevents an extra tick. Exported speed/pause, invalid rate rejection, background gap, menu/load debt reset and render-only clock invariants pass.
- Invalid save rejected without mutation; exact 8,734,640-byte restore passes.

Existing native allocator shutdown warning remains. This is native llvmpipe, not Android/WebGL conformance. Exact-rate assertions add significant CPU work and a concurrent WASM build ran; emitted timings are correctness diagnostics only, not a performance benchmark. Prior isolated repeated timings and candid tail/memory tradeoffs remain the relevant performance evidence.

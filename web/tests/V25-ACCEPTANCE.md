# v25 · Faster atmosphere and frame diagnostics

## Exact per-tick atmospheric edge cache
Each directed edge rate is computed once per tick rather than three times. Wind and geometry are refreshed every tick; original f64 rates and accumulation order remain unchanged. This reduces 18 rate calculations to 6 per cell, not the simulation's O(N) complexity. The six-neighbor lookup is bounded.

Extra transient memory is 1,966,176 bytes at the normal 40,962-cell grid, or 7,864,416 bytes at the higher 163,842-cell grid. Default detail is unchanged. Allocation failure falls back to exact uncached work. The cache is not saved and is freed with the planet. Save schema stays 6.

Paired native 30-day full state hashes match, including changed terrain and wind. Canonical Raise/LowerTerrain plus geometry refresh verifies every outgoing and reverse-gather rate against the original calculation. Poisoned-cache refresh, allocation failure, replacement and teardown pass. An initial dynamic fixture mismatch was traced to unsaved fixture geometry not being reset; both failed and corrected logs are retained, not represented as a production fix.

Two native software-GL timing pairs reduced atmospheric work about 38–42%, with improved median frames. Tail latency improved only in the second pair. No blanket smoothness or Android performance claim is made. Synthetic two-frame pointer tests are not touchscreen/OS latency. Current user-reported phone throughput remains a separate observation.

## Remaining boundaries
No reserve/schema migration, terrestrial evolution completion or fire tools ship in this checkpoint. Actual device behavior still needs local diagnostics. Native runtime's pre-existing allocator shutdown warning remains; tracked cache ownership balances. Root JavaScript suites and WASM build are required after final integration.

## Local frame-tail diagnostics
The optional, local-only performance panel now reports nearest-rank p95 frame interval and a strict >50 ms frame count over the existing blocks of up to 60 frames. Maximum and count remain visible because p95 can miss rare stalls. Bounded 60-double storage; no sampling while disabled and no external telemetry. Closing/hiding resets measurement. This is not touchscreen latency or a GPU timer. Deterministic tests cover empty/partial blocks, ties, reverse order, rare stalls, invalid values and reset; a native actual-world callback test preserves the full 8,867,927-byte save and clock. Its injected timing values test serialization, not performance.

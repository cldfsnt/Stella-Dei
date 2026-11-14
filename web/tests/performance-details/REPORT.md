# Local performance details candidate

Optional collapsible section inside existing Speed panel. Existing target/achieved rates remain above it. New read-only values: actual terrain cell count, observed frame intervals, physics-update duration (per active frame, potentially two ticks), number of physics ticks, and render CPU submission duration including swap call. NOT GPU completion time or Android FPS certification.

No network calls, uploads, device identifiers, persistent records, or growing history. Two bounded aggregates cover the current and latest completed 60-frame block. Before the first block completes, partial observations are shown. Measurement resets when enabled and is disabled/reset on section collapse, dialog close (including Escape), explicit Close, or background visibility change. Closed overhead is a boolean test on the existing physics timing path; no extra render clock reads.

Physics values reuse the existing simulation timer after the bounded tick loop. Measurements never influence step size, rate, update budget, camera, or world fields. CSS explicitly overrides generic diagnostics-details rules, so the collapsed summary remains visible and stays in dialog flow.

## Verification
- ReleaseSafe WASM static library build passed.
- Aggregate pure test passed: disabled no-op, bounded rolling blocks, rejected nonfinite input, reset.
- Production shell suite passed: valid metrics, malformed JSON, unavailable API, negative/nonfinite/impossible values, section/dialog close disable, correct CSS flow.
- Actual generated Origin world native callback run exited 0: full save 8,867,927 bytes identical before enable/read/disable; hash `7bf3835fa4fd5a13`; simulation clock exactly unchanged. Diagnostic durations in this particular invariance fixture were supplied to test aggregate serialization, NOT benchmark results. No biology ticks advanced. Browser availability guard only was adapted for native callbacks. Existing allocator teardown warning remains.
- Current v23 source reviewed hunk by hunk: PlayState differs only after existing physics timing, main only new exports and web render timing. renderer.zig and simulation/planet.zig byte-identical to v23, preserving atlas registration and wind scratch. Fit code untouched. git apply --check passes.

## Integration
Apply performance-details.patch. Includes new src/performance_details.zig and exports in web/build.sh. Full final browser link/deployment belongs to parent. No main files edited by this worker.

Native reproduction: STELLA_SOURCE_ROOT=<candidate> python3 qa/prepare.py /tmp/stella-perf-qa; use web/tests/egl-origin-build.zig with -Dsource=/tmp/stella-perf-qa/main.zig; run QA_PERFORMANCE=1 STELLA_ORIGIN_FAST=1 binary from repo assets cwd. See results/native-callbacks.log.

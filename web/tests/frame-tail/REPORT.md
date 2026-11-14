# Frame-tail diagnostic candidate

Adds two local-only measures to the existing Speed → Performance details: exact nearest-rank p95 frame interval and the count of intervals strictly greater than 50 ms. Keeps average, max, physics update, and **Render call** wording. No input-event timestamp is measured: these numbers are not touch latency. Render call still includes possible driver waits and is not a GPU timer.

## Why both
A single 200 ms stall among 60 frames will appear in maximum and long-interval count, but not p95. Even three such stalls can remain above the p95 rank. The UI explicitly warns about that rather than treating a good p95 as proof of smooth interaction. The completed block remains paired across average/max/p95/count; partial next-block samples never mix into an older completed percentile.

## Cost / lifecycle
Fixed 60 × f64 buffer (480 bytes), no allocation or growing history. One write and comparison per accepted enabled frame. A stack-copy sort of at most 60 numbers runs only on block completion or diagnostic snapshot reads before the first complete block. The existing opt-in gate returns before any new work when disabled. Existing collapse/dialog-close/hidden reset behavior is unchanged. No network, uploads, persistent logs, simulation or camera edits.

## Deterministic checks
Three aggregate tests pass: empty/single/tied/reversed inputs; exact rank 57 of 60; rare 200 ms stalls; strict 50 ms boundary; nonfinite rejection; completed/partial-window consistency; reset/disabled no-op; snapshot purity. Production shell suite passes with output assertions and invalid percentile, fractional/excess long counts, nonfinite/unavailable fields. Render call wording retained.

## Integration
Apply frame-tail.patch (four files only). BASE-SHA256.txt records the base. Main was not edited. Native generated-world enable/read/disable save-invariance test is under qa/prepare.py; results/native-callbacks.log records completion when available. Durations deliberately injected in that invariance test are serialization test data, not device benchmarks.

## Actual-engine invariance result
Native ReleaseSafe build and generated-world callback run both exited 0. Full save before/after enable/read/disable was exactly identical: 8,867,927 bytes, Wyhash `7bf3835fa4fd5a13`; simulation-clock structure also unchanged. The actual callback serialized 60 deliberately injected intervals (59 × 20 ms, one × 200 ms) as average 23 ms, max 200 ms, p95 20 ms, long_frames 1. This confirms percentile/count serialization and state purity, not a hardware performance measurement. Existing unrelated allocator teardown warning remains. Only the native web-availability guard was adapted; callback and metric bodies were the candidate's actual source. All build/temp files were workspace-local; no /tmp consumption.

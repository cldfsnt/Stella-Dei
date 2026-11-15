# Performance investigation after v42

## Scope and limits

Todd reported slow play on both Android and a laptop. Earlier Android screenshots
show 40,962 terrain cells. The laptop grid and renderer are not observed. Never
attribute the report to a large retained save without an actual local sample.
Only the cloud test computer is available. Native EGL/llvmpipe timings are
controlled software-renderer proxies, not measurements of his devices.

## Findings so far (not all shipped)

- The simulator honors a requested 24 hours/sec only when work fits. A physics
  tick is indivisible, followed by rendering. The two-tick/16ms budget is not a
  guarantee of a <=16ms frame; do not fake the achieved clock or drop biology.
- A 163,842-cell retained-grid proxy with only 1–12 cohorts reproduced roughly
  6.2–6.5 simulated hours/sec. Climate/grid work is substantial. This is a
  conditional diagnosis, not evidence that Todd loaded that grid.
- Earned arrival/loss effects are bounded. Corrected browser-policy A/B generated
  twelve natural receipts, about 9–11 visible cue draws/frame. Eighteen paired
  complete-world hashes match. Three timing repeats show no consistent large
  gain from suppressing the effects. Do not remove them or blame Zig on this
  evidence.
- Whole-frame profiling includes deferred jobs. Periodic normal jobs were a
  measurement blind spot, but averaged roughly 0.14ms/frame in the measured
  proxy, not the dominant cost. Early native fixtures included an atmosphere
  mesh upload that actual WASM skips: their render totals are not exact browser
  workload. Corrected runs are distinguished in worker evidence.
- Experiments separately investigate sparse ordered biology traversal, exact
  geometry upload retention and atmospheric geometry computations. All need
  full-state parity, invalidation, memory and timing acceptance before shipping.
  A large edge cache may not justify its memory cost. No simplification or
  reduced scientific precision is authorized by a successful microbenchmark.

## Delivered source checkpoint

Opt-in renderer context was saved to cldfsnt/Stella-Dei master
`dc14da482a1135ef0daa5ffb1c5c40f81e15bd54` (local bdc84c5; exact tree
1fba17567282562596c45f15cdb0a55bbe287489). JS tests: 13 passed. WASM build
passed and unchanged WASM SHA256 is
34e5bfc9ff28948baa0d99668f163160c4d723ebda4d66d76b7b7edfa16fd79a.
This checkpoint alone has not yet been deployed; live host remains v42.

# Actual Node-WASM cutoff workload screen

Fixed protocolfe4c87c, binaries3104edc. Coordinator granted exclusive CPU after other native jobs finished and archives paused. Correctness first, then exactly two bounded processes: seed42ABBA and1337BAAB, one warmA/B each. Every block resets its respective actual day14 endpoint,72wholePlanet scheduler ticks with12warm+60timed. No added repeats, ecology selection, tuning, deployment or schema change. CPU released immediately on completion.

|Fixed measured ms/tick|Legacy.0025|Candidate.001|Median difference|
|---|---|---|---|
|Seed42|26.8927,27.1760|29.0397,30.0104|+9.21%|
|Seed1337|23.6733,23.8194|23.4024,22.7506|−2.82%|

Seed42 is a real cost warning: both candidate samples exceed both legacy samples. Its actual candidate endpoint has545living/344occupied versus427/250 legacy. Seed1337 has194/121 versus158/91, but this small screen shows no slowdown. Do not claim a speedup from that negative percentage or a universal overhead from42. The comparison includes different ecological workloads and environmental trajectories after seven days, not just the CPU cost of changing a literal. Native/browser render and deviceFPS were not measured.

## Correctness

For all four binary/input pairs: zero-step loaded state is typed-exact; fresh-process72+10 equals82 complete save/RNG bytes. Each legacy72 endpoint also equals the prior accepted combined WASM reference binary on the same input. All timed/warm72 endpoints equal their independently captured gate hashes. Source comparison confirms only the cleanup literal differs across model copies; no per-cell tracing or phase instrumentation is active. Full endpoint hashes retained, large duplicate rawstates omitted.

## Memory and lifecycle

Both binaries363,467bytes, identical94,248byteJSglue. Cohort88bytes/cell368bytes;40,962cell array15,074,016bytes, same both. Root amount and owner arrays each1,310,784bytes, unchanged. Actual linear heap capacity128MiB in all retained logs, including harness I/O; this is capacity, not solely live model allocation.

Two modules compiled once per process, eight instances total (zeroA/B,warmA/B,four measured). After each block GC ran and both discarded-instance and memory WeakRefs were cleared. No accumulating128MiB external-memory steps; RSS under1GiB safety bound. Measured post-GC RSS stayed approximately274.14–274.22MiB for42 and281.75MiB for1337. RSS includes Node, both compiled modules and harness, not game-only memory or Android requirements.

All samples, warm/zero blocks, GC timings and memory snapshots are in p42/p1337-results.json and corresponding logs. Timing windows02:04:45.208–02:05:01.559UTC and02:05:01.677–02:05:16.592UTC on2026-11-16. No failure or excluded sample.

## Recommendation

The weak-colony change has a demonstrated gameplay tradeoff and a measurable cost in the larger42world. It is not a free optimization. If chosen for a product law, budget for more active colonies/occupied patches and validate actual target rendering separately; don't conflate this isolated cutoff result with the separately tested thermal candidate. This screen supports a bounded cost assessment, not automatic promotion or a new permanent runtime. The typed cutoffQA identity remains experimental; wire14 stays with the climate owner.

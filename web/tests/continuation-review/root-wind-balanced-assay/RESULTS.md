# Balanced same-module assay: completed once

Accepted execution2026-11-16 01:04:03.961–01:04:46.026UTC. Exclusive CPU/IO released by coordinator. Two fresh Node processes, identical frozen WASM40b6de7bcfefee8f4ca903ea1065fe3468649e677b297521deb651539247d239 and original glue5038c38425dca1e72b28afdcf7b2507cb9ed6c1f6abb2345f7cbbc45e0df049c. No engine change, no stage clocks, no tier flags. One compiled Module and10 fresh instances perprocess: two zero gates, four warm blocks, four measured blocks. All16 warm/measured full endpoint hashes match existing accepted references; all four zero-state/topology gates passed. Each measured block restores original input, never warm endpoint.

## All measured results

| Process/order | Sample | arm | ms/tick |
|---|---|---|---:|
|1 ABBA|1|off|24.622245|
|1 ABBA|2|enabled|24.130632|
|1 ABBA|3|enabled|28.929714|
|1 ABBA|4|off|29.493815|
|2 BAAB|1|enabled|23.187691|
|2 BAAB|2|off|25.937840|
|2 BAAB|3|off|26.178737|
|2 BAAB|4|enabled|25.501184|

Four adjacent enabled/off ratios:0.980033807,0.980873928,0.893971575,0.974118210. Geometric mean0.956527378 (−4.35%). P1 medians off27.058030/enabled26.530173 (−1.95%); P2 off26.058288/enabled24.344438 (−6.58%). Pooled medians off26.058288/enabled24.815908. Both AB and BA order pairs favor enabled in this assay, but P1 later blocks are markedly slower for BOTH arms and P2 first enabled sample is particularly fast. No inference of universal speedup or statistically resolved zero cost.

The previously accepted cold-process screen's+10.25% seed1337 result remains retained. This stronger balanced warmed assay does not reproduce sustained enabled regression in the tested scenario. Differences in compilation/warmup/instance/GC regime prevent rewriting prior evidence or claiming stage attribution proved noise. It is a source-equivalent Node scheduler assay, not browser-rendered gameplay, device responsiveness, or FPS. Enabled/off projected inputs intentionally diverge biologically; exact comparisons are each arm to its own original endpoint.

## Memory/restoration and bounds

Process durations21.482/20.448seconds, below180second bound. Peak sampledRSS392,622,080/374,054,912bytes, below1GiB stop. Post-GC ArrayBuffers exactly510,046bytes at every boundary; all20 discarded instance and memory-buffer WeakRefs cleared. Post-GC RSS settles near292.1/275.5MB, does not return to initial baseline (allocator/code retained); not described as a leak. GC10.7–21.2ms outside timers, with individual rows retained. WASM128MiB capacity perinstance; discarded memories do not accumulate. Explicit boundary GC is assay-specific, not representative browser GC. Timer includes original final60 simulationticks after12 untimedticks; parse/restore/save/hash/GC excluded.

Generated glue registers uncaughtException listeners: loader preserves preexisting host listeners and removes only listeners added by each completed instance. It does not disable host error handling. No per-cell instrumentation.

## Preserved preflight failures

First zero preflight failed because custom instantiate bypassed normal generated WasmOffsetConverter initialization. Coordinator approved initializing the exact existing converter with identical bytes/shared Module as normal glue does. Second zero preflight passed state equality but lacked parsed logs because NODERAWFS writes fd2 directly, not Module.printErr. Coordinator approved VM-local fs.writeSync capture ONLY forfd2; all other calls delegated unchanged. Both failures occurred before warm or accepted measured blocks and are archived with original loaders. Final full zero/release/parser preflight passed before any measured block. No accepted result was discarded or rerun. Source loader and all block logs accompany results.

# Actual-WASM full Sandbox scheduler: nearest optimization

One fixed warm saved world,40,962cells and82initial rabbits. Actual production Planet.simulate runs in a compiled wasm32 module under Node24.22.1, including climate, water, vegetation, rabbit movement/feeding/births and saved RNG. No rendering/browser/rAF or device FPS claim.

## Correctness gates before timing

Existing headless harness was explicitly OriginOnly. This isolated adapter uses actual save_game rabbit restoration and capture blocks, all plant/rabbit counters, authoritative geometry and arrays. Topology identity checked for everycell. No physics stubs. Production source unchanged.

- Both modes reproduce the complete input JSON atzero ticks.
-72ticks baseline/candidate saved world bytes exactly equal, including rabbit RNG and all climate/vegetation.
- Genuine new Node processes:72ticksave→10ticks equals uninterrupted82ticks, separately inbothmodes.
- Both82tick endpoints also exactly equal.
- Rabbits82→98 over72ticks and104 by82ticks: actual births exercised, not empty-agent timing.
- All four timed endpoints match the pre-timing complete-state hash98340832edf0c03a10e601aaf9da6c612545e5ea4ade523190645543a14e4fdc.

## Fixed exclusive ABBA result

Each fresh process executes12warmup ticks, then60timed full simulation ticks (1440simseconds/tick). Input parsing, state construction, serialization, process startup and rendering excluded. Same binary runtime switch isolates the old strict rounded-sqrt scan versus current production pruning. No extra repeats or selected exclusions.

| Arm | Scan | ms/full simulation tick |
|---|---|---:|
|A1|Old|32.8977|
|B1|Pruned|28.5423|
|B2|Pruned|25.4185|
|A2|Old|30.3571|

Median31.6274→26.9804ms/tick,14.69% faster. Both candidate runs beat both old runs, but the range still shows runtime variance. This supports a real WASM simulation benefit in THIS rabbit-populated world, not a universal device/browser speedup. Single fixed world, oneABBA, no statistical population claim. Timed15:33:43–15:33:54UTC with explicitCPUrelease fromparent andbothsiblings.

## Scope and reproduction

The source is the deployedv67 nearest helper; no new production change or deployment. The old metric is literal sqrt(delta.dot(delta)), strict<, ascendingfirstties. Full save parity is the gameplay gate, not squared-distance approximation.

Files: prepare-wasm-nearest-sandbox.py; wasm-nearest-sandbox-main.c; run-wasm-nearest-sandbox.py. Compile qa_wasm_nearest.zig using existing wasm-planet-build.zig and emcc flags in runtime.json. Run script gates first, then timing ONLY in a coordinated quiet window. Input path/hash and copied source/graph hashes in provenance.json. Complete compressed logs and failures retained. Initial preparer exact-source match failed on whitespace, followed by expected incomplete-copy compile errors; fixed before any executable run. No successful result came from that partial source.

No browser context, GPU rendering, DOM/input, animation pacing or actual phone/laptop was measured. Best remaining device gate is the already available in-game measurement on the user's device, or a supported WebGL browser when available, not inventing FPS from this headless result.

# Empty-bloom fast path: correctness and native performance

## Scope and safety proof
This allocation-free O(1) eligibility guard skips a bright pass and four blur passes only when their contribution is provably zero. It does not make the whole simulation O(1), change physics, skip simulation ticks, reduce texture resolution, or change saves.

Eligibility requires browser Origin mode, Normal map, stable radial daylight, orbit camera, zero animals, and finite camera radius strictly between 0 and 250000. Every other configuration retains the original HDR path. The sun is centered 300000 units along the radial camera direction with radius 8000; in eligible orbit it lies fully behind the camera, with at least 42000 units of margin. Browser Normal terrain returns before HDR specular lighting. Valid terrain color mixes are bounded by 0.96; vegetation is clamped and water depth is nonnegative. Compact selection disables the old ring, whose palette is itself bounded by 1. The sky uses a normalized RGB8 cubemap. Hover, seed, flora, god-tool and UI overlays render after postprocessing. Therefore the strict brightness > 1 extraction is empty. Wind and vapor views can be HDR and are excluded.

The enableBloom uniform prevents sampling stale glow on a newly eligible frame. Unsupported frames freshly execute all passes. New emissive scene paths require revisiting this guard. Two pure helper tests cover positive and negative gates.

## Final integrated correctness smoke
Current main includes empty-bloom, performance details and Continents. Native build and both runtime tests exited 0. INTEGRATED-HASHES.txt identifies the exact source snapshot and all entries matched after testing. No core files were edited by this verification.

- Three eligible views (nursery, globe, side): full versus skipped bloom framebuffer bytes identical. Hashes: b4e00b892a2ef407, 8c48e02184eee016, 4cb8175ce1a75e28.
- All four other map modes unchanged.
- Actual free-camera HDR sun peak 9.96875 retained. Direct bright-to-eligible transition without clearing the prior bright buffer matched the empty frame exactly.
- Sandbox rabbit render fixture unchanged. This is not proof of evolved Origin animals.
- Serialized model state equal after normalizing only intentionally changed view fields; no restore hides biological changes.
- All three clock targets produce six fixed ticks and identical physical save hash d523353839672a4.
- Actual pointer down/render/up/render pause prevents any extra simulation tick. Exported pause/speed, invalid rates, long background gap, menu/load debt reset and no-tick render-clock behavior pass.
- Invalid save rejected without mutation; exact restore passes (8734640 bytes).

Existing native shutdown allocator warning remains present. This new path allocates nothing. Tests use llvmpipe software OpenGL with browser-style branches, not actual Android/WebGL conformance. Integrated timings were emitted during other builds and are correctness evidence only, not a benchmark.

## Earlier isolated native performance comparison
The post-v23 native profile measured scene plus postprocessing at 15.17 ms/frame versus actual scene drawing at 2.65 ms. UI was 0.46 ms, sprouts 0.41 ms, nearest lookup 0.067 ms and geometry upload 0.48 ms. This motivated targeting bloom rather than speculative geometry caches.

Sequential same-binary full versus auto runs, five seconds per target on native llvmpipe:

| Target | Median frame ms | p95 ms | Max ms |
|---|---|---|---|
| 1 simulated h/s | 15.06 → 7.02 | 23.60 → 18.00 | 47.03 → 74.92 |
| 6 simulated h/s | 15.76 → 7.34 | 31.82 → 25.00 | 175.89 → 255.23 |
| 24 simulated h/s | 42.89 → 35.23 | 50.70 → 52.76 | 74.34 → 86.07 |

Fast actual throughput was 17.33 → 19.27 simulated h/s. Synthetic native two-frame pause was 29.77 → 17.25 ms, not OS/touchscreen latency. Median improved, but tail/max did NOT consistently improve. Do not claim universal smoothness or extrapolate phone FPS. Todd separately reported v23 at 6–7 simulated h/s versus about 2 previously; that is user-reported device evidence, not this benchmark.

## Reproduction
See qa/README.md and qa/prepare.py. The preparer creates an isolated adapter from the specified current repository; it does not edit the checkout. qa/empty-bloom.patch is the narrow original production patch, not a full old PlayState copy. results/ retains original isolated measurements and final integrated logs. Final WASM/browser deployment verification belongs to the integrator.

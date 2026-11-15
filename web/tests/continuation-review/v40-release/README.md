# v40: reuse atmospheric phase coefficients once per tick

Production change: `AtmosphereWater.PhaseStep.init(dt)` computes the same three exponential relaxation coefficients once for the current timestep. Planet reuses them across its cells. Scalar `phase` remains an API wrapper. Temperature-specific evaporation, saturation, conservative transport, arithmetic ordering and resource rules are unchanged. This does not make the entire simulation O(1): only these repeated timestep-only calculations become O(1) per tick. No persistent cache, extra per-cell allocation, world invalidation requirement, save field or biology change.

## Release gates
- Frozen independent original reference versus prototype, production PhaseStep and scalar wrapper: 37,283 native cases, status plus all five float fields bitwise; all eight test cases pass.
- Pure wasm32-freestanding/Node parity: 15,316 cases across those three implementations, zero mismatches. This is not browser gameplay.
- Three alternating baseline/candidate real-world pairs: actual generated 40,962-cell Origin world, normal nursery and seed, 30 coupled days, 12 warmup plus 60 measured full update/render frames at a fixed 1/60 input delta and requested 24 simulated hours/second. All six complete measured serialized worlds have SHA256 `03374f92d0fd9dbc458a6a1b14119a461074486e304ea1f51024745013fa5993`. A final build using integrated production PhaseStep has the exact same hash. Original saves restored exactly; no fabricated biomass or state reset inside timing.
- Native mobile-policy, one cooperative worker, 390×700, no bloom, llvmpipe software rendering: median update 11.7158→10.5661 ms (9.81% lower), full frame 21.0529→19.6317 ms (6.75% lower). Three paired update reductions range 4.6–17.1%; normal timing variation and outliers remain. This is a sparse biosphere, not dense stress testing or Android/WASM frame-rate measurement. Requested fixed input delta and compute throughput are not measured browser achieved pace.
- Seven JavaScript suites and all 47 save-schema regressions pass. Schema 6 preserved.
- Pinned Zig 0.13.0/Emscripten 3.1.64 production WASM build passes, generated JavaScript syntax passes. Exact built artifact hashes retained in build.json.

Details and raw evidence are in neighboring phase-cache, phase-cache-world, physics-phase-profile and atmosphere-phase-profile directories. Existing native shutdown allocator-leak warning remains. Cloud browser previously could not create the WebGL window; actual Android touch/graphics and on-device performance remain unverified. No GitHub CI success claimed.

## Ecology research is not shipped
The paid-resting null assay is deliberately research only: it shows costs but no drought/heat survival benefit. Current active ancestors lack an explicit basal energetic budget, so reduced resting maintenance is not yet a demonstrated gameplay strategy. No dormant organisms, fire immunity, seedbank or forced succession was added by this release.

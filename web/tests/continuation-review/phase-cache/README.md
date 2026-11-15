# Per-tick phase relaxation cache (isolated experiment)

No production edits in this experiment. `experimental/phase_cache.zig` stores dt and the three relaxation results once. API: `Cache.init(dt)`, then `.phase(liquid,vapor,saturation,temperature,old_rain_rate)`. Use only immutable cache constructed by init for the current tick's exact dt. Do not reuse across timestep changes or alter fields manually.

Validation, zero-dt handling, arithmetic order, comparisons and result fields duplicate original scalar phase. Temperature-dependent evaporation still occurs conditionally; precomputing a factor for frozen cells is benign. Invalid/nonfinite/negative dt yields null on phase; signed zero preserves original fields. No clamp, approximation or reordered rain-rate calculation introduced. Evaporation and rain-memory constants currently equal; intentionally compute both as original, not a new assumption.

## Independent reference and parity
`experimental/phase_reference.zig` freezes original scalar algorithm (only Phase result TYPE is shared). This keeps reference independent of future production optimizations. Original prototype remains a research artifact. `qa_phase_cache.zig` tests37,283 cases:16000 bounded random/edge-dt cases,1280 per-field×dt edges,20000 random f64-bit inputs,3 specials. Each optional status and all five output fields compared bitwise, including signed zeros, subnormals, extreme finite values, invalid inputs and NaNs. All8 native tests passed including imported water-cycle tests. BUILD_EXIT=0.

`qa_phase_cache_wasm.zig` executes15316 deterministic cases against independent reference, all five fields bitwise. Compiled wasm32-freestanding ReleaseSafe, instantiated using Node,0failures. This is **pure-WASM parity**, not Emscripten, browser rendering, mobile frame rate or actualgame validation.

## Microbenchmark
40962 varying cells×8evolving ticks, runtime dt360–362s,7passes. Alternated baseline/candidate order; reset inputs identically; all output fields feed integer hash and liquid/vapor/rain update subsequent ticks. Matching hashes for every paired run. Final independent-reference medians:
- scalar10.548598ms/8ticks
- cached2.502890ms/8ticks
- about4.21× faster phase microbenchmark, about1.006ms saved/tick here.

CPU variability is visible. Earlier actualproduction phase baseline trials were9–10ms versus2–3ms and also matched hashes. No full-game performance claim. Actual atmospheric saturation, transport, rendering and scheduling are absent. Candidate still O(N) over cells; expensive relaxation work moves to O(1) PER TICK, not O(1) whole simulation.

Optimized LLVM excerpt `batch-ir.txt` confirms scalar phase is called inside baseline cell loop (its relaxation calls remain inside phase); cache initialization computes relaxation before candidate loop, with cached values used in loop. Compiler did not automatically hoist original scalar phase across per-cell validation. Initial benchmark mistakenly initialized an unused cache once per baseline batch; removed and reran before final evidence. No extra initialization remains in final baseline.

## Reproduce
Zig0.13.0:
```
zig test src/qa_phase_cache.zig -O ReleaseSafe
zig build-exe src/qa_phase_cache_wasm.zig -target wasm32-freestanding -O ReleaseSafe -fno-entry -rdynamic -femit-bin=<output.wasm>
node web/tests/continuation-review/phase-cache/check-wasm.cjs <output.wasm>
```
`run.log`, `wasm-parity.log`, source hashes and IR excerpt preserve evidence. Actual-world copied-Planet comparison is separately owned by reviewer; integration/deployment not performed here.

## Final production parity after PhaseStep integration
Parent integrated `AtmosphereWater.PhaseStep` and scalar `phase()` now wraps it. Final QA explicitly compares THREE implementations to the independent frozen pre-change algorithm for every case: experimental Cache, production PhaseStep, production scalar wrapper. All five fields/status remain bitwise equal.37283native cases and15316pureWASM cases pass; each case now performs3reference comparisons. All8native tests pass, BUILD_EXIT=0; pureWASM0failures. This directly checks production arithmetic, not only its earlier prototype.

`initial-run.log`, `initial-wasm-parity.log` and `initial-SHA256SUMS` preserve pre-integration research evidence. Existing `batch-ir.txt` remains the initial benchmark IR; benchmark still measures frozen reference versus experimental cache, not a new fullgame claim. Updated `SHA256SUMS` records final production source and finalQA. Actualworld/copiedPlanet and eventual browser deployment verification are separate tests owned by parent/reviewer.

# Fixed actual-WASM land-beta screen

Frozen isolated integration c6819a0, unchanged production v72. One fixed screen, no retuning or additional timing repetitions. Node/V8 WebAssembly, ReleaseSafe, 40,962 cells, one event-loop worker. Each timed process runs 12 warmup and 60 measured full `Planet.simulate` ticks (1,440 simulated seconds each). ABBA per scenario; startup, parsing, restore, JSON serialization and rendering excluded. This is not a browser, mobile, rAF or full-game frame-rate claim.

## Correctness first

All four starting scenarios pass zero-tick restoration (old v6 version/default zero toughness migration explicitly recognized). Natural60, warm Sandbox and empty legacy projection retain exact old typed state/RNG versus actual v72 after 72 ticks. Only legal empty `cohorts:[]` encoding differs in candidate Origin wire output. Every mode passes genuine separate-process 72+10 versus uninterrupted82 complete saved-state equality. No field-value tolerance was used.

Beta input is the previous **new-world** seed42/subdivision6/radius5000 beta2 save, not an existing world's activation. Its comparison legacy input retains the same projectable fields, but omits beta soil and rounds vapor to the compatibility f32 projection. **These are not identical full water inventories or an ecological controlled comparison.** Enabled beta is checked against its own continuation, not legacy physics. At72 further ticks, soil is finite [0,1], maximum0.999987482kg/m², 2,602 positive cells, summed density932.670686kg/m² (not global kg). No cohorts or assigned roots in this empty test. Bounds/continuation are not a global conservation proof.

## Fixed timing results

| Scenario | v72 median ms/tick | Candidate | Difference |
|---|---:|---:|---:|
| Natural60, beta off |18.313|15.274|−16.60%|
| Warm Sandbox, beta off |28.837|24.115|−16.38%|
| Empty projection, beta off |17.082|12.494|−26.86%|
| Empty beta versus v72 projection |16.592|30.734|+85.23%|

No observed disabled regression in this bounded screen. Apparent improvements are **not a speedup claim** from two samples each. Enabled cost is material: about1.85× the legacy projected scenario. No further runs or optimizations were selected after seeing results. This remains isolated, not production-ready; cost does not establish a usable mobile frame budget.

## Memory / wire size

WASM Planet struct2936→3000bytes. Enabled arrays: soil327,696bytes, vapor327,696bytes, scratch/root-hydration1,310,784bytes: total1,966,176bytes beyond legacy arrays. Candidate Cohort88bytes; no measured baseline cohort-layout delta or whole-process RSS claim here. Off beta arrays remain unallocated in this loader. Existing atmospheric scratch and allocator overhead are not included in that added-array subtotal.

72-tick save sizes: natural baseline11,131,292 / candidate11,663,798 (+532,506 legal serialization bytes); warm7,704,842 both; empty off10,977,036 /11,509,542; beta12,034,989. Beta size comparison includes intentionally different physical outcomes and added authority. Save-owner compact variant aa2e686 can remove off redundant empty cohort arrays but was **not substituted into this measured source**.

## Adapter and failures retained

Loader combines previously verified Origin and Sandbox actual-WASM restore paths, restores all cohort/RNG state and beta authoritative soil/vapor/current+scratch, and validates every neighbor slot against actual graph enum order. Capture persists current authority; old fields are not silently substituted. Simulation source is unchanged except unused diagnostic globals. Source hashes and exact QA source retained.

Initial link omitted Emscripten offset-converter support, failed before simulation; corrected to the existing diagnostic link configuration. Initial zero-tick comparison overlooked default zero toughness omitted in old v6 input; corrected explicit default handling, not model state. Initial logs/source provenance retained where available. No physics, rates or numerical budget changes.

Limits remain: soil thermal capacity and latent heat are omitted, inherited liquid transport drift remains, and no positive-root full-scheduler birth or ecological establishment is demonstrated. The enabled empty-world cost is now measured rather than assumed.

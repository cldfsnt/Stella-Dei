# Actual-WASM compact liquid transport: numerical improvement, practical gate FAIL

Production and live game are unchanged. The fixed three-world60tick gate completed. All structural/binary-rounding and save-continuation checks pass, and accumulated absolute global liquid drift falls about91%. However, per-cell absolute error relative to actual one-way transferred water is1.34–1.77%, exceeding the predeclared0.1% cap. **HOLD. Performance timing and420tick follow-up were not launched**, per the frozen stop rule. Their scripts are prepared, not evidence of execution.

## Actual work executed

Current production actual Planet/EventLoop under wasm32 ReleaseSafe, emcc-O2, Node; same hashed natural40,962-cell day30/day60/day90 inputs and actual geometry as afe9e62. Only Origin liquid scatter is replaced by the unchanged previously tested compact helper. Same f32 absolute head/flow law, immutable donors, destination gather, unique reciprocal edges including tails, fixed f64 accumulation then f32 final pools. No roots, alternative hydraulic head or finite-validation performance candidate.

Candidate private helper adjacency uses the established send order [0,3,1,4,2,5] of public neighbor rows, preserving prior helper operation order. Planet's actual adjacency remains original enum order. Independent oracle verified all40,962 remapped rows. Private topology is prepared once, invalidated at computeNeighbours/save.apply, pointer/count guarded. No per-tick topology hashing. Actual WASM scratch payload is58bytes/cell (24edge+24neighbor+6reverse+4head),2,375,796bytes at40,962cells; native prior82bytes/cell is not the WASM value. Allocation/node-count rebuild uses the existing simulation arena and has process/planet lifetime; same-size terrain changes do not affect topology, and heads refresh each tick.

Independent standalone native/WASM compact-vs-cached gate also passed all3worlds×4dt×both source orders, exact outputs/widened edges/ledgers (sibling checkpoint860c868 source, subsequent saved results). Those helper checks are not a full-game performance test.

## Complete-state proof

For all three worlds:
- Zero-tick candidate loader returns the exact parsed original save.
- Candidate plain and diagnostic60tick output files are byte-identical.
- Legacy diagnostic60tick output equals the frozen production WASM hash.
- Candidate70tick complete save is byte-identical to its60tick serialized save reloaded into a **new Node process** and advanced10ticks.
- Output schema6/model5 validates. The loader uses actual production schema/physics, not browser IndexedDB or menu callbacks. No UI save/load interaction claim.

`controls.json` preserves input, complete output, process-restart and trace hashes. Large original saves are read-only; separate QA outputs/binaries remain local with hashes. Trace-only allocation stores the actual pre-cast f64 accumulator; it does not change the uninstrumented helper or timed candidate. First diagnostic compile failed solely because a QA declaration preceded the module doc-comment, retained and fixed. First uninstrumented day60 tick succeeded before trace integration. Its cold timing is not an accepted performance measurement.

## Independent all-cell exact oracle

Fire's integer-dyadic oracle (`web/tests/liquid-wasm-oracle.py`,11 tests; checkpointad6ba41) audited every destination at every tick, using actual pre/post f32 masses, all f32 edge values, actual f64 pre-cast accumulators and actual patch area7,669,529,600m². Structural checks enforce finite/nonnegative, unique edge debt/credit, no donor overspend, exact cast, gamma12 accumulation and half-ULP final rounding bounds. All pass; no clipping, tolerance increase, hidden refill or global correction.

Native mass unit=10^9kg. A=Σcell,step |output−exact immutable edge balance|. D=Σstep |global liquid inventory error|. T=gross one-way edge mass counted once, not incident mass counted twice. D and A are deliberately distinct.

| Input | Candidate A (10^9kg) | T (10^9kg) | A/T | Candidate D / legacy D | A / derived budget |
|---|---:|---:|---:|---:|---:|
| day30 |1,807,675.194|101,874,660.100|1.77441% FAIL|0.091879 PASS|0.423475|
| day60 |1,861,791.472|124,977,373.891|1.48970% FAIL|0.085392 PASS|0.436185|
| day90 |1,866,010.789|139,588,364.140|1.33680% FAIL|0.085264 PASS|0.437219|

Candidate signed liquid totals are−253,091.159/−259,693.446/−268,445.997native units; legacy−2,754,619.938/−3,041,193.588/−3,148,404.397. Candidate D equals absolute signed total here because each step's global drift is negative, not because cancellation was used as an acceptance shortcut. Multiply numbers by1e9 for kg.

Maximum individual local equivalent water-depth error is about1.03029mm per cell-step. A divided by summed per-step inventory is1.83–1.89e−8; A relative to initial inventory is1.10–1.13e−6 over the60tick horizon. Small ocean-relative ratios do not override the failed movement-relative budget.

Resolution warnings (B>positive incident flow/128) occur in1,682,992/1,696,494/1,678,642 cell-steps, not distinct permanent patches. Positive-net-receipt events whose output fails to increase number10,649/14,116/16,377. These are diagnostic precision limitations, not automatic organism deaths or visible game glitches. The failed cap does **not** demonstrate that a player would notice1mm of local error, nor that91% less aggregate drift is worthless. It means this candidate did not meet the criterion fixed before the actual movement totals were known. No retrospective threshold relaxation.

## Coupled and ecological outcomes

Total surface+vapor endpoint changes (not just liquid transport), native units:
- day30 legacy−2,736,236.959; candidate−234,786.540.
- day60 legacy−3,014,082.094; candidate−232,711.605.
- day90 legacy−3,117,059.344; candidate−237,122.281.

Other atmosphere stages contribute; do not assign the total entirely to liquid. These values are independently summed from represented endpoint inventories.

Baseline/candidate endpoint living colonies:23/23,64/64,45/44. Occupied patches:13/13,38/38,37/37. Day60 biomass2.619323545 versus2.610378801; day90 2.012372026 versus2.006209145. Different legitimate water trajectories alter ecology. No survival, evolution, land-life or natural fitness improvement is claimed.

## Next design implication, not implementation

The f64 accumulation error allowance alone, normalized to observed gross transfer, is bounded around0.94–1.29e−9 in these traces, vastly below the failed0.1% criterion. This analytical bound concerns this gather stage only, not a whole-engine upgrade. The dominant limitation is writing each new liquid pool back to f32, not a failure of the immutable edge budget.

A defensible next isolated design would preserve an authoritative f64 surface-water pool through the entire physical cycle, with explicit legacy f32-parse-then-widen migration, audited phase/tool/save boundaries, and read-only rounded rendering/thermal views where intentionally retained. Immediately casting a local f64 result back to f32 cannot solve this failure. A hidden residual water account, global renormalization, or quantized refusal of all tiny transfers would change physical behavior and must not be smuggled in as precision repair. Broader representation changes need their own scoped preregistration and practical tests; no broad climate rewrite or new rates are proposed here. Alternatively, a future independently declared player-scale criterion could investigate whether this bounded error matters for actual gameplay, without relabeling this failed gate.

## Reproduction

`prepare-liquid-gather-wasm.py` copies the frozen actual-Planet loader and transplants only the already tested compact Origin integration. `build-liquid-gather-wasm.sh` builds plain candidate and separate candidate/legacy trace emitters. `run-liquid-gather-wasm-controls.py` runs the fixed60tick/zero/restart gates. The oracle reads `helper-graph.json`, `candidate-dayD.bin`, `baseline-dayD.bin`; all trace header/area/count checks are explicit. All source/artifact hashes, exact diffs, complete-state hashes and control logs are saved. Independent numerical reports are saved by the oracle owner. No performance runner or420tick run was executed after numerical failure.

# Cached topology gather: exact model, performance remains unresolved

Isolated optimized SAME-output variant of naive immutable gather. One-time copied/validated reciprocal topology, sixu8 reverse slots and self/duplicate masks replace per-step topology validation and36incoming-edge searches. Dynamic finite/head/sourcebudget/negative-output guards remain. No head-law, biology, save-schema or source accounting changes.

Actual geometry writes in production occur only appendNeighbor/computeNeighbours, called during construction. Copied candidate explicitly invalidates cache at computeNeighbours and successful save.apply, and rebuilds on topology pointer/count change; newPlanet defaults empty. Cached arrays are private owned snapshots and immutable between rebuilds. Samecount changedgraph requires explicit prepare/invalidation; a raw in-place write bypassing those hooks is NOT detected by a per-tick hash. Invalidload validation exits before cache reset. Pure helper requires prepared immutable arrays, not arbitrary forged reverse indices.

Independent helper gate passes: mixedscales, three dt, both source traversals, duplicate/self/tail, samecount changedgraph rebuild, nonreciprocity and offsetalias refusals. Exact outputs/edges/ledger versus naive solver. Actual day60 correctness run and all18 timing-run endpoints equal previous naivegather byte-for-byte; all uninterrupted/restored10tick continuations exact. No process-restart claim.

## Fixed timing outcomes: HOLD performance claim

Same protocol as earlier naive gate:3alternating pairs×3worlds,60actual1440-second ticks, cold first cache construction included, onlysimulate+clock timed. No known heavy sibling work. All18 results retained; no additional favorable repeats.

|World|Baseline median ms/tick|Cached median|Change|
|---|---:|---:|---:|
|day30|8.373232567|9.881868567|+18.02%|
|day60|7.981011517|8.544388217|+7.06%|
|day90|9.958721333|9.7634532|−1.96%|

Paired changes: day30+34.41/+12.42/+18.12%;day60+6.08/+4.52/+40.89%;day90−1.96/+10.09/−4.78%. Baseline variability is material; do not compare medians from separate naive/cached windows to claim a cache speedup. Nativeproxy, not browser/device/frame proof. This does not meet a general no-regression/speed goal.

Scratch native64 is102bytes/patch:6f64 flows+6usize neighbors+6u8 reverse,4,178,124bytes/40962. Not per-tick allocation; no saved authority. Memory and scalar edge work remain possible costs. A future strictly separate compact-layout experiment could store edgeflows asf32 (they are already computedf32 and merely widened) and neighborIDs asu32, then widen on gather without changing arithmetic. This is a proposal, not tested or automatically approved. Do not change head precision or float operations to obtain favorable timing.

Numerical drift, changed ecology and remainingf32 pool residuals are identical to naivegather evidence. Correctness improvements do not by themselves authorize promotion or unblock roots. No live source edits/deployment.

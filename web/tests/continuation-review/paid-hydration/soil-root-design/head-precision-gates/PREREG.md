# Head precision: independent gates for a later immutable-solver variant

Design only. Do NOT change the current same-head immutable gather candidate. First establish its material/ownership/basic behavior gates independently. A later variant may change ONLY the head expression; no conductance, cap, timestep, soil/root model, terrain, topology or biological parameters change. No new selected ecology trial or promised successful land outcome.

## Frozen source and comparison arms

Use all directed edges from the exact40962cell day30/day60/day90 census and the already preserved `head-edges-day*.npz`. Original snapshot and topology hashes are recorded in the census. Existing complete edge outputs remain unchanged.

Arm G: verified same-head immutable gather, current f32(elevation+representedDepth) then subtraction. Arm H: IDENTICAL gather/source allocation and receiver handling, but `(f64(elevation_from)-f64(elevation_to))+(f64(representedDepth_from)-f64(representedDepth_to))`. Keep represented depth identical in both; do not simultaneously change native water precision or multiplication order. Differences between G and H can then be attributed to head arithmetic, not replacing the old mutable solver.

## Fixed scenario partitions (all qualifying cases, no winner selection)

1. ALL existing edges, both orientations, all three worlds. Retain routing, head, proposed and actual source-funded transfers, cap hits and residuals.
2. Actual shallow-source edges: source represented depth<0.2m, including dry/cold cells. Do not silently restrict to living, fertile or warm cells. Stratify positive/zero source water and source-cap-limited versus head-limited behavior.
3. Actual near-equilibrium edges: absolute difference-before-add head<=0.02m, including exactzero. The threshold is twice the predeclared1cm probe, not fitted to outcomes. Apply both source/target orientations and no-pulse controls. Distinguish arithmetic ties from genuine equal heads.
4. Actual deep-basin edges: BOTH represented depths>50m, and separately a deep source adjoining a shallower target. Preserve all ocean cases; they may dominate aggregate changes but are not terrestrial success evidence.
5. Synthetic equal-terrain pair at each actual12352 radius scale, explicitly NOT an actual discovered habitat. Fixed common depths0,0.001,0.01,0.02,0.1,0.2,1,100,10000m; ±1cm difference where source water permits, plus zero. Also fixed terrain differences0,±0.01,±0.5m expressed as declared high-precision fixture geometry only: if stored f32terrain cannot represent the requested difference, label the actual represented geometry and do NOT pretend it retained centimeters. This separates head-addition loss from terrain-storage loss.

## Perturbation material and cap rules

For each pair, compare arms from EXACT SAME initial represented water and elevation. A nominal1cm paired perturbation is a conservative transfer from one member to the other, not free added water. Choose downward representable common-quantum transfer no greater than1cm, verify exact endpoint debit=credit with an independent rational oracle; record actual delta. If no positive exact transfer exists or donor lacks water, retain as rejected/zero-resolution case; never top up water or tune delta to get a preferred routing outcome. Repeat opposite direction. The original unperturbed pair remains a control.

For geometry-only response witnesses, a separately labelled nominal1cm addition may illustrate arithmetic but is NOT included in closed-inventory solver claims. Preserve source caps under zero, tiny, sufficient and cap-saturating inventories. Report cases where head sensitivity improves but the unchanged available-source cap leaves transfer unchanged.

## Required correctness gates

- Source and receiver ownership/material conservation pass the already frozen SAME-HEAD gather budget, without relaxing it for H; no extra error-credit pool.
- No negative/nonfinite mass, duplicate target/edge writes, self/padded-edge transfer, or source overspend. Root/soil are not part of this gate.
- Reversing a pair negates the same represented relative head; a single pair cannot propose simultaneous opposite downhill flows. Exactly equal represented terrain/depth implies zero head-driven flow.
- Raising represented source water cannot decrease its head; lowering it cannot increase its head. Once source caps apply, assert boundedness rather than demanding a larger actual transfer.
- On equal-terrain fixtures with a representable1cm differential, H retains the differential instead of the known0/.488m radius-scale snapping. No exact equality to requested1cm when stored water rounded; compare to actual represented depth difference.
- Uniform water/geometry fixed point and one-step two-cell equalization controls. Do not assume all multi-neighbor real-world cells are static equilibria or that correcting a head automatically improves ecology.
- Cell/edge iteration permutation produces equivalent results under the SAME-HEAD solver's defined arithmetic order policy. Do not introduce a new slot/order privilege.

## Engine and performance gates, only after local gates

First copied full-scheduler10ticks on all three fixed natural worlds, G versus H from independently deep-frozen identical starting saves. No water/terrain intervention, no founder selection. Log material ledgers at transport stage separately from phase/advection, actual routing/cap changes and any exposed-habitat changes without claiming benefit. Keep disabled/sandbox behavior and existing save/load policies intact; true uninterrupted/restored continuation must remain exact within each variant. Comparison between different algorithms is NOT expected byte-identical.

For time-resolution diagnosis use the SAME fixed elapsed interval with dt1440/720/360; retain all results, no choosing whichever makes roots win. Convergence is measured, not claimed merely from one monotonic example. Actual ReleaseSafe and supported browser/WASM arithmetic need targeted parity/finite checks. Measure native full-stage/frame cost with the same world/view; no assumed speed improvement or device claim. A measurable cost/behavior tradeoff remains the coordinator's decision before promotion.

No experiment in this protocol establishes evolved roots, animals, persistent land colonization or accessibility. This is a numerical/hydraulic gate, distinct from conservation repair and later inherited ecological experiments.

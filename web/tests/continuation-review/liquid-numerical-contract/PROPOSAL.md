# Proposed practical liquid-transport numerical contract

Design only, before new outcomes. No implementation or tolerance activated. Applicable to immutable source / shared f32 edges / f64 gather / one f32 output cast. Other arithmetic requires its own operation count. This does not reopen held performance results.

## 1. Exact structural gates remain

Finite nonnegative authoritative pools; each directed transfer has one immutable shared edge value, counted once at its donor and once at its receiver; no duplicate/self transfer; sum of outgoing edge values never exceeds donor source. Test these from exact stored binary operands. Do not permit a donor budget violation under a global tolerance or correct totals by modifying an arbitrary cell. Topology/order/tail and save-continuation tests remain mandatory.

## 2. Permit ordinary endpoint rounding, bounded by operations

For each cell use an offline exact oracle:

`x_i = M_i - sum(outgoing stored edges) + sum(incoming stored edges)`

`e_i = stored_f32_output_i - x_i`.

At most six subtractions and six additions in f64 precede one round-to-nearest f32 cast. With u64=2^-53, gamma12=12*u64/(1-12*u64), S_i=M_i+sum(out)+sum(in), a conservative bound is:

`B_i = gamma12*S_i + 0.5*max_adjacent_f32_spacing(output_i)`.

Use the larger adjacent finite spacing at binade boundaries; zero/subnormals use2^-149, and largest finite f32 uses its lower finite spacing (do not turn the bound into infinity). Keep the bound positive in exact/offline arithmetic even below f64 range. Gather and casts must retain the documented strict arithmetic; re-associated/vector code needs matching proof/operation count. Finite nonnegative x and output are hard gates.

Require EVERY |e_i|<=B_i, then verify signed E=sum(e), A=sum(abs(e)), and A<=sum(B). This accepts theoretically expected f32 cast noise rather than demanding exact endpoint equality. Signed cancellation alone cannot pass. Current final-cast-only diagnostics omit f64 accumulation; the independent endpoint oracle includes both. Native mass units are10^9kg, so multiply by the exact integer1e9; equivalent local water-depth metres are kg/(1000*actual_area_m2).

## 3. Inventory and transport views, without denominator tricks

Per step publish E/I, A/I, A/F and sum(B)/F, where I=sum initial liquid and F=sum directed transferred mass counted once. Zero inventory or zero transfer has an explicit zero/not-applicable case, never an epsilon denominator. If F=0, exact unchanged outputs should be required: no rounding is needed. For valid conservative shared edges, sum(x)=I; the inventory-relative scale is consequently of order u32=2^-24 plus the much smaller f64 bound, not an empirically selected percentage. Publish actual ratios, not just a pass label.

A small global ratio can still erase a meaningful tiny local flux. Independently flag cells where B_i>incident_transfer_i/128, meaning fewer than seven useful binary digits of guaranteed transfer resolution. This128 ratio is a proposed engineering resolution target (~0.78% worst-case local relative uncertainty), NOT measured ecological tolerance or real-water calibration. Report flagged cell count, fraction of transferred mass touching them, zero-received positive intended flows, and maximum local error/depth. Do not silently discard these cells or freeze the entire world merely because a microscopic leg cannot alter a large f32 pool. Do not claim such legs are accurately resolved either. Seven-bit target requires coordinator approval before becoming an acceptance rule.

## 4. Time horizon and comparison

Freeze current three worlds and60tick horizon for initial gate;420tick follow-up before any root integration/release. At every step record E,A,B,I,F; over the fixed horizon require all local bounds and sum(A)<=sum(B), publish sum(E), sum(A), sum(B), sum(A)/sum(I), cumulative error relative INITIAL inventory, and transport-weighted ratios. Sum absolute temporal errors, not only final-minus-initial liquid (climate legitimately changes liquid between stages). No assumptions of independent random errors or sqrt(N) cancellation. If long-horizon uncertainty grows unacceptably, shorten the supported claim or redesign precision; do not widen a numeric constant after seeing results.

Compare original scatter and candidate on the SAME frozen per-step inputs for numeric attribution where feasible. Changed solver trajectories need not be identical, and different ecological outcomes are neither performance nor accuracy benefits. Retain measured legacy receiver/add/subtract imbalance and candidate three-gather signed/SUMABS records. The existing candidate A~1.8million native over60steps is not automatically a bug merely because its kg value is large: assess against operation-derived bound AND local traffic resolution. Conversely, a small world-relative error does not excuse hidden unfunded transfers.

## Decision boundary

Passing these gates supports 'bounded ordinary f32 rounding for this solver and tested horizon', not exact conservation, calibrated hydrology, browser performance, or safe root physiology. The exact cross-unit root-receipt experiment remains separately failed/held under its own predeclared contract. No retrospective tolerance is applied to relabel that experiment.

## Coordinator approval amendment (before new outcomes)

The operation-derived per-cell bound and absolute-accounting gates above are approved for the next isolated test. Local B>incident/128 remains a descriptive resolution warning, NOT automatic whole-game failure.

Additional practical acceptance gates fixed by the coordinator:

- At least50% reduction versus legacy WASM in `D=sum_over_ticks(abs(global_per_step_drift))`, separately from the stricter no-cancellation per-cell `A=sum_over_ticks,sum_over_cells(abs(e))` accounting. Report both quantities by name; do not substitute one for the other.
- Native/browser distinction retained: fixed18 actual-WASM timing runs, three alternating pairs per each of the three frozen worlds. At most5% per-world median slowdown and at most3% pooled geometric-mean slowdown allowed as a cost of the correctness repair. No extra favorable reruns.
- Only if the60tick gate passes, execute the already-declared420tick numerical follow-up. Preserve all per-step bounds, absolute errors, local-resolution warnings, original outputs and failures. No threshold widening from observed outcomes.

These are prospective engineering acceptance targets, not universal physical accuracy guarantees and not permission to deploy without the remaining correctness/source review.

# Throughflow receiver precision: feasible local receipt, integration withheld

Three executable ReleaseSafe helper tests pass. No live or frozen candidate file changed. New helper is a pure feasibility transaction over **two authoritative f64 kg/m² pools**. It is not current Planet, a residual accumulator, a second vapor store or a full climate fix.

## Observed operands and outcomes

Actual root25k10 Water− arm ticks1/2, area7669529600m²:

| Pulse | Existing paid density | Existing f32 vapor received | Exact common f64 debit/credit | Unspent fraction |
|---|---:|---:|---:|---:|
|1|5.445914790658257e−5|4.774881336920585e−5|5.445914788992923e−5|3.057951879442541e−10|
|2|1.3555834952327928e−6|0|1.3555834925682575e−6|1.9656002514568814e−9|

No missing amount is silently granted. Unspent quantity remains in the source, and only the common represented endpoint receipt could fund hydration. Conversion of original f32 native vapor into f64 density is one initial representation choice, not a new physical source; subsequent conversion back would reintroduce the blocker.

Receiver-led proposal is rounded downward, donor removal bounded, receiver rechecked against actual donor capacity. Commit only when error-free two-difference decompositions show zero low parts and equal high source debit/target credit, bounded by original request/source. Otherwise no mutation and no receipt. No f128 runtime, no protected buffer, no interpolation, no target-total correction. Exact closure here is this particular represented two-pool transaction, not every coupled atmospheric operation.

Fixed10000 scale/request cases:7285 paid,2715 refused unchanged. The enormous-vapor/tiny-request example refuses with zero signal; f64 cannot support all scales. Ten thousand sequential transfers from1 into200 produce total paid.09999999974752427 with identical actual cumulative source decrease/receiver increase. Invalid/negative/nonfinite inputs refuse. No threshold tuned to desired survival. No ecology or performance claim.

## Why this is not a small drop-in fix

Current Planet stores waterVaporMass AND newWaterVaporMass as f32 native billion-kg arrays. Phase exchange and atmospheric gather explicitly cast back to f32; water/wind transport writes/switches the second array. Temperature, pressure and renderer read the same authority. Save.vapor is f32. A local f64 receiver cast back on the next tick loses the represented flow again. A permanently segregated transpiration-vapor sidecar would evade condensation/advection/thermal effects and become an unphysical protected reservoir, unless all those operations genuinely consume the combined authority with explicit receipts. Do not add such a sidecar merely to pass this helper.

A coherent f64-vapor option needs one authoritative unit choice across both arrays, initialization, phase/condensation, advection/gather, pressure/temperature readers, shader/display views, tools and versioned capture/apply. Keeping native mass units requires a separate area-conversion budget and different test; this density-based helper has NOT demonstrated that migration. Widening just the two vapor arrays costs327696bytes/40962patches before allocator/render buffers. All-f64 authority still needs measured finite coupled budgets and performance, cold/empty controls, disabled parity and true save continuation. Not proposing an unreviewed climate rewrite.

A lower-scope alternative is to reject/unspend any f32 receiver-unrepresentable transfer and derive hydration only from final represented source-and-receiver funding. It is conservative but preserves a coarse small-flow cutoff, can systematically suppress rare weak roots, and requires an area-conversion receipt proof. Rounding up source spend or granting signal for water that disappears is not an acceptable substitute. No such f32 alternative is implemented here.

Recommendation: retain this as a bounded f64-authority feasibility proof; do not wire into current candidate. Resolve full physical ownership and receiver precision before using the transient two-pulse biological benefit as a mechanic.

Run Zig0.13.0: `zig test src/qa_root_vapor_receipt.zig -O ReleaseSafe`. Inputs came from frozen root-drain-qa/root25k10.log, action1 tick1/2; source hashes in provenance.json.

# Prospective practical water-error gates

Read-only analysis of frozen5604b4b outputs. No rerun, implementation, tolerance applied retrospectively or approval of production. **The prior exact cross-unit conservation gate remains FAILED.** This proposes a different prospective engineering criterion for future experiments, requiring independent review before use.

## What the old measurements mean physically

Diagnostic actual roots debit428,072.6728250545kg and lose0.0002767580838280992kg. Aggregate loss fraction6.46521260050639e−10 (0.00000006465%). Individual loss fractions3.6239831195263876e−10 and1.2060931106699611e−8. Each loss is below ONE ULP of its f64 vapor receiver (~.000227374kg). Near-one f32 hydration signal spacing is2^-24≈5.96e−8, larger than either relative physical deficit. These are ordinary receiver-scale rounding losses, not disappearing ecological doses.

Original actual f32 trial lost14.45% overall and100% of its weaker pulse. The new actual trajectory's second dose changes slightly; do not pretend this is a byte-identical whole-world comparison. Its weak pulse is now received rather than vanishing. Exact refusal eliminates the tiny error by eliminating BOTH root doses, a scientifically meaningful kinetic distortion, not automatically a superior game model.

Across diagnostic six recorded ticks, phase per-cell-net SUMABS.003208483kg against2.571754654e15kg represented vapor exchange gives1.2476e−18. Atmospheric gather sum of absolute per-tick global net errors.192449124kg divided by1.315202108e15kg endpoint half-L1 redistribution gives1.4633e−16. Signed gather net is−.117777591kg. Endpoint half-L1 is a transport lower bound, not measured gross edge flux. Phase per-cell net can hide cancellation between operations; neither ratio proves every individual exchange fair or accurate. Inventory-normalized and per-tick values are in normalized-errors.json.

Meanwhile unchanged liquid transport loses~3.9e13kg PER PASS. Its inventory-relative percentage may appear small because oceans are vast, but that does not make an avoidable, order-dependent, non-conservative solver acceptable. Separate an ordinary representational rounding envelope from algorithmic ownership/order errors. Do not use a planetary inventory denominator to forgive a vanished small biological dose.

## Proposed dual gate, BEFORE any next experiment

### Hard structural gates (not tolerances)

- Finite, nonnegative authoritative endpoints; no source overspend or hidden sidecar/topup.
- Each physiological credit≤its request and actual source debit AND conservatively converted actual receiver receipt. Shared allocations remain permutation-invariant and cannot duplicate a shared receipt.
- Root transfer must not create physical water (exact receiver kg≤exact source kg for the existing downward-receipt design). A measured allowed LOSS is not permission to grant bonus mass.
- Zero represented receiver receipt means zero corresponding credit; if transfer cannot meet the prospective error bound, leave source unchanged rather than remove a dose then silently discard it.
- Distinguish material error from REQUEST UNDERDELIVERY. A zero-flow exact transaction must still be reported as kinetic failure if the intended dose is meaningful.

### Arithmetic envelope

Trace the executed strict-f64 operations and forward-propagate their ULP errors in common kg, rather than choosing a constant from the observed loss. For the current soil→vapor path, conservatively allow up to2ULP for each rounded-down multiply/divide/difference (nearest operation plus possible nextAfter), propagated through subsequent area/unit factors, plus2ULP of the final vapor addition. Use the actual intermediate operand values, not global inventory, and reject nonfinite/overflow cases. Exact TwoDiff/Fraction audit checks whether this envelope is valid over declared ranges before accepting it as a runtime rule.

For source debit density d and area A, a candidate bound includes density-difference rounding×A, product rounding in d*A kg, division rounding in (d*A)/1e9 native×1e9, and receiver-addition rounding×1e9. Do not omit the difference error or assume source density and native units are exactly interchangeable. This is a proposed derivation to verify, not an already-proven universal2ULP theorem for the whole helper.

For phase/advection use the corresponding per-operation leg envelopes, accumulated as SUMABS as well as signed residual. Per-cell or world cancellation cannot make a failed leg pass. Actual source-bound tests remain mandatory for donor coefficients and gather.

### Separate ecological resolution cap

Propose maximum material loss **2^-20 of each positive source-paid root dose** (about0.954ppm), AND the arithmetic envelope above: the tighter bound wins. This is chosen prospectively as a power-of-two engineering resolution, not fit to an endpoint winner. It is~16× near-one f32 signal spacing and>30,000× smaller than a1/32 allocation step; a1kg dose can lose under1mg, while a tiny dose gets a proportionately tiny allowance. It explicitly rejects the original14.45%/100% failures. It prevents enormous receiving inventories from excusing loss of a rare organism's entire dose.

Keep signal conversion separate: f32 h must be rounded down and its demand-relative deficit bounded by that particular adjacent-f32 spacing×demand, not included as fictitious physical water loss. Unmet demand from scarcity/conductance is not rounding loss.

For any future fixed multi-day gate require cumulative absolute root material error≤both summed arithmetic envelopes and2^-20×sum source-paid root doses, with all refusals/underdelivery logged. No signed cancellation. Phase/advection should first use their verified arithmetic envelopes; any additional practical whole-engine cap must be separately preregistered from the input/flux scale, not inherited from the local1e−9kg/m² laboratory threshold. The existing recorded phase totals alone are insufficient to certify per-operation envelopes.

## Decision implication

A common-unit soil/vapor model may simplify exact accounting, but the present mixed-unit residual no longer justifies invasive migration by itself. Preserve it as a failed exact gate, then assess a reviewed bounded-error implementation against the prospective criteria. Prioritize fixing the demonstrated huge legacy liquid transport loss and maintaining performance before broadening root physiology. Still no sustained terrestrial habitat benefit is demonstrated; refill and actual soil availability remain separate physical questions.

Reproduce normalization: `python3 web/tests/normalize-vapor-errors.py ../site-tmp/vapor-cycle-engine`. Reads only existing logs/binaries; no new simulation. Raw inputs retain5604b4b hashes.

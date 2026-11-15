# Independent cross-unit root receipt gate (prepared, not candidate acceptance)

Soil authority is f64 kg/m²; proposed vapor authority is f64 native units of10^9kg per patch. Compare original binary endpoint differences in a common unit:

`residual_kg = (vapor_after-vapor_before)*1e9 - (soil_before-soil_after)*area_m2`.

Use the actual engine's stored mean area, not a rederived nominal spherical area. The new offline Fraction oracle uses exact binary operands and exact integer1e9. It must not first round the source into native units and compare that rounded nominal debit with the receiver. Initial conversion is part of the audit, not free funding. Request/credit/signal checks are separate: actual source density debit funds aggregate credits; each credit fits demand; actual f32 h times exact demand fits credited water. Per-cohort values/bit patterns should be emitted for the two observed nonzero pulses and every later event, including zero-demand and refused events.

The tool reports exact signed and SUMABS physical residuals and exits2 on any nonzero residual. This is a strict diagnostic gate, not a newly selected practical engine tolerance. A nonzero result must be retained and reviewed; it neither proves a bug by itself nor permits deployment. No source topup, hidden compensation, hydration from a nominal request, or relative-global-mass excuse is allowed. Mixed-f32 column phase, all-neighbor vapor transport, and saves must separately preserve the same authoritative vapor; a correct root receiver alone is insufficient.

`audit-root-vapor-crossunit.py` is prepared before the proposed fullscheduler f64 implementation. It has not yet accepted any candidate trace. Existing pure cycle proof shows108 exact same-unit transfers in conditioned columns, not this density/native bridge, and retains deep-condensation and huge-receiver refusal negatives. No production/schema change.

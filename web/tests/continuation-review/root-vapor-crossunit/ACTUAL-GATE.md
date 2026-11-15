# Independent actual three-tick bridge gate

Reviewed generator `egl-vapor-cycle-prepare.py` (bf437bf lineage) and generated `site-tmp/vapor-cycle-engine/src`; read completed diagnostic/strict logs (six tick records each: untouched/action ×three).

Executed the prepared Fraction oracle directly on all four VAPOR_ROOT records. All source-debit, aggregate credit, per-demand credit and actual-f32-signal funding assertions passed. Conservation results:

| Mode/event | Paid density kg/m² | Exact cross-unit residual kg |
|---|---:|---:|
| Diagnostic1 |5.445914790658257e-5|−665710725/4398046511104 ≈−0.0001513650943252287|
| Diagnostic2 |1.3555754403427045e-6|−68935525/549755813888 ≈−0.00012539298950287048|
| Strict1 |0|0|
| Strict2 |0|0|

Diagnostic signed−0.0002767580838280992kg, SUMABS+0.0002767580838280992kg: **FAIL exact conservation**, even though source and receiver fund the physiological signal. Strict mode conserves by refusing both events, not by preserving effective hydration. Its second request differs after coupled trajectories diverge; do not call these identical later inputs. Fixed original two-pulse comparisons are logged separately by owner.

## Source audit

Current and next atmospheric vapor arrays truly become f64 native mass; advection uses separate f64 coefficients instead of f32 liquid scratch. Root throughflow and soil evaporation use the same bridge. No hidden sidecar or return escrow. Mixed standing evaporation/condensation uses equal-or-refuse actual endpoint transfers. Incoming/outgoing atmospheric summation remains ordinary floating arithmetic; local root exactness does not establish global closure. Owner separately audits raw stage binaries.

Strict bridge requires exact single-f64 source and receiver differences (TwoDiff low parts zero), then compares f128 area×density and native×integer1e9. For these f64 operands, products need at most106 significant bits, within f128's113; no permissive epsilon is used. This validates exact products after difference checks, not arbitrary all-world conservation.

Private save import deliberately reconstructs original f32 vapor before widening. Actual branch restores verify original liquid/vapor/soil equality. This is a legacy-input adapter, NOT a supported widened save/restart protocol. No schema or production approval. No additional heavy runs performed by this independent audit.

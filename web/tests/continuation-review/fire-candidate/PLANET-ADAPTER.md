# Experimental Planet ignition accounting adapter

**Not connected to the player UI or production update loop.** `src/experimental/planet_ignition.zig` wraps the isolated primitive against real `Planet` fields. `src/qa_fire_planet.zig` is a controlled real-Planet fixture; it assigns test fuel and organisms and is not a naturally evolved-world demonstration. The separate generated-world replay belongs to its own evidence.

## Units and global budget
Planet atmospheric gas fields store **average 10^9 kg per mesh point**. For `N` equal-area points of area `A`, total oxygen is `averageOxygenMass * 1e9 * N` kg. The adapter gives one action at most the selected patch's equal-share oxygen allocation: `averageOxygenMass * 1e9 / A * 12/32` kg carbon-equivalent/m². It does not give one patch the entire planet's inventory.

Actual burned carbon per area comes from representable f32 detritus removal. Burned kg = per-area amount × `A`. Atmospheric averages decrease/increase by actual O2/CO2 kg divided by `1e9*N`, not merely `1e9`. Each later action sees the updated finite global reservoir. O2/CO2 actual stored deltas must match intended transfer within an explicit operation-derived ULP budget, additionally capped at one part per million of the event, or the entire action refuses. Ideal mass, actual stored mass, signed residual and budget are all reported. See the numerical diagnosis below.

No global ecology recycled/fixed carbon counter is updated: this explicit experimental event receipt is its only accounting record. This avoids silently labeling combustion as ordinary respiration or counting it twice. A future production design must decide a persisted event counter if needed.

## Atomicity and read-only preview
Requires matching expected/selected indices, Origin mode, array lengths matching vertex count, positive finite radius/area/heat capacity, valid selected microbial cell, nonnegative finite gas inventory and water. Any positive selected water refuses. Only then is a local copy of detritus/reservoir passed to the primitive. All atmospheric and f32-temperature results are validated before assigning any Planet field. Preview performs the same calculation with no commit.

Only selected detritus, selected temperature and the two atmosphere fields may change. Cohorts, nutrient, lineage, RNG, reproduction credit, other cells, water and ecology statistics remain untouched. Selection/pause/time belong to the calling PlayState and are not accessible to this adapter.

## f32 thermal quantization
Planet temperature is f32, unlike the primitive's f64 reservoir. The receipt separately reports:
- `fuel_heat_joules`: actual removed carbon × gameplay heat calibration.
- `stored_heat_joules`: actual representable temperature change × real current patch heat capacity.
- `thermal_rounding_joules`: signed `fuel_heat - stored_heat`, an explicit numerical residual, **not a modeled physical heat loss**.

A zero/nonfinite stored increase, temperature exceeding500K, or residual greater than0.01% of fuel heat refuses atomically. The primitive already reduces burn to stay below the thermal ceiling; there is no silent temperature clamp. Very small fuel can correctly refuse because the current thermal field cannot represent its effect accurately. This is a visible integration caveat, not inventory absence.

## Executed tests
Pinned Zig0.13.0 lifecycle-build, ReleaseSafe. Seven adapter tests plus imported primitive/model tests pass:
1. Seven-cell real Planet: preview equals execution, exact preview state preservation, global carbon/O2/CO2 and thermal ledger, all other cell state and nutrient/statistics unchanged.
2. Oxygen-limited action uses no more than one equal-share allocation, leaves remaining fuel and positive global oxygen. This explicitly detects a missing-N conversion bug.
3. Wet, zeroO2, stale selection, subresolution fuel, ceiling, Sandbox mode, absent fuel, enormous CO2 precision refusal, negativeO2 and invalid selected index all leave snapshot unchanged.
4.100 sequential actions across seven cells cannot duplicate or overspend the finite global oxygen inventory; each step checks total carbon, oxygen and nutrient ledgers. Failed actions are exact no-ops.

First controlled burn:4,487,989,760kg carbon,11,967,972,693.333338kg O2,16,455,962,453.333313kg CO2,19.4345703125K stored increase. Fuel heat1.346396928e17J; stored heat1.346396085074002e17J; signed rounding8.4292599808e10J (about0.000063%). Global carbon error printed0. These huge masses reflect seven very large test patches on a100km-radius planet; this is not a measured real ecosystem.

Command:
`zig build --build-file web/tests/lifecycle-build.zig -Dsource=src/qa_fire_planet.zig --cache-dir <absolute-cache> --global-cache-dir <absolute-global-cache>`

Still absent: physical ignition threshold/chemistry, fuel moisture, fire spread/kinetics, burning live tissue, inherited fire protection, seeds or automatic reseeding. Current dry-water proxy and30MJ/kgC parameter remain simplified explicit gameplay assumptions. No new save schema or live deployment.


## Mesh-scale numerical diagnosis and bounded correction
The first generated40962-point attempt correctly refused under the original1e-8relative gas-transfer guard; no burn happened. `planet-scale-diagnostic.log` preserves a controlled exact-scale reproduction. radius5000km, area7,669,529,600m², real dry heat capacity2,959,748,131,454,976J/K, selected fuel.07642566412687302kgC/m², temperature295.4659423828125K, averageO2 26334.627192919306 andCO2 754.3573973337534.

Ideal O2 removal is1,563,063,715.2552285kg. Updating the stored mean then reconstructing the total gives1,563,063,734.7276206kg: signed rounding+19.472392082214355kg. The old guard allowed15.630637152552286kg, but half one representable ULP of the mean, scaled to the whole atmosphere, is74.50944394804537kg. The failure was normal floating-point representation, not insufficient fuel/O2 or a missing-N bug. CO2 residual is−1.1665024757385254kg. Thermal rounding was already within its separate0.01% bound.

Current gas bound explicitly covers rounded division by normalization, mean update, subtraction of represented means, and scaling back to total mass. It uses one full ULP per operation, a conservative allowance covering half-ULP rounding plus evaluation of the bound. If O2 subtraction rounding would spend more than the patch allocation, nextO2 is moved one representable value toward oldO2; this adds one mean-field ULP to the error budget. Actual O2 must still be no more than the original patch allocation, nonnegative and positive in amount. The budget is also capped at1ppm of the ideal transfer: a huge atmospheric ULP cannot justify erasing a tiny event. Zero represented gas or heat transfer refuses. These are numerical errors disclosed in the receipt, not physical sources/sinks or exactly conserved gas masses.

New tests:
5. Exact40962-point equivalent now succeeds, reports gas residuals explicitly, preserves live tissue, and satisfies both ULP and relative caps. Original failing evidence remains separate.
6.32/32 oxygen-limited cases at40962points succeed and verify actual consumption never exceeds equal-patch allocation; all receipts satisfy both bounds. Fourteen cases explicitly exercise directed rounding: their uncorrected rounded subtraction would overspend the allocation, and corrected actual removal is smaller. Existing tiny-fuel and huge-CO2 cases still refuse without mutation. Repeated finite global-budget test remains passing.

Current final log: `planet-ulp-tests.log`; `planet-tests.log` and `planet-scale-diagnostic.log` are historical pre-correction evidence. No gameplay wiring or release followed this numerical correction.


## Cumulative large-mesh audit
Corrected the probe's `carbon()` helper to use actual `p.vertices.len`, not the seven-cell fixture constant. It now sums cell carbon separately with compensation before adding the much larger atmospheric stock, avoiding avoidable summation loss.

Seventh test:40962points,1028sequential calls across257distinct initially fueled patches, **without resetting gas inventories**.257burns succeed; later fuel-exhausted calls are inert. Actual fuel removed492,767,276,800kgC. Summed actual O2 receipt1,314,046,062,318.984kg versus final represented stock delta1,314,046,062,318.9792kg; accumulated signed O2 rounding−9,147.687376kg. Summed actual CO2 receipt1,806,813,348,853.4905kg versus final stock delta1,806,813,348,853.484kg; accumulated signed CO2 rounding+586.817271kg. Small differences between summing many receipts and reconstructing one final delta are bounded using ULPs of the summed quantities, not hidden in a broad percentage.

The disclosed CO2 rounding predicts+160.041074kg global carbon; total-stock subtraction observes+158kg with8.250977kg ULP budget. This is **not exactly conserved carbon**: it is explicit bounded numerical residual. Nutrients and ecology counters remain exactly unchanged. Actual O2 allocation caps and nonnegative final inventory are checked throughout. Original before-correction logs remain historical evidence; final executed results are `planet-ulp-tests.log`.

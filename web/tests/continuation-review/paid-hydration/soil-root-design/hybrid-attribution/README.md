# Read-only hybrid precision attribution: no changed physics

Same258 cases and candidate c39e699; supplemental native emitter adds exact unchanged PhaseStep→f32 legacy result. Removing this one observation field reproduces ALL258 prior records exactly. No rates, budgets, flow semantics or cases omitted. Fraction analysis separately tracks source debits, receiver credits and physical source-limited requests; infiltration's capacity/rate request is also retained so source exhaustion is not mislabeled numerical underdelivery.

## Legacy versus added soil boundaries

High-standing actual-nine-world columns(162cases, initialdepth>.2m): unchanged legacy phase/cast max absolute signed one-step error3.1832542246137236e-5kg/m². Enabled whole-phase SUMABS max5.616112905635932e-5; newly introduced soil-transfer phases alone max2.432858681022209e-5. Enabled-minus-legacy SAME-INPUT one-step residual is recorded for every case. It is not a full-world cumulative attribution: soil exchange can alter subsequent vapor/condensation rounding.

Dry-controlled47cases: legacy max1.1657425138966271e-8; enabledSUMABSmax7.693329715944266e-9. Shallow-controlled49cases(initial0<depth<=.2m): legacymax4.196673050027858e-7; enabledSUMABSmax4.5418012557725876e-7. These dry/shallow controls use small vapor pools, so do NOT extrapolate their smaller errors to all future exposed high-vapor climates. No original maxima are replaced or hidden.

The previous1e-9 local-f64 guarantee CANNOT simply be inherited by this hybrid. It was never an approved whole-engine policy; this is not an unexpected violation of a chosen engine budget. No new budget is adopted here.

## Requested versus actual physical rates

High-standing infiltration credits99.3175–99.6995% of source-limited requested flow. Source-funded soil credit is conservative; no nominal water grant.

High-standing drainage removes essentially the requested soil water, but represented standing receiver gains76.3981–152.7962% of that request depending on timestep/quantum. This is a practical hydrological-rate issue, not only an absolute mass-total statistic. Full phase ratios/source-versus-receiver values are retained in summary.

In dry controls drainage receiver ratios~99.999998–100.002056%; shallow~99.999998–100.272508%. Exposed-soil evaporation receiver/request ratios~99.999643–100.000570% in dry controls,~100.000130–100.000375% in shallow depleted controls. Tiny deviations remain errors, not exact conservation. Root physiology is absent and no atmospheric saturation gate has been added to root demand.

## Receiver-first alternative: design-only upper bound

Offline compute largest representable receiver increment NOT exceeding the original request, using exact Fraction request/conversion and floor-to-f32. This is an optimistic RECEIVER-ONLY bound, not an implemented complete donor/receiver transfer or proof all donor constraints can fund it.

High-standing drainage could then deliver0–76.3981% of request;54/162 cases deliverzero, all at the shortest360s step. At720/1440s the quantum permits only76.3981%. It prevents rounded-up receiver mass but produces severe timestep-dependent underdelivery. More conservative checks cannot improve this optimistic bound. Simply switching to receiver-first does NOT solve the practical precision problem.

Dry receiver-first drainage bound99.997393–99.999998%; shallow97.885067–99.999998%. Exposed-soil evaporation bounds~99.997192–99.999643%. These more favorable small-pool cases do not justify dropping high-standing cases or silently selecting habitat-dependent numerical policies.

Next architecture decision needs an explicit practical coupled budget and comparison of coherent alternatives, not another special phase patch. No broadf64 migration, accumulator, compensating sidecar, rates change or production release is authorized by this analysis. All native values/requests and code hashes retained for independent review.

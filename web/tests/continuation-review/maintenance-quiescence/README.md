# Common energy-budget hypothesis: isolated physiology, not shipped ecology

`experimental/maintenance_quiescence.zig` adds an explicitly **uncalibrated gameplay hypothesis** around the real microbial core. Production and the prior null adapter are unchanged. `qa_maintenance_quiescence.zig` passes37tests including imported core tests. No saves, inherited propensity, offspring, spread or competition in this experiment.

## Hypothesis and bookkeeping
Positive basal active/rest rates produce analytic tissue-carbon maintenance demand. One shared finite O2 allowance is allocated proportionally to both demands. Actual represented biomass debit becomes CO2 and releases its bound nutrient once; no paid carbon is fabricated. Resting photosynthesis remains disabled. Entry/wake uses existing experimental10% carbon conversion cost, requiring finite O2. Every timestep still incurs unchanged actualcore baseline thermal/dry mortality. No ignition hook, immunity or fire bonus.

Unfunded O2 fraction produces the SAME fractional stress hazard in both pools, maximal at zeroO2. Assumed maximum0.5/day is phenomenological, not calibrated ATP biology. Death becomes detritus with nutrient release, not unsupported respiration. New fixation O2 only helps subsequent maintenance. Stable uptake penalty already in core is retained as acquisition efficiency cost; whether it partly represents maintenance remains an integration ambiguity, not settled physiology.

Rounding: debit remainder rounds up to avoid overspending. Oxygen-allocation deficit, not sub-ULP tissue shortfall, drives stress. Unrespired rounding stays as living tissue and is explicitly logged (maximum accumulated4.7121e-5kgC/m² in54runs). Therefore this is numerical approximation, not exactly delivered theoretical metabolism. ZeroO2 still gives full stress, never free immortality.

The first run exposed the null adapter's upward f64-to-f32 capacity cast, allowing tiny O2 overspend(-6.75e-14). Initial failure and diagnostic logs retained. This new adapter alone uses directed-down capacity casts for BOTH O2 and CO2 at each actualcore call; prior adapter and production untouched. No biology parameter/tolerance was changed to fix it.

## Matrix
54runs: active rates0.05/0.2/0.6perday × resting ratios1/0.5/0.25 × stablelight/alternatingdark/resource-limited-dark × active-only/rest-pool strategy.20days,1440s steps. Paired initial0.2living,0.1free nutrient,10gasunits each; limited case0.005nutrient/0.05CO2/0.01O2. Dark windows days2–4,6–8,10–12,14–16,18–20. SAME prescribed transfer windows in stable controls, avoiding environmental prophecy. Half active mass enters rest at window start; whole remaining rest attempts paid wake at end. Failed wake is not free. No refill.

Additional9slow-active runs couple activity fraction0.25/0.5/1 to BOTH actual acquisition potential and basal demand(base0.2/day). No resting pool. This tests Todd's slow-growing/lower-real-resource-demand preference without independent free maintenance reduction. No reproduction tested, so no spread claim.

## Quantitative findings
At base0.2/day andrest ratio0.5, day20:
- Stable: active-only0.91670living vs rest0.88340 (rest costs growth).
- Alternatingdark:0.56514 vs0.59315.
- Limiteddark:0.08935 vs0.12657.
At base0.05/day, resting loses all three environments, even at ratio0.25. Thus not automatic advantage. Cumulative respiration lower in resting runs; full mass, respiration, stress, conversion and resource values in results.json. Per-mass demand reductions are model assumptions, not inferred natural adaptations.

Slow-active fraction0.5 vsfast1:
- Day2stable:0.69628 vs0.89659living; maintenance0.08891 vs0.25575.
- Day20stable:0.90074 vs0.91670.
- Day20alternatingdark:0.66106 vs0.56514.
- Day20limiteddark:0.14169 vs0.08935. Fast accumulates0.10494stressdeath when O2 depletes; slow0 under this chosen hazard model.

These are separate finite-resource populations, NOT competition, selection, invasion fitness or evolved persistence. Sampling day20 ends in darkness; complete cycles and recovery trajectories matter. No winner inferred from isolated survival.

## Validation/limits
NoO2dark test keeps O2zero and both pools eventually die, never reactivating after extinction. Rest cannot fix carbon. Equal-demand slot swaps preserve maintenance/stress allocation exactly. Invalid parameters refuse atomically. Same maximal fractional hazard with zeroO2. Full carbon/nutrient ledgers checked each step at1e-4/1e-5 absolute tolerances; observed snapshot maxima4.8316e-5/4.7088e-6. Not arbitrary-duration exact closure. Core cutoff still independently eliminates small active/rest compartments; not a spore bank.

Next: actual common-resource2-cohort assay, not bolting isolated runs together. Need shared C/N/O2, original light/space competition, per-lineage acquisition and demand, slot swaps, crowded/empty settings and parameter sensitivity. A copied/instrumented core is necessary because null sidecar only permits one lineage. Full scheduler later must fund inheritance, reproduction, movement and predation and version saves. Existing inherited light-efficiency trait is NOT silently equivalent to metabolic pace; redefining it needs separate semantic and cost tests.

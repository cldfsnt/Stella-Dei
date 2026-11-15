# Coarse beta cost attribution: column phase is the measured suspect

One fixed sequence from2862a34, unchanged frozen beta law. Actual Node WASM full scheduler, same candidate binary supports off/on. Plain and traced artifacts each preserve exact full endpoint bytes/RNG versus prior uninstrumented hashes for off/on after72ticks. Twelve warmup ticks,60measured. No per-cell clock/import, model edit or second timing attempt.

## Results (milliseconds per tick, traced medians)

| Phase | Off | Enabled |
|---|---:|---:|
| Thermal |2.261|2.097|
| Liquid/wind |3.184|3.055|
| Atmospheric wind/edge preparation |2.258|2.766|
| **Column** |**2.268**|**15.942**|
| Coefficient |1.083|0.950|
| Gather |2.005|2.158|
| Ecology |0.910|0.864|

Column encompasses environment calculation, standing evaporation, shared finite soil/root withdrawal, condensation and infiltration. It is57.2% of enabled traced runtime, compared with16.2% off. The other measured phases do not exhibit a comparably large increment. These data identify a useful coarse target, not the cost of any individual helper.

## Instrumentation caution

Plain off13.456ms versus traced13.982 (+3.91%); plain enabled33.280 versus traced27.849 (−16.32%). Off passes the predeclared positive5% intrusion check, but the large enabled negative difference is still a material code-generation/noise warning. **Do not call it a speedup or present traced stages as an exact decomposition of uninstrumented runtime.** Stage timer sums differ from traced totals by about0.014/0.017ms per tick; that small accounting gap does not remove the cross-artifact warning. No repeats selected to improve this result.

Enabled/off use identical projectable starting fields but different authoritative soil/vapor inventories and trajectories. This is numerical implementation attribution, not an ecological benefit comparison. Startup/restore, JSON/save serialization and rendering are outside the timed window and cannot explain the measured scheduler overhead. No mobile/browser/rAF claim.

## Source-backed next question, not an implemented optimization

Legacy computes `PhaseStep.init(dt)` once before its column loop. Beta `capillary_bucket.step` computes it per call at source level; that initializer contains three relaxation exponentials. Whether WASM compiler hoists these is not yet established. Strict finite/receipt checks, mixed-representation exchange, canonical shared allocation and infiltration also occupy the column. Inspected column/bridge/shared implementations contain no runtime f128. Bridge exits immediately when source debit is zero.

Next justified work, if separately authorized: inspect generated WASM/IR or a bounded same-input column microprofile to distinguish repeated timestep-constant setup from receipt/soil work. No blind second empty-cell optimization, no skipped abiotic cells, rates or physical law changes. Original +85% enabled screen and rejected empty-env optimization remain preserved.

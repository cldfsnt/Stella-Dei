# Liquid order witness: isolated one-pass evidence

Three tests pass on each frozen day30/60/90 world. Native scalar f32 copy of current block semantics, not the actual SIMD method execution. Directions correctly remap exported FL,BL,L,FR,BR,R to sendWater FL,FR,BL,BR,L,R. Actual topology40962 nodes has zero duplicate nonself/zero nonreciprocal edges and12selfslots. Preserve graph provenance; no world edited.

Current16-lane forward/reverse block traversal differs at20188/22719/23858 cells. Forward total deltas are−33923.745/−37895.140/−39582.317 native billion-kg units (plain f64 totals; independent exact ledger is more precise). Four-lane paths also differ, and final2cells never donate. Toy same-lane and tail donors remain unchanged under legacy pass. These are deterministic order/lane omissions without needing a data race; true concurrent scatter adds a separate possible race not demonstrated here.

Immutable same-f32-head/flow source budgets plus destination gather covers all nodes, preserves downhill rate/share cap, skips self/deduplicates repeated slots, and yields exact forward/reverse source-processing equality. Endpoint total signed deltas day30/60/90:−3338.324/−2900.409/−2823.029. One finalf32 store per node still has SUMABS rounding29879.083/31253.460/31554.243. **Not exact conservation**; no global renormalization. Reciprocal topology is required, not inferred for arbitrary graphs.

Separate promoted-f64-absolute-head experiment gives signed−32.352/−34.789/−31.323 but SUMABS35073.640/35412.074/35466.335. Smaller signed cancellation does not mean lower absolute rounding. It changes head precision and must not be credited to ownership/gather alone. Earlier single-day promoted-head and pre-conversion-expression outputs preserved. Exact current getKmPerWaterMass expression rerun produces unchanged day60 results.

No scheduler, multiworker, save, ecology, performance or device claim. This checkpoint precedes authorized full-scheduler same-head integration. Independent fire ledger e04f5ce corroborates order counts and decomposes actual rounding exactly. Source scratch candidate uses6f64/patch and fixed neighbor gather, no per-edge invented corrections; performance unmeasured.

Input generator and executable are web/tests/liquid-transport-input.py and src/qa_liquid_transport_order.zig. Set QA_LIQUID_INPUT to generated JSON then Zig0.13.0 test -O ReleaseSafe. All three sourceworlds and graph remain frozen. Input initial hashes in inputs.json; further inputworld provenance is already preserved by root-input-preflight.

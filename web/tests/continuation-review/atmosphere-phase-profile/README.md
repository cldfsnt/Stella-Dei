# Atmospheric subphase profile

Isolated copied source, no production algorithm changes. Same representative actual30-day world and native mobile-policy60-tick24h/sec workload as physics-phase-profile. Exit0, exact save restored; output saved-world SHA256 a2a5befefe0e2c4b205416f63d1ecf6902cb0f3d87a12416987ac306194d544f exactly matches preceding phase-only instrumentation.

Atmosphere324.0232ms across60ticks: wind-cache42.7931ms(13.2%), edge-cache79.4363ms(24.5%), phase including saturation-pressure computation109.5766ms(33.8%), donor coefficients43.1088ms(13.3%), gather49.0980ms(15.2%). Atmospheric subphase totals323.0128ms; remaining~1ms includes swap/timers/loop-boundary overhead. Counters wrap actual copied functions, no substitute simulation.

Phase+saturation is largest, so test per-tick cached evaporation/condensation/rain-memory coefficients first. Gather is not dominant; reverse-slot cache or outgoing-sum additions cache should wait. This isolates stage cost, not all cost attributable to repeated relaxation: saturation computation remains per-cell and legitimately varies.

Whole-run physics had a119ms outlier and organisms total187ms versus prior95ms. Do not call that a regression from this single native software-renderer run. Real browser/device performance remains unmeasured. Existing native shutdown leak reported. New preparer composes previous phase preparer; source unchanged outside isolated copy.

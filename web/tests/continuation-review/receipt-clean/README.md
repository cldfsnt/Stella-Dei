# Clean performance and microbial regression gate

Recommendation: **promote the narrow arithmetic candidate to normal integrated release checks**, not as an exact-conservation or speed fix. No reproducible meaningful coupled-physics slowdown was observed. Production and Site were not changed by this experiment.

Candidate remains frozen realized-receipt SHA `9efae4e34a4588413fe59bd2395a19fdcc795a994980bea89e451f5b917898e3`. It only changes represented-loss/growth receipts and directed-down support/credit additions. No new field, schema, trait, global resource topup, persistent cache or per-cell allocation. All **32 existing production microbial tests pass on both unchanged baseline and copied candidate**, including inherited movement/grazing/reproduction, resource accounting, submergence and rare-mutation tests. Candidate default is explicitly true while testing; tests do not accidentally exercise baseline.

## Timings

Actual coupled Planet.simulate + gameTime advancement, 300 ticks per arm, dt1440 seconds, following30 identical restored-world warmup ticks. Six-arm order baseline/candidate/candidate/baseline/baseline/candidate gives three neighboring reversed-order pairs. Each arm restores the exact input save. The entire timed block contains no shadow physiology, telemetry, serialization, validation, render, or UI. Validation and exact restore checks occur outside timing. Compilers and other workers were idle during measured execution. Native EGL cloud CPU, **not browser, phone, laptop or FPS**.

| Real input | Baseline median ms/tick | Candidate | Median change | Three paired changes |
|---|---:|---:|---:|---|
| Early two-colony world |8.614|8.822|+2.42%|+11.36%, -2.37%, -1.64%|
| Early repeat |8.064|7.883|-2.25%|-2.25%, -1.59%, -8.02%|
| Natural day30 |8.104|7.962|-1.76%|-2.68%, -1.54%, -1.76%|
| Natural day60 |8.383|8.403|+0.24%|-1.60%, -2.14%, +0.91%|

The early repeat was explicitly run because the initial first pair was an outlier; neither run is discarded. Variability precludes claiming a speed improvement. No consistent meaningful regression appears, including the most established world. Full-frame/render performance is not measured here. Input hashes and actual initial simulation clocks are in runs.json. Early-repeat uses the same early input/hash.

## Remaining limits

Prior actual-engine evidence establishes only bounded average residual reduction. Known exact tiny-N funding failure remains. Per-step maxima and signed endpoint residuals can worsen; no uniform/worst-case or strict conservation claim. Full trajectories can diverge from rounding changes. Exact save/load and repeated restored-state continuation passed in the prior gate, but uninterrupted-vs-restored equivalence was not tested. Separate WASM arithmetic evidence exists, not an actual browser coupled-world benchmark. Normal integrated source/build/save/runtime checks remain the release owner's responsibility.

## Reproduction

Use `web/tests/egl-receipt-clean-prepare.py <copied-source-dir>`; it invokes the frozen engine preparer then removes all shadow calls from step. Build the copied main with `web/tests/egl-origin-build.zig` using Zig0.13 ReleaseSafe. Run this directory's run.py with STELLA_WORKSPACE set and copied binary at site-tmp/receipt-clean/build/bin/stella-egl. Run `zig test <copied-source>/simulation/microbes.zig -O ReleaseSafe` and baseline src/simulation/microbes.zig. No source changes during these measurements.

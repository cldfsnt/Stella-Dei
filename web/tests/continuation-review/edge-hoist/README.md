# Per-source atmospheric edge validation hoist (isolated research)

No production changes. Current v53 copies preserve f64 displacement, length-squared, dot-product and division order, as well as original wind construction and f32 scratch components. Per-source point/wind load and finite validation move outside the 5/6 actual-neighbor loop. Destination validation and final length/dot validity remain per edge. No static geometry cache, approximation, allocation or donor-remainder change. Allocation-failure fallback outside the edge scratch rebuild is untouched.

## Preliminary compiler/microprofile gate

Optimized Zig0.13 ReleaseSafe LLVM IR from a standalone loop matching the source/wind/neighbor shape retains source loads, conversions, and finite checks inside the inner neighbor loop. This is standalone IR, NOT proof that the complete Planet compiler emitted identical code. The actual whole-engine gate is necessary.

Synthetic40962-point, six-neighbor microprofile:245772 edge outputs bit-identical; repeated special-input checks include NaN, infinities and signedzero. Six alternating pairs,50 passes each: baseline median67.366ms versus hoisted37.295ms. This is a bounded synthetic microprofile, NOT real-world frame or device performance. Frozen reference/probe/IR/logs retained.

## Whole-engine method

Actual production engine copied with only edge-rebuild branch changed and a QA baseline/candidate selector. Real early two-colony, naturalday30 andday60 saves. Same input restored each arm,30 untimed coupled1440-second steps then300 timed coupled steps. Arm order0/1/1/0/0/1. Each endpoint serialized save must match the first baseline exactly, including biology/RNG. Original save restored exactly at end. Timed block excludes serialization, shadow computation, UI and rendering. This measures native coupled simulation, not full-frame/browser/laptop performance. All compilers/other heavy runs coordinated away from timed execution.

Two QA setup build failures (unused import, then discard-before-declaration) were corrected and retained; they did not execute inventory or model tests. Actual comparison results follow in summary.json once run.

## Whole-engine result

All18 arm endpoints passed byte-for-byte complete serialized state equality against their first baseline, including model/RNG fields; original input restored. Three paired medians:

| Input | Baseline ms/tick | Hoisted | Median change | Paired changes |
|---|---:|---:|---:|---|
| Early |7.776|7.605|-2.2%|-1.44%, -5.03%, -0.54%|
| Natural30 |7.928|7.552|-4.7%|-2.63%, -5.54%, -4.71%|
| Natural60 |8.222|7.552|-8.2%|-10.60%, -8.80%, +2.76%|

Eight of nine pairs improve; one established-world pair regresses2.76% and is retained. This modest low-memory candidate is more promising than the rejected large caches, but not a guaranteed device speedup. No image/render change, screenshot parity test, full-frame measurement or actual browser/WASM whole-world execution is claimed here.

Recommendation: proceed to independent code review and targeted WASM exactness/integrated source gates, not direct deployment. The implementation is currently a copied-source experiment only. A production design should centralize the validated-source helper in atmosphere_water rather than duplicate edge arithmetic in Planet; revalidate exact outputs after that refactor. Guarded fallback behavior must remain unchanged.

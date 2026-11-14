# Nearest-point performance review (no production edits)

## Baseline and scope
`qa_nearest_benchmark.zig` calls the actual Planet.getNearestPointTo against40962 synthetic radial terrain points and200 varying queries, five passes, native Zig0.13 ReleaseSafe. Synthetic data is not a captured game mesh; measurements are microbenchmarks, NOT native frame timings or Android/WebAssembly results. Checksums consume every result. Cache/CPU warmup and fixed measurement order affect timings; no statistically robust game-speed claim.

Observed microseconds/query:
- actual original sqrt-every-point:71.087,60.928,60.880,59.930,57.791 (median60.880)
- naive squared:48.638,48.573,48.465,38.200,38.438 (median48.465)
- guarded exact-tie candidate:43.672,43.489,43.585,33.218,32.755 (median43.489)

Guarded candidate is about29% cheaper by medians here, saving about17µs/query. It is still **O(N)** and not an explanation/proof of faster simulation hours per second. With one camera query per frame, this saving alone is small. Larger rabbit populations multiply the cost.

## Semantic trap and bounded recommendation
Original f32 sqrt rounds: points(1,.0003,0),(1,0,0) queried at zero have different squared distances but equal represented distances. Original first-wins chooses0; naive squared chooses1. Test demonstrates this exactly.200 broad finite queries match all variants, but that does not invalidate the edge case.

Candidate keeps best accepted squared distance AND best original sqrt distance. Only if squared distance is smaller does it calculate sqrt and apply original strict-less comparison. This preserves first-wins rounded-distance ties for finite valid meshes, retains original summation with Vec3.dot, and skips most square roots. Equal, NaN and infinity handling must be explicitly considered before integration: current production method returns undefined for empty/all-nonfinite sets, so do not claim it supports those inputs or silently redefine that contract. Input validation improvement is separate.

Recommended first bounded change: use guarded candidate in Planet.getNearestPointTo and have mouseMoved call that one method instead of duplicating it. Validate real generated mesh, camera/picking boundaries, duplicate points, near sqrt ties, terrain update, saves and actual WASM player behavior. Integrator should retain original reference test. No production change made by this review.

## Calls and meaningful limits
- PlayState update executes one camera nearest query each update in either camera mode, even when stationary.
- mouseMoved fallback performs full scan after colony/seed glyph picking and ray hit; source calls distance again for winning candidates (compiler may common-subexpression eliminate; don't assume double full cost).
- zoom handling and Find-life camera positioning have occasional nearest calls.
- Every original rabbit invokes nearest in aiStep per eligible simulation tick; selected rabbit habitat inspector also calls it. Origin does not have rabbit population cost. Native full frame profiling still required to locate actual fast-forward bottleneck.

## Why defer index/cache until validity is explicit
transformedPoints is written at construction and recomputed in mesh upload from elevation, axial tilt and radius. Terrain height exaggeration matters to Euclidean nearest; angular-nearest or local-neighbor hill climbing is not equivalent and can miss the true closest point. A cache keyed only by query position becomes stale after geometry changes. A KD/BVH must rebuild/refit on geometry generation and preserve lowest-index rounded-sqrt tie semantics, including pruning tolerance. Average O(log N) queries are possible, not guaranteed O(1), and rebuilding O(N log N) may erase gains if done frequently.

A camera-only exact-result cache keyed by query bits plus an explicit geometry revision may save more stationary scans, but needs trustworthy revision updates on all geometry paths and should be independently measured. Do not add an index merely because a TODO mentions BSP.

## Evidence
`run.log` BUILD_EXIT=0. `SHA256SUMS` captures benchmark/nearest source/vector operations. No production edits, deployment or browser performance claim.

# Atmospheric basis / reverse-index experiment (not shipped)

## Decision
Keep this candidate experimental. The large-world native trial preserves the tested state exactly, but its overall speed benefit is small and noisy compared with its extra memory. It is NOT part of the v43 sparse-index release and was never deployed.

## Candidate
The final candidate caches only the original tangent right/up basis and six reverse-neighbor index hints. Keys contain three explicit f32 coordinate components; comparisons use their u32 bit patterns, **never undefined Vec3 SIMD padding**. Cached basis components are packed f32 arrays and reconstructed into the original Vec3 operations. No precision reduction or edge-rate formula change occurs. Each reverse hint is checked against the current topology endpoint before use; a stale hint falls back to the original search. Geometry changes cause basis regeneration. Allocation failure falls back to the original path by inspection; forced-OOM integration testing was not performed.

Payload is 42 bytes per point: 12-byte xyz key, 24-byte basis, 6-byte hints. This is 1,720,404 bytes at 40,962 points or 6,881,364 bytes at 163,842 points, excluding allocator metadata. No save/schema, climate, organism or rendering-quality change.

## Correctness actually executed
- Native unit: 1,200 dynamic wind vectors / 3,600 f32 component-bit comparisons match the original vector operations, including poles and changed coordinates. Topology changes exercise validated-hint fallback.
- The actual naturally evolved 30-day, 163,842-point Origin save has 7 occupied patches / 12 cohorts. Both arms run the same full scheduler, fixed 1/60 input delta, 12 warmup frames and 60 measured 1,440-second ticks, then serialize the entire world.
- All five full-world hashes match: after measured ticks; after actual Raise Terrain plus three ticks; after axial-tilt change plus three ticks; after the fine-water API plus three ticks; and after restoring the original save plus three ticks. See `WORLD-SHA256SUMS` and `final-parity.log`.
- Terrain proof explicitly asserts the real pointer-on-planet precondition, successful tool invocation, and increased selected elevation. The represented elevation increased by 0.14990234375 km. The tilt field changes by 0.17 before the normal renderer refreshes transformed geometry. Water invokes the actual +0.1 m API; this fixture does not separately log its returned receipt.
- Simulation solar rotation continues through the ordinary changing game time and solar vector. The load and terrain cases refresh the same geometry used by baseline physics, rather than inventing an alternative geometry model.

These are native EGL / cooperative-loop tests, not browser or Android gameplay verification. No new topology generation, forced OOM, dense biosphere, or integrated-v43 performance test was run for this candidate. A WASM-specific parity gate would still be needed before shipping.

## Three alternating loaded-save pairs
No known worker compiler or heavy test overlapped this final window. Shared-host variability still produced 100+ ms outliers. The engine copies are frozen **before** the sparse-index optimization, so gains cannot be added to v43 percentages.

|Pair|Baseline update ms|Candidate update ms|Baseline full frame ms|Candidate full frame ms|
|---|---:|---:|---:|---:|
|1|44.9928|40.6494|59.7590|56.5665|
|2|45.8863|43.9348|61.9420|59.2005|
|3|44.9380|45.1394|59.5325|59.7977|

Median update decreases from 44.9928 to 43.9348 ms (2.35%); median full frame decreases from 59.7590 to 59.2005 ms (0.93%). Pair 3 is slightly slower with the cache. Do not claim a robust general improvement or a laptop/browser speed guarantee. Stage timings show repeatable basis-work savings, but unrelated phase variation/cache effects obscure total benefit.

Process peak RSS for the first pair, including extra invalidation JSON capture: baseline 562,396 KiB, candidate 568,652 KiB (+6,256 KiB). Subsequent pairs: 508,600 versus 515,740 / 515,568 KiB. Absolute RSS includes the native software renderer, loaded/generated world and large JSON assay buffers; it is NOT the game's browser memory footprint. All six processes exit 0. The existing native allocator shutdown leak remains reported.

## Superseded experiments / failures
The initial full directed-edge geometry cache used about 51 MB at the large grid and did not show a worthwhile edge-stage advantage. Its raw Vec3 byte guard was also invalid because SIMD padding is undefined. Its preliminary matching hashes and timings are diagnostic only, not release proof. That design is not recommended.

The first loaded-save invalidation fixture omitted pointerOnPlanet before Raise Terrain, so the tool correctly refused. Its terrain hash equalled the restored-world hash. That test was not accepted as terrain proof. The final fixture asserts successful real intervention and produces a distinct terrain hash. An attempted `/usr/bin/time` invocation failed before running the game because that binary is absent; final RSS is collected using Python `os.wait4`, not inferred.

## Reproduction
Use a pre-sparse-index production tree (the baseline evidence checkpoint is `48bb45c`) plus these isolated preparers:
1. `egl-cpu-resolution-prepare.py A` creates the current-source baseline fixture. Build/run it at STELLA_CPU_LEVEL=7 to create the actual 30-day save, using the flags in the CPU-resolution report.
2. `egl-cpu-geometry-prepare.py A G`, then `egl-cpu-basis-prepare.py G B`. G is an intermediate experimental source tree only; do not ship it.
3. `egl-cpu-replay-prepare.py A RA` and `egl-cpu-replay-prepare.py B RB`.
4. Build RA/main.zig and RB/main.zig with `egl-propagule-visual-build.zig`, Zig 0.13 ReleaseSafe, and absolute prefix/cache paths.
5. Run with the original nursery flags plus STELLA_CPU_LEVEL=7 and STELLA_CPU_LOAD pointing at the actual save. For the proof pair, set STELLA_CPU_INVALIDATE=1 and distinct STELLA_CPU_RESULT_PREFIX values. Repeat alternating arms three times; do not run competing heavy work.

Logs are losslessly gzip-compressed after workspace-path sanitization. Source hashes pin the actual copied fixtures and preparers. Large generated JSON fixtures remain local; their exact hashes are archived. No production change, commit of production code, push or deployment was made by this experiment.

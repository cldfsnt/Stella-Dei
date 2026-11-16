# Proposed balanced same-module assay — awaiting coordinator approval

Status: design only. No implementation/build/measurement authorized by this document. Existing accepted seed1337 +10.25% and coarse diagnostic remain unchanged. This protocol tests robustness to order/compilation/run variation; it does not presume that variation explains the regression.

## Fixed inputs and binary

Use only actual seed1337 Pioneer day7 input ca9c2d4cb9a4c5f02bb3d8cc6a01dfc172fee38f6a40d26d949a8383754e9b78 and its previously frozen wind-off projection936f4e37ab8b095c71a6e8ec1dab0ba6f75be541ae66d5e40fdc4fb6eaef2796. A=off, B=enabled. Identical current candidate profile.wasm bytes/hash from root-wind-established-cost/binary.json, no stage clocks, no engine source change. Preserve authoritative root/soil/vapor. Projection removes aerial/config and is deliberately not biologically identical. Initial123living/114occupied; no initial positive roots.

## Why not repeatedly call qa_run in one instance?

The existing accepted adapter allocates parsed saves, graph, Planet arrays, arena, and output through process-lifetime c_allocator and does not destroy them. Repeated qa_run would retain multiple worlds and contaminate memory. Do not silently add allocator replacement or improvise partial cleanup inside timing.

Use two separate Node processes. Each compiles the exact WASM bytes ONCE into a WebAssembly.Module, then explicitly supplies that SAME module to a fresh Emscripten instance for every block. Fresh linear memory and instance globals are a complete reset; saved state/graph are restored by the unchanged accepted adapter. JS glue must actually honor the supplied module, not compile the bytes again. Verify by counting compile/instantiate calls and retaining module identity. Compilation is outside timing. This reuses compiled code within each process; it does NOT prove V8 tiering has stabilized.

A small JS loader invokes unchanged C main with the original filenames/72ticks and captures its timer/output. No engine modifications. If actual glue cannot accept repeated instances safely, stop and report the harness limitation rather than silently substituting another assay.

## Fixed sequence and quantity

Process1: untimed warm instances A B B A, then measured instances A B B A.
Process2: untimed warm instances B A A B, then measured instances B A A B.

Every instance runs72ticks of1440seconds from its original frozen input. Its first12ticks remain untimed, final60 use the original simulation-only timer. Each branch therefore receives144warm ticks per process before the measured sequence, without extending any scenario horizon. ALL16 warm/measured endpoints must equal their corresponding EXISTING accepted72tick complete-save SHA (including RNG). Warm outputs are discarded only after hash verification; each measured block is a fresh restore, never the endpoint of a warm block. Before accepted measurement, each arm additionally gets a zero-tick typed-state/topology check through the same shared-module loader. Any mismatch invalidates the whole assay; no selective samples.

Eight measured blocks total, four samples perarm. Do not repeat if unfavorable. No extra seed, parameter, tier flag, stage instrumentation, or chosen warmup extension after seeing results.

## Memory, GC, restoration

Inputs/graph can be read once as immutable Node buffers; no parsed JS world mutation. Full parse/restoration/serialization/hash and instance creation occur OUTSIDE the timer. Each instance's C main owns its temporary world and output. After verifying its output, drop all instance/Module/typed-array references except the shared COMPILED module and frozen input buffers.

Run Node with --expose-gc solely to request GC at EVERY inter-instance boundary, outside measured simulation, before creating the next instance. Apply identically to warm and measured blocks; record GC duration, process.memoryUsage (RSS/heapUsed/external/arrayBuffers), and WASM memory capacity before/after each block. This is a controlled assay, not an estimate of ordinary browser GC behavior. Do not force V8 optimization/tier settings. RSS may retain allocator pages despite collection; report high-water and trend, do not call it a leak or hide it.

Abort rather than continue if a discarded instance is still strongly referenced, WASM instance count grows, or live external/array-buffer memory increases by at least another full128MiB perblock after collection on two consecutive boundaries. Predeclared safety stop at1GiB RSS. Retain aborted data; no automatic retry with a higher threshold. Actual memory collection cannot be inferred solely from RSS returning to baseline. A lack of stable memory makes performance interpretation inconclusive.

## Scope/time/interpretation

Reserve exclusive CPU/IO after coordinator release. Sixteen72tick blocks plus two zero gates:1152simulatedticks, expected roughly1–2minutes. Hard wall limit180seconds perprocess, total6minutes (compilation/preflight excluded and separately bounded). Stop on limit/error, preserve all output. No automatic retry unless coordinator identifies a specific harness failure before accepting measurements.

Report all eight samples in order, perprocess A/B medians and ranges, pooled medians, and four adjacent opposite-arm pair ratios: P1(A1,B1),(B2,A2), P2(B1,A1),(A2,B2), expressed enabled/off. Report geometric mean of all four ratios and whether order/direction agree; no outlier exclusions or significance claims with this sample size. Record Node/V8 versions, binary/glue hashes, compile count, input/restored/output hashes, memory and GC diagnostics. Timer continues to exclude restore/save/GC and is not FPS, browser, or laptop responsiveness.

The earlier historical off-path exact proof stays relevant but this assay does not re-test classic compatibility. If enabled overhead remains consistently positive across balanced pairs, report sustained cost honestly for coordinator acceptance/deferral. If inconsistent, report unresolved effect; do not declare zero overhead, a speedup, or that previous stage results proved noise. No optimization or release decision is automatic.

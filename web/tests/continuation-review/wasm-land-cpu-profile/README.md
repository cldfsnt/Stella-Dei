# One unchanged-code V8 CPU sample

Node24.22.1 `--cpu-prof --cpu-prof-interval=1000`, one72tick empty-beta process. No tiering changes, internal clocks, benchmark repeats or source edits. Same archived Zig library and C wrapper linked with `--profiling-funcs --emit-symbol-map`. Verified **all10 non-custom WASM sections byte-identical** to original frozen candidate; only a function-name custom section was added. Complete endpoint equals prior hash177388476e42306cadfbe9694bf5cbca003ef8738a2e1765ce667fefa1d1b699.

## What the sample establishes

2,675 whole-process samples, including startup, parse, all72ticks (including warmup), save validation and serialization. This is not the previous60tick timing window or an exact time allocation.

Stack-classified samples:
-1,599 main/inlined or unresolved;
-541 named simulation stacks;
-186 serialization;
-167 JSON parsing;
-33 save validation;
-149 outside WASM main (startup/runtime/GC/etc., not uniformly idle).

Large individual stack entries: main891, direct-main memcpy310, expm1 helper186, thermal/liquid job wrappers270, edge rebuild88, atmosphericWind46, mixed liquid/vapor exchange38. These are sampled occurrences, not exact per-phase milliseconds. Direct-main memcpy can include restore/state-copy work and cannot be safely assigned entirely to simulation.

## Important limitation and actionable conclusion

The retained Zig archive names shared_soil.step, vapor_bridge.step and PhaseStep.init, but the final linker optimizer inlines these into main. Final symbol map confirms their absence as standalone functions. Named nextAfter/lower/upper functions remain, yet lack enough samples to rank; inlined copies are invisible. Consequently this profile **cannot establish whether directed rounding, validation, copied result structures, or coefficient setup dominates the column**. Absence of a named sample does not establish zero cost.

Expm1 is visible, but its186 samples do not identify which call site (relaxation or exposed substrate law). The already-tested identical coefficient hoist produced no benefit; this profile does not justify revisiting it or deleting physical/receipt checks. The earlier coarse column finding remains the best supported target. No additional actionable helper optimization is established by this one sample.

More granular attribution would require instruction-address sampling with usable inline debug information, or a separately reviewed function-boundary build that could alter optimization. Neither was attempted. Do not promote another blind fast path. Raw cpuprofile, final symbol map, exact executable identity and endpoint proof are retained.

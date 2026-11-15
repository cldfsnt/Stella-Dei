# Optimized arithmetic/work inspection before next prototype

No model change or new speed result. Zig0.13.0 ReleaseSafe build-obj of src/qa_liquid_ir.zig exports a runtime pointers/length wrapper around the exact cached helper, avoiding constant-fixture specialization. Full emitted LLVM is retained locally; hash/excerpts preserved here.

The validation pass evaluates mass×km+elevation, source loop evaluates it again, and each of six unrolled edge blocks loads neighboring mass/elevation and repeats fmul/fadd. Compiler does not precompute/share per-node heads across cells. Flow remains float through min/division/product; edge store explicitly extends float to double. Gather later loads double and subtracts/adds in fixed order.

This justifies testing, not assuming benefit from, one compact working-set variant: preserve exactf32 head operations once per node, reuse those represented heads, and store representedf32 edge flows then widen exactly where previousf64 edge values entered the same sums. Savings edge24bytes/patch minus head4bytes/patch =20bytes/patch (819240bytes40962). Added conversion cost may offset memory savings, so whole-step fixed-pair tests still required. No relative-head arithmetic or different rates, projection, SIMD approximation, precision-loss donor repair, or favorable-repeat search proposed.

Build: `zig build-obj src/qa_liquid_ir.zig -O ReleaseSafe -femit-llvm-ir=<output>/cached.ll -fno-emit-bin`. This is native codegen evidence, not WASM or hardware performance.

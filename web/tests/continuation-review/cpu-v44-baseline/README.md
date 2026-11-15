# Remaining v44 physics, with the sparse index applied

Frozen current production copy at task start (HEAD5f52002), not a rollback of the sparse index. Actual40,962-cell Origin nursery, early and naturally evolved30 days (10 occupied patches /18 cohorts). One cooperative thread,12 warmup frames,60 measured frames/60 actual1,440-second ticks at24 simulated hours/sec requested. No model or visual reductions. Native EGL390x700 mobile rendering policy and software llvmpipe, not an actual browser/device benchmark.

Early update9.3318ms; established update9.8213ms. Established per-tick stage means: temperature2.4175ms, liquid/wind1.8818ms, atmospheric water4.4875ms, organisms1.0325ms. Atmospheric breakdown: tangent wind basis0.7349ms; edge rates1.3801ms; phase/saturation0.8402ms; coefficient0.7244ms; gather0.8078ms. Nested atmosphere is included in water; do not double-count it.

The single-run timings are directional, not a causal before/after comparison against historical measurements. Established full-frame19.5905ms includes9.7688ms render/finish on this software GPU. Fixed input1/60s controls workload; measured native compute-throughput20.418h/sec is not guaranteed browser speed. Full save restoration checks passed; process exited0 with the existing allocator shutdown-leak warning.

Reproduce with egl-cpu-resolution-prepare.py and the standard native nursery build/flags from cpu-resolution-v42, STELLA_CPU_LEVEL=6, using the frozen production revision. Copied-source hashes pin the actual measured fixture, including profiling-only instrumentation.

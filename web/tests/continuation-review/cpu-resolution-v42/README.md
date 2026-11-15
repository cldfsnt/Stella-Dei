# Current CPU resolution profile, pre-optimization

Actual generated Origin nursery, coupled production physics and normal seeding, at early and30 days. One run per mesh,12 warmup then60 measured frames with60 actual1440-second ticks,24h/sec target, cooperative thread count1.40,962 versus163,842 cells; same generator seed but different grids/ecological trajectories, NOT identical-state performance comparison. No reduced-resolution production change or visual cut. Native390x700 mobile rendering policy, llvmpipe software GPU, not actual browser/laptop/phone timing. Timing noise and other shared-workspace work remain limitations; repeat matched candidate tests before speed claims.

Early large-grid update49.06ms/full64.87ms; established update46.01ms/full61.76ms (7 occupied patches/12cohorts). Small-grid update10.63/10.47ms; full20.39/20.42ms (established10patches/18cohorts). Large-grid compute-throughput6.17–6.48simulatedhours/sec despite24requested, versus small19.59–19.62. This supports checking retained save topology when investigating a6–7hour ceiling, but does not establish the user's actual topology/device bottleneck.

Atmosphere remains largest classified physics cost after prior phase-coefficient optimization. Large established per-tick:temperature9.79ms, liquid/wind7.44ms, atmosphere19.85ms, organisms8.93ms. Sparse organisms still incur fullmesh walks. Geometry caching and ordered activity-set alternatives are separate experiments, not proven by this baseline.

Both fixture runs exit0 and exact-save restore checks pass; existing native allocator shutdown leak remains. Raw logs compressed losslessly after workspace path sanitization. Source copy used existing atmosphere-phase preparer, re-enabled early profile and changed only copied newworld subdivision choice to STELLA_CPU_LEVEL=6/7. Native Save fixtures remain in scratch for comparison (not deployed).

## Reproduce

Run `python3 web/tests/egl-cpu-resolution-prepare.py <isolated-source>`, then build that main.zig using `web/tests/egl-propagule-visual-build.zig` with Zig0.13 and absolute build/cache paths. Run with `STELLA_ORIGIN_COUPLED=1 STELLA_ORIGIN_FAST=1 STELLA_PRODUCER_LONG=1 STELLA_DIAGNOSTIC_DAYS=30 STELLA_FORMS_SINGLE=1 STELLA_ORIGIN_WIDTH=390 STELLA_CPU_LEVEL=6` (then7). Provide isolated absolute `STELLA_EGL_CAPTURE_PREFIX` and `STELLA_EGL_SAVE_PATH`. Existing preparers apply native mobile rendering policy and cooperative loop. No candidate cache changes belong to this baseline.

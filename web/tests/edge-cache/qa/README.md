# Isolated directed-edge QA
Set STELLA_SOURCE_ROOT to the current checkout. Run `python3 prepare.py /absolute/workspace/qa-output`.
Build with the checkout's `web/tests/egl-origin-build.zig`, `-Dsource=/absolute/workspace/qa-output/main.zig`, a unique prefix and writable caches. No checkout changes.
Run from checkout cwd with STELLA_PRODUCER_SEED=42, STELLA_FORMS_SINGLE=1 and STELLA_EGL_CAPTURE_PREFIX set to a workspace path (parent directory must exist).
- QA_WIND_LONG=1: paired 1800 ticks / 30 days, forced edge allocation failure vs cache; exact serialized state and poisoned-cache refresh. Historical WIND label here refers to edge scratch.
- QA_WIND_LONG=1 QA_EDGE_MUTATION=1: additionally changes terrain geometry and wind at ticks 300 and 900 identically in both runs.
- QA_WIND_LIFECYCLE=1: tracked teardown and two grid6→7→6 replaceWorld cycles.
- QA_CLOCK=1 QA_WIND_UNCACHED=1: edge allocation failure baseline, existing wind cache retained.
- QA_CLOCK=1: enabled edge cache. Full model hashes, frame quantiles and synthetic pointer pause. Native software GL only; not Android benchmark.
Profile logs additionally use the isolated stage timing instrumentation in instrument.py. Rendering counters in that older instrumentation are not hooked into the newer quantile harness, so zero render_cpu/gpu_wait counters must not be interpreted as real zero costs.

`prepare-direct.py` creates a smaller 20-tick paired test with canonical Raise/LowerTerrain actions and normal geometry upload. Every cached outgoing and reverse lookup is compared exactly with the original calculation after each rebuild. Run QA_WIND_LONG=1 QA_EDGE_MUTATION=1 on that executable. Its preserved initial direct.log contains a historical final print label saying full_30day_hash_equal; this run is only 20 ticks as its per-pass lines state, and the preparer corrects that label.

# Sandbox shader QA
Set STELLA_SOURCE_ROOT to current repository. `python3 prepare.py /workspace/path/to/isolated-source` creates native browser-style QA, with original and candidate shaders compiled into the same executable. Does not edit the checkout.
Build using current repo web/tests/egl-origin-build.zig, unique prefix, writable caches and -Dsource pointing to isolated main.zig. Run from repository cwd with QA_SB_SHADER=1 STELLA_PRODUCER_SEED=42 STELLA_FORMS_SINGLE=1. Set STELLA_EGL_CAPTURE_PREFIX to a workspace directory prefix that already exists.

Paired pixel checks: demonstrably visible rabbit; all five maps with atmosphere off/on; HDR free-camera sun; bright-to-normal and stable/day-night changes; full serialized model unchanged apart from intentional view fields. Render-only timing uses paused identical scene, original/candidate/candidate/original windows. Render-call wall time and separate glFinish wait are NOT GPU timer measurements. Test shim defaults to390×700; STELLA_ORIGIN_WIDTH=920 tests920×700, not the actual phone's aspect ratio or GPU.

Both shader versions remain embedded as QA fixtures even after production integration. Candidate differs from tested shader only by whitespace and explanatory comments.

Optional after preparing: `python3 profile.py /path/to/isolated-source` adds source stage wall timers; `--bracket` also puts glFinish before/after final composite and uses six-second ABBA windows. The completed-work bracket deliberately changes pipeline scheduling; compare bracketed original/candidate only, and do not present its timings as normal game frame costs or hardware GPU timer values. Without --bracket, composite_completed_ns=0 is an unmeasured counter, not zero cost.

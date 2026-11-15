# One bounded coarse beta attribution

Frozen c6819a0 beta engine, same candidate artifact supports enabled and disabled. Old exact endpoints from ebc2393 retained. Instrument only coarse outside-loop boundaries: thermal; liquid/wind; atmospheric wind/edge preparation; whole column (environment+standing+soil/root+condensation+infiltration); coefficient; gather; ecology. No per-cell clock imports, no extra phase execution, no optimization or rate change.

Compare plain/traced full endpoint bytes to prior plain off/on hashes before timing. Fixed sequence plain-off/plain-on/traced-on/traced-off/traced-off/traced-on/plain-on/plain-off,12warmup+60measured1440s ticks. Same projected inputs as previous screen, not identical full soil/vapor inventories or ecology. Exclusive CPU after sibling correctness completion. No repeats. Startup/save/serialization/render excluded.

Report trace-versus-plain overhead per mode and timer-sum residual. If apparent instrumentation overhead exceeds5%, do not treat absolute traced stage timings as reliable runtime costs; keep qualitative evidence qualified. Negative/variable overhead is not a speedup claim. Source-level per-column PhaseStep initialization is a hypothesis, not established compiler behavior or a requested optimization.

# v57 load geometry correctness

Loading now synchronously rebuilds derived terrain positions using the exact shared renderer formula, before physics can run. No GPU calls, new jobs, allocation, save schema changes, resource corrections or RNG draws. This removes dependence on a post-load render occurring before the next simulation tick. Normal frame-clock reset may already postpone that tick, so the witness does not claim every ordinary Load misbehaved.

Production witness began from identical saved data after rendering a legitimately different terrain/tilt. Before repair the first actual1440s tick differed in temperature, liquid and vapor. After repair the complete endpoint exactly matches the original correctly refreshed control. Four tilts across40962vertices match frozen old geometry bits. Same-geometry10tick continuation and invalid-load state/geometry atomicity pass;49 existing native save/core tests and66 JavaScript tests pass.

Final ReleaseSafe singlethreaded WASM and emcc3.1.64-O2 build exited0. Native EGL is proxy evidence, not actual browser/device pacing verification or a speed improvement. Existing unrelated native allocator teardown diagnostic remains. Schema6 and live ecology unchanged; experimental hydration/mutation is not imported into the game. No landplant/animal progression claim.

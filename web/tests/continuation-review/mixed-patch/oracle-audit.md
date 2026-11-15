# Borrowed-array oracle audit

`save_game.capture` returns a schema object whose elevation, temperature, vegetation, water, vapor, rainfall and plant arrays borrow current Planet storage. Keeping that object alone is NOT a deep snapshot.

The mixed-patch fixture handles this correctly: immediately `stringifyAlloc(capture(...))` before simulation; parse those frozen bytes with `.allocate=.alloc_always`; restore parsed baseline before each arm; serialize the observed endpoint before restoration/unobserved ticks; compare the two separately allocated byte strings. `save_game.apply` copies parsed dense arrays into runtime storage using memcpy, not pointer adoption. Each new window freezes its new starting world again.

Prior natural colony-watch fixture uses the same `frozen` → `parsed_before` pattern and immediate `with_watch` / `without_watch` strings, restoring parsed baseline before BOTH arms. Its claimed full saved-world parity is not a borrowed-reference comparison. This proves equality of serialized world fields, not unsaved UI/cache internals.

The separate controlled two-patch birth/movement fixture does not call capture. It duplicates mutable microbeCells, copies stats, feedback and atmospheric scalar reservoirs by value, and shares only geometry/neighbors/temperature/water input arrays for `simulateMicrobes`, which does not mutate those inputs. Its assertions concern cohorts/RNG, stats, feedback and scalar gases. It is not a whole-climate or full saved-world comparison; no stronger claim should be made.

Read-only audit found no affected oracle requiring a rerun. Production unchanged.

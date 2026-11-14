# Corrected film integration candidate, not deployed

Base44fb136bbc9a3f7dae39a429e3c24f94116716bd. Apply film-v28.patch narrowly and add src/producer_habitat.zig. Main v29 has performance changes: NEVER replace main.zig or shell.html wholesale; full files included only as exact review evidence. Native test scripts are QA-only; no new serialized fields or hidden water.

Read FILM-V28-QA.md for corrected zero-depth/support continuity, actual paired100-day evidence and failed offspring, old-save physics changes, final native seed/guidance/load gates, WASM pass and browser/mobile visual limits. Raw fullfixtures/logs remain locally preserved; compact summaries carry hashes. events/ files are explicitly filtered logs. Original uncorrected frozencheckpoint remains unchanged.

Reproduction uses baseline EGL test chain plus added egl-film-prepare.py/build.zig/shim.c; see earlier frozencheckpoint REPRODUCE-FILM.md. Guidance harness extends existing egl-world-menu-prepare.py, uses QA_EXISTING_SAVE and QA_GUIDANCE_OUTPUT, and test-only webPlayState gate to exercise actual snapshot export natively. No test-only globals or generated source belong inproduction.

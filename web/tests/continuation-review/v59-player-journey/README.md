# v59 actual native player journey

PASS, native exit0. No bounded user-facing defect reproduced in this scripted sequence; no production/UI/ecology changes made. This exercises actual engine tool paths and rendered target picking, NOT actual browser dialogs, IndexedDB sync, Android touch, laptop FPS, or a novice's ability to discover a target.

Input is unchanged natural-day60 world (hash in provenance),40,962 cells. Existing fixed-rule nearshore scan selects an empty patch next to life,13594. This is automated selection, not a claim a person found it without help. No cohort/trait assignment or repeated favorable search.

Verified sequence:

1. Paused real `stella_habitat_prepare` Nursery preview then one-use execute. No new organism/birth from habitat action.
2. Real `stella_seed_colony` succeeds at13594,5m center, biomass0.02. This is deliberate manual seeding, not natural colonization.
3. Real Advance start/callback60ticks/dismiss/neutral-release completes exactly86,400 simulated seconds, paused afterward, original speed unchanged. Seeded patch total living biomass0.025759216 at that point.
4. Real Find life succeeds, real rendering produces targets, actual shim pointer→`mousePressed` selects the rendered target and Life snapshot reports that exact patch.
5. Real fine-water export adds actual0.100000024m; explicit checked Resume&Watch starts afterward with speed unchanged.120 ordinary update callbacks yield30actual solver ticks/0.5day observation. Local total goes2→4colonies, biomass0.025759216→0.040849273. This single trajectory does NOT establish that water caused the growth or that offspring belong to the manually seeded lineage; incoming neighbors may contribute. Watch baseline is after edit, not an intervention-effect measurement.
6. Pause/stop watch and render. Actual390×700 screenshot inspected: plant-form/history glyphs, selection brackets, tracked arrival/loss marks and0.5day local observation remain visible. No browser overlay test implied.
7. Actual filesystem save adapter writes isolated test save, reads/parses it, a deliberate subsequent water change demonstrably changes world bytes, and applying decoded save restores complete serialized state exactly. Original input then restores exactly. Save adapter differs only in redirected private QA path, never user's canonical save. Browser durability/IndexedDB wrappers and main Save/Load buttons are not exercised here.

All55 copied public export bodies are byte-identical to production, audited after final fixture construction. Microbial core is byte-identical. Inherited native harness keeps explicit web availability/browser-policy/cooperative-loop bridges; Planet only adds read-only flux counters and does not change flux/application ordering. Production/play and copied hashes are recorded, so no claim the entire native host is a bit-identical WebAssembly build. The final image is a lossless encoding of captured pixels, verified equal. Inherited GPA teardown diagnostic retained in full compressed log; exit0 and every journey assertion pass.

Reproduction: `egl-v59-journey-prepare.py` plus existing `egl-propagule-visual-build.zig`, pinned Zig0.13. Run with LIBGL_ALWAYS_SOFTWARE=1,EGL_PLATFORM=surfaceless,STELLA_ORIGIN_COUPLED=1,STELLA_ORIGIN_FAST=1,STELLA_ORIGIN_WIDTH=390,QA_PULSE_SAVE pointing to hashed natural60-day60.json and a writable STELLA_EGL_CAPTURE_PREFIX. Large generated copies and test save stay local. No speed measurements made; sibling work need not be excluded from this correctness run.

Remaining practical gap: actual browser/device interaction and new-player onboarding have not been established by this script. No speculative UI fix was added solely to create a change.

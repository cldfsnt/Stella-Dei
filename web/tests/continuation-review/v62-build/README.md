# v62 finite-foraging aggregate release gate

Frozen production source543655a (reviewed feeding e7ce8c0 plus truthful Sandbox guidance/Bites label). No further source edits during pipeline. All gates passed: full JS75/75; actual production qa_ecology vegetation/rabbit/microbial regressions; actual aiStep qa_rabbit_foraging; full pinned-toolchain WebAssembly build. Sequential && pipeline overall exit0, so every prerequisite succeeded before build.

Reproduction: node --test web/tests/*.test.cjs; Zig0.13 zig build --build-file web/tests/lifecycle-build.zig with an absolute cache directory and -Dsource=<absolute src/qa_ecology.zig>, then same for qa_rabbit_foraging.zig; finally STELLA_TOOLCHAINS=<pinned tools> STELLA_WEB_CACHE=<existing v34-web-cache> bash web/build.sh. ReleaseSafe, Emscripten-O2, web GL per-draw diagnosticfalse. Logs retained verbatim compressed. Source and raw build hashes in provenance.json; binaries not committed.

The old controlled ecology test still produces feeding, births and plant inheritance; the finite-bite helper is constrained by actual food debit and hunger/time budget. Its dimensionless vegetation/satiety bookkeeping is not full carbon conservation. All10 real-world hypothesis arms and exact warm/cold native endpoint/restart proof remain the native owner's separate evidence. This build gate alone does not prove a universal ecological outcome or device performance. Sparse food takes longer to graze, but local plant loss and rabbit extinction remain possible. No guaranteed regrowth, refuge or boom-bust claim.

The Sandbox visible counter now says Bites (positive feeding events), while saved rabbit_meals/rabbitMeals schema and values remain unchanged. v61 seed target and offspring controls remain in the full suite/build. Recent-statistics and arrival/loss visibility work are not integrated here; source inventory hashes do not imply every standalone experimental/helper file is linked.

Raw HTML keeps historical source label; coordinator packaging supplies v62 and a separate final manifest. No deployment by this worker. Later source changes require a fresh build or explicit packaging-only provenance.

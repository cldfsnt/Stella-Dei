# Isolated protective strategy wire15

Required protective_strategy contains law1, mutation_law1 and explicit u64 stream_seed (enabled implied).15 additionally requires existing valid Origin/root3/wind1/thermal1 identity. Historical1–10/13/14 omit the new config/cohort fields and reset configoff on apply;11/12 remain rejected. No implicit conversion, namespace change or production modification.

Investment must be finite0..1; clock exactly−1 or finite nonnegative. Clock>7200 is legitimate and preserved. Zero investment requires−1. Dead records may retain valid nonzero investment; no forced canonical-empty reset. Historical saves cannot disguise positive investment or active clock. Capture validates live config and all cohorts; apply sets config only after existing validation/allocation boundary.

Schema-focused tests cover synthetic historical7/8/9/10/13/14 strict unchanged-reader byte equality, actual natural60 and warm14 old-reader equality,15 full field roundtrip including dead traits/clock8000/maxu64, malformed/missing identity,11/12, disguised14, invalid clocks/NaN. The inherited older-version tests also run. Actual live apply atomicity and full-scheduler restart belong to parent native acceptance, not this focused test.

Reproducer: protective-save-prepare.py on fresh root-water-ui copy after owner core fields exist; prepare-protective-save-tests.py creates distinct QA copy; lifecycle-build.zig ReleaseSafe points at its save_schema.zig. First compile found owner core operator whitespace error; owner corrected it, QA-only microbes refreshed. Logs retained.

Final focused ReleaseSafe run90421 exited0; no adapter changes were needed after the owner core whitespace fix.

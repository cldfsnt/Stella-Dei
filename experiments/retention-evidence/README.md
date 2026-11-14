# Experimental Continents ecology checkpoint — NOT PRODUCTION

Do not merge this directory into live game source or deploy it. It preserves an investigation, including negative results. The live game remains schema6; the isolated coupled reserve model uses experimental schema7. No saved user world was migrated.

## Contents
- REPLAY-QA.md: measured-environment replay, explicitly synthetic trait contrasts rather than naturally evolved organisms.
- replay/: standalone precise reserve model, replay program, exact5400-row measured climate trace,36contrast results and model tests.
- replay/trace-overlay/: exact changed source files and harness chain needed to regenerate the trace on the base below.
- coupled/overlay/: exact experimental changed source files and harness dependency chain for paired actual-engine tests.
- results/: compact outcomes, unit-test logs and hashes of large serialized snapshots retained locally. Snapshots are omitted to avoid redundant tens of megabytes; deterministic regeneration produces them.

## Reproduction base
Start from repository commit b73cf9c10692b1dfad70452ab819c713347d9d46 in a separate checkout, with the project's existing dependencies/assets. Overlay EITHER replay/trace-overlay OR coupled/overlay onto that checkout, never both. Each source manifest records every expected source SHA256, so missing base files or unintended edits can be detected. These are full-file overlays for this exact historical base, not a safe merge onto current main.

Use Zig0.13, standard native EGL build harness and software GL. Set TMPDIR to a workspace-local directory. See reports for flags. Native EGL does not prove Android/WebGL rendering, and the known shutdown allocator leak remains disclosed.

For standalone replay: compile replay/run.zig and pass replay/results/continents-trace.csv. It explicitly accounts prescribed environmental exchanges; biological ledger accuracy is not a claim of exact conservation by the entire climate solver.

For coupled test: run web/tests/egl-retention-world-prepare.py into an isolated generated source copy, build with egl-origin-build.zig, then use STELLA_FORMS_SINGLE=1, STELLA_ORIGIN_COUPLED=1, STELLA_ORIGIN_FAST=1, STELLA_PRODUCER_LONG=1, STELLA_DIAGNOSTIC_DAYS=100. QA_MATCHED_INITIAL must name a writable workspace-local absolute JSON path. Run reserve-enabled first, then STELLA_DISABLE_RESERVE=1 with the SAME initial path. The second run asserts byte-identical initial serialization, restores it, and asserts all initial stored water is zero. Actual one-time Nursery and one Seed create the initial state, with no ongoing irrigation or assigned biological traits.

The target30111 becomes the nursery's explicit dry outer rim, with center30114. That player terrain/water action changes local climate; its prior unmodified trace must not be assumed to apply afterward.

The100-day paired result is complete; see COUPLED-QA.md. Both arms develop naturally funded moist-shore descendants; the reserve arm has no overall biomass advantage and neither shows dry-period fixation. Thirty-day results remain preserved as an earlier negative checkpoint. Do not present terrestrial plants, seedbanks or fire recovery as complete.

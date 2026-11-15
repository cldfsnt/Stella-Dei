# Directed sample: real-world eligibility gate (negative result)

Research only. No production wiring, UI, saved fields, physiology or thresholds changed. New `experimental/directed_sample_planet.zig` wraps the earlier isolated conservative transaction with actual Planet ownership, current runtime world serial, actual cohort ID and real adjacency. A prepared ticket contains source/target cell snapshots; execution refuses if either changed. Adjacency is rederived from Planet at execution, not accepted as caller-supplied truth. This strict snapshot rule may make previews short-lived while time runs; no user workflow is claimed.

## Actual current-scheduler result
Loaded the preserved genuinely evolved40,962-cell nursery at day30 (`watch-natural-30day.json`) into the current engine, then advanced600 coupled1,440-second ticks to day40. No assigned traits, biomass, earned credit, gases, water or extra nutrients. Inspected25,139 living cohort-states over601 checkpoints. **Zero** simultaneously met the existing biomass≥0.03 AND reproduction_credit≥0.04 conditions. Therefore zero legal funded samples were available; full-target rejection was not the cause (zero funded threshold hits, zero tested full edges).

Independent maxima were biomass0.123999804 and credit0.08146889; these occurred in different cohort-states and must NOT be combined into an imaginary eligible donor. Initial read-only inspection of five actual30-day save variants (40k natural/v44/cold,163k natural and earlier nursery) also found no threshold-eligible donor. This is bounded negative evidence, not proof that eligibility is impossible in every game.

The likely interaction is existing small-propagule routing: it spends0.01 credit once biomass reaches0.02, often before a larger0.01 daughter becomes available. That is an interpretation, not a causal intervention tested here. The earlier routing experiments already failed to show a consistent benefit from saving credit for larger daughters. Do not loosen thresholds, inject credit or disable normal reproduction merely to manufacture a useful button.

## Verified wrapper refusals
On the actual loaded/evolved world, stale world serial, wrong cohort ID, wrong Planet owner, changed target snapshot, same-cell and out-of-range target are refused. Complete serialized world bytes before/after this refusal batch match. No RNG/resource/ancestry change. Current source/target snapshot checks are code-level guards; these are not UI selection tests or proof of an eventual asynchronous browser workflow.

Both native runs exit0. The second independently counts simultaneous funding hits versus blocked adjacent edges and reproduces the first negative result. Original world restore/save validation succeeds. The native harness retains its known GPA teardown leak warning; no clean leak-check claim. Earlier fresh-world lead-in diagnostics show zero history frames/NaN timing because the preserved save is loaded afterward; no performance claim uses those lines.

## Explicitly NOT demonstrated
- No successful naturally funded transaction, so no real-world immediate transfer receipt or resulting daughter fate.
- No wet-versus-shallow transplant outcome, survival benefit, altered fitness, coexistence or supported plant progression.
- No closed whole-world carbon/nutrient/oxygen ledger proof across the ten-day physiology run. Existing f32 physiology/global accounting drift remains separate from the prior exact local-transfer experiment.
- No arbitrary saved-geometry/browser rendering or Android verification. This is the established nursery fixture with current native coupled scheduling, not a general browser-load test.

## Whole-cohort alternative also held
A GOD whole-cohort transplant would remove the source occupant rather than duplicate it and would not require earned reproduction credit. However preserving its identity/history conflicts with current save validation: `save_schema.zig` requires `last_to == current cell index` whenever `relocations > 0`. Resetting history, incrementing autonomous movement counters or bypassing validation would be dishonest. A deliberate schema/provenance design separating manual intervention from biological movement is required; it was NOT implemented here. Restricting to never-relocated cohorts would be a distinct, visible eligibility limitation, not a generic transplant tool.

Conclusion: do not ship an effectively unavailable sampling button. Stop this experiment as directed; prioritize observable natural competition. Revisit manual transplantation only with deliberate history/schema semantics and meaningful player costs, not free cloned life.

## Reproduce
`python3 web/tests/egl-directed-world-prepare.py /absolute/new/src`; build with Zig0.13 and `web/tests/egl-propagule-visual-build.zig`, `-Dsource=/absolute/new/src/main.zig`, dedicated prefix/cache. Run native binary with `QA_DIRECTED_SAVE=/absolute/watch-natural-30day.json`, `STELLA_ORIGIN_COUPLED=1 STELLA_ORIGIN_FAST=1 STELLA_PRODUCER_LONG=1 STELLA_FORMS_SINGLE=1 STELLA_ORIGIN_WIDTH=390 LIBGL_ALWAYS_SOFTWARE=1` and writable capture prefix. Logs/provenance are retained with deterministic gzip. No deployment performed.

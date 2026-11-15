# Periodic Origin guidance: bounded read-only audit

Standalone native ReleaseFast microbenchmark of current habitat_feedback.originStage; not full-game or browser profiling. 40,962 real Cell records. Empty and one-founder controls plus exact cohort values extracted from the previously generated 30-day actual world (10 occupied patches,18 cohorts). Three batches of1,000 calls each, noinline wrapper and compiler memory barrier, checksummed stage outputs. Full represented-cell JSON remained identical before/after. Source data were initialized outside timing. Sibling correctness work could overlap; one early batch is visibly noisy.

Median scan cost: empty165.774µs; one-founder175.525µs; actual30day178.998µs. At one scan every3seconds this native proxy is about0.006% of a CPU core, not a plausible explanation by itself for continuous frame slowness. This excludes WASM crossing, DOM layout, snapshot construction and JSON parsing, so it does not bound the complete periodic UI callback.

## Proven avoidable invocation

refreshJourney reads _stella_goal_stage then, when the guide is visible, calls checkHabitat, which reads the same stage again synchronously. Passing the freshly obtained stage into the guide renderer removes one duplicate scan without cached-world invalidation issues. Expected saved work in this native measurement is about0.18ms once per3seconds while that guide is open, not per frame. No production change was made.

## Snapshot path

refreshStarter uses full lifeSnapshotForState JSON, although its summary/trend needs only selected cell, day, biomass, water, temperature and eligibility. The full endpoint computes four tissue descriptions and four relocation-opportunity results; each opportunity constructs up to six neighboring environments before checking whether the cohort is alive/capable. This is bounded local work, not another mesh scan. A slim endpoint could remove work, but this audit did NOT measure its actual generation/parse/DOM cost, so no speed claim or implementation is justified yet. Shared snapshot consumption must preserve the trend's sampling behavior and all current action-time eligibility checks.

Reproduce: Zig0.13.0 build-exe src/qa_origin_stage_cost.zig -O ReleaseFast, then run generated executable. The source contains the actual extracted cohorts as an explicit read-only test fixture; no random or simulated winner is synthesized. Preserve original 30-day save separately; its whole-save SHA256 is recorded below.

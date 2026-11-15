# Isolated compact Life panel candidate

Not applied to production or deployed. Candidate lives in `site-tmp/compact-life/web`; `compact-life.patch` applies to the v45 shell and life-trend files identified by BASELINE.json. New test included in patch. Existing control IDs are all preserved, with no duplicates. No engine or saved-world changes.

## Changes
- Above folds: live summary, actual seed eligibility/depth/temperature, Watch, fine water adjustment, Refresh. Exact-depth/basin controls remain under an explicit advanced-water disclosure; existing target-binding handlers unchanged.
- Current colonies show exact string IDs, existing form, actual biomass and current mass share. Four-slot mapping is applied before filtering so tissue forms remain matched. Positive tiny colonies display <1%, not zero. No winner, death, adaptation or growth rate is inferred.
- Existing full cohort ancestry/traits, competition explanation, resource conditions, recorded-feeding controls and glossary remain available in closed native details groups. Refresh closes folds to avoid carrying disclosure context across patches. Existing event handlers and their guards are unchanged.
- Empty trend text now says “No living biomass observed here” rather than inferring colony loss.
- Native details CSS overrides the game's generic panel positioning; summaries have44px minimum height, and ID/share lines can wrap anywhere.

## Verification
All21 isolated JavaScript tests pass, including all20 existing tests and new exact20-digit IDs, preserved slot/form association, immutable snapshot, empty/invalid input, tiny mass, action-order/collapsed-details and truthful trend assertions. Existing shell target-binding/control regression tests pass unchanged. First aggregate run failed because isolated test copy lacked its read-only play.zig source dependency; adding an exact copy fixed fixture setup. Original failed log preserved.

**Rendered390px verification is blocked, not passed.** Installed Chromium aborts before rendering: process-singleton socket() Operation not permitted; ptrace also denied. No workaround or security bypass attempted. The explicit mocked-data fixture is included for parent's supported browser verification. It contains actual candidate styles/markup but not live gameplay or real biology. Do not claim visual acceptance until it is inspected in the supported browser. No screenshot was produced.

Suggested final check: at390px, inspect initial viewport, open each disclosure and exact-depth controls, scroll, repeat refresh, select another patch, then verify all actions still target that patch and observations cancel as before. Parent may apply with `git apply --check .../compact-life.patch` then integrate after v45 packaging. Rebase rather than overwrite if BASELINE hashes differ.

## Parent integration and supported browser acceptance
Applied candidate to production source after v45 deployment. Added visible plus/minus disclosure affordances after visual review. All21 final JS tests pass. Supported managed preview/CUA checked the actual integrated shell and scripts with explicit mocked engine data,374px dialog width: Watch and water controls visible without traversing glossary,20-digit ID and share readable/wrapped, advanced water exposes existing controls, Refresh closes it, detailed ancestry preserves exact ID. This is narrow-panel UI evidence, not an Android viewport/device or live simulation test. Preview stopped. The worker's earlier direct Chromium attempt is retained as a failed unsupported test and was not used to establish acceptance; all visual acceptance uses the supported CUA route.

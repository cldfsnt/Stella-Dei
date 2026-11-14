# Direct Origin starter controls

Origin now has a compact expandable strip with Find habitat, Shape basin +15m, Seed colony, and Inspect. Basin and Seed remain separate explicit player actions. A successful seed collapses the strip and displays confirmation; the summary stays available to reopen it. A valid snapshot supplies selected patch number, actual water and temperature. Buttons reject stale selection, Sandbox mode, invalid snapshots and unavailable runtime. The basin retains the previously tested19-cell/15m/17m-rim semantics and does not refill automatically.

The callback preserves pause and chosen simulation speed and works when the pointer is outside the 3D canvas. Shell regressions cover action isolation, stale/failed/no-state cases, visible feedback, and CSS specificity so generic closed-details styles do not hide the starter forever. Controls use44px touch targets. Native actual-engine callback checks reject a stale point without biomass changes, then make the real basin and seed via the same callback used by the webpage. No biological fields are assigned.

The browser runner in this execution environment cannot create required sockets, including after approved escalation; no physical Android/end-to-end browser usability claim is made. Native software-rendered engine and Node shell tests provide complementary, limited evidence. An existing native teardown allocation warning remains.

Moist-shore evolution work was deliberately NOT merged here: controlled physiology checks succeeded, but ordinary-world colonization was not demonstrated. Its source and failure evidence are preserved on branch `experimental/moist-shore` instead of making a false terrestrial-plant claim.

## Seed-zone discovery

The user reported resorting to random tapping. Origin Find habitat now searches the same read-only eligibility predicate used by the real Seed action, including water/temperature, free cohort slot, nutrients and carbon. It switches to Seed placement mode without seeding. Green '+' map rings indicate eligible actual cell centers; a selected invalid cell shows a red X. The starter and Inspect show the exact current rejection reason, and the direct Seed button disables when invalid. Markers are bounded/de-cluttered and skip UI-covered areas; they are not a promise that a colony will thrive indefinitely.

`egl-seed-guidance-prepare.py` renders unmodified real eligible and too-deep sites; `egl-starter-prepare.py` checks genuine seedable focus followed by stale rejection, actual basin action and off-canvas direct seed. Neither assigns biological values. The marker and action share `seed_eligibility.zig`; eligibility unit tests include slots, resource exhaustion and boundary temperature/depth checks.

Executed discovery acceptance: native390×700 actual-engine view showed green eligible targets and red too-deep X; current too-deep text replaced stale focus success. A simulated physical pointer click on the centered green target created a living colony through the real canvas input callback (`SEED_TARGET_TAP actual_pointer_click=true living_colony=true`). Direct starter callback also passed genuine eligible-focus, stale rejection, off-canvas seeding, pause/pace preservation and exact save restoration. Node shell/touch/storage suites passed; complete browser WASM build succeeded. These are not physical-device touch/performance measurements.

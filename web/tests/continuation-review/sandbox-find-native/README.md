# Actual Sandbox survivor finder acceptance

Source83a875c combined with exact nearest-point helperbc2b4ee. No biology, water, save-schema or Origin Find changes. Actual40,962-point day30 world has82living rabbits and89positive vegetation patches, while the original center436 is bare.

## Native actual route
Both390×700 paused and700×390 Playing runs pass. Plants choose current sprout-visible patch27000, cover.1171681; real sprout is visible and selection matches. Rabbits frame an actual current animal position, with the ground patch27037 selected (cover.00242). Rabbit selection is deliberately terrain, not a fabricated persistent animal identity. Screenshots inspected; target animals/plants clear the toolbar/footer in both shapes.

Complete captured simulation/resources/RNG/time/pause fields remain exactly unchanged. Only intentional camera/distance/display fields are normalized for comparison; selected/clicked ground patch is asserted separately. Empty-plant, empty-rabbit and narrow-small-viewport refusal leave state unchanged. Original complete input restored. Landscape QA input differs from original only by paused:false; no steps are run, so this verifies immediate Find while Playing without a stale-time/chunk loop, not animal tracking.

One-shot action diagnostics on this actual world: portrait plants.068704ms/rabbit.040651ms; landscape plants.040761ms/rabbit.041332ms. These are single native calls, not a controlled performance benchmark or browser/mobile speed claim. No per-frame scans or scheduled background work.

## Guards and UI
Four pure tests cover visible→sparse→submerged plant preference, empty, geometry/polar, malformedcover>1, exact current rabbit position, portrait bounds and700×390 landscape support. Three mocked-controller tests plus full92JS suite pass. Sparse/submerged positive vegetation is not mislabeled as extinct. Unsupported mode and unsafe view refuse rather than changing world. Existing v66 Origin finder body/handler are unchanged.

Initial portrait screenshots/run passed before the review-requested viewport correction; those logs are retained. The final guard uses actual toolbar width breakpoint rather than rejecting all heights<400. QA EGL shim adds optional STELLA_ORIGIN_HEIGHT, default700 unchanged. Final combined source includes promoted nearest helper, then both actual screenshots/purity runs. All public export bodies match production (audit retained).

Reproduce via web/tests/egl-sandbox-find-prepare.py and existing EGL build helper, input pinned in provenance. Same STELLA_ORIGIN_COUPLED/FAST+QA_PULSE_SAVE native test seam as warm30. Set STELLA_ORIGIN_WIDTH=700/STELLA_ORIGIN_HEIGHT=390 for landscape. Explicit exit occurs after original restoration, not inherited teardown.

Coordinator mock shell fixture is separate: stella-competition-preview/dist/sandbox-find-fixture/index.html, labeled UI MOCK ONLY. It uses current shell/scripts and scripted Sandbox/Origin plus success/sparse/submerged/no-life/unsafe controls. No server/browser/WebGL claim from this fixture. Actual engine evidence is above, final browser/mock acceptance belongs to coordinator.

# Exposed-detritus ignition player wiring

Separate Origin button, not replacement for Sandbox Scorch. Existing stella_god_action export gets kind3, no new exported symbol needed. stella_god_target includes ignition eligibility from shared PlayState.previewIgnition(expected); actual action invokes PlayState.applyIgnition(expected), which calls the tested accounting adapter again against current selected target. It clears previous unrelated god visuals, gives plain truthful feedback, and does not change pause/time/pace or save schema.

UI is fail-closed when ignition eligibility is absent, invalid or blocked; other existing god tools retain independent readiness. Explains dry Origin dead carbon/oxygen requirements, sensible discovery through Life snapshot and deliberate Water−, optional pause because water can return, and no automatic fuel creation/draining. No live tissue burn, wildfire propagation, adaptive unlock or guaranteed benefit is promised. No invented flame visualization added.

Success foregrounds actual local kgC/m² burned and temperature change. Expandable last-session record retains exact returned JSON with actual/ideal gas quantities, signed numerical residuals/budgets, fuel heat and stored heat. Explicitly not saved event history; refresh does not clear it, successful Load does. Gameplay calibration30MJ/kgC disclosed, not fuel chemistry measurement. Unknown/malformed result advises inspection rather than claiming no changes after a possibly applied action. Known refusal reports no ignition changes and retains last successful record.

Shell tests pass readiness/refusal cases, real kind3 call, fully specified receipt rendering, separateScorch state, refresh retention, wet/stale server revalidation, malformed receipt handling, absent readiness, and clearing after successful Load. Native/actualWASM build and player-flow tests are separate workers' release gates; no claim here those completed. This agent did not compile, commit or publish.

Owned modifications: src/main.zig, src/states/play.zig (shared seam), web/shell.html, web/tests/shell.test.cjs. Other concurrently edited fire modules/native fixtures belong to their workers.

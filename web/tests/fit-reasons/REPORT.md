# Fit-life rejection feedback · v23

Read-only camera operation; no changes to fit calculation, model, save format, gestures, or speed.

Adds typed internal fit errors while preserving optional `fit` and boolean `fitLivingCluster` interfaces for existing callers. Web API returns specific refusal codes: -2 Sandbox (Origin-only), -3 undersized viewport, -4 polar center, -5 invalid geometry, -6 cluster beyond supported extent; 0 still means no nearby living colony, -1 unavailable world, 1 success.

Shell now gives an actionable, accurate message for each case instead of always telling the player to pan toward nonexistent Origin colonies. The control remains visible in Sandbox so its limited scope is explained rather than silently disappearing. Refusals never change the camera. Existing gesture reset and More dismissal remain unchanged.

Verification: all 4 pure life-camera tests pass, including exact failure reasons and unchanged existing success geometry. Production shell suite passes with all five new refusal-code cases, explicitly asserting no misleading pan advice. Integrated full-engine and WASM checks are recorded with v23 acceptance.

Integrated in v23 after isolated review. BASE-SHA256.txt records source base for conflict checks.

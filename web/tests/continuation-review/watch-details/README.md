# Native Inspect → Watch baseline

Actual native rendered colony pick at Origin patch 12395 opens Inspect. With that panel open, both normal and checked explicit-resume Watch return -2 for paused and running states. Refusals preserve complete save/RNG, selected identity and prior watch. Closing the panel makes running Watch succeed; paused normal still refuses and explicit resume succeeds. Original save restored. This is actual native API/render interaction, not a browser WebGL test.

Baseline frozen before fix 0389740; compressed complete log and source hashes retained. First build failure was QA-only pointer argument, corrected before execution. Fixed acceptance is separate and retains these negative results.

## Fixed acceptance: 0389740

Copied actual production source passes both paused/running rendered-pick branches. Normal running Watch commits and dismisses native Inspect; normal paused Watch refuses without changing saved state, watch or details. Explicit resume commits with only the requested saved pause change. Stale world, stale selection, Escape, Climate and invalid-population refusals preserve prior watch/pause/details; invalid population returns -3 and the controlled malformed fixture is restored. Repeated start captures a fresh baseline; cancellation stops. One actual 1440-second scheduler tick after the transition remains actively watched, rather than immediately guard-cancelling. Original complete save restored. Source hashes, binary/input provenance and complete log retained. No model/physics changes, no browser performance claim.

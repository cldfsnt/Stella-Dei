# Opt-in local renderer context

Added for the player's reported laptop slowdown, not as evidence of its cause.
The explicit **Measure gameplay · 10 seconds** action captures available WebGL2
renderer/vendor/API text and drawing-buffer dimensions once after successful
measurement startup. Passive speed/Performance-details opening does not query
renderer information. Extension absence/errors fall back safely. Context is
copied into the retained sample and neither stored to disk nor uploaded.

Known software-renderer strings produce a qualified hint, not a diagnosis;
absence of a match never claims hardware acceleration. Text is bounded and
rendered with textContent. No user-agent, device-memory, renderer enumeration,
new browser permission, or telemetry endpoint is added.

Validation: node --test web/tests/*.test.cjs: 13 tests passed. Unit fixtures
cover normal/restricted/unavailable contexts, bounded strings, fallback,
immutable capture, startup refusal, capture failure and no passive query.
Shell wiring test uses a mocked runtime and does not establish actual laptop
WebGL performance. Actual renderer results still require a player-initiated
sample in their browser. No save format, simulation or rendering logic changed.

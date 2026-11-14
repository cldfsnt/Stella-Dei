# Historical pre-v20 climate diagnostic

This negative test predates corrected atmospheric transport, new habitat ranking and the explicit shallow nursery. It is retained as evidence, not the final v20 acceptance. See V20-ACCEPTANCE.md and WATER-CYCLE-ACTUAL-ACCEPTANCE.md.

# Integrated production propagules: 15 m, one seed, Grow

Tested the current working production source with the new propagule, observed-loss,
Watch and trend integrations. Native generated-world test used the ordinary
15 m basin, exactly one explicit seed and Grow (6 hours per second, 240 frames per
simulated day). No experimental geometry, low-latitude selection, resource/trait
assignment or conditional propagule flags were present in prepared source.

## 30-day outcome (120 seconds of normal play)
- Attempts: 0; arrivals: 0; births: 0.
- Occupied patches: 1 initially, 0 by day 30.
- Final selected water: 16.876139 m; temperature: 289.84583 K.
- Final biomass: zero. This is **not** a successful spreading ecosystem.
- Total liquid+vapor relative change: 8.8231e-6.

The result agrees with the original scenario: the colony does not earn sufficient
reproductive growth before declining. The mechanic does not invent offspring to
make the display look active. Starter viability remains a separate blocking issue.

## Engine checks
- Stale seed selection rejected without biology mutation.
- Explicit off-canvas starter button seeding works.
- Basin and seeding preserve deliberate pause and selected pace.
- Invalid save rejected with state unchanged.
- Exact current-schema save roundtrip succeeds (12,199,062-byte fixture).
- Transient observer reset assertions pass. A separate one-day fixture sets
  observational serial to 17 and counters to 3/2/1 before restore (no biological
  change); load resets them to 1 and 0/0/0 while preserving exact saved world data.
  That fixture also passes invalid rejection and exact 12,243,021-byte roundtrip.
- Shell wiring tests pass.

The native process exits zero but retains the pre-existing shutdown GPA leak
warning seen in earlier fixtures. This test does not certify leak-free shutdown.

Evidence: `results/propagules-production-15m.log` and corresponding source hashes.
Use `egl-propagule-prepare.py` plus the documented native origin build command.

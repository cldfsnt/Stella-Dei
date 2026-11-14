# Clean propagule mechanics candidate

Apply `mechanics.patch` to the production repository, alongside the sibling
`visuals/` overlay. BASE-SHA256.txt records exact source files used. Nothing in
this directory has been applied to production by this worker.

Defaults:
- One randomly sampled adjacent destination per eligible parent per simulation
  step. Requires parent biomass >= 0.02 kg C/m² and earned growth credit >= 0.01.
- Accepted bud transfers 0.004 kg C/m² from parent, including proportional support.
  Child inherits existing mutation logic, starts with zero reproduction credit.
- Destinations must have finite environmental values and a free cohort slot,
  but are not filtered for favorable water/temperature. Actual physiology can
  kill arrivals in dry, deep, cold or hot patches. No new life/resources injected.
- Successful propagules spend credit; normal adult reproduction remains unchanged
  as fallback. No separate frontier-first policy is included.
- Transient tracker remembers up to 32 actual arrivals and observes actual losses
  while they remain tracked. No time-expiry, establishment claim or universal
  loss census. Relocation forgets the pending observation, not counted as death.
- Session counters and visual tracker reset on load. Save schema/version unchanged.

Tests executed:
- 23 microbiology tests, including paid offspring carbon/nutrient conservation,
  dry failure accounting, wet growth, zero-credit no-chain behavior.
- Three bounded observer tests, including older tracked loss and no fake deaths.
- Actual generated-world 30-day Grow tests with one explicit seed and experimental
  nursery geometry: exact save roundtrip, invalid-save rejection and unchanged
  state all passed. Those environmental experiments are NOT in this patch.
- Parent must run integrated clean-base build, ordinary production-geometry
  interaction and save regression after combining the visual overlay.

Known 30-day outcomes (120 seconds at Grow):
- Original 15 m basin: local-first and frontier-first each had zero births and
  extinction by day 30. Geometry and climate can prevent earned growth entirely.
- Experimental 5 m nursery at current latitude with paid propagules: four arrivals,
  one occupied patch at day 30, biomass 0.003132. Early spread, not durable thriving.
- Same nursery at deterministic low latitude: first arrival day 1, four occupied
  by day 3, five total arrivals, back to one by day 30. Flooding caused decline.
- Actual 15-day flux diagnosis in that low-latitude case: rain +107.275 m,
  evaporation -0.208 m, liquid inflow +0.100 m, outflow -83.050 m; net +24.117 m.
  Nursery depth rose from 5 to 29.117 m. This is simulated excessive rainfall,
  not realistic weather or a successful life-friendly preset.

Ship only as an incremental exploratory-spread/observed-loss mechanic. Do not
claim a complete ecosystem, reliable thriving, established land plants, animals,
or a validated beginner preset. Combine with actual biomass trend feedback.

Future reserve-schema integration must transfer every stored resource
proportionally. Do not overwrite newer reserve reproduction code wholesale.

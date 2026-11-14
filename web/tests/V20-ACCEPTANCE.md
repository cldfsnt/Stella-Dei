# v20 · living frontiers

This release keeps schema 6 and the original Origin/Sandbox separation. It does
not claim terrestrial evolution, fire strategies, or a complete SimEarth game.

## Implemented
- Paid exploratory propagules transfer existing carbon/support into adjacent
  cells, including unfavorable cells. Growth must earn the next attempt; newborns
  cannot cascade across the grid in a single step. Limited slots are respected.
- Cyan diamonds show actual arrivals; amber X marks a tracked lineage lost, not
  necessarily an entire dead patch. Event trackers are bounded and transient.
- Find habitat ranks suitable low-latitude shallow water. Optional Shape nursery
  explicitly modifies up to 19 patches: center 5 m, surrounding reservoir 15 m,
  dry rim. It adds water once, not life, and is not automatic habitat care.
- Watch life hides placement overlays and gives a compact Pause/Tools/Pace header.
  It does not change camera, pause, pace, or ecosystem.
- Net biomass feedback measures changes over simulated days; it is not evidence
  of a particular biological cause.
- Atmospheric transport now follows velocity and distance, with donor-bounded
  transfer. Evaporation relaxes toward saturation and rain removes supersaturation.
  This is a game climate model, not validated weather physics.

## Checks executed against integrated source
- Production shell and JS suites: 6 passed; includes guarded nursery action,
  separate seed, Watch, trend reset after load/seed and modal flows.
- Pond/nursery helper: 2 passed, including repeatability, exact stale-selection
  rejection and no partial mutation after invalid inputs.
- Atmospheric helper: 6 passed, including mass accounting and time-step fixtures.
- Propagule feedback: 5 passed.
- God action/model imports: 29 passed, including paid propagule conservation and
  self-neighbor-safe waves.
- Native compact Watch: actual pointer callbacks and rendered 390x400 game view;
  Pause/Pace/Tools do not select underlying terrain.

Actual nursery API: 30 simulated days at Grow, one seed; 53 paid arrivals, 24 tracked losses, 11 inhabited patches and five aquatic growth forms. Native final-day rendering shows six visible inhabited patches. Save roundtrip and invalid-save rejection passed. See NURSERY-QA.md. WASM packaging passed. Fixed-seed examples do not guarantee survival in every world.
Browser/mobile physical-touch QA is not claimed: local browser unavailable and
cloud browser encountered the private site's sign-in wall. Native EGL captures
and callback tests do not substitute for Android performance or WebGL conformance.

## Existing worlds
Older saves may contain excessive atmospheric vapor accumulated under the old
transport model. Loading preserves that water; it can rain out under corrected
physics. No hidden world reset or deletion occurs. Before first overwrite of an older save, browser storage preserves one exact legacy copy and requires its persistence sync to succeed. No restore button or cloud durability is claimed. Fresh-world balance is the
validated comparison, not a guarantee that old climates remain visually unchanged.

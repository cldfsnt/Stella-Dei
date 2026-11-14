# Independent Sandbox Scorch review

Read-only inspection of stella-fire-v30; no production/candidate/evidence edits.

## Model and UI
Independently reproduced39/39 imported action/visual/model tests. Scorch computes
actual removed dimensionless cover and actual capped temperature delta/external
energy before writing either value. Mode, stale target, bounds, nonfinite,
nonpositive capacity, wet patch, empty cover and hot cap reject atomically.
Neighbor fields and inherited plant traits are untouched. Equal input state
gets equal intervention; no invented resistance or fuel chemistry.

Existing rabbits eat actual vegetation, lose satiety, seek neighboring food when
hungry, and die above333.15K on their next AI update. Scorch does not directly
remove rabbits or add a health/escape model. Existing vegetation recovery under
controlled light is not a guarantee under the full changing climate.

Pre-action UI explicitly says75% cover destruction, up40°C heat, possible rabbit
death, external destruction and no guaranteed recovery. Origin button disabled
and engine independently rejects. Brief charcoal ellipse is appropriately an
accepted-action marker, not a persistent burned biome or flame simulation.

## Requested completion/repair gates
1. Real exported stella_god_action callback JSON/state/effect evidence and native
   screenshot before restore; direct applyGodAction alone is insufficient for
   the complete UI contract. Reject after success must clear marker/lifetime.
2. Invalid kind>2 currently returns before applyGodAction, retaining an earlier
   marker. Clear transient receipt/effect or narrow rejection-clear claim.
3. Precision failure text currently always describes a deep-water Wave, even
   for Scorch. Use kind-specific or neutral truthful message.
4. Tiny subnormal cover can round quarter-cover to0;75% claim should be protected
   by representability rejection or describe actual fraction. Ordinary cover
   operates as intended; requested focused boundary test rather than a broad
   model change.
5. Native first-run save alias failure retained in results/native.log; corrected
   serialize/parse fixture must finish and record final state/save/animal results.
   WASM reported passed by worker, not a browser gameplay claim.

No new combustion/carbon ledger is claimed or expected: Sandbox cover was not
carbon mass. Wetness predicate means external surface water only, not measured
plant fuel moisture. Real Origin combustion remains explicitly out of scope.

## Final checkpoint review: ACCEPT for integration
Reviewed stella-scorch-checkpoint final source/evidence and byte-matched action/
visual source against stella-fire-v30. Independently reran39 visual/action/model
and37 precision/import tests against full candidate (compact checkpoint alone
requires baseline imported simulation files, as expected for a narrow overlay).

All requested gaps closed: invalid-kind clears transient receipt/lifetime;
non-wave precision message is truthful; next_cover<=0 or wrong fractional removal
rejects atomically. Native final log includes actual exported JSON, pause/save
exactness, success→wet rejection exact state/no effect, invalidkind clear, and
original complete world restoration. Earlier harness failures retained/disclosed.

Viewed final portrait accepted/rejected PNGs: actual localized charcoal ellipse
with orange rim appears beneath the plant and is absent after rejection. No
flames or unsupported persistent burn-state. Landscape centered marker is clipped
by correct UI-exclusion rule, not a model failure or release blocker. Diagnostic
surroundings look blue/purple because neighboring map water remains; selected
fixture water is0. This is controlled mechanism evidence, not natural wildfire.

Rabbit outcomes and recovery claims match actual code:275K+40K rabbit survives
with less satiety67.14 vs89.64;295K+40K rabbit dies via existing333.15K threshold.
Controlled favorable vegetation update grows remaining0.2cover to0.70903546;
not a promise of future recovery in changing climate. No new fire adaptation,
combustion chemistry, tissue moisture or Origin fire claims.

Recommendation: accept bounded Sandbox Scorch for v32 integration, conditional
on parent completing combined-main build and host review. No main edits here.

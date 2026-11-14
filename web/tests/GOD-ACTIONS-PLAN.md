# God tools: isolated candidate, not integrated or released

`src/god_actions.zig` provides explicit one-shot actions only. It never schedules
itself, changes pause, selects a target, creates organisms or advances time.

## Wave
A selected donor transfers at most 25% of its existing water, capped at 1 m
of depth-equivalent, to its immediate neighbors (at most six). Only seven
water entries can change. Duplicate/invalid indices, nonfinite water and
sub-resolution transfers fail before mutation. Water mass is conserved within
floating-point tolerance. It is not terrain erosion or a complete wave-momentum
model; subsequent normal hydrology and ecology determine flooding consequences.

## Lightning / heat strike
A selected patch receives an externally supplied heat impulse of at most 40 K,
capped at 500 K. The caller must supply the real current engine heat capacity in
J/K. The receipt reports actual delta K and added joules. This is a disclosed god
power, not a scientific lightning-energy simulation. No biomass or animal is
silently killed by the action. Existing temperature-dependent ecology reacts on
subsequent simulation steps, and heat may dissipate first. Integrated tests must
establish what users can actually observe before claiming ecological damage.

## Receipt and integration
`Receipt` has kind, failure, success(), count, affected[7] (cell, water_mass,
temperature_k), moved_mass, heat_joules. Animate only successful receipts and only
these affected cells. No casualties field: action execution cannot know future
deaths. Failed receipts must not animate success. One deliberate tap, stale
expected-selection guard, UI disclosure and accessible outcome text required.
Use existing serialized waterMass/temperature, no save schema changes.

## Executed and pending
26 isolated unit/imported ecology tests pass. Wave conservation/bounds/stale/NaN
atomic failure; heat energy/bounds/stale/nonfinite; real Ecology.grow thermal
response and inherited microbial thermal fitness comparison tested.
Still pending: production Planet heat-capacity plumbing, generated-world paired
control runs, flood response, real rabbit response, renderer/event feedback,
mobile interaction and save roundtrip. No active main/play/shell edits made.

## Later inherited fire/drought strategy design
Do not infer fire tolerance from decorative form names. Add inherited continuous
fire-protection investment with ongoing construction/growth cost, plus a dormant
seed/propagule pool funded by real parent biomass. Maintain carbon and nutrients
across parent → dormant pool → germinated cohort. Fire oxidizes only exposed
fuel, bounded by actual oxygen; route oxidized carbon through CO2/O2 accounting,
retain unoxidized killed carbon as detritus, release associated nutrient exactly.
Protection changes survival probability/fraction, not immunity. Dormant propagules
pay maintenance, can die, and germinate only after sustained actual temperature,
water and resource conditions; no wall-clock reward or spontaneous reseeding.
Delayed fire-triggered germination requires a saved actual fire-exposure history
and inherited threshold, with migration/defaults for old saves. Separate controls
must establish cost/benefit under fire and nonfire and conservation over many
cycles. Sandbox vegetation is cover, not carbon mass; don't fabricate matching
atmospheric flux until that model has an explicit calibrated mass mapping.

## Integrated candidate update
Planet exposes its current actual heat capacity; PlayState wrappers preserve
pause/pace and store successful transient receipts for 1.2 real seconds. Main
exports return target depth/temperature and action JSON. More → God tools shows
separate explicit actions; wave reports lowered metres and neighbor count.
Precision refusals tell the player to try shallower coast; no water moves.
Shell tests cover target/receipts/dry/invalid selection. 27 god/model tests pass.
Generated-world receipt test measured total water 1645139793076.6052 before and
1645139793076.6062 after, with seven affected patches (floating-point difference
0.0009765625); 40 K heat impulse supplied 2.9387406625787085e18 J. Pause and pace
unchanged, stale target rejected. That fixture subsequently shapes a basin, so it
is receipt validation only, not downstream ecological causality. A separate
`egl-god-ecology-prepare.py` forks the same serialized day-20 world into control,
wave and heat branches for one day, and also checks a generated deep-ocean patch.

### Actual serialized day-20 paired results
The same actual generated Origin world snapshot (not synthetic organisms) was
restored separately for untreated control, Wave, and Lightning, followed by one
simulated day through `state.update`. Initial selected biomass was 0.0054616746
kg C/m² and temperature 290.6838 K in all branches.

- Control: biomass 0.0049817897, temperature 290.56827 K, water 13.484698 m.
- Wave: seven-cell transfer of 7669.546875 engine mass units; biomass 0.00503208,
  temperature 290.56653 K, water 12.964333 m. This test does **not** show harm from
  the wave; redistribution persists and normal ecology continues.
- Lightning: one-cell input 1.735215715851436e19 J; biomass 0.0034666732,
  temperature 329.16965 K, water 2.0266619 m after a day. In this fixture it causes
  greater biomass loss and drying than control, not immediate guaranteed death.
- Deepest generated ocean patch: wave succeeded with 7680 mass units moved.
  Extreme precision-limit unit fixture instead rejects without mutation.

No rabbits existed in this Origin fixture, so animal consequences remain
unverified by this test. No sustained fire, erosion or new biological strategy
is implemented. Full logs: test run produced GOD_BRANCH_DAY21 records.

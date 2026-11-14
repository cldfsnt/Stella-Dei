# Fire effects: bounded candidate proposal, not implemented

## What the current game actually models

Origin has aquatic producer/consumer cohorts with explicit kg C/m² biomass,
support as a subset of biomass, detrital carbon, mineral nutrient and atmospheric
CO₂/O₂. The six visible forms are aquatic architectures, not trees or terrestrial
fire-adapted species. Current production has no tissue-water storage, fuel-drying
history, bark, seedbank, roots or inherited fire response.

Sandbox has dimensionless vegetation cover, thermal plant traits and rabbits with
food/energy/health logic. That cover cannot honestly be converted to kilograms of
fuel, oxygen demand or atmospheric emissions without a new mass model.

## Recommended staging

1. Keep Heat available for ponds. Fire on submerged Origin cells should reject
   explicitly, without heat, mortality or animation. Never show burning water.
2. Before Origin ignition, define real combustible dry matter and a moisture rule.
   Surface water zero alone is insufficient evidence of dry living tissue. The
   separate water-reserve candidate may provide tissue hydration, but detrital
   drying still needs definition. Do not infer fire resistance from the existing
   structure trait (currently it affects support, desiccation and architecture).
3. A narrowly testable carbon-combustion helper can be developed before ignition
   is enabled. Inputs are explicit eligible fuel amounts and available oxygen,
   not a guess from graphics. Output is a proposed transaction/receipt. Parent
   validates and commits atomically only after all checks succeed.
4. Sandbox may get an explicitly labeled **Scorch** intervention: reduce actual
   cover and apply accounted external heat, then existing food loss and thermal
   stress affect rabbits. Do not claim a carbon-conserving fire simulation or
   immediate rabbit kills. Keep this distinct from Origin chemistry.

## Origin combustion transaction contract (proposal)

- One selected cell; stale target, invalid/nonfinite values, submerged patch,
  absent eligible fuel or insufficient oxygen reject without mutation.
- Consume actual eligible carbon, bounded by request and oxygen/stoichiometry.
- Per carbon consumed: oxygen mass decreases 32/12, carbon dioxide increases
  44/12. Carbon balances across live/detrital/atmospheric compartments.
- Biomass removal reduces support proportionally; support is not extra fuel.
  Removed live tissue releases its bound nutrient into mineral nutrient. Detritus
  carries no additional bound nutrient under current model, so never double-credit.
- Preserve surviving cohort lineage and inherited traits. If an individual cohort
  reaches zero, clear it and notify the existing lineage-loss observer. Do not
  arbitrarily wipe subthreshold survivors as part of combustion accounting.
- Heat is separate: report externally supplied ignition energy and any modeled
  released energy distinctly. Until a justified fuel-energy model exists, omit
  combustion heat, rather than reuse Lightning and label its arbitrary heat fire.
- No global balancing/clamping to hide rounding. Quantize/read back actual f32
  decrements, compute gas/nutrient flux from those actual decrements, and reject
  transfers whose oxygen budget is exceeded after quantization.
- Dryness/reserve changes must coordinate with the reserve worker. No schema
  changes merely for transient flashes or receipts.

## Graphics / interaction

Successful actual combustion: brief low orange patch-local ember outline and a
small smoke pulse; only at affected cells, no fullscreen flash or generic life
loss claims. Receipt: 'Carbon burned ...; O₂ used ...; colonies lost ...'. For
Sandbox Scorch: report cover removed/temperature changed, not carbon burned.
Submerged rejection: blue extinguished icon plus reason, not flame animation.
Do not share cyan arrival diamonds, amber colony-loss X, or green seed markers.

## Tests required before integration

- Full carbon/oxygen/CO₂ mass bookkeeping and nutrient conservation; support
  subset invariant; gas updates scale correctly from kg/m² to global averages.
- No-fuel, all-water, no-oxygen, stale and invalid requests atomically unchanged.
- Partial fuel and oxygen-limited requests; tiny f32 fuel/large atmospheric
  backgrounds; repeated operations cannot make negative reservoirs.
- Equal exposure with equal actual fuel yields equal chemical removal regardless
  of drawn morphology. Differential responses only where real modeled traits or
  environments explain them; no guessed resistance bonuses.
- After event, survivors may recover only by existing resource-paid growth;
  extinct cell stays extinct unless actual neighboring propagule arrives.
- Native + browser receipt/effect agreement and no effect after rejection.

## Future inherited strategies (separate research/design)

A seedbank would need real reserved carbon/nutrient/water, paid reproductive
allocation, viable age/decay, real establishment checks and mutation/inheritance.
Protected recovery tissues similarly need maintenance/space costs and actual
survival protection with a justified exposure model. Neither may generate free
replacement plants or grant immunity by naming a morphology 'fire resistant'.

## Implemented foundation (isolated, after scope approval)

`combustion.zig` now provides a pure f64 transaction planner with explicit kg/m²
inputs, four live compartments, support subsets, detritus, measured physiological/
detrital/external water, oxygen and CO₂. Seven tests pass (`tests.log`).
Rejected plans return the exact original state and no effect receipt.

Ignition is deliberately conservative: any external water/ice, any measured body
or detrital water, or unknown moisture rejects. No arbitrary wet-tissue threshold
or free evaporation is inserted. Therefore this helper is NOT yet a usable Fire
button for current production aquatic life. A future adapter must obtain actual
moisture rather than default absent fields to zero.

Accepted plans use actual reservoir decrements, enforce requested/O₂ budgets,
release live-bound nutrients, reduce support proportionally, and report chemical
fluxes. Large-background transfers that fail representability checks reject.
Repeated-operation tests cover no fuel regeneration or negative oxygen. Native
engine f32 mapping, global-average gas conversion, lineage-loss notification and
reserve integration still require separate tests before any production mutation.
No graphics, heat, Sandbox scorch, schema changes or deployment were added.

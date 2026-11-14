# Proposed next ecological states: conserved water first, distinct fire strategies later

**Status update: Stage A reserve-only prototype is implemented and tested in the isolated lab, not deployed; numerical bridge review is ongoing. Stage B seed/fire strategies remain design only.** The current shoreline experiment remains isolated and unaccepted for release. Drought and fire functions below are proposals, not completed game features or validated species physiology.

## Why a water reserve is needed

The coupled shelf actually alternates wet/cold night and dry/hot day. Daily observations had misleadingly sampled only a wet phase. A real descendant grew while daylight and liquid overlapped, then died. Nonlinear protective dormancy extends survival but does not create sustained establishment on this harsh fixture. A finite, displayed physiological water reserve is a more defensible next mechanism than repeatedly reducing environmental penalties.

## Stage A: physiological water reserve (proposed save version 7)

### State and units

- `Cohort.water_reserve`: kg H2O per square metre, separate from kg C/m² biomass. It is neither carbon nor a biomass multiplier.
- Prefer a distinct inherited `water_retention` trait in [0,1], rather than making structural toughness confer every strategy. Retention reduces water loss at a cost to maximum photosynthetic uptake. Initial simple founder value zero; reproduction mutates it normally without assignment/unlocks.
- Capacity depends on actual living biomass/support and is finite. Parameters remain phenomenological and must be calibrated against the measured environment trace before full-world acceptance. No promise of survival at every capacity/temperature.
- No soil-water store in this first stage. Only actual surface liquid can recharge tissue. Rainfall history and atmospheric humidity are not substituted for liquid.
- `Environment.liquid_available` uses kg H2O/m², converted by Planet from real water mass using the existing mean-cell area. Optional relative humidity may regulate loss only if sourced from the existing physical humidity function; it cannot create water.

### Ledger and update ordering

1. Determine finite capacity and existing reserve; any overflow caused by carbon loss must be explicitly returned, never clamped away.
2. Calculate all cohorts' liquid uptake demands simultaneously, scale by actual available surface water, then allocate. Do not let array order grant first access to water.
3. Evaporation/transpiration subtracts actual reserve and adds the identical mass to local atmospheric vapor. High retention reduces this loss but also imposes carbon-uptake cost.
4. Photosynthesis requires usable hydration, light and temperature. If surface water and reserve are both zero, fixation is zero. Frozen water/reserve cannot fund fixation. Carbon growth is capped by an explicit finite water-use demand, in addition to carbon/nutrient/light limits.
5. Continue maintenance and eventual drought/cold mortality. Stored water is not free carbon or indefinite dormancy.
6. Death/failed establishment returns remaining reserve to surface liquid (or an explicit tracked vapor path). Never discard it when clearing a cohort.

Extend Flux with `water_taken`, `water_evaporated`, `water_returned`, all kg H2O/m². Planet subtracts/adds their converted amounts to `waterMass`/`waterVaporMass`. Chemistry remains the game's existing coarse carbon model; this stage tracks hydrological uptake/transpiration, not new unbalanced photosynthesis chemistry.

### Every cohort operation must conserve reserve

- Reproduction transfers the donor's proportional reserve with paid offspring biomass; it must not copy the reserve.
- Whole-cohort relocation moves reserve with identity, paying existing carbon costs and explicitly returning any capacity overflow.
- Grazing: consumed tissue's water must be transferred to the consumer up to capacity; all remaining consumed water returns to a tracked environmental compartment. Predator/prey order must not duplicate water.
- Support respiration, growth, starvation, failed-propagule clearing, reset and seed actions must have defined water handling.
- Seed remains donor/resource-funded; a newly introduced founder starts with zero reserve and absorbs only real local water during update.

### Save/migration

Version 7 adds f64 reserve and f32 retention to cohorts, plus nonnegative f64 surface/vapor numerical carries per microbial cell. Carries remain strictly below one f32 bulk-water quantum and are not soil or physiological reservoirs. Legacy carries default to zero. Legacy ≤6 saves default both to zero, preserving previous carbon/nutrient totals; aquatic cohorts may recharge next simulation step, but dry cohorts do not receive invented reserves on load. Validate finite/nonnegative reserve, trait range, and capacity bounds before mutation. Preserve sparse slots and lineage identity. Exact v7 roundtrip, all prior migrations, invalid-save atomic rejection, and reset behavior are required.

### UI contract

Show actual reserve, capacity and current hydration, plus why growth is limited: dry, frozen, dark, nutrient-limited or thermal stress. Explain that high retention sacrifices rapid uptake. Surface depth zero with positive reserve must be visibly intelligible rather than appearing to grow from invisible water. These are producer strategies, not yet full rooted land plants.

### Acceptance tests before release

- Closed water ledger: surface + vapor + all living reserves conserved through uptake, loss, condensation-compatible flux, reproduction, grazing, movement and death.
- Existing carbon/nutrient conservation unchanged; water is never counted as carbon.
- Zero total usable water ⇒ zero fixation; frozen hydration ⇒ zero fixation; finite drought ultimately kills.
- High retention outperforms low retention in measured wet/night–dry/day cycles; low retention is faster in reliably wet conditions. Neither strategy dominates every habitat.
- Replay measured depth/light/temperature with exact genotype snapshots, not defaulted missing traits.
- Actual one-founder coupled world: real mutation, donor-funded dispersal, shore survival and reproduction over many daily cycles without hidden irrigation or assigned traits. Include counterfactual reserve-disabled control and at least another habitat/seed; do not tune only for one lucky fixture.
- No seedbank, fire or extra geometry changes bundled until this ledger and ecological path pass.

## Stage B: distinct conserved fire/reproductive strategies (later save version)

These should be separate allocation/reproductive strategies, not a universal hardiness number:

1. **Protected-root resprouting:** root/storage carbon is a paid subset of producer biomass, not additional mass. It limits above-ground collecting tissue. Fire can spare some roots based on explicit heat exposure, but regrowth transfers real stored carbon/nutrients into shoots. Repeated burning depletes reserves and can kill the lineage.
2. **Heat-opened cones:** mature plants invest carbon/nutrients into closed propagules before fire. Heat releases existing seeds; it does not create offspring. Burning before reproductive maturity leaves no seed source.
3. **Buried heat-triggered bank:** a finite dormant propagule compartment carries inherited genotype, lineage, carbon and bound nutrients. Burial/protection is paid, decay is positive, and sufficiently severe heat kills seeds rather than universally stimulating them.
4. **Delayed germination:** funded seeds age and wait for actual moisture/temperature conditions and inherited timing response. A timer may make existing seeds eligible, never create a plant from nothing. Repeated fires before seed production/germination can prevent recovery.

A seed bank needs explicit state, capacity, allocation costs and save migration. Birth/lineage IDs should be allocated once when a funded propagule forms; germination moves its mass into a free active slot and preserves identity, without double-counting birth or resurrecting an extinct unfunded lineage. Failed germination returns mass to detritus/nutrients. Germination competes for real space and water.

Fire itself requires a resource ledger: burnt carbon splits into tracked atmospheric carbon and detritus/char; nutrients return to tracked ash/soil nutrient pools; combustion respects available oxygen. Root and seed survival must depend on a modeled heat exposure, not a blanket fire immunity flag. Persistent char/ash or fire-dose history would require explicit state or a documented derived approximation.

## Implementation boundary

Do not implement these new states until parent approves this state/ledger/migration plan. The direct-controls production release remains separate. New reservoir acceptance cannot be replaced with hand-placed thriving plants or edited biological traits.

## Numerical conservation correction

Bulk hydrology remains f32 in engine mass units. Biological water flux/reserves use f64 kg/m² with a saved sub-quantum remainder per surface/vapor field; climate sees bulk until re-quantization. Direct water edits reconcile carries before immediate save. See web/tests/WATER-PRECISION-QA.md for the measured old-bridge failure and corrected timestep/depth tests. Do not infer exact full-climate conservation from biological-bridge tests.

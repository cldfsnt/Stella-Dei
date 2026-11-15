# Paid resting-pool null model: research only

Files: `src/experimental/quiescence.zig`, `src/qa_quiescence.zig`.
No production biology, save schema, UI, mutations or deployment changes. This is deliberately a **negative feasibility assay**, not inherited dormancy or full scheduler integration.

## Core behavior and model
Actual `Microbes.step` governs mortality, thermal/dry damage, recycling and active growth in both compartments. Resting light and carbon uptake are zero; it receives NO lower mortality, heat resistance, seedbank or survival bonus. Same phenotype and lineage in active/rest sides, each explicitly owns living biomass. Transfer spends10% of transferred carbon via finite oxygen-limited respiration and releases its bound nutrients once. No O2 refuses transfer atomically.10% is an experimental cost parameter, not calibrated biology. No automatic response to ignition or no-cost return.

Initially0.2kgC/m² living biomass,0.1 available nutrient,10carbon-equivalent gas units each. Resting treatment pays to move0.1 into resting pool, receiving0.09. No ongoing resting-specific basal maintenance is invented. Only unstructured, nonfeeding, nonmoving phenotype accepted; support, organization, feeding, mobility and extra active slots are excluded. Trait propensity is NOT implemented/inherited: transfer schedule is experimental assignment.

Carbon includes both living pools, both organic matter pools and gas. Nutrient includes free nutrients plus all living tissue once. Detached core probes calculate active potential and mortality; global space includes resting biomass before the real active fixation allowance is passed to core. Probe-only abundant resources are never committed to the state or counted as experimental supply. Resting mortality is processed first; its nutrient release is shared with active pool. Rest detritus is merged only AFTER active processing, avoiding double decay in one step. This sequential operator imposes an O2 allocation order, not a fair multispecies scheduler. All units retain core conventions.

## Executed assays
Five tests plus imported core tests, ReleaseSafe Zig0.13.0.12 ecological runs (six environments × active/rest assignment),30days each,1440s ticks; transfers, zero lineage/invalid state, zero O2 refusal, extinction and small-active cutoff tests. Added10-day darkness/no-O2 case: no photosynthetic replenishment, oxygen stays zero and waking cannot be paid. Bright initial-zero-O2 treatment correctly generates oxygen through photosynthesis; it is NOT described as continuously anoxic.

Environments: stable1m wet303K; same with days2–5 fully dry; permanently dry;400K wet; initially zero O2; initially zero free nutrient. No external resource refills. Pulse return to wet is controlled environment, not full hydrology.

## Results and limits
- Stable wet day2 total living: active-only0.9706068 versus paid-rest0.937939305. Cost visible, no universal advantage. Day30 totals0.9861876 versus0.98577317, with inactive share still present.
- Three-day complete dryness: both treatments reach zero living tissue and remain extinct after rewetting. Same outcome under permanent dryness and400K. No quiescence rescue manufactured.
- Tiny0.002 active pool is destroyed by real core cutoff (applied independently to BOTH compartments) even with substantial resting tissue. Test exposes this. Later active mass can only be purchased from still-living rest; both pools gone can never reactivate. This cutoff coupling must be resolved explicitly in a production model, not hidden by restoring old cohorts.
- All declared per-step carbon/nutrient budgets pass1e-4/1e-5 absolute bounds. Baseline active-only core accumulates about8.53e-5 carbon and8.24e-6 nutrient floating-point error over30days, near these bounds. Thus NOT exact numerical closure and not evidence of arbitrarily long-run stability. No new tolerance was loosened to hide a failure.
- No offspring, mutation, evolved resting trait or demonstrated persistence benefit. Read-only probes do not consume live RNG. No opportunity to claim plants, fire armor or real dormancy.

## Important feasibility blocker
Active unstructured core has no explicit basal energetic respiration/starvation draw. Growth-rate subtraction lowers potential uptake but does not spend existing carbon or create maintenance CO2. Consequently reduced maintenance in resting tissue has no honest starvation benefit to compare with. Adding lower mortality to rest would assume the hoped-for benefit. Common active/rest energy costs must be specified, funded and tested before asserting a meaningful metabolic persistence strategy. Existing paid structural dry protection must also be distinguished from any new trait.

## Requirements before full scheduler integration
1. Cohort schema: total biomass, support and resting fractions with disjoint bounds; establish active/rest mortality and shared energetic maintenance without creating carbon, O2 or nutrient. Legacy saves default rest=0; schema validation and roundtrips mandatory.
2. Photosynthesis/light/space and canopy geometry use actual active tissue. Rest still occupies capacity; no hidden free space. No active support geometry benefit from fully inactive tissue without a defined paid mechanism.
3. Predation must consume compartments explicitly with matching nutrient/respiration; dormant tissue cannot be unconditionally unattackable. Shared finite O2 allocation must be simultaneous/fair enough to avoid slot-order advantage.
4. Reproduction, dispersal and moves transfer funded active/support/rest material; resting alone cannot earn growth credit or produce free daughters. Inherited bounded propensity mutates through genuine donor rules; lineage ownership survives only while some living compartment exists. Extinction and0.0025 cutoff policy must apply to total lineage and establishment explicitly.
5. Save/load, counters, inspector and renderer distinguish active/rest tissue, never resurrect cleared identity or show a new organism that was never funded.
6. Compare paired resources, stable versus intermittent environments, multiple genuine evolved donors and full spatial scheduler. Count descendants, extinction, timing, competition and long-run numerical drift. No prescribed winner or guaranteed beneficial disturbance.

This prototype should NOT be wired to production. It locates missing physiology and compartment integration needs without inventing an advantage.

Ownership/capacity audit: combined active+rest biomass is validated <=1.0001; two living pools with same lineage must have matching phenotype fields, otherwise transfer and step refuse without mutation. No tiny dormant-spore survival is implemented; resting core cutoff also applies. Shared initial free nutrient is0.1 in active and explicitly0 in rest, not two defaults.

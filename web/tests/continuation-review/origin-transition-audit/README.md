# Origin's missing organism transition is mechanical, not just visual

Read-only current-source and saved-world audit. No new traits, physiology, simulation run or production edit. The30/60day natural saves and normal-grazing90day continuation have explicit hashes in census.json. They are one evolving history across earlier versions, not a current-version rerun or selection experiment.

## What actually evolves now

Cohorts inherit optimum, efficiency, structure, organization, feeding and mobility through small mutations plus existing rare larger mutations. Organization is bounded0–.7; structure/feeding/mobility0–1. Cohorts divide/propagate paid tissue; each patch has four cohort slots. There is no inheritable organ graph, individual body-size lifecycle, root-water compartment, sexual reproduction or taxonomic transition state.

Actual support consumes carbon that otherwise forms collecting tissue and pays respiration. Height and shared-light interception are continuous functions of real support/fronds/efficiency/structure. Feeding consumes other cohorts and pays growth/mortality costs. Mobility is a coarse neighboring-patch frond relocation toward more prey, not animated individual locomotion. These mechanisms are real, but do not amount to rabbits or vascular plants.

|Day|Living cohorts|Aquatic form classes present|Largest modeled height|Median modeled height|Vegetation / rabbits|
|---|---:|---:|---:|---:|---:|
|30|18|5|7.64mm|0mm|0 /0|
|60|64|6|34.65mm|3.26mm|0 /0|
|90|41|6|37.70mm|9.07mm|0 /0|

Heights are a read-only float64 evaluation of the exact production expression, not a new native bitwise oracle. Day90 feeding ranges.0515–.3778, organization0–.2605, structure0–.1636; phenotypes are changing, not all identical clones. Full ranges/forms and dominant-patch classifications retained. The40962 `plants` save records are per-cell dormant Sandbox trait arrays; none imply living plants.

## Two hard boundaries

1. `photosyntheticHabitat` returns0 for depth<=0 for **every** legal genome. There is no soil moisture distinct from surface standing water. Dry mortality has a positive floor even at maximum toughness, and no dry-land carbon acquisition route exists. More generations cannot mutate around this environmental gate. A moisture-free desert should not support indefinite plants, but currently there is also no representation of a moist rooted soil beneath a dry-looking land surface.
2. Origin remains in `simulateMicrobes`; Sandbox `simulateVegetation` is a separate branch. No evolved-cohort-to-Lifeform conversion exists. Origin refuses sandbox animal placement and never creates rabbits. Waiting/fast-forward cannot reach an unimplemented bridge, and adding a rabbit icon would not create evolved animal biology.

## Graphics reality

`producerForm` maps actual support/organization/structure/efficiency to six aquatic classes (mat/cushion/rosette/ribbon/branching/canopy); these category boundaries do not unlock new physiology. Rendering chooses one dominant cohort per patch by support then biomass, draws its36px Blender atlas silhouette (vector fallback), color from thermal optimum, and a small amber dot if any cohort has recorded feeding. At most64 de-cluttered glyphs are drawn. Thus four functional lineages in a patch are not four distinct animal/plant bodies, and inherited feeding/mobility has no dedicated functional-organism body representation. That is a visibility limitation, but the hard ecological boundaries above cannot be fixed by graphics alone.

## Proposed next substantive test: paid water retention before terrestrial forms

Do not add a forced 'plant' unlock or convert arbitrary generation numbers to animals. First test whether a **finite, conserved root-zone moisture mechanism** can support a real aquatic-to-moist-land tradeoff.

Proposed isolated feasibility assay, requiring parent scope approval: retain actual evolved whole phenotypes; compare an unchanged aquatic control and an explicitly modeled finite moist-substrate state with the same total available water. Root/retention tissue must be paid by reallocating existing organism carbon, reducing collecting or aboveground-support capacity rather than adding free benefits. Partition existing water, do not invent moisture; no automatic refill. Track retained water, surface water/vapor, any transpiration and all C/N/O2 receipts. Zero storage/zero root tissue must provide no protection; persistent drought must eventually exhaust the finite reservoir. Compare repeated wet/dry exposure against continuously wet exposure with equal supplied-water budgets; include an all-dry negative control. No outcome or 'stronger' winner is prescribed.

This is larger than a UI patch: the model currently has no soil/organ-water storage. A valid candidate needs explicit water representation, transfer laws, save semantics and bounded numerical tests before an actual coupled-world invasion/establishment test. Start with one specified retention allocation versus zero, not a tuned sweep; restore unchanged phenotypes and resources between arms. Any improved persistence is conditional on the new hypothesis until actual inherited allocations evolve and pay their costs. No root trait or new physiology implemented here.

An alternative purely visual change could make current aquatic grazers easier to recognize, but must remain labeled aquatic cohort morphology, not the requested autonomous evolution into land plants/rabbits. The core capability gap should be acknowledged rather than disguised as polish.

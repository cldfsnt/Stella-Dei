# Proposed inherited-root intervention gate (NOT EXECUTED)

This is a separate practical mechanism question after dbd8648, not an extension until the day30 result becomes favorable. Production and the frozen beta law remain unchanged.

## Deterministic subject and read-only feasibility

From the complete day30 checkpoint, choose the lowest living lineage ID with positive root_fraction and support_mass: **524**, parent319, generation3, cell18327, slot2. It has root allocation1/32, biomass0.0037663544062525034 and support0.00008706833614269271 kgC/m². The allocation was inherited through actual paid births, not assigned. Current soil is0.9999940591328513 kgH2O/m²; temperature296.555023K; actual logged standing depth0.46777409315109253m. The native standing amount is3587.60693359375 units of10^9kg. Mean patch area is7.6695296e9m² (planet radius5000km, not5000m).

The existing public selected-patch target API accepts target0m, with an expected-selection guard, and writes only that patch's standing water. It does not empty soil, supply water, change terrain or create tissue. A single target0 action therefore replaces repeated 1m taps. This is an explicit, very large-area external water removal, not natural drainage. Record actual endpoint native water difference times10^9kg, separately from its rounded returned depth.

The last recorded biological light was0.90435648; that is historical and is NOT a substitute for checking current light in the actual simulation geometry.

## Proposed fixed protocol

1. Load the unchanged day30 checkpoint using the proven beta adapter. Freeze ID524 and cell18327 before any advance; never retarget another survivor.
2. At the current state (wait index0), compute the same geometric biological surface-light expression used in simulateLandAtmosphere. If nonpositive, advance actual1440s ticks, checking after each, up to60 ticks. Require the same ID still alive on the original patch with positive paid support/root, finite soil in(0,1], and valid finite environment. Death/movement, invalid state, exhausted soil or no light by60 is a setup failure, not a reason to select another subject.
3. At the first positive-light state, pause both eventual arms identically and call the actual selected target0m action once. Verify standing water becomes0, actual removed amount is logged, and all other physical fields/soil/cohorts/RNG remain unchanged. Save this common post-action state. No repeated drainage, refill, nursery, transplant, fertilizer or reseeding.
4. Branch into two arms: unchanged actual mutant versus an explicitly counterfactual ablation of ONLY ID524 root_fraction to0. Total biomass/support, lineage, all other traits/resources/RNG/config stay identical. Thus ablation returns allocation to aboveground tissue and changes height/competition as well as uptake; it is not a pure uptake-channel deletion. No positive trait assignment. Other organisms retain their actual traits; law/mutation stays enabled, so later ablation descendants could independently mutate and must be reported.
5. Run exactly24h/60 ticks of1440s per arm, with identical original scheduler and no further player actions. Stop on nonfinite state, validation error or practical cap900seconds/512MiB log per arm. Retain failures; no extension or parameter changes.
6. Save at12h and24h; fresh-process12h continuation must equal uninterrupted24h complete state/RNG and event traces. Preserve the original day30 bytes and exact reload proof.

## Required observations and interpretation

Every tick: tracked subject/family identities and fates, support/root tissue, aboveground height, actual phase depth/light/temperature, soil before/after, bare evaporation, requested/credited root water, actual source/vapor endpoints, accepted/refused bridge budgets, h, carbon/growth/stress flux where already available. Log all births, plus total living and physical inventories. Report native-to-kg conversion explicitly and retain known global legacy transport limitations; no new whole-world conservation claim.

Immediately dry tool state is NOT guaranteed dry physiology: liquid transport precedes the beta column phase and can refill the patch before the first root request. Report that as a meaningful negative if it occurs. Do not reorder the scheduler or repeatedly drain to force uptake. A positive dose is evidence of evolved paid tissue accessing finite water under external intervention, not natural establishment, calibrated roots, selection advantage or long-term survival. Differences between arms include the declared aboveground allocation tradeoff. Zero demand, zero credit, rapid refill and decline remain valid outcomes.

No code, simulation, tool action or new biological result has been executed for this proposal.

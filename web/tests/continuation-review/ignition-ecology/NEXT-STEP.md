# Proposal only: inherited reversible quiescence, not fire armor

The controlled ignition assay found no special burn response beyond matched heating. Do not tune a fire bonus to manufacture one.

## Small alternatives
1. **Storage reserve**: divert fixed carbon from growth to metabolizable reserve. Provides night/starvation buffering, but current biomass already funds maintenance and nutrient accounting assumes all biomass has uniform stoichiometry. A pure-carbon pool requires separating that accounting and may duplicate existing biomass behavior. It would not by itself prove recovery from drying or heat.
2. **Reversible quiescent fraction within the living cohort** (recommended bounded prototype): retain a paid, inactive fraction of existing biomass during unfavorable conditions, with slower baseline maintenance but no growth, grazing or reproduction from that fraction. Returning to activity costs biomass/respiration and takes time. This offers drought/starvation persistence and slower recovery versus fast opportunists, without promising heat immunity.
3. **Dispersed dormant propagule pool**: actual persistent recruitment after adult extinction, dispersal and activation. Most directly supports seedbank-style gameplay but expands lineage ownership, capacity, saves, accounting and renderer substantially. Defer until the smaller tradeoff is demonstrated.

## Minimal prototype contract
No production implementation yet. Prototype a single inherited bounded allocation/transition propensity and a separate current quiescent mass, a subset of existing total living biomass. Keep composition unchanged so carbon and nutrient remain counted once. Active mass = total minus support minus quiescent, with validation preventing negative/overlapping tissue. Existing support geometry needs an explicit policy before coding: quiescent tissue must not still provide full activity/grazing merely because its carbon remains present.

Quiescence is paid by lost productive allocation, conversion respiration and nonzero residual maintenance. Maintenance draws actual finite oxygen; no silent ATP or O2 source. Reactivation consumes real biomass and time, only when environment permits activity. Quiescent tissue may still die under thermal extremes or extended starvation. Start with the same heat damage as active tissue; lower maintenance is not fire armor. No ignition-event trigger, resurrection from zero, free nutrient release, or hardcoded successful descendants.

Carbon released by conversion/maintenance goes to CO2 with matching O2 limit. Nutrients bound to respired tissue return once according to existing stoichiometry. Mortality transfers remaining living carbon to detritus and releases its nutrients once. Quiescent mass never adds extra carbon on top of total biomass; dead cohorts zero their compartment. Predation/dispersal must debit all participating compartments consistently and cannot export quiescent tissue as active offspring for free.

## Schema, inheritance, feedback
Requires versioned save fields/default migration (legacy quiescent mass=0; legacy trait default explicitly chosen), finite/bounds validation and exact roundtrip/refusal tests. Daughter trait inherits/mutates with existing small/rare distribution and bounds; daughter compartment funded by transferred tissue, never generated from trait value. Lineage copies/moves preserve compartment state and parentage. Initial existing cohorts must not retroactively receive free reserve mass.

Feedback: distinguish active versus resting biomass in inspector and a subtle resting glyph/color, not fake disappearance. Explain that resting colonies may resume if conditions improve, but may also die. Return-to-growth should be visible over normal simulation time and fast-forward, not immediate bonus. No claim of plants, seeds or fire adaptations when still modeling microbes.

## Go/no-go experiments
- Per-step carbon/nutrient/O2 ledgers during entry, maintenance, reactivation, death, predation and daughter transfer; invalid/tiny/extreme inputs and no-O2 cases.
- All-resting zero active uptake/grazing/reproduction, no negative compartment, no free growth, zero cohort remains extinct.
- Save legacy/new roundtrip and invalid import atomicity; pause/pace unchanged by UI inspection.
- Equal finite initial resources, paired low/high trait and actual evolved descendants, reciprocal steady-friendly versus intermittent unfavorable climate, slot swaps and multiple seeds. Expect possible costs/benefits, not prescribed winner.
- Complete Planet scheduler, natural dispersal and normal hydrology follow-up to distinguish fixed-cohort sorting from evolution. Run long enough to count descendants and extinction/recovery; no periodic gas/nutrient refills.
- Reject if quiescence wins universally, never costs growth, survives indefinitely, or only appears beneficial because controls receive worse resource budgets.

This is a manageable engineering hypothesis, not a promise of biologically complete dormancy or natural-fire regrowth. First inspect whether existing maintenance and structure already provide the same strategy before adding a new trait.

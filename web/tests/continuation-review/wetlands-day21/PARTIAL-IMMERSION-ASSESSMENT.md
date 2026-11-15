# Partial immersion: units, prior coverage and one concrete physiology question

Read-only; no new simulation, mutation change, care, runtime or production edit. Rare-root-tail proposal is held. Sources: existing law3 Wetlands preview microbes/shared_soil/basal_geometry/Planet target-depth; immutable day21 and final-demand shoreline inputs/results.

## Exact scale matters

The depth passed to physiology is kilometres. `0.0002 km` is **200mm**, not0.2mm; existing smooth aquatic transition is150–200mm. Target-depth public input is metres and stored water is f32 in10^9kg per patch. Geometric law3 immersion uses metres divided by max(actual paid architecture, biomass/100kgC/m³). Density100 is declared illustrative, not calibrated.

Actual day21 ID704@36453: B=.0148621583kgC/m², support=.000448759529, root1/32, efficiency1.02707446, structure0. Its architecture height is approximately **3.503598mm**; basal height.148622mm. The13mm figure was the maximum of OTHER logged supported-root states, not704. Its actual starting water is approximately150.739342mm. A half-height target is approximately **.001751799m** (1.751799mm). Source-equivalent f32 target conversion produces native13.43547249 and realized.001751798904m; one local native-water ULP is about1.24346e−10m. These read-only calculations are not native tool execution. Precision of stored water is not the bottleneck at this depth. World-radius terrain/head quantization and subsequent hydrology are separate issues.

## Existing moderate path, not a new discovery

The immutable524 law3 1mm arm began at approximately80.84% geometric immersion (architecture1.237008mm). It then evaporated/refilled under the real solver, became dry by tick2 and died2.8h. The earlier10mm arm began fully submerged and dried by tick5, dying5.6h under law2.100mm persisted24h but remained submerged with zero root demand. Therefore another arbitrary0/1/10/100mm sweep would duplicate evidence. Half-height704 would differ in subject, community and maturity; it would not establish that partial immersion had never been tested.

## Specific mismatch worth a focused test

Current root demand is explicitly only the exposed fraction `(1−I)`, where I is geometric immersion. Its funded signal h is credit divided by max(entry exposed-demand,current exposed-demand), never a free tissue-wide dose. Mortality already blends wet fraction as `I+(1−I)*h` (algebraic expansion of its two existing blends). But growth uses `max(existing film habitat,I,h)`. When0<h<I<1, real paid root water changes mortality yet contributes ZERO photosynthetic habitat. AtI=.5,h=.2, the funded exposed contribution is.1, while current max remains.5 instead of.6. This is a coupling inconsistency/question, not proof that the ecological model must have a particular empirical response.

One small prospective new physiology law could use:

`growth_habitat = max(existing_film_habitat, I + (1−I)*h)`.

Keep root demand, ownership, actual credit, denominator guard, water debit, bare evaporation, mortality and all growth C/N/space/light costs UNCHANGED. Do not use `immersed=max(film,I)` in the blend, because filmProtection is not an independently quantified wet fraction. The proposed maximum preserves that old adaptation as an alternative rather than double-counting it. AtI0 this is exactly the old max(film,h); atI1 it is1; withh0 it is exactly max(film,I). No new benefit at fully dry/full-submerged/zero-credit endpoints. This is a new declared response law, not a retroactive repair of historical results.

## One bounded next gate, only if authorized

First fixed actual-core controls at I=0,.5,1 with zero/fractional/full funded h, wrong owner/zero demand and source/entry caps; verify old law byte-exact, no additional water, and actual growth still pays C/N and support costs. A tiny fixed arithmetic test can establish whether the zero marginal growth response really exists without another world horizon.

If an actual-world path is then requested, use the already deterministically selected704, no new phenotype search: unchanged day21 control; one half-height target with actual704; same target with root0 ablation.24h and12h restart, no repeats/care/clamp, no waiting for favorable weather. Derive the target ONCE from the original actual704 architecture and record its f32 metres before execution; do not recompute as biomass changes. Root0 changes aboveground geometry, so it is an allocation counterfactual, not uptake-only deletion. Record each phase depth/I, soil, entry/current demand, credit/h, film/max/blended habitat, actual growth/grazing/loss and whole selected community. Natural rapid drying/refill is a valid outcome. This three-arm old-law path would diagnose usable exposure; it would not test the new blend unless a separately explicit law-pair scope is approved. Do not conflate those questions or run both automatically.

Practical decision: inspect/test this exact partial-immersion growth coupling before adding mutation search. Even a coherent correction may not overcome heat, grazing, low support, disappearing film or the establishment cutoff. No sustainable terrestrial path is currently demonstrated.

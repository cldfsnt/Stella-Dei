# Proposed next model milestone: from simple life toward ecosystems

Status: design only. The current plant/rabbit sandbox and its guidance are a foundation, not SimEarth-like macroevolution or a finished game. No large rewrite or new biological system has been started.

## First playable increment

Add a separate **Evolution world** starting with a seeded population of simple photosynthetic microbes in suitable shallow water. Keep existing **Habitat sandbox** and all legacy worlds playable. The player changes water, terrain and climate, watches actual population growth/spread and inherited traits, and learns why a population thrives or declines. Do not claim abiogenesis: the player seeds already-living organisms.

Implement one bounded production model before promising multicellular plants or animals:
- Per-cell microbial biomass plus a small bounded number of lineage cohorts, each with inherited thermal optimum/tolerance and light-use efficiency. Cohort birth events introduce small seeded mutations; mortality and reproduction depend on local conditions and energy/resources. Avoid a single globally overwriting genotype that can fabricate selection.
- Growth requires energy and limiting resources. Photosynthesis exchanges bounded carbon/oxygen amounts using the same explicit mass units as the atmosphere; uptake cannot exceed available resources. Habitat suitability includes water depth, temperature and light. No guaranteed growth timer.
- Reproduction/spread uses neighboring cells with available habitat, carrying capacity and an energy cost. Trace actual parent/child lineage and reproductive generation. Trait distributions, not merely maximum generation, demonstrate adaptation.
- Rendering: visible microbial mats whose area/intensity follows real biomass, selected-cell population/trait/energy information, and a small lineage history view. A population is not an individual drawn microbe. Give clear environmental warnings and modest, readable on-screen activity without faking ecological movement.
- First goal is ongoing: establish a reproducing population, inspect descendants, change an environmental condition and observe selection/recovery. No 'plants unlocked' badge until a plant lineage actually exists in a later model.

## Subsequent functional transitions

A second increment can model a cooperative/multicellular photosynthetic form: cooperation/structural allocation has an energy cost but may confer environmental protection or habitat access. A transition is an authored game-model rule requiring heritable traits, successful reproduction and viable resource conditions, not a decorative animation triggered by elapsed time. When the resulting lineage actually establishes, its dispersal tool becomes available. Explain this as a simplified evolutionary sandbox, not a scientifically complete account of the origin of plants.

A later consumer increment can introduce heterotrophic traits with real food/oxygen requirements and the costs/benefits of mobility. It must feed from actual producer biomass and reproduce through real energy budgets. The existing rabbit feeding/gestation framework can be reused as a sandbox consumer demonstration, but a microbe must not silently 'turn into a rabbit' at an arbitrary counter threshold. Early consumer forms should be visually and mechanically appropriate. Existing modern plants/rabbits remain explicit sandbox organisms.

## Architecture and persistence

Separate life models from rendering and guidance. A fixed or capped small cohort count per cell keeps 40,962-cell browser worlds bounded; cohort merging must preserve biomass and documented trait moments rather than silently discard diversity. Prefer explicit structures and pure update functions that can be tested without graphics. Reuse actual climate/water fields and deterministic PRNG state.

Version saves with explicit world mode and new microbial/cohort/resource state. Old saves migrate to sandbox with their existing plants/rabbits unchanged. Do not reinterpret old vegetation as microbes or resample old topology7 worlds. Exact new-mode save/restore and old save compatibility are acceptance gates.

An accelerated simulation clock is a gameplay abstraction. Do not label days of microbial selection as a realistic million-year macroevolution timeline; any geological-timescale mode requires separate explicit framing and numerical integration.

## Required evidence before shipping the first increment

1. The actual rendered engine starts with only simple-life seeds, with no hidden vegetation/rabbit population or forced completion counters.
2. Suitable habitat supports resource-limited reproduction and neighbor spread; dark/no-resource, thermal and flooding changes give explainable outcomes.
3. A controlled selection experiment shows a shift in the **living trait distribution** across descendants, with a no-mutation/control comparison. Random trait variation alone is not adaptation proof.
4. Biomass/resources remain finite and bounded in an extended soak; resource accounting cannot create unlimited energy or consume negative reservoirs.
5. A real intervention scenario demonstrates decline and recovery without assigning success counts. Visual mats/lineages match actual state.
6. New-mode exact save roundtrip and old sandbox saves remain valid. Mobile footprint/startup/frame cost is measured independently; physical Android still needs direct testing.

## Tradeoff

This is more substantive than staged unlocks, but a genuinely evolving food web cannot be delivered honestly by re-labeling the current vegetation array. Build and verify the microbial increment first, then add functional complexity. Keep the existing sandbox available throughout, with its current proven tools, feedback and persistence.

# Read-only next gameplay gap, after the fixed wind trials

No additional experiment or production change. Sources inspected: current main simulation/microbes.zig, simulation/ecology.zig, simulation/foraging.zig, plus frozen wind prototype scheduler/genetics. Sandbox and Origin are different models and must not be conflated.

## What the new mechanism actually provides

Aerial allocation redirects an already earned reproductive opportunity. It does not increase photosynthesis, growth rate, reproductive credit generation or resource supply. Pioneer .5 has the same starting physiology as an ordinary founder until real packet decisions occur. Calling it a fast-growing weed would be unsupported. All42 actual wind donors in the fixed seven-day trial were chosen founders; inherited offspring existed, but none yet released wind packets. Retain that generation limit, not another extended run to force it.

The genuine result is a reach/establishment tradeoff: fewer total births, failed paid packets, broader geographic reach and modestly more survivors in this world. Local reproduction is still useful. The single deep founder's negative result shows that dispersal cannot rescue a parent that fails to earn enough growth credit.

## Existing real physiological strategy knobs

- **Efficiency** already multiplies light-dependent growth and pays a quadratic maintenance term: rate contains positive efficiency times habitat/thermal/light and subtracts .15×efficiency². It is inherited; it is not an unconditional faster-growth trait. Optical support-spread and maintenance effects also depend on it.
- **Structure** already reduces photosynthetic production by (1−.5×structure), adds mortality cost in wet habitats, and improves dry/film protection together with paid support tissue. It changes architecture continuously. Important missing connection: Origin graze currently distributes prey demand by prey biomass only; it does NOT read prey structure. Therefore Origin structure is not currently a herbivore-defense strategy, despite the separate Sandbox Tough mechanic.
- **Organization/support** allocates a share of actual paid growth into support, a subset of total carbon. This reduces active frond carbon and pays support maintenance; height/spread redistribute a finite local production budget. No separate canopy bonus or promised takeover follows from a display form label.
- **Feeding/mobility** reduce photosynthetic terms and add costs; feeding uses actual prey and oxygen, and relocation pays respiration. These offer real heterotrophic/movement strategies, not fake animal labels.
- **Thermal optimum** changes environmental match, not a generic fitness score. Light attenuates over20m while seeding accepts up to50m; seed eligibility is not productivity. This helps explain why broad coverage succeeds where a single legal deep patch can stagnate.

## Why succession is not guaranteed

Origin supports four distinct cohort slots; full slots reject arrivals instead of overwriting residents. Growth competition is within actual co-located resource/light budgets; new habitat occupation depends on paid arrival, vacancy and subsequent survival. There is no rule making Pioneer dominate early then automatically give way to tough forms. Morphology categories are read-only, not species with scripted roles.

Sandbox already has a different, explicit tender/tough tradeoff: positive plant production is scaled by(1−toughness), rabbit maximum handling by1/(1+2×toughness), and spread allocation is reduced. Its occupied replacement uses thermal suitability, not toughness-based invasion. Those outcomes cannot be attributed to Origin's structure or new wind trait.

## Most useful next bounded design question

Do not add a free growth bonus to aerial allocation. If the next substantive goal is a weedy-versus-defended Origin community, inspect a new explicitly saved law in which existing COSTLY structure affects actual grazer handling. That is a missing ecological dependency, unlike inventing another trait or scripted succession. It would require source-funded C/N/oxygen accounting, no invulnerable biomass floor, zero-structure historical parity, mixed occupied/vacant and grazed/ungrazed controls, and runtime cost review before any test. No coefficient, test horizon or production behavior is chosen here.

Immediately truthful player framing is “wind-dispersing Pioneer,” with separately observed growth, parent biomass cost, remote arrivals and deaths. Aerial allocation, paid support, grazing resistance and growth speed must not be presented as interchangeable.

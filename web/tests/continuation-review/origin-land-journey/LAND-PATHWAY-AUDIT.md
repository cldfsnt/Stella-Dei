# Exposed-land pathway: bounded read-only audit

Scope: isolated `site-tmp/origin-land-beta/src`, not production. Reviewed after fixed day30 and drain evidence (`270b154`). No simulation, rate change, or new favorable phenotype selection performed.

## Source and lifecycle

- `simulation/planet.zig:1807–1820`: paid exploratory propagules accept any finite destination depth/temperature. Dry land is not categorically excluded. The fallback neighboring reproduction path at 1824–1832 still requires `Microbes.habitable`; same-cell reproduction is tried first.
- `simulation/shared_soil.zig:13–22`: roots require warm conditions (273.15<T<355 K), depth below 20 cm, actual living support and positive allocation. Demand is proportional to exposed height, frond mass, elapsed time and light; capacity is bounded by paid root tissue and soil. Submerged tissue has zero root demand.
- `simulation/microbes.zig:46–49,65–100`: height uses actual aboveground support; root allocation reduces that support. Moist-film protection requires both paid tissue and inherited `structure`. Film contact, aquatic submergence and photosynthetic habitat interpolate continuously; there is no binary 20 cm growth cliff.
- `simulation/planet.zig:1386–1391,1746–1838`: root hydration resets before each atmosphere phase; physiology precedes relocation and births. No found route lets a new/moved cohort consume a previous occupant's hydration in that same tick.

## Negative evidence and a phase-contract risk

Day30's 5,172 root-phase records had zero demand. Even the shallow paid-support cases remained submerged: maximum paid height about 1.1944 mm versus minimum water 63.3434 mm. That outcome is not evidence of a failed small-water transfer.

`planet.zig:1389–1390` captures the environment before column processing. `capillary_bucket.zig:63–77` removes standing water before shared roots, but passes that original environment to `shared_soil.step`. Condensation/infiltration subsequently change standing water (80–99), and physiology recomputes the environment. Thus source-funded uptake and physiological use may refer to different depths. This is a phase-definition risk, not a demonstrated cause of the day30 failure.

Bounded future contract cases, only if needed: (1) standing evaporation exposes previously submerged tissue; (2) condensation submerges tissue after uptake; (3) constant dry and constant submerged controls. Record pre/root/post depth, actual debit/credit and final hydration; choose and document which phase owns exposure. Do not silently retarget depth or recover spent water by accounting correction.

The fixed actual drain test resolves the immediate ambiguity for lineage 524: all seven pulse depths were zero, seven funded credits totaled 2.545327054217191e-6 kg water/m², hydration initially about .076, and both root-positive and root-ablated subjects were absent by tick7 (2.8 simulation hours). The last living rooted biomass was about 2.98% higher. This demonstrates a small real transient benefit, not land establishment. It does not implicate the above phase-depth mismatch.

## Is a gradual wet–dry intermediate possible?

Yes as a mechanism, not yet demonstrated as a surviving player progression. Existing inherited `structure` already provides real drying tolerance:

- `microbes.zig:135`: dry mortality is `4 - 3.3*structure` per day, falling continuously from 4 to .7. This benefit is not merely a render category and does not require a new mutation law.
- Lines65–68 and132–143: with paid aboveground support, structure also improves moist-film protection, reducing drying mortality and exposure penalties. Lines95–100 retain some photosynthetic habitat in shallow water. Both protection and growth approach zero smoothly as water goes to zero, absent root hydration.
- Lines140–159: actual root hydration continuously interpolates mortality toward wet mortality and can permit photosynthesis at zero standing water. A small signal such as .076 is partial relief, not immunity.
- Costs remain real: support respiration (50,124–129), support versus frond allocation, and growth multiplier `(1-.5*structure)` (159). Increased root allocation also competes with aboveground support. Thermal mismatch, daylight, resources and grazing still matter.

There IS a hard establishment cutoff at `microbes.zig:148`: biomass below .0025 is recycled before growth. Small arrivals and the actual .003766 starting subject have little reserve above it. This is an existing explicit model rule, not proof that every drying trajectory is impossible; nor should it be removed solely to make this trial survive. Temperature boundaries and the 50 m maximum aquatic habitat are other hard bounds, separate from the continuous shallow-water transition.

Practical judgment: a moist/shallow margin with an already paid, structured lineage is the smallest plausible wet–dry intermediate to observe. Structure already supplies a genuine tradeoff; no guaranteed-success root mutation or new trait is justified. A player-facing future trial should preserve the real lineage and finite water, show measured survival/growth and current depth, and accept failure. Current evidence supports only funded roots plus transient drought relief after explicit drying, not sustained exposed-land growth or natural selection for roots. Keep this beta unexposed until its physical/performance gates and meaningful progression evidence justify otherwise.

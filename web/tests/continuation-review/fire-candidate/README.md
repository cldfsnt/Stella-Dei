# Isolated exposed-detritus ignition candidate — NOT integrated or released

Source: `src/experimental/detritus_ignition.zig`. No production import, Planet writes, UI, save-field change or deployment. This is a bounded mathematical primitive, not a complete fire simulator. A user cannot ignite anything with it in the current game.

## Contract
`ignite(*f32 detritus, *Reservoir, Input)` changes only the supplied detritus float and explicit oxygen/CO2/temperature reservoir. `preview` runs exactly the same calculation without committing it. All carbon quantities are kg C-equivalent/m². `oxygen_carbon` is the amount of carbon that the supplied O2 can oxidize, not oxygen mass; CO2 is likewise represented by its carbon content. The receipt also returns O2 mass consumed and CO2 mass added via existing game stoichiometry C:O2:CO2 = 12:32:44.

A caller must provide a real finite oxygen allocation and reconcile it with the planetary atmosphere. This helper never invents oxygen or reaches into the atmosphere. No caller exists yet. No live tissue, support, nutrient, lineage, credit or RNG pointer is accepted.

Requires exactly zero surface-water depth, positive actual detritus, positive available oxygen, temperature below500K, and finite positive heat capacity and fuel-heat parameter. Zero surface water is only a coarse exposed-surface proxy, NOT measured fuel moisture. It does not permit burning underwater organic carbon.

Actual burn is bounded by fuel, oxygen and remaining thermal capacity below500K. Remaining f32 fuel is rounded upward if necessary so quantization never overspends those bounds. All gas and thermal changes are calculated from actual removed fuel. Subresolution transfers or overflowing/nonfinite arithmetic refuse atomically; resource changes must agree with their intended transfer within1e-9 relative error. There is no silent heat clamp: insufficient thermal room reduces burned fuel and leaves the rest unburned.

Heat parameter defaults to30MJ/kg carbon as an explicitly named **gameplay calibration**, not a measured fuel composition or scientific constant. Heat capacity is J/K/m². All fuel heat is deposited in this primitive; no atmosphere radiative loss, vaporization, moisture, combustion chemistry, ignition threshold, flame kinetics or spreading model is claimed. A later model must account explicitly for any heat-loss partition rather than silently discard energy.

## Nutrient accounting trap avoided
Production mortality already releases the nutrient associated with dead biomass when it creates detritus. `Microbes.nutrientTotal` is free nutrient plus living biomass×0.1 and excludes detritus. Therefore this helper releases **no nutrients from detritus again**. CO2 increases, O2 decreases, total carbon remains constant; nutrient remains untouched.

## Tests
Pinned Zig0.13.0, five test cases pass:
- Actual fuel removal, gas stoichiometry, carbon closure and heat ledger; preview exactly matches execution and leaves supplied state unchanged.
- Sentinel live biomass/support/nutrient/lineage/RNG untouched. This is a container/pointer isolation test, not a real coupled Planet acceptance test.
- Oxygen/temperature caps retain unused fuel without discarded heat.
- Repeated exhausted-fuel calls and absent-oxygen calls are inert.
- Fifteen refusal fixtures: wet/negative/nonfinite depth, invalid heat parameters/inventories/temperature/fuel, thermal ceiling, subresolution O2/CO2/temperature and heat underflow. State bytes unchanged.
-100 deterministic parameter combinations, at least90 successful burns; carbon and oxygen closure, finite bounded state and heat ledger checked. Refusals leave state unchanged.

Command:
`zig test src/experimental/detritus_ignition.zig --cache-dir <absolute-cache> --global-cache-dir <absolute-global-cache>`

## Required before any gameplay wiring
1. Review independent global atmosphere conversion and finite per-cell oxygen budget. Avoid double-counting burned carbon as ordinary respiration; add an explicit event ledger or carefully documented flux category.
2. Real serialized-world control versus intervention tests with actual patch heat capacity and subsequent coupled hydrology/ecology. Do not claim immediate or guaranteed deaths or recovery.
3. Preview/targeting/action receipts and save restoration, including refusal when selection changes. This primitive has no selection identity; integration must enforce it.
4. Document zero-water moisture proxy and the fuel-heat calibration.
5. Keep dormant seeds, regrowth and fire-protection evolution out of claims. Current Origin has no dry-land producer lifecycle or dormant pool. Existing structure affects drying and geometry; it is not validated fire armor. New inherited protection/reserves need their own paid costs, mutation/inheritance, migration and paired-habitat tests.

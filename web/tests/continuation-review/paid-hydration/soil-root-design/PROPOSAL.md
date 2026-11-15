# Finite substrate moisture and paid root uptake: design only

No code, rate values, soil prefilling, mutation changes or production approval. Previous80-case negative results e1acd1b remain fixed. Existing production has standing liquid, vapor and phenomenological phase/advection, not a soil-moisture compartment. Existing experimental organism storage can buffer a pulse but does not create access to continuing non-standing moisture.

## Smallest local physical compartment

Add patch-owned soil_water:f64 in kgWater/m² representing a bounded porous surface layer, not taxonomic soil or a calibrated rooting depth. A finite parameter Smax (same units) defines capacity. All new/legacy worlds start soil_water=0. Fill only by actual represented transfer from current physical liquid after hydrology (including rain already delivered into liquid); never copy rainfall history into water. Existing rainfall is diagnostic and must not be double counted.

Symbolic fluxes, no rates selected:
- Infiltration: bounded by physical source receipt, remaining pore capacity and a finite infiltration conductance×dt. Transfers liquid→soil; no organism benefit before an actual debit.
- Soil evaporation: bounded by soil's actual represented withdrawal and a finite atmospheric-demand law, delivered to current vapor through explicit receipt/return handling. It must remain active without organisms, so soil is not protected escrow.
- Leakage/drainage: bounded soil withdrawal returned to standing liquid, governed by a finite drainage law; no lateral groundwater simulation in this minimal model.
- Uptake: simultaneous paid-root demands share only actual available soil withdrawal, with bounded proportional receipts and loss-detecting arithmetic. Slot order cannot monopolize moisture.

Keep source compartments and transfers distinct: standing liquid, soil, cohort-owned stores, vapor and nonhydrating numerical return escrows all appear separately in total water. Soil is physically accessible and evolves; numerical liquid_return remains inaccessible. Unrepresentable source/receiver changes refuse or preserve explicitly counted returns, never nominal water credit. Failed transactions atomically preserve all participants.

## Paid uptake without an impossible two-new-trait dependency

Prefer a distinct root allocation rather than granting root access for free to a storage trait. Actual root carbon comes from ALREADY PAID support tissue, not a multiplier that creates tissue. Proposed support partition is explicit: root fraction u, storage fraction r, aboveground fraction1−u−r, with u>=0,r>=0,u+r<=1. Existing support maintenance remains charged on the whole support mass. Diverting tissue reduces actual aboveground height, light competition and spread; storing roots cannot simultaneously count as canopy or reservoir tissue. No new transport-cost coefficient is chosen here; existing real tissue/opportunity/maintenance costs are the minimum, additional pumping costs require separate justification.

Root throughput is limited by actual root carbon×finite conductance×soil moisture availability. A ROOT-ONLY organism (r=0) can use paid same-step water throughflow for its existing water-demand/stress mechanism, then return that water to vapor. Thus uptake can be useful without waiting for a separate storage mutation. No permanent unowned water is created. Storage-only (u=0,r>0) retains its existing finite surface-pulse use, without access to soil. Both allocations can later coexist but are not required to unlock either effect.

For positive physiological water demand, a conservative proposed throughflow signal is actual paid transpired water / that demand, bounded[0,1]; zero demand gives no invented paid signal. If storage participates, draw from the actual store only for unmet demand and account its debit. Water exceeding demand may fill paid storage only within capacity, otherwise stays in soil or a counted return; it cannot be credited twice. This signal is a phenomenological water-stress model, not exact vascular hydraulics/photosynthetic water stoichiometry. How it combines with existing habitat gates must be separately specified before implementation.

Existing support is still a prerequisite; this is not a free root system on zero-tissue microbes. It is not an impossible compound NEW unlock: naturally evolved supported organisms already exist, so one inherited uptake allocation can become functional in that background. Demonstrate this with fixed actual supported whole phenotypes and root-only controls before any claim about natural emergence. Do not hand-pick an eventual winner or silently assign beneficial support. Starting from-zero mutation/reproduction remains a later independent proof.

## Local lifecycle, costs and time

Soil belongs to its patch, never follows a migrating/manual-transferred colony. Root tissue is a carbon partition, not extra biomass. Births inherit allocation through the explicit saved law; actual daughter tissue must be parent-funded. Allocation changes redistribute only existing support, and any reduced storage capacity returns water before reuse. Grazing/death follow actual gross tissue loss and return owned water locally; root loss immediately reduces conductance. Support-shedding motility loses roots, not a magical portable soil pool.

Flux rates use seconds consistently; conductance units must explicitly convert kgRootC/m² to kgWater/m²/s. Compute demand, represented removal and fair receipts before physiological update; apply carbon/oxygen flux once. Exposure/mean-reserve alternatives remain named model choices, not silently folded into this new mechanism. No coefficient selected until the compartment and fairness contract is reviewed.

## Saves, legacy behavior and tools

Use explicit experimental model/config identity. Persist soil-water array or sparse nonzero patch records, root allocation, existing storage/return fields and enabled hydrology/uptake law. Unknown/disguised laws reject before mutation. Legacy load defaults zero soil, zero roots and disabled new hydrology; therefore exact old-world physics/RNG is possible. Enabling the new soil law WILL alter physical hydrology even without organisms; do not claim enabled root0 equals legacy water motion. Enabling never prefills soil. Old root allocations must be rejected if they violate the combined support partition; do not silently renormalize an invalid save.

Water− currently means selected-patch STANDING-water removal. Keep that narrow meaning explicitly: pore water remains and can later leak to the surface or support uptake. If the player wants to desiccate soil, that is a distinct requested tool with visible scope and a recorded water sink, not an invisible extension of Water−. Water+ adds surface liquid; infiltration competes with runoff/evaporation naturally. Terrain edits do not invent/delete soil water; fixed capacity avoids implicit capacity change until a later defined erosion/soil-depth model. Fire/drought tools must report which physical stores they affect. No recharge from historical rainfall or numerical escrows.

## Required gates before any enablement

1. Closed liquid/soil/owned/vapor/return ledger with actual receipts, extreme representability, zero pools, no tissue, full soil, dt bounds and all slot permutations. Empty patches still drain/evaporate; no reproductive RNG for water-only updates.
2. Identical finite total water partitioned between standing/soil controls; no free initial wet soil. Root-only, storage-only, neither and both at matched actual tissue costs, fixed wet/dry/recharge schedules and timesteps declared before results. Both successful and failed uptake retained.
3. A root-only paid phenotype can be useful without storage IF finite soil supply supports it; if no advantage appears, retain the negative rather than increase conductance until it wins. Neither zero soil nor exhausted soil can sustain it.
4. Actual scheduler integration: current post-hydrology pools, soil exchanges once, core metabolism once, lineage/material ownership through birth/graze/move/death, saved uninterrupted/restored continuation and old disabled exact parity.
5. Natural from-zero runs and actual player-accessible rain/standing-water setup, without prefilled soil, trait assignment, favored destinations or guaranteed plant/animal categories.

Open decisions for review: finite capacity and hydraulic rate laws; whether root access should use a separate allocation versus an alternative single multi-purpose paid tissue trait; handling active r mutations near u+r=1 without arbitrary normalization; physical depth versus existing15–20cm habitat gates; performance/memory of another per-patch f64 pool. No numbers or implementation are approved by this proposal.

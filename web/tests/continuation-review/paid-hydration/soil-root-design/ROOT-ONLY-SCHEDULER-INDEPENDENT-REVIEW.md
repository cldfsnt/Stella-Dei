# Root-only scheduler plan review

Read-only review of622dc74 before activation. No conceptual blocker for its explicitly bounded isolated pilot; actual copied-source, ownership and persistence gates remain required.

Production order supports the plan: thermal update, liquid transport/current-array swap, atmospheric column phase once, vapor advection, then biology. The new all-patch soil phase must replace—not supplement—the existing phase call and use current pools. It must run for empty/dead patches without marking them reproductive-active or drawing biological RNG. Posthydrology root throughput must not repeat abiotic infiltration/evaporation. Vapor received from roots after advection/condensation is available to the NEXT tick's climate; this operator lag is explicit, not a reason to execute climate twice.

Root-only rejection of unsupported retention/stored-water/return-escrow states is necessary. Do not erase them on migration. Soil starts zero and receives only actual represented standing-water debits; remains patch-owned on birth/movement/death. Actual root credits remain bounded by paid soil withdrawals; receiver roundoff is logged, never converted into additional physiological credit. Feature-disabled exact old-state/RNG parity and enabled-zero-root hydrology are distinct controls. Keep the existing large-dt hydrology suspension contract explicit; proposed normal1440-second pilots do not validate arbitrary timestep behavior.

## Thermal limitation, quantified from source

`SurfacePhysics.originHeatCapacity` currently gives per-area capacity:
`385910 + min(standing_depth_m,50)*1000*water_cp` J/(m² K), with warm water_cp4184 and cold2093. Soil is not included.

At the proposed maximum1kg/m² soil water, omitted warm sensible capacity is at most4184 J/(m² K): **1.08419%** of dry-ground baseline; **0.125342%** at the fixed478 local fixture's .70558084m standing depth; **0.00199632%** at50m. Cold-source Cp would give .542354% of dry-ground capacity. These are bounds on a missing capacity term, NOT a bound on cumulative energy error or temperature error. Moving surface water into soil can remove its represented thermal contribution until return; this remains an explicit approximation.

Existing atmospheric phase exchange has no latent-heat closure. New soil evaporation/root vapor transfer likewise lacks latent cooling. Freezing cutoff is a declared availability convention, not an ice/enthalpy model. A whole-climate rewrite is not required for this bounded experiment, but no claim of full energy conservation or calibrated soil thermodynamics is supported.

Before promotion: actual source review, per-stage water ledger, enabled-empty/dead behavior, source-funded root-vapor receipts, exact disabled comparison, atomic invalid-load rejection and true restored-versus-uninterrupted continuation. Retain zero-benefit/soil-exhaustion outcomes and do not change habitats or rates to obtain an advantage.

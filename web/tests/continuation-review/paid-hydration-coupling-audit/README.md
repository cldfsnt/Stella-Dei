# Read-only coupled-scheduler hydration audit

Scope: proposed isolated QA experiment, not production integration or a thermodynamically complete model. Coordinate physiology with paid-hydration owner and inheritance/save/lifecycle with independent reviewer. No implementation in this checkpoint.

## Actual current sequence and units

`Planet.simulate` joins thermal jobs and swaps temperature/newTemperature, then runs liquid/velocity jobs and swaps current water arrays. `simulateAtmosphereWater` follows after those jobs join. The microbial scheduler runs near the end of the tick, after climate/water. Therefore a new biological uptake uses the actual post-hydrology surface pool; any added vapor will enter ordinary phase/advection on the NEXT tick, unless deliberately inserted earlier. Do not let job threads and physiology concurrently mutate the same pools.

Current `waterMass` and `waterVaporMass` are f32 in units of 10^9 kg per patch. `getKmPerWaterMass` documents km / 10^9 kg. Microbial biomass/support and the experimental retained-water reservoir are per square metre. Use the actual world's `getMeanPointArea`, not the isolated experiment's fixed 7,669,529,600 m² constant. Density conversion is native_mass × 1e9 / area. `newWaterMass` is stale liquid/scratch after atmosphere uses it as vapor transport coefficients; it must NOT be used as a biological source or a second conserved physical pool. Similarly count only current vapor, not its old swapped scratch.

Existing phase transfer is phenomenological:
- evaporation = min(liquid, max(0, saturation − vapor) × (1 − exp(−dt/86400))) above freezing;
- condensation = min(vapor + evaporation, max(0, vapor + evaporation − saturation) × (1 − exp(−dt/3600)));
- liquid/vapor results are cast to f32, rainfall memory updated, then vapor advected.

There is **no existing latent-heat transfer**. Planet's comment explicitly excludes a latent-heat/real-weather claim. Origin heat capacity is area × [0.1×5513×700 + min(surface_depth_m,50)×1000×water_cp], with water_cp4184 above freezing and2093 below; it currently counts surface water, not internal water. Adding only evaporation cooling would not close energy because later condensation has no matching release. Parent decision: retain this limitation and current thermal model; do not silently rewrite climate or claim thermodynamic closure.

## Minimal physical pool/receipt contract

1. A sidecar reservoir belongs to a real lineage, not a reusable slot. Derive actual area and current water/vapor array pointers each tick, after swaps. Zero allocation must take an exact bypass with no water/RNG/temperature mutations.
2. Uptake credit is the actual represented f32 surface debit ×1e9/area, never nominal demand. Directed rounding must ensure debit ≤ requested capacity and finite source. Unrepresentable debit gives exactly zero credit/protection.
3. Compute all eligible cohort demands from one source snapshot. A sequential slot-first allocation is not a demonstrated fair community rule. Use a separately tested bounded allocation policy before making competition claims; neither order nor remainder may create water.
4. Internal reservoir addition may itself round; any difference remains nonhydrating local liquid escrow. Never drop a receipt residual or invent a fresh source. Source/receiver must be planned and validated atomically.
5. Evaporation spends actual represented internal water and credits vapor or nonhydrating vapor escrow. The next climate step may condense/transport represented vapor normally. Liquid and vapor escrows are physically distinct, included in the water ledger, not available as hydration until representably returned to the matching real pool.
6. Settle capacity loss/death immediately after the real microbial core step, before any reproduction/movement can reuse that slot. Release all water when its owner vanishes. Handle movement, grazing, newborn allocation and manual transport only after independent lifecycle contracts exist. Do not let a newborn inherit an unrelated corpse's sidecar through slot reuse.
7. Use the real `Microbes.step` once and its existing `applyMicrobeFlux` once. The isolated wrapper's separate CO2/O2 budget must NOT be layered on top of Planet's shared atmosphere, which would double-account flux. Water handling must not change C/N, support or donor funding except the explicitly approved physiological seam.
8. Ledger = current liquid + current vapor + internal stores + both phase escrows. Report incremental adapter receipts and baseline coupled f32/global-water drift separately. Preserve all finite/zero/exhaustion/overflow refusal tests; no global correction or coefficient tuning to force a favorable result.

## Bounded actual-world experiment proposal

Input: existing natural60-day60.json SHA25676d5f4af52b9b26272381e220d899a0ff6f780479b7164709c8d09b1fde97dd7. Use the previously preregistered natural root478 at patch12352, slot1, generation6/parent232. Its baseline surface depth is about .70558m. This is not a newly searched favorable target. Prior actual .08m edit refilled toward .696m over7days; transient exposure must remain visible in analysis.

Prescribed experimental allocation0/.25 × untouched/one actual Water− after1simulated day; continue6more days without care. Retained water starts0, so charging must be paid during the first actual coupled day. No held bulk-water control pool, repeated refills, clamped depth, assigned favorable temperature/nutrients or synthetic initial retained water. Use every unchanged1440s coupled tick and exact public edit, record its external water receipt.

Before biological claims, allocation0 must match frozen production full saves exactly at checkpoints. If a minimal founder-only sidecar is used before lifecycle integration, keep actual reproduction but explicitly give new descendants no experimental allocation and report founder physiology only, not inherited fitness. This is a deliberate restriction, not a valid full evolutionary integration. A full shared inherited strategy requires the reviewer's lifecycle proof first.

Record actual surface depth/temperature duration, finite charging/evaporation/returns, founder identity/biomass/support, ordinary offspring outcomes, liquid/vapor/store/escrow inventories, C/N and accounting residuals. Retain extinction/reflooding/null outcomes. Native coupled evidence is neither Android performance nor proof of land plants, fire resistance, or universal drought advantage.

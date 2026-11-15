# Hybrid soil/root integration: smallest testable seam

Read-only source audit. No rates, model law, production fields, save version, or shipping authorization chosen. Local f64 kernel is still an isolated numerical/physiology proposal, not the world scheduler. Companion performance protocol: soil-root-performance-readiness. Owner's alternative: soil-root-design/WATER-REPRESENTATION-PROPOSAL.md, hybrid appendix b8dfef3. Current source hashes are recorded separately.

## 1. Keep authorities explicit; do not widen climate by accident

Candidate A: retain authoritative legacy `Planet.waterMass`/`waterVaporMass` f32 billion-kg arrays and current f32 scratch/SIMD/weather/render path. Add physical soil f64 kg/m² and cohort-owned stored water, with root/storage allocation traits only through a separately versioned, explicit experimental law. Soil is not a numerical residual or an organism-only protected reservoir. Diagnostics are not spendable pools. Do not retain a hidden f64 copy of surface/vapor which disagrees with the f32 authority.

This avoids automatic changes to water transport lanes, GPU upload stride, atmospheric coefficients, global heat/weather code and all existing tools. It does NOT avoid boundary precision work. Four f32 climate arrays need not grow; one f64 soil value adds327,696bytes at40,962 cells. Cohort fields/alignment and save overhead are additional: measure actual structs, no assumed packing savings. A separate soil slice avoids making empty soil depend on microbial sparsity; a field in Cell is acceptable only if every empty cell participates in physical update/capture. Pick one ownership, not both.

### Mandatory native-boundary adapter

- Convert actual f32 mass to f64 kg/m² using the planet's actual area; reverse conversion only at declared surface/vapor commit boundaries. Audit `getMeanPointArea`, not a laboratory constant. Record source/destination units in every receipt.
- Stage both endpoint writes plus soil/stores. After f32 round-trip, calculate actual represented debit/credit, then allocate biological receipts from the actual funded debit, never nominal request or intended f64 intermediate. Zero actual debit means zero physiological credit.
- Returning evaporation/transpiration into a huge f32 vapor pool can round to zero or jump one quantum. Infiltration from a tiny f32 source can overdraw relative to requested flow. Derive a new boundary-specific error envelope including conversion and cast ULPs; the local all-f64 ledger does not cover these errors automatically.
- Do not silently debit a full source quantum and park excess in protected escrow. That previously rejected shortcut changes drought/storage biology. If hybrid cannot satisfy preregistered precision/performance limits, HOLD it and compare measured full-f64 authority, rather than widening tolerances or tuning survival.
- Account actual source and recipient change, signed/absolute residual, cumulative physical total, unpaid requests and any source debit uncredited to biology. Tiny uncredited throughput must be explicit and budgeted, not called exact conservation.
- Invalid area, overflow, NaN/Inf, negative amount, f32 cast overflow, capacity overflow and failed receipt validation must reject the whole patch transaction without modifying water, cohorts, gases or RNG. No post-write validation failure.
- Native and actual wasm32 strict-arithmetic gates, offline exact/rational oracle, real nearshore/ocean/vapor endpoints and subnormals. No runtime f128 required by this design. Inspect generated WASM helper calls before performance conclusions.

## 2. Minimal scheduler candidate, preserving old law

Observed order in `simulation/planet.zig::simulate`: temperature jobs/join/swap → liquid/wind jobs/join/swap → atmosphere phase/advection → Origin growth → relocation → funded reproduction. `newWaterMass` is reused as atmospheric coefficient scratch; it is NOT physical water after that phase. Never use it as soil or save it as water. The existing `dt<15000` hydrology guard needs explicit candidate semantics, not a silently independent soil clock.

Suggested isolated seam: explicit model-enabled branch in the existing ascending first pass of `simulateMicrobes`, after atmosphere finishes. For each patch, stage abiotic soil exchange and any owned-cohort uptake once; commit finite paid receipts; run the single physiological step once; retain the original movement/birth passes and their ordering. Current `if biomass<=0 and detritus<=0 continue` must occur AFTER necessary abiotic work. Empty wet soil still evaporates/drains, empty surface can infiltrate, and rainfall can recharge soil without life. An active-cohort bitset alone cannot schedule this work.

Do not run the full local kernel once in an abiotic pass and again for living uptake: that double-counts infiltration/evaporation/drainage. Either one atomic staged patch call or an explicitly split API with identical tested operator order. Demands derive from the same pre-physiology cohort snapshot and current world environment; do not recompute after one slot has consumed water. Same-call root/store credits feed the copied physiology adapter; original production `Microbes.step` does not magically consume a new `h_paid` field. Do not run both old hydration and new root payment.

Post-atmosphere timing means returned vapor advects/condenses next tick, and soil drainage reaches surface transport next tick. State this operator split and test timestep refinement; do not claim simultaneous hydrology. Heat capacity/latent heat are also NOT supplied by the local kernel: production Origin heat capacity currently sees surface mass only. Either explicitly scope the first experiment as one-way prescribed-temperature water/physiology coupling, or separately specify energy coupling before calling it a complete physical soil model. Fire eligibility likewise sees exposed surface water, not soil moisture; don't claim new soil-aware ignition without a model.

Disabled law must call unchanged old scheduler/core with no extra random draws, casts, initialization side effects or per-cell root work. Enabled physical soil with zero root traits is NOT the disabled control: abiotic soil processes can still alter climate/water. Keep these controls distinct.

## 3. Full ownership / read-write inventory before integration

| Path | Required treatment / acceptance |
|---|---|
| Planet allocation, init/setSeaLevel, beginOrigin, Sandbox switch, deinit | Allocate/zero/free soil consistently; reset model configuration and cohort stores; never activate stale Origin water after Sandbox. Allocation failure precedes world mutation. |
| Temperature/currentHeatCapacity, atmosphere, water transport | Explicit scope above; f32 authority retained. New exchange only after jobs join. Preserve wind, rainfall, partial pressure and transform freshness. |
| `microbeEnvironment`, growth/upkeep/starvation/decay | Derive exposed demand from real surface depth and current temperature; paid fractions, no passed nominal water overrides. Reconcile capacity shrink and water release before dead slots clear. |
| Grazing | Gross prey tissue loss must release proportional owned water to a declared local physical sink; no free predator hydration. Net prey gain cannot hide gross-loss water release. |
| Reproduce/propagate | Inherit traits by actual lineage, not slot; parental tissue/credit and water donation fund child. No capacity fill. Mutated capacity reduction returns real excess to declared destination; failed birth leaves all endpoints/RNG according to old contract. |
| Relocation | Current support shedding requires explicit root/store fate. Shed rooted tissue does not teleport underground water. Transfer only physically retained owned water; return shed reserve locally. Keep once-per-tick move rules. |
| Manual whole-colony transport | Whole cohort's owned reserve travels; patch soil stays. Source/destination pending snapshots include every relevant new field and environment; stale previews reject. No new births/evolution counters. |
| Seeding/nursery arrival | Zero initial owned reserve unless explicitly donor-funded. Do not copy soil into a newborn. Empty patch invasion does not create water or root tissue. |
| Water+ / Water− / fineWater / targetWater | Current APIs change SURFACE only. Soil persists and can drain back naturally; soil not silently emptied. Existing actual-meters receipts still describe surface intervention, not whole-patch dryness. Test repeated drain/recharge and bounds. |
| Wave | Current `god_actions` redistributes surface f32 water; soil stays unless a separate erosion/inundation law is approved. Explicit external/closed budget. |
| Pond/nursery floor/rim + Land tools | Habitat preview's19-patch full dependencies need soil in stale checking if relevant. Clarify 'rim surface drained', not all pore water dried. Changing elevation/capacity cannot erase excess soil: preserve or route it through an explicit real transfer. No auto-recharge from shape creation. |
| Scorch/lightning/detritus ignition | No invented fire-triggered adaptation. Current heat/exposed-fuel rules unchanged unless explicitly revised; organic-water release/capacity changes must be accounted if cohort tissue is affected. |
| Inspect / rendering / finder / Watch / snapshots | Surface depth remains surface depth; add only truthful sampled soil/store fields as needed. Current GPU water upload remains f32. No per-frame full-world soil census. Watch on/off must retain exact world/RNG parity. |
| Advance-day / pause / load / context loss | Same fixed solver ticks and cancellation rules; save after partial progress includes all physical reservoirs and law. Read-only UI does not advance exchange. |

Current files to cover: simulation/planet.zig, simulation/microbes.zig, states/play.zig, water_brush.zig, pond_action.zig, habitat_preview.zig, god_actions.zig, experimental/planet_ignition.zig, manual_transport.zig and its transfer core; main public bridges and save_schema/save_game. This is a path checklist, not a claim that code already handles soil.

## 4. Save/lifecycle gates (do not choose a new version here)

Production currently schema6; multiple later versions are experimental fixtures, not shipped migrations. Reserve an explicit version/model-law/config only after fields and semantics settle. Unknown or disguised newer fields reject before mutation. Legacy loads default new physical pools/traits/config to zero/off without changing old totals; never silently rewrite canonical storage on Load. Existing128MiB bounded atomic write and old-save retention stay intact.

Capture → JSON → validate → runtime must cover soil even with no living cohorts, cohort stores, root/storage fractions and enabled numerical/model policy. Current `SavedCell` manually enumerates fields and sparse cohort predicate; adding runtime fields alone loses them. A separate dense soil slice needs exact length validation even though cohorts are sparse. New public snapshots must fit existing fixed buffers or fail clearly, not truncate valid identifiers/amounts.

Validate finite/nonnegative reservoirs; root/storage fractions and their paid support partition; owned capacity; impossible dead-slot stores; reserved policy IDs; shapes/indices. Capacity rules must be consistent with step/death settlement, not reject legitimate loaded endpoints differently. Allocate all new arrays and validate fully before `save_game.apply` crosses its non-fallible mutation boundary. Keep CPU transformed-geometry refresh added in v57. Update reset/clear paths and cache/ticket invalidation, not only serialization.

Required actual native and WASM gates: legacy zero/off old-field and all-RNG bit parity; enabled capture/parse/apply exact roundtrip; uninterrupted vs restored continuation (not only restored-repeat); load after another rendered terrain/tilt; invalid/unknown/oversize failed load/write atomicity; empty soil-only patch retained; old enabled→Sandbox→Origin reset; dense supported limits measured without shortening valid input to force success. User's stored save changes only on explicit successful Save; rollback limitations disclosed before future migration release.

## 5. Bounded actual-player experiment, preregister before outcomes

Reuse fixed natural-day60 save and previously audited nearshore topology, not a favorable-site search. Freeze one eligible actual nursery center and its19-patch footprint from prior habitat evidence before running. Do not assign roots to claim natural evolution: if all real cohorts have zero traits, label the run hydrology/tool/disabled-control only. A separately labeled prescribed phenotype fixture may test paid physiology but is not a naturally evolved plant or invasion result.

Suggested four fixed arms from independent deep-frozen copies: (A) no intervention; (B) actual paused Nursery preview→Apply once; (C) same nursery then predeclared day1 surface drain using actual Water−/target API; (D) same drain plus one predeclared day2 surface recharge through actual API. No follow-up care or edits after observing failures. Use existing laboratory rates only if owner explicitly freezes them; this document chooses none. Seven-day fixed horizon, actual day/night, solver dt1440 with a preregistered720 control, not a changed duration until survival appears.

Record exact manual receipts, actual surface/soil/vapor/stores and world water accounting, signed/absolute native-boundary error, source-paid/root/store physiological receipts, deficit/depletion, actual lineage fates/offspring, support partition, temperature/depth and incoming neighbors. Separate external intervention water from closed transfers. Soil must evaporate/drain in an identical empty-patch control. Zero source debit yields no benefit. Eventual survival alone is not proof of root causality; compare unchanged controls and report extinction/underwater outcomes honestly.

Require actual exported tool path, one-use/stale confirmation, selected patch identity, original save restoration, no silent pause/speed change, and observer-on/off parity. Only then compare sparse/empty/dense actual scheduler and full-frame cost using the existing readiness protocol. No renderer/device claim from a local kernel or Node-only test.

## Go/no-go sequence

1. Owner local f64 numerical audit/matrix passes its unchanged limits.
2. Separate hybrid boundary receipt/cast gates pass real source ranges; compare to full-f64 alternative if not.
3. Isolated disabled scheduler/save parity and empty physical-soil lifecycle pass.
4. Fixed actual-player controlled experiment and true continuation pass, with explicit energy/time-split limitations.
5. Actual native/WASM performance/memory and migration safety reviewed. Only then discuss production. No stage here authorizes shipping.

## Climate gate addendum: local constant evaporation is NOT a world law

Direct source comparison makes this a blocking contract, not a minor follow-up. `soil_root_kernel_f64.step` transfers `evaporation_rate*dt` from soil to vapor BEFORE its root temperature/depth eligibility check. The laboratory prescribed rate would therefore evaporate frozen or deeply submerged soil if wired unchanged. Current production `AtmosphereWater.PhaseStep.phase` instead uses one temperature/saturation-dependent demand: above273.15K only, `min(liquid,max(0,saturation-vapor)*relaxation)`, then condensation/rain. The kernel's later273.15–355K/root-depth<0.2 condition does not protect abiotic evaporation. Neither mass conservation nor a successful300K laboratory trial validates this climate behavior.

Before a whole-world enabled run, explicitly decide/test:

- Exposed versus submerged soil: use real surface depth/cover. Bare-soil evaporation must not operate as a second atmosphere-facing surface under an ocean. The root eligibility cutoff is not automatically the exposed-soil boundary. No depth/rate chosen here.
- Cold/frozen soil: production has a no-liquid-evaporation boundary at273.15K but no new soil-ice phase. First bounded prototype must declare its cold behavior and refuse unsupported claims; do not run constant warm-lab soil evaporation under freezing conditions. Root uptake, drainage and infiltration need their own explicit cold contract, not accidental reuse of the root condition.
- Finite atmospheric demand: do NOT add a full independent soil evaporation request after production already spends the same vapor-pressure deficit. Prefer a single actual-temperature/saturation demand shared or partitioned between exposed surface water and soil, with finite donor availability. A possible engineering seam is exposing the existing requested budget and actual surface consumption, then allowing only eligible bare soil to satisfy an unspent remainder; this requires proof of operation order and boundary accounting, not a newly selected coefficient.
- Place vapor return consistently relative to condensation/advection. If sharing phase demand requires abiotic soil work within the phase pass, split the local kernel into explicit abiotic and physiology stages and prove each executes once. The earlier post-atmosphere single-call seam is only suitable for a scoped prescribed-climate assay until this demand ownership is resolved. It is not permission to double-spend evaporation potential.
- Transpiration/root demand must likewise identify whether it consumes the same atmospheric/energy limitation or an explicitly separate physiological prescription. Count its water source and vapor sink, but do not infer plausible latent-heat behavior from those two receipts alone.
- Energy: current local kernel has no latent cooling or soil heat capacity. Retaining legacy temperature unchanged is an explicit one-way-coupled approximation, not energy-conserving new climate. Any future thermal feedback needs a separate finite energy ledger/model, no silent global heat source/cold sink.

Preregister cold, saturation/supersaturation, dry surface/wet soil, submerged wet soil, hot/dry air, empty and occupied paired controls. Compare old surface-only atmospheric demand with new total demand; a no-root empty world must not gain arbitrary evaporation simply because soil storage exists. Check timestep refinement, rain/evaporation accounting and thermal interpretation separately from numerical mass bounds. Hybrid remains plausible, but climate-demand ownership must pass before the actual-world nursery experiment or performance-based promotion.

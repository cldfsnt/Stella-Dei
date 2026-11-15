# Paid hydration integration audit (read-only production review)

## Status and recommendation

The isolated `experimental/paid_hydration.zig` feasibility wrapper is NOT reproduction-, relocation-, save- or coupled-hydrology-ready. It uses slot-indexed retained[4], a hardcoded patch area7669529600m² and a held-water control pool. Those must not be transplanted into the game unchanged. No production edit or biological promotion in this audit.

Smallest defensible sequence: first a cohort-owned, disabled-path-exact water ledger and every lifecycle fate; then actual scheduler/save gates; only then enable inherited retention variation and compare ecological outcomes. Do not ship a fixed-slot side table or a seventh existing-cell RNG draw as a shortcut.

## Proposed ownership / units

- Cohort: inherited `retention_allocation:f32=0` in[0,1], `stored_water:f64=0` in kg water/m². Water belongs to lineage, not slot. Retention allocates a fraction of already paid support tissue; capacity hypothesis10×support_mass×allocation, with reduced aboveground architecture. No instant support/credit/carbon grants and no capacity-fill on initialization.
- Cell: separate `liquid_return:f64=0` and `vapor_return:f64=0`, both kg/m². These are nonhydrating return escrows, not a second reserve available to physiology. They survive empty cohorts and slot reuse; do not travel with manually moved colonies. Empty escrow can be omitted from wire JSON, with explicit defaults0.
- Planet waterMass/waterVaporMass are f32 billion kg **per patch**, not kg/m². Use actual current `getMeanPointArea()` to convert1e9/area; never the experiment's fixed area or atmospheric average-gas normalization.
- Withdraw only represented f32 donor loss, credit only represented retained increase, put any remainder in proper return escrow. Deposit only represented sink increase bounded by escrow; preserve remainder until representable. Escrow cannot confer hydration before becoming real surface water and being paid for again.
- Experimental `held` is an external-control reservoir only. Production has no equivalent automatic wet/dry toggling, scripted water withdrawal/refill, or off-world water source.

## Exact integration seams and fate obligations

| Current seam | Required behavior |
|---|---|
| microbes.zig Cohort/Cell, initialized/seed | Defaults all0. Seeded founder gets no free store even if capacity exists. Reusing biomass==0 slot must not erase residual owned water: settle first or require canonical water-empty slot. |
| step upkeep and mortality around lines121–138 | Capacity may shrink before/after physiology. Move excess retained water to liquid escrow; evaporation/transpiration to vapor escrow only against actual stored debit. Before `c.*=.{}` at failed-establishment cutoff, release ALL remaining store. No hidden vanish. |
| growth/support receipts lines159–167 | New capacity remains empty until real uptake. Retention cost must not create extra carbon or earned credit. Preserve the existing represented-carbon accounting; known f32 nutrient limits are independent. |
| reproduceSized lines189–215 | `child=parent.*` currently copies every field: naive water addition DUPLICATES stores. Split actual parent stored water proportional to funded daughter tissue, subtract actual donor amount, bound recipient/capacity, route rounding/capacity excess explicitly. Inherit allocation; mutation lowering capacity cannot delete water, mutation raising capacity cannot fill it. Handle same-cell and cross-cell births. Failed births are completely unchanged. |
| graze lines264–285 | Simultaneous snapshot losses/gains need explicit water handling, including zero-biomass prey whose slot otherwise persists. Minimal model: no water nutrition bonus to predator; prey water released locally when tissue/capacity is lost. Decide gross-consumed-tissue versus post-net-capacity release in advance; do not silently treat net growth as zero prey turnover. Test simultaneous predator/prey roles and slot reversal. |
| relocate lines341–360 | Current movement sheds ALL support and transports only frond minus paid cost. Since proposed capacity depends on support, moved cohort capacity becomes0: return its stored water at source before move, rather than carrying unsupported hydration to destination. Reset source only after receipts settled. Keep existing relocation RNG unchanged. |
| manual_transfer_core.zig apply | Whole cohort/support identity is copied: carry stored water exactly with colony, clear source owned store with cohort; source cell escrows stay there. Full source/target Cell snapshots already catch changed water fields once fields belong to Cell/Cohort. Preview receipt/schema must disclose water if relevant; not a new lineage. |
| god_actions heat/scorch + experimental/planet_ignition | Origin scorch is refused; current ignition burns exposed detritus and raises temperature, does not directly burn cohorts. No automatic 'fire adaptation'. Subsequent heat/death uses ordinary hydration-loss fate. If future fire consumes living tissue, it must add explicit water fate first. |
| water_brush, fine/target water, wave, pond/nursery | These manipulate free surface water only; they must neither directly fill nor erase intracellular water/escrow. A dry rim can contain a paid organism reserve. External added/removed water goes in the intervention ledger, separate from closed-world total. Full Cell preview snapshots guard changed reserve fields. |
| initialization/new world/Sandbox load | Fresh state zeros all owned water and escrow. save_game.apply already resets all Origin cells when loading Sandbox; this is replacement of a world, not physical water deletion within a running world. No stale side arrays allowed. |

## Scheduler order and exact-zero path

Planet.simulate performs temperature, liquid/wind and atmosphere-phase/advection before simulateMicrobes (line1743). Preserve that order initially. At organism stage, settle pending returns, perform bounded uptake/transpiration/physiology, then settle shrink/death; perform movement/birth water transfers with their existing phase order and settle their destination excess before end-of-step. Deposits enter the next physical hydrology tick; do not run a second advection pass just for hydrated organisms. Test and document this one-tick coupling lag.

Critical skip trap: simulateMicrobes line1501 skips biomass<=0 AND detritus<=0. Include pending return escrow in the required-processing predicate or dead empty patches can never repay water. Keep reproduction/movement activity marking for actual living cells; don't make escrow-only cells consume reproductive RNG. All no-trait/no-water/no-escrow paths must call unchanged old arithmetic, without extra random draws, reordered operations or new water writes. Zero-case model/RNG bit parity is possible while the feature/mutation is disabled, not after intentionally enabling new mutations that alter ecology.

No new per-frame world scan is needed. Reuse the existing per-tick cell pass. Hydration changes must not use rendered glyph visibility or local inspected patch as a simulation condition.

## Inheritance and randomness

Existing successful mutating births consume six draws. The sixth draw's top24bits supply organization; its low40bits already supply rare-tail gate, trait selector, sign and magnitude. It is NOT free entropy. Do not add a seventh draw or secretly reuse correlated low bits.

Stage first with an explicit experimental enable/mutation toggle and no mutation of allocation; prove disabled exactness and donor-funded inheritance. Later choose a documented separate deterministic, domain-tagged retention stream (or a separately persisted stream), never fitness-dependent selection or hidden favorable reroll. A derived stream must specify seed/lineage/generation/tag and collision/correlation limits; it is not mathematically independent just because it is hashed. Failed reproduction must not consume it or change any state. Persist the model/feature revision before enabling this in continued saves. Unmutated existing traits and their six-draw sequence remain fixed; ecological trajectories may legitimately diverge once retention variation is enabled.

## Save/schema and validation

Current schema.VERSION=6; Origin model_revision=version−1. Cohort wire representation directly uses Microbes.Cohort, and canonicalEmpty reflects all fields bitwise. New cohort defaults0 naturally parse old saves; bump schema to7 only at actual integration and reject nonzero new fields/escrows disguised as version<=6. Old loading must not prefill water or advance model/RNG.

SavedCell manually enumerates capture, jsonStringify, runtime and captureSparse: **all four** need escrow fields/defaults. Adding only runtime Cell fields loses escrow on save. Sparse cohorts remain<=4, unique indexed slots; canonicalEmpty includes new fields. Reject nonfinite/negative water or escrow, allocation outside[0,1], zero-biomass nonzero stores, stored water above computed capacity at committed boundaries, invalid future model revision and malformed duplicate sparse entries. Do not reject finite escrow merely because there is no living cohort: that is a legitimate debt. Bound magnitudes for JSON/numeric safety without converting legitimate water into hydration.

save_game.apply must validate and allocate before mutation, then load exact stores/escrows and reset transient plans/watchers as now. Failed loads preserve all new fields. Existing storage pre-v7 backup policy already recognizes <=6; test durable backup/readback and quota failure rather than rename it speculatively. Current128MiB read cap and max163842cells require a worst-case save size/memory gate.

Main lifeSnapshotBuffer8192 currently serializes full cohorts; adding fields needs maximum-length4cohort/large-ID regression, not an assumption of room. Manual/habitat pending snapshots grow with Cell size; keep JSON bounded and fail closed. Unknown old/new schema must not silently erase state.

## Memory / performance

Measured isolated native illustrative layout: current Cohort80B/Cell336B; wrapper adding retentionf32+storedf64 and two cellf64 escrows gives Cohort96B/Cell416B. Extra3,276,960B at40962cells,13,107,360B at163842cells. This is an explicit layout proposal, not a final ABI promise; WASM layout and reordered production fields still need measurement. Sparse JSON saves avoid most empty cohort fields, but always writing two zero escrow keys per mesh cell adds unnecessary wire bytes: omit canonical0 with defaults and test exact roundtrip. No added per-cohort heap allocation.

Existing full-cell snapshots for patches/transport/preview, save staging and peak load memory multiply some of this cost. Benchmark same natural worlds and dense/high-resolution controls with disabled and enabled paths; no claim native result predicts Android memory/FPS.

## Required gates, smallest stages

1. Pure represented transfer/escrow helpers, ownership and zero-case parity; extreme f32 pools/sub-ULP no-credit, bounded returns, invalid refusal, finite conservation ledger. No reproduction or phenotype outcomes claimed yet.
2. Actual Cohort/Cell lifecycle in isolated copy: funded same/cross-cell daughters, mutation-lowered capacity, graze simultaneous losses, support-shedding relocation, whole manual move, cutoff/death and escrow-only empties. Assert no duplicate/missing water or lineage; no scripted refills.
3. Version7 experimental save branch: real oldv2–v6→zero defaults, exact roundtrip/continuation, failed-load atomicity, sparse/reset/newworld/Sandbox paths, bounded receipts and memory. Do not promote schema before these pass.
4. Actual scheduler with real varying area/temperature/daylight, liquid+vapor+cohort+escrow totals and explicit external water ledger; finite/no-overdraw per transaction plus reported numeric residuals. Compare1440/720steps and multi-seed wet/dry cycling/continuous wet/scarcity, not fixed300K only. Exact disabled fullworld/save/RNG parity required. Existing physical hydrology has f32 residuals; measure and isolate biological delta, do not erase drift with a global top-up.
5. Enable inherited variation only after ledger/save gates. Natural donor-funded generations, opportunity cost under wet conditions and finite drought/recovery outcomes, no guaranteed winner. Only then consider visual differentiation and truthful progression claims. This mechanism alone is not land plants or animals.

## Clarified integration recommendations

These are proposed behavior, not current production water handling: release the proportional stored water associated with gross consumed prey tissue to local liquid escrow, before post-loss capacity settlement; do not introduce predator dietary hydration in the first stage. Support-shedding motility returns all capacity-dependent reserve at source. Whole-colony manual movement carries owned reserve but not cell escrows. A daughter receives only its funded parental share; mutation-lowered capacity releases excess at destination.

Migration must remain in-memory on Load. Current stella_load reads/parses/applies; storage.load performs sync(true) then native load, not save/writeback. Keep old canonical bytes unchanged until the player explicitly Saves. On that explicit Save, existing pre-v7 durable backup policy must complete before overwriting; failure blocks overwrite. A newer version7 save may not open in an older build, and the current UI has no automatic backup-restore workflow. Disclose that rollback limitation; never advertise reversible migration merely because a backup exists. Test unchanged old bytes after successful Load and after failed Load separately from exact loaded-model continuation. Disabled feature bit parity is an experiment property, not a promise that newly enabled evolution cannot change future outcomes.

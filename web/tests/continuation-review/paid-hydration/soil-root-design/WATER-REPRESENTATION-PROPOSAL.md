# Next design: consistent physical water, not another phase exception

Design only, following f038ac7. No current assay, production physics, rate, schema or field changed. Finite paid-root uptake plus recharge supported one prescribed phenotype for seven days, but recharge lattice refusal and infiltration binade caps confound hydrology. Preserve those findings. The next gate must compare whole water transfer semantics, not keep patching individual successful cases.

## Recommendation

Prototype ONE authoritative f64 physical-water path with an explicit, measured bounded-roundoff policy across all enabled flows. Use strict f64 arithmetic and ordinary bounded requests, not runtime f128 exact-or-refuse/binade caps. Keep a high-precision/exact-rational oracle OFFLINE for verification. First measure whether double precision suffices over actual supported world ranges before adding compensated storage. No production promotion or new numerical tolerance is selected by this document.

Surface, soil, vapor, organism stores and laboratory held reservoir must all have declared physical ownership and participate in their appropriate processes. Numerical error diagnostics are signed observations, not spendable water, not hidden return pools, and never used to top up a world to a target total. Physical soil is exposed to evaporation/drainage independent of life; held reservoir exists only in the laboratory fixture. Soil/root physiology does not justify global climate parameter changes.

## Alternatives

### A. Compensated physical pool (high+low)

Store a high scalar plus a signed low residual; together they are the authoritative physical amount. This is NOT an escrow that biology alone can drink. Every evaporation, runoff, advection, condensation, root flow, death return and god-tool read/write must use the combined pool, including empty patches. Save/load must preserve both words and nonnegative combined state. Resetting, draining or moving a pool moves both parts. Otherwise the low component becomes the protected reservoir already rejected in earlier reviews.

Advantages: can retain tiny transfers against large water pools; error-free transforms can provide strong local accounting. Disadvantages: normalization, cancellation, comparisons and parallel transport become substantially more complex; moving only a high-word coefficient would strand low water. Existing f32+f64 sidecars are not cheap drop-in precision because current hydrology reads only f32. Kahan summation of totals alone does NOT fix individual transactions. Prefer this only if measured f64 error fails a preregistered physically meaningful bound.

### B. Authoritative f64 plus explicit roundoff budget (preferred first prototype)

Each transfer computes a finite nonnegative request, clamps against actual source/capacity, and updates staged f64 physical endpoints. Record actual represented source debit and recipient increment separately. Do NOT require exact binary equality or crossing at a binade boundary. A signed debit-minus-credit difference is numerical error, not biological water; audit its magnitude/cumulative behavior. Root h_paid must be limited by actual source debits and individually allocated paid demand, never nominal requested flow. A receiver rounding increment is not permission to increase physiological receipts.

Do not silently allow arbitrary discrepancies: derive a per-operation forward-error envelope from actual endpoint ULPs and arithmetic/conversion operations, validate finite/nonnegative outcomes, and compare empirical totals against an independently summed high-precision reference. State clearly that a bounded positive receiver rounding error is small numerical mass creation, not exact conservation. Do not cure it by arbitrary pool correction or resource topups. A failed precision requirement blocks promotion or motivates option A; do not widen it after seeing survival.

Large pool ULPs must be quantified first. If source subtraction produces no represented debit, no biological credit is allowed. An entirely sub-resolution request is recorded as unrepresented, not paid. Unlike current exact-lattice policy, a small nonzero mismatch does not freeze valid hydrology or stop a macroscopic recharge. For simultaneous cohorts use one source budget and permutation-invariant proportional allocation; sum demands canonically, handle rounding without first-slot leftovers, and test each cohort's receipt≤actual funded share. No iteration per receiver binade.

### C. Common fixed quantization/integer units

Exact integer transfers are attractive only after selecting a scientifically adequate unit and safe dynamic range. A global unit fine enough for tiny founder demands but spanning deep oceans can overflow64bits; density units also depend on patch area when moving mass. Larger units create artificial uptake/reproduction thresholds and soil layers. Per-pool exponents recreate incompatible-lattice and exchange problems. u128 arithmetic/WASM software helpers and conversion costs require evidence, not assumption. This option is not recommended without first reporting actual min meaningful demand/max world inventory and required bit width. Quantization must be an explicit model resolution, never adjusted to rescue a phenotype.

## Actual production seam and memory/compute implications

Current Planet has f32 waterMass and waterVaporMass in10^9kg/patch; f32 newWaterMass/newWaterVaporMass scratch. newWaterMass is reused as an atmospheric coefficient after phase exchange, NOT consistently liquid state. Rendering streams f32 water; saved arrays are current physical arrays. A careless type replacement can change both liquid physics and coefficient semantics.

For40962cells, widening four scalar arrays fromf32 tof64 adds655392bytes (0.625MiB); adding one f64 soil array adds327696bytes (0.3125MiB), before extra transport scratch. Keeping separate four-array f64 authority alongside legacy f32 arrays instead adds1310784bytes (1.25MiB), plus soil. Cohort storage/mutation overhead is separate and already measured in earlier experiments. Four compensated f64x2 arrays replacingf32 add1966176bytes (1.875MiB), plus any soil/store compensation. These are arithmetic storage estimates, not observed total heap use.

f64 is a normal WebAssembly numeric type; current vectorized f32 water code would lose lanes or require a separate path, so speed is unproven. f128 reference helpers are software-heavy and must not be assumed viable per40kpatch tick. Native profiling alone cannot establish browser/mobile speed. Measure actual enabled/disabled full-scheduler cost, allocations, transferred GPU bytes and WASM execution before rollout. Rendering may downcast a read-only view without making it authoritative.

## Native f32 bridge and save compatibility

Do NOT cast authoritative enabled pools back tof32 after every tick. That would erase the precision improvement. An explicit model-version branch may import old f32 values exactly intof64 once, initialize new physical soil/store states tozero, and save enabled f64 physical arrays thereafter. Exported rendering/diagnostic views can be f32. Every enabled hydrology/tool/save path must use f64 authority; legacy disabled path remains unchanged for exact old-model parity. This is a candidate migration architecture, not a chosen schema.

Keep current10^9kg/patch units initially to minimize changes to physical transport, with actual area conversion to kg/m² for physiology. Conversions themselves introduce rounding and must be included in the receipt/error budget. Within a local fixture, all pools can stay in common kg/m²; that does not prove cross-patch conservation. Existing Planet uses a mean cell area; do not silently introduce a different area model while changing representation. Future nonuniform area requires mass-conservative edge transfers, not density copying.

## Bounded next gates, before another biological result

1. Inventory actual world ranges: surface/vapor masses, actual areas, soil capacities, minimum/median/max positive requested biological receipts; compute f32/f64 ULP in physical density at each source/receiver. Use all patches and declared positive demands, not only successful lineages. Predeclare acceptable absolute/relative water error in terms of smallest meaningful request and total transported inventory BEFORE experimental runs; parent/reviewer approves values.
2. Implement one isolated f64 local transaction path consistently for infiltration, evaporation, drainage, root/store flow, recharge and capacity/death return. Keep material requests/rates frozen. Test original step27 and actual day6 recharge operands; no binade ceilings. Compare actual receipts to an offline rational oracle, signed/error-bound accumulation, negative/invalid atomicity, empty/full pools, source exhaustion and all4slot permutations.
3. Repeat the same36case experiment, preserving previous runs and reporting actual delivered doses, finite budgets and error exposure. A corrected recharge should approximate requested.25 absent a real source/capacity shortage; if it does not, inspect numerics rather than tune rates. Report any changed survival as conditional on explicit numerical implementation, not a new mutation.
4. Only after local gates: isolated full Planet f64 path including empty soil, all surface/vapor transport and god tools, exact disabled old-model comparison, migration/save/continuation and performance gates. No automatic soil prefill, protected low-word water, extra global RNG or new habitat/movement gate. Actual inherited root variation is a later model task, not supplied by this representation work.

Stop if a practical error policy cannot be justified or if the conversion requires a broad climate rewrite. The goal is an affordable consistent model that can express ecological competition, not exact arbitrary-real conservation or a series of favorable phase exceptions.

## Scheduler alternative to measure before broad migration

Parent explicitly requests comparing a HYBRID authority, not assuming climate must migrate: current standing liquid/vapor remain authoritativef32; new physical soil and organism stores remain authoritativef64, with no per-tick cast-back of soil/stores. Boundary exchanges must debit/credit actual represented f32 changes, include area/unit conversion error, and never manufacture source-funded hydration or keep a hidden drinkable low-word sidecar. Soil remains fully physical under its own evaporation/drainage/tools; legacy climate still acts on its actual pools.

This may preserve SIMD/GPU/save paths at lower integration cost, but the original f32 uptake barrier means it could fail useful small boundary-flow precision. Measure actual infiltration/return/evaporation demand distributions and boundary receipt/error budgets before rejecting it or adopting a whole-climate rewrite. A pure localf64 pass does not validate this bridge. Define separate full-engine absolute/signed/cumulative and physiological-credit gates BEFORE coupled biological outcomes. If repeated subquantum boundary requests cannot be represented without protected accumulation or material error, report the limitation and compare explicit physical-compartment alternatives; do not quietly add an escrow that climate cannot act on.

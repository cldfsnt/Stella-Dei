# Next gate: a funded root pulse through the complete vapor cycle

Design only. Inspected current production ec54ced and frozen root-only helpers. No source changes, simulation, rates, precision budget or production migration approved here.

## Decision

Do not invent another physiological advantage to compensate for lost water. Existing root-only physiology already produced two source-funded pulses and transient protection; it failed receiver conservation and the habitat refilled. These are two independent problems. First test whether a practical authoritative vapor representation can retain, advect and condense those actual pulses. Do not repeat the seven-day biology trial until this succeeds and the liquid transport problem is separately resolved.

The useful new seam is **a complete atmosphere cycle**, not another isolated soil-to-vapor transaction. Widening only the two vapor arrays does not remove the f32 coefficient bottleneck: `Planet.simulateAtmosphereWater` writes `AtmosphereWater.coefficient32` into `newWaterMass`, reused liquid scratch, then multiplies it back into f64 gather. Next phase also casts liquid and vapor independently. Thus a root receipt passing once is insufficient evidence that it remains physical next tick.

## Smallest coherent candidate to review

Keep native mass units (10^9 kg per patch) for authoritative vapor; widen current/next vapor to f64. Keep standing liquid f32, soil f64 density. Use separate f64 atmospheric coefficient scratch; never alias f32 liquid scratch. Retain the same edge rates, phase times, temperature law and phase/advection order.

For liquid↔vapor phase exchange use represented endpoint receipts, not two independent requested writes. Evaporation must be funded by the actual f32 standing-liquid decrease. Condensation must be limited by the actual representable f32 liquid increase and actual vapor debit. Untransferred condensation remains in ordinary authoritative vapor, exposed to pressure, temperature, advection and the next phase; it is not escrow or a protected second pool. Rain history must reflect transferred condensation. The precise receiver algorithm still needs independent review; do not round up spending or add compensating water. This can legitimately underdeliver phase relaxation, which must be measured rather than called solved.

Root source density→native vapor conversion requires a separate realized receipt proof and error inventory; the existing f64-density helper is not that proof. Derive h only from common funded receipt. A pulse too small for the chosen authority must remain unspent soil with zero corresponding signal.

## Concrete dependency map

- `src/simulation/planet.zig`: `waterVaporMass`, `newWaterVaporMass`, arena allocations, zero/init and both swaps/copies in update; all consumers of their types.
- `simulateAtmosphereWater`: phase writes, coefficient32/newWaterMass alias, gathered endpoint and typed swap. Add dedicated coefficient allocation with fail-closed model activation, not mixed authority fallback.
- `src/simulation/atmosphere_water.zig`: phase requested amounts already f64; coefficient already has f64 variant. Source bounds still require endpoint tests; merely replacing coefficient32 is not a conservation proof.
- `getAirMass` currently returns f32; pressure returns f32 but accepts f64 vapor. Explicit diagnostic/force conversions can remain f32 if they never become water authority. Thermal greenhouse reads must consume current authoritative vapor (both stable-daylight and rotating branches).
- GPU WaterVapor display switch presently uploads the vapor array as f32. Convert to an explicit view buffer; never write that view back. Existing staging buffer may be reused after geometry upload, avoiding an additional permanent array.
- `src/save_schema.zig` vapor slice is f32; `save_game.capture/apply` borrows/copies both buffers. New experimental version must carry f64 vapor and model identity, promote legacy f32 exactly, validate all ownership before mutation, and not downgrade on capture. `PlayState` raw legacy writer emits vapor u32 bits and must explicitly remain legacy-only or reject candidate saves; silent narrowing is forbidden.
- `sendWaterVapor` currently has no call sites; do not invent a second vapor transport to retain it. Audit dormant APIs at compile time rather than assuming they are active paths.
- Existing root-only soil ownership, canopy costs, inherited allocation, and source-paid physiology remain unchanged. No new mutations, soil grants, retention stores or habitat gate changes.

Two vapor-array widening costs 327,696 bytes at40,962cells; dedicated f64 coefficient adds327,696 bytes: total655,392 bytes (0.625MiB), excluding optional display staging. f64 arithmetic is native WASM functionality, unlike f128; actual whole-step and Node/WASM parity must nevertheless be measured. This is much narrower than migrating liquid transport, terrain or all climate fields.

## Bounded staged gates proposed before outcomes

1. Freeze actual root-drain action1 ticks1/2 operands and native area, plus the complete natural30/60/90 arrays/topology. Retain every existing receiver witness. Synthetic controls: no root pulse, cold column, subsaturated and supersaturated vapor, dry liquid, high/deep liquid, zero wind and reversed wind. No selected successful habitat.
2. Pure phase-boundary native-unit receipts: actual source/receiver deltas and exact offline Fraction oracle. Record requested/paid/unspent per leg, both signed and sum-absolute residuals, conversion residual and demand-relative loss. No inherited 1e-9 local-density threshold asserted as engine approval. Establish prospective ULP envelopes and practical bounds before coupled outcomes.
3. One complete phase→advection pass on all three frozen worlds, with zero-biology control and paired versions adding only the two actually funded root receipts at the original patch. This is an accounting sensitivity fixture, not injected biological water: pulse branch must debit its recorded soil donor. Track full inventory and pulse-minus-control distributions; no claim individual water molecules have identifiable ancestry.
4. Ten coupled ticks, unchanged root mechanics and no intervention, only after stage2/3 pass; separate soil/root/phase/advection/liquid ledgers. Baseline liquid transport's known loss is reported independently, not masked by improved vapor. Existing root-only trial roots remain prescribed, not natural selection.
5. Exact save roundtrip and true uninterrupted/reloaded10tick continuation after different rendered geometry; legacy import and invalid-load atomicity. Feature-disabled production remains exact; enabled numerical model is intentionally not old-climate bit parity.
6. Standalone actual WASM correctness before performance interpretation; then clean native and WASM whole-stage comparisons. Do not infer browser FPS or Android behavior.

## What this does not buy

It does not fix .49m radius-head quantization, repeated-liquid scatter loss, fast refill, scarcity of exposed habitat, or bare-soil evaporation. It does not create new land organisms. If vapor-cycle precision succeeds, the next biological trial should wait for a reviewed conservative liquid solver and use the already-fixed Water− route without tuning a favorable new site. If the vapor/f32-liquid boundary still causes material underdelivery, retain that result and decide broader authority explicitly, rather than add another hidden reservoir.

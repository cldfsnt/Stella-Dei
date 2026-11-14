# Actual generated-world detritus ignition experiment

**Not connected to playable game. Live v37 remains unchanged.** This is an isolated native-engine adapter experiment, not Android/WebGL acceptance, wildfire or evolved fire resilience.

## Setup
Actual standard nursery formed through production API, seeded once normally,30days of unchanged coupled PlayState updates. No injected organism traits, fuel or automatic care. World40962cells,10occupied patches,48paid arrivals,31tracked losses and maxgeneration3. The standard native actual picking/god-preview/selected-only Water−/save checks also run.

There are ZERO naturally dry patches with detritus in this snapshot. Pick patch13596 with greatest naturally accumulated detritus:0.076425664kgC/m²,8.542563mwater,295.46594K. Freeze its whole world as JSON and parse an independent restore source. Three branches restore EXACTLY the same snapshot:
0. Untreated, ignition preview refuses wet.
1. Nine actual Water− tool taps remove water; no fuel/biology assignment. Read-only ignition preview, no ignition.
2. Same nine taps, then experimental detritus ignition. Preview exactly preserves complete save; actual burn/save roundtrip verified.
Each branch follows10days through normal coupled PlayState.update; identical86400s target and1/60real-step, measured elapsed days1and10. Restore exact original complete save afterward. No user save opened. Final existing save test confirms invalid rejection and exact restoration. Exit0; original allocator shutdown warning persists.

## Actual burn
All0.076425664kgC/m² of selected detritus oxidized. Actual model patch area makes this586,148,893kgC; huge totals reflect coarse planetary patches, not measured real fuel.
- Ideal O2 debit1,563,063,715.255kg; stored debit1,563,063,734.728kg. Explicit rounding+19.472kg, within149.019kg operation-ULP budget and1ppm cap.
- Ideal CO2 addition2,149,212,608.476kg; stored addition2,149,212,607.309kg. Explicit rounding−1.167kg, within4.657kg ULP budget.
- Fuel heat1.758446680e16J, stored heat1.758443378e16J, signed rounding3.302038273e10J (about0.000188%). Actual temperature rise5.941193K.
Finite local oxygen allocation, global gas conversion includes40962patch normalization. No new nutrients: production mortality already released them. Living biomass/RNG not directly burned. Gas and heat conservation are bounded numerical ledgers, NOT exact floating-point equality. Receipts expose actual and ideal values plus residuals.

## Outcome after10days
|Branch|Living biomass kgC/m²|Detritus kgC/m²|Temperature K|Water m|
|---|---:|---:|---:|---:|
|Untreated|.030010736|.060538657|295.93176|8.544768|
|Drain only|.02968448|.06543036|294.41937|8.308215|
|Drain + ignition|.03416348|.024101356|298.978|8.083971|
Water returns from the surrounding system: drain-only already3.505m by day1,8.308m byday10. Drain is not sustained drought. The ignition branch has more living biomass than drain-only in this run, not guaranteed destruction. This does NOT demonstrate fire-triggered seed germination, evolved fire resistance or beneficial fire generally. Multiple physical/ecological effects differ; no single-factor causal trait claim is justified.

## Failures retained
- first-fixture-failure.log: test forgot actual tool requires pointerOnPlanet; no fire executed. Corrected fixture precondition, not production bypass.
- precision-refusal.log: correct real-world case safely refused due old flat1e−8 relative atmospheric check.19.472kg O2 quantization was normal rounding of large global stored average, slightly over arbitrary15.63kg limit. Adapter now uses operation-derived ULP budgets AND1ppm cap with explicit signed gas residuals; no blanket conservation-check deletion. Exact40962regression and cumulative tests accompany adapter.

## Still required before shipping
Deliberate UI naming/targeting/receipts, a durable explicit burn-event accounting decision, meaningful visual feedback based only on actual burns, and further varied habitat testing. No spreading, live-fuel combustion, hydration physiology, seedbank, fire-protection trait or plant/rabbit fire-life-cycle proof. Existing structure is not claimed fire armor.

Reproduce: `STELLA_TOOLCHAINS=<toolchain-root> bash web/tests/playtest-fire-candidate.sh <absolute-artifact-dir>`.

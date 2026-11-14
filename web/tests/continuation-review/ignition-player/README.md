# v38 bounded ignition release validation

The separate Origin action oxidizes exposed dead organic carbon, not live colonies or spreading wildfire. Existing Sandbox Scorch is unchanged. The calculation is constant bounded work on one cell; no global scan, fuel invention, free nutrients, or save schema change.

## Actual game/player path
Run: `STELLA_TOOLCHAINS=<toolchains> bash web/tests/playtest-fire-candidate.sh <absolute-output> --player-flow`.
The native EGL runner executes the exact production PlayState.previewIgnition/applyIgnition methods invoked by the browser export kind3. It does not bypass the browser guard or claim browser execution. Normal generated world, one seeded colony, 30 days of coupled scheduler growth, actual inherited descendants and earned mortality detritus. No player save used. Zero naturally dry fuel sites in this fixture; deliberately exposed patch13596 by nine ordinary Water− taps, never injected fuel.

Verified: wet and stale-target refusals leave exact complete save/time/pace/pause unchanged; preview is read-only; paused successful action preserves time/pace/pause and matches preview receipt; immediate no-fuel repeat inert; save roundtrip of burned world; exact original world restored after three normal ten-day followup branches; invalid save rejected. Exit0. Existing allocator shutdown leak warning remains. Native390×700 screenshot shows real world/colonies and actual action feedback, not an invented flame graphic.

Burn .076425664kgC/m², actual temperature +5.941193K. Existing finite O2 debited and CO2 credited, with explicit bounded floating-point residuals. Seven accounting tests also rerun, including 32 planetary O2-limited scenarios and cumulative1028calls/257burns with no atmospheric reset. This is not exact floating-point equality; gas error is constrained to per-operation ULP bounds AND1ppm cap, heat residual separately explicit.

After ten days, burn branch living biomass .03416348 versus drain-only .02968448. This particular result is not evidence of fire adaptation, seedbank germination or guaranteed benefit. Drainage refills through normal hydrology and is not sustained drought.

## Browser boundary
Pinned Zig0.13/Emscripten3.1.64 WASM build and all seven JavaScript regression suites passed. Narrow374px production-shell UI fixture inspected independently with mocked receipts and clearly labelled NOT gameplay; actual Android/WebGL end-to-end play remains unverified. No claim full game complete.

Event accounting decision: exact last successful receipt is retained in this browser session UI, explicitly not saved history; Refresh keeps it, successful Load clears it. Planetary resource state is saved normally. No misleading reuse of ordinary respiration/recycling counters. Future durable event history would need an explicit design/migration.

UI inspection found and corrected the initial prose wall: all four tool buttons now appear in a compact top grid; explanations collapse below. Actual 374px dialog fixture verified disabled/ready states, disclosure expand/collapse, stale-action refusal, Refresh and Close. Fixture is not gameplay.

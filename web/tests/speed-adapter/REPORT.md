# Fixed-step fast-forward acceptance

## Decision
1440 simulated seconds is the tested fixed physics quantum. Requested speed controls how many such ticks are demanded, never tick size. Bounded adapter integrated into v21; real browser/mobile runtime verification remains unavailable. The user can request1/6/24 simulated hours per wall second; measured actual speed must stay visible because hardware may fall short.

## Same-save step screening
All tests start from identical parsed seeded-world JSON,8,734,640bytes, Wyhash c5cdbe3d3e203252, ordinary seed42 nursery+one seed. No continued care, climate gifts, forced traits or fabricated births.

| Quantum | Day7 occupied/cohorts | Day7 forms | Final biomass sum | Mean native update | Absolute water drift |
|---|---|---|---:|---:|---:|
|360s|6/9|4|0.07843|26.89ms|0.000353%|
|720s|4/10|3|0.08205|26.47ms|0.000415%|
|1440s|6/9|1|0.07961|25.92ms|0.000176%|

All pass finite/nonnegative water, vapor, temperature and ecological-resource checks, plus save integrity. Different mutation trajectories are expected because opportunity counts/RNG timing differ; this is not proof of numerical ecological equivalence.

1440s extended30day test:17occupied patches,42cohorts,151arrivals,102tracked losses, all6forms (23mats/5cushions/7rosettes/1ribbon/3branching/3canopies); final biomass0.615407. Founder29254 ends296.995K/~5.13m, versus360baseline296.881K/5.61m. Water drift0.002002%, finite/resource checks and exact restore pass. The post-load diagnostic selectedPoint was0, so HOURLY patch0 is NOT the nursery; actual nursery was verified in saved JSON. Do not cite those patch0 climate values as founder conditions.

## Actual adapter callbacks and consistency
- Exported requested preset setter preserves pause; rejects invalid values.
- Raw60s gap causes0ticks; menus/load/newworld clear debt and achieved samples.
-0tick frames do not advance renderGameTime.
- At1/6/24h requested rates, executing6fixed ticks yields identical full normalized save hash d523353839672a4 (only requested pace normalized after taking the observed snapshot). Same physics, solar phase, ages and RNG states.
- Save/load uses serialization then independently parsed JSON. capture() alone borrows live arrays and is not a restore snapshot.
- Four pure clock tests include0.3s active frames, bounded debt and actual rate observation; three guidance tests pass. Exact Custom fallback for nonpreset saved/menu rates is integrated and tested.
- Static web-path check confirms raw monotonic dt passed separately from clamped input dt; this is not a real browser runtime test.

## Real wall-clock loop with rendering/input
Three5second windows on this native test machine, actual monotonic delta, real engine update/render/GLfinish and input polling every frame. Framebuffer/shaders warmed first. Target is not reported as achieved.

| Requested | Actual elapsed | Simulated time advanced | Observed whole-window rate | Latest2s snapshot rate | Frames | Slowest frame |
|---|---:|---:|---:|---:|---:|---:|
|1h/s|5.0033s|17280s|0.959h/s|0.984h/s|260|241ms|
|6h/s|5.0388s|100800s|5.557h/s|5.390h/s|168|216ms|
|24h/s|5.0307s|151200s|8.349h/s|8.384h/s|106|293ms|

The2s snapshot is a recent window, not identical to the5s aggregate. Fast-forward materially accelerates this test relative to6h target, but does NOT achieve24h/s. These are native results, not Android FPS/performance. A single physics tick is indivisible and can exceed the16ms scheduling budget; budget prevents starting another tick, not preempting one already running.

## Sandbox subsystem regression
Generated ordinary Sandbox, actual Drain/Plant/Add-pair pointer actions. At requested200000s/s (intentionally above legacy100000 rabbit gate), effective engine timeScale1 and1440s steps execute5days. Results:4living rabbits,2births,59meals,0deaths, finite positions/satiety, actual movement on unchanged-population ticks, correct432000s elapsed age. Maximum population4; no runaway births. Existing global512 cap retained. No forced animal births, food refills or relaxed UI guards.

## Artifacts and limits
Integrated source lives in src/simulation_clock.zig, src/states/play.zig, src/main.zig, src/save_game.zig and src/mobile_guidance.zig; shell Speed panel is in web/shell.html. `qa/prepare.py` and parts reproduce callbacks and Sandbox through production source override. `check-web-clock.cjs` is static only. Logs under results. Native tests exit0; preexisting allocator shutdown warnings remain.

Engine changes are included in v21. Camera Fit-life remains an isolated pure-helper prototype with3tests; no rendered acceptance or integrated camera action yet.

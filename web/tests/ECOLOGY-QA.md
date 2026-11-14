# Ecosystem iteration and acceptance evidence

This is the actual Stella Dei engine, not a video or replacement simulation.

## Changes
- Plants now grow logistically, regrow after grazing, spread to land and die in deep water or extreme heat.
- Neighboring plant populations inherit a thermal optimum with bounded mutations. Sparse populations can be replaced by better-adapted lineages. This is a simple heritable thermal-adaptation model, not speciation or a biologically complete evolution simulator.
- Rabbit feeding now works during gestation as well as movement; hungry rabbits seek neighboring vegetation, remain on the surface, and can breed after maturity with a cooldown. Breeding also needs nearby food and respects a food-dependent local carrying capacity.
- Game age and physics use the same elapsed simulated time. Births, grazing meals, deaths and plant generations are observed counters.
- Water suitability uses physical water depth, not the water-mass unit. Rainfall is no longer mistaken for deep water.
- Plant updates are sequential with a biomass snapshot, removing parallel neighbor-write races in the old plant code.

## Production-core tests
```
../stella-toolchains/zig-linux-x86_64-0.13.0/zig test src/simulation/ecology.zig --global-cache-dir /tmp/stella-global-cache --cache-dir /tmp/stella-life-test-cache
../stella-toolchains/zig-linux-x86_64-0.13.0/zig build --build-file web/tests/lifecycle-build.zig -Dsource=src/qa_ecology.zig --global-cache-dir /tmp/stella-global-cache --cache-dir /tmp/stella-life-test-cache
```
The controlled habitat calls production `Lifeform.aiStep` and `Planet.simulateVegetation`, not duplicate test implementations. Seven days produced 5 births, 37 meals, 7 living rabbits from 2 founders, and biomass 6.775084 from 0.35. Selection test verifies a warm-adapted descendant (316.35K, generation 3) replaces a poorly adapted population in a 315K habitat. Pure function tests also verify grazing regrowth, flooding, extreme-heat death and ordinary rain survival.

A further 30-day soak (37 days total), including a warming/selection event, ended with 35 living rabbits (peak 35), 39 births, 1,106 meals, 6 deaths and plant biomass 5.297848. The previous mating rule without carrying capacity overshot to 77 rabbits and collapsed to extinction; this regression drove the density check. Normal mortality remains possible; the test does not force survival.

## Real rendered planet scenario
```
python3 web/tests/egl-prepare.py --mobile --paused --ecosystem
../stella-toolchains/zig-linux-x86_64-0.13.0/zig build --build-file web/tests/egl-build.zig -Dsource=/tmp/stella-egl-src/main.zig --global-cache-dir /tmp/stella-global-cache --cache-dir /tmp/stella-ecology-cache
MESA_SHADER_CACHE_DIR=/tmp/stella-mesa-cache STELLA_EGL_INTERACT=1 STELLA_EGL_ECOSYSTEM=1 web/tests/zig-out/bin/stella-egl
```
Uses fixed world seed, real input callbacks to zoom/plant/place rabbits, then the real update loop with 600 simulated seconds per step. Climate, water, plants and animals all run. No births or growth counters are forced. Screenshots are captured every half simulated day, after re-rendering the changed state. The same selected vertex also passed real engine tool tests for raise/lower terrain and add/drain water; these exercise the shared tool implementation, not Android taps.

Observed final 5.007-day run (native background update may advance one extra 600-second tick between checkpoints): 37 seeded cells / biomass 12.95 grew to 91 cells / 39.954 biomass; peak cover 0.35 -> 0.916. Plant generation 2, thermal optima 290.111–299.178K. Rabbits 2 -> 4, 2 births, 23 meals, no deaths. Habitat temperature varies roughly 6–53°C through the day/night cycle.

## Boundaries
These are native Mesa software-rendered engine tests using mobile interface branches, not physical Android WebGL, touch hardware or browser lifecycle evidence. A previous native allocator shutdown leak remains outside the ecology claim. A fullworld exact JSON capture/parse/apply roundtrip passed after erasing live vegetation/rabbits: 34,880,319 bytes, all four rabbits and their PRNG/state, plants/traits and counters restored. This is the real save adapter, not proof of Android IndexedDB persistence. It exposed and corrected an allocation-order bug where the arena snapshot preceded new trait allocations. Do not claim every game feature is complete based on this scenario.

## Full-world twenty-day soak (13 November 2026)

Reproduction: prepare a distinct source tree with `python3 web/tests/egl-prepare.py /tmp/stella-egl-soak-src --mobile --paused --ecosystem --soak-days=20`, then build the EGL harness with `-Dsource=/tmp/stella-egl-soak-src/main.zig --prefix /tmp/stella-egl-soak-out` and run with the same `STELLA_EGL_INTERACT=1 STELLA_EGL_ECOSYSTEM=1` settings. The ten observations are now two simulated days apart. Do not run two default-output EGL processes concurrently.

Actual full generated world, climate, water, vegetation and animals ran for 20.007 simulated days. No feeding, replanting, counters or survival were forced after the initial brush patch and two founders. Initial biomass 12.950 across 37 cells grew to 130.868 across 200 cells, maximum cover 0.952, maximum inherited plant generation 8 and thermal optima 288.407–302.366 K. Rabbits increased from 2 to 16 through 14 births and 209 meals, with zero deaths. Ten observations reported zero nonfinite values in temperature, water, vegetation and elevation. End-state schema validation additionally checked all serialized arrays, atmosphere, wind and rabbit state. Exact full-world save/delete/restore JSON roundtrip passed at 34,986,557 bytes.

Native elapsed time was 1m48.200s (user CPU 3m20.296s, system 4.029s), including generation, rendering and roundtrip. This is a desktop native harness measurement, NOT phone/browser frame-rate evidence. Known allocator-leak diagnostic remains on shutdown despite exit 0.

Visual evidence: `evidence/soak20/{founders,day10,day20}.png`, with raw diagnostics in `ecology-twenty-day.log`. Day20 was inspected: broad green habitat, a brown grazed central region, visible rabbit models and orange location markers. Some animal meshes remain terrain-occluded; markers do not establish every mesh is visible.

Interpretation: this suitable habitat sustains growth and breeding without repeated intervention, so it establishes an observable sandbox life cycle, not a difficult management game. Food availability influences satiety, grazing, movement and breeding; flooding/thermal limits still affect survival. This run does not prove every climate setting, adverse terrain choice, indefinite equilibrium, or every game function. Two-day temperature snapshots are at similar phases of the diurnal cycle and are not full daily extrema. No production simulation changes were needed for this soak.

## Browser-topology-six regression (13 November 2026)

After new browser worlds changed to subdivision6 (40,962 vertices), repeated the full actual five-day ecosystem harness with the production one-ring brush (7 cells at 0.35) and mixed-sex rabbit pair. Legacy subdivision7 results above remain separate; no biological constants were retuned. Prepared `/tmp/stella-egl-six-src`, built with prefix `/tmp/stella-egl-six-out`, and used `STELLA_EGL_CAPTURE_PREFIX=/tmp/stella-six` to avoid output collisions. The copied test's save path was changed to `/tmp/stella-day5-six-save.json`, preserving the original topology7 fixture for load-compatibility testing.

Result at exactly five days: initial biomass2.450/7cells grew to8.864/37cells, maximum cover0.910 and plant generation2; rabbits2→4,2births23meals0deaths. Actual climate/water remained active. Exact8,661,045-byte world save/delete/restore roundtrip passed. Same-vertex raise/lower/add-water/drain checks passed. Native elapsed32.509s (46.517s userCPU,1.255s systemCPU), including generation/render/save. This is not Android timing or a controlled comparison with the longer20dayrun. Known shutdown allocation leak remains.

Inspected `evidence/topology6/day5.png`: green growth and brown grazed areas visible;4markers and2visible rabbit meshes, with mesh occlusion caveat unchanged. Founders/day3/day5PNG and rawlog are preserved in that folder. This confirms the smaller brush still supports actual feeding/birth/growth without forced outcomes.

## Ecological intervention and visible biology (v10)

`web/tests/egl-intervention-prepare.py` prepares a nine-day native actual-world scenario using topology6 and the current browser UI/render branch. It establishes the ordinary one-ring seedlings and rabbit pair for3days, then applies ten actual Water+ tap actions to each vegetated cell, waits one day, uses the actual Drain and Plants handlers and an actual rabbit `mousePressed` to repopulate, and resumes to day9. The simulation advances normally, including climate/water movement. No biomass, births, deaths, meals or survival outcomes are assigned by the intervention script.

Observed first run:
- Day3 before disturbance: biomass5.408 across19cells,3rabbits,1birth,12meals.
- Waterediting:18vegetatedcells each received10 one-meter Water+ taps (the grazed central cell was initially excluded; water subsequently moved into it through real simulation).
- Day4 flooded: biomass0.005, no cells above0.001cover,0rabbits,3deaths.
- Drain/reseed/repopulate: shared tools restored dry patch with0.35seedcover and a new pair, not forced growth or births.
- Day9 recovered: biomass8.129 across33cells, maxcover0.914, inheritedgeneration2,4rabbits, cumulative3births33meals3deaths. Two births occurred after repopulation.
- Exact8,677,304-byte save/delete/restore roundtrip passed. Nativeelapsed53.579s, not phone performance evidence.

`evidence/intervention/{day3-established,day4-flooded,day9-recovered}.png` were visually inspected: actual growth-green with sproutglyphs/rabbits becomes brown with no sprouts/rabbits, then returns green with sprouts and four visible rabbit meshes/markers. Sprouts represent real cell biomass, not individual added organisms. New radial/foot-aligned rabbit rendering improved visibility in this view. This does not prove every possible camera/model orientation.

The old brush depended on simulation speed and/or update frequency. The production `edit_rates.zig` now makes Water+1m per tap plus5m/real-second held, and terrain100m/tap plus500m/real-second held (neighborshalf). Real update elapsed is capped0.1seconds to avoid stall spikes; paused editing works. Water is not multiplied by simulationtimeScale. A short tap is applied at pointer-down, so it is not dependent on how many update ticks occur before pointer-up. Pure tests cover15/30/60/120Hz and1/6/24h simulation speeds, plus invalid/stalled time. Waterdepth is available in Inspect; shallow flooding need not render as deep blue ocean.

Known diagnostic caveat: a habitat-temperature line printed sentinel extrema after all vegetation fell below the report threshold. This means “no vegetated cells,” not an actual9726°C temperature. Final world schema validation passed. A later report should explicitly print “no vegetated cells” instead. The native shutdown allocator diagnostic remains.

A second native intervention run additionally exercised the actual unchanged shared production editor handler (made public only in the temporary QA copy) at15/60Hz and1/24h simulation speeds. In all four combinations, one tap plus a two-second hold produced exactly11.0000mwater and1096.191mterrain rise. Nominal terrain amount is1100m; existing f32 coordinates near5000km produce a small quantization difference, identical across tested combinations. Test fixture edits were restored before the ecological scenario, not used to force biology. The repeated nine-day scenario again recovered4rabbits,3cumulativebirths33meals3deaths, biomass8.127 across33cells and generation2; exact8,677,569-byte save roundtrip passed. Nativeelapsed51.613s. See `evidence/intervention/handler-regression.log`.

The preparation script now prints “no vegetated cells” for empty-habitat temperature diagnostics on future runs; retained raw logs preserve what was actually observed. Production ecology was not retuned for this intervention.

## Truthful goals and nearby-animal feedback (v11)

`egl-feedback-prepare.py` wraps the real nine-day intervention scenario and asserts goal progression from live fields: initial barren `plant`; seed patch `add_pair`; added animals `feeding`; two actual meals `offspring`; actual birth with current grown/descendant plants `living`; flooded extinct patch regresses to `plant` despite historical births/meals; restored habitat returns to `living`. The final stage is an ongoing instruction, not proof of permanent resilience or a completed game. A snapshot after exact save/restore still reports the same real current conditions.

Actual result: 9days,4rabbits,3cumulativebirths33meals3deaths,biomass8.127,33vegetatedcells,plantgeneration2. Exact8,676,503-byte save/delete/restore passed. Unit tests also verify empty/new-world reset and animal removal returning no status. No production ecological behavior was modified for this milestone.

Visually inspected `evidence/feedback/gestation-inspect.png`: actual nearest female at24hours age,93.40%fullness,12hours minimum gestation time is displayed as24.0hours/93%/12.0hours, with explicit food/space caveat. It does not pretend the animal is currently eating or moving. Nearby animal index is recomputed each inspection, not retained across removal/reordering. Real logs and phase screenshots are in `evidence/feedback/`.

A recovery instruction was subsequently generalized from “drain flooded ground” to “check water and temperature” so historical deaths alone do not imply a particular cause. Goal predicates and tested simulation remain unchanged. Existing shutdown allocator-leak diagnostic remains; this is native mobile-layout verification, not physical Android testing.

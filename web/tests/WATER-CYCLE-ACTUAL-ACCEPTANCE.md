# Water-cycle candidate: actual engine acceptance

Candidate sources were copied into a temporary native harness. No biology,
traits, nutrient or carbon were assigned. One explicit starter seed was used.
Normal Grow rate is 6 simulated hours per real second (240 frames per game day).
All tests use the same deterministic generated world with 40,962 patches.

## Fixed prior flood case: cell 13508, explicit 5 m central shelf
The central floor is raised 10 m with 5 m water; neighbors retain 15 m at the same
initial water surface. This experimental geometry is NOT the production 15 m
basin. Cell 13508 is fixed to match the previous diagnosed case, not searched for
favorable outcomes. Physics is the frozen atmospheric candidate.

First 15 days, actual transfer budget:
- Rain: 0 m (previous model: 107.275 m).
- Evaporation: 0.500946 m.
- Liquid inflow: 2.852930 m.
- Liquid outflow: 0.040430 m.
- Net depth increase: 2.311554 m, versus previous +24.117 m.

At day 30 (120 seconds of normal play):
- 181 accepted, parent-funded propagule arrivals; 130 tracked colony losses.
- 14 occupied patches; 39 living cohorts; maximum generation 4.
- Actual forms: 9 mats, 10 cushions, 10 rosettes, 7 ribbons, 3 branching.
- Total biomass 0.67460 kg C/m² summed over cells, versus previous 0.00540.
- Selected depth 8.056912 m, versus previous 31.004263 m.
- Topology has reciprocal unique nonself edges; self-filled slots are permitted.
- Exact save roundtrip, invalid-save rejection and transient reset checks pass.

This demonstrates real exploration, loss and inherited diversity in this tested
scenario, not universal success or complete evolution into animals.

## Ordinary improved Find habitat: production 15 m basin
The read-only focus function was recopied after the parent's ranking fix and
selected cell 13596, latitude z=0.22653137. No fixed-cell override or nursery was
used. Day 30: 5 arrivals, 2 tracked losses, 3 occupied patches, biomass 0.02948.
This survives and spreads slowly; it is not the dramatic nursery result.
Topology and exact save checks pass.

## Precision and performance limits
Liquid+vapor total drift over 30 days was +6.88e-5 (0.00688%) in both scenarios.
Report this measured float-storage drift, not exact conservation. No hidden
balancing adjustment was used. Mean native update time was 24.93 ms for the
instrumented fixed case and 24.59 ms for ordinary 15 m on 40,962 patches; maximum
187.6/228.4 ms. This is not a phone-browser frame-rate guarantee.
The pre-existing native shutdown GPA leak warning remains; process exits zero.

## Evidence labels and camera limitation
The first prepared harness inherited a generic `production_15m=true` daily-log
tag. That tag is wrong for the explicitly overridden fixed nursery case; actual
HYDRO_START, selected water and assertions show 5 m. The reusable preparation
script now labels it `water_candidate=true`. Do not use the inherited tag to
infer geometry. The fixed-cell override did not recenter the QA camera, so its
`visiblemats=0` does not measure rendering correctness. This fixture establishes
engine behavior, not a visual-playtest pass.

Logs and actual source hashes are in `results/water-cycle-*`. Reproduce with
`egl-water-acceptance-prepare.py`, then native `egl-origin-build.zig`. The optional
`QA_FOCUS_SOURCE` selects the current production read-only focus implementation.
Fixed comparison uses `QA_FIXED13508=1 QA_NURSERY=1 QA_HYDRO=1`; ordinary 15 m
unsets those. Both use the existing coupled, single-seed, 30-day Grow harness.

## Old-climate compatibility is a separate risk
Existing saves can contain supersaturated vapor inventories produced by old
transport. The corrected condensation phase can rain out that already stored
water after loading. Schema compatibility and exact restore are not a promise
that an old climate becomes healthy immediately. Do not silently remove water,
normalize humidity, reset terrain or discard a user's saved planet. Fresh-world
results above should not be presented as an old-save recovery test.

## Ordinary improved Find habitat: explicit shallow comparison completed
Same selected cell 13596 and same physics, with the approved experimental
5 m central shelf / 15 m surrounding reservoir, one seed and no further care:
- Day 15 (60 normal-play seconds): 25 arrivals, 6 tracked losses, 7 occupied
  patches, total biomass 0.15362.
- Day 30 (120 seconds): 53 arrivals, 24 tracked losses, 11 occupied patches,
  total biomass 0.20312.
- Exact save roundtrip and invalid rejection pass (10,455,262 bytes).
- Global water drift +6.8822e-5 (0.006882%); mean update 24.56 ms, max 281.95 ms.

This same-location comparison shows materially more visible exploratory spread
than the ordinary 15 m basin (5 arrivals / 3 occupied at day 30). Geometry must
remain an explicitly described player action if adopted, not a hidden world
change. Neither scenario guarantees every colony survives. Logs retain the
inherited generic `production_15m=true` tag; selected-depth assertions and this
run's startup record explicitly show 5 m. Use the corrected reusable preparer for
future runs. No additional location search or curve tuning was performed.

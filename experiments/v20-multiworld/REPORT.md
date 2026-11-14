# v20 bounded fresh-world playtest

Two preselected additional worlds, seeds **42** and **2027**, were tested once each against current v20, without production edits or a favorable-seed search. Both used the actual Find habitat → Shape shallow nursery → one Seed colony path, then 30 simulated days at Grow. No refills, reseeding, trait/resource gifts, temperature intervention or forced births occurred. Existing seed1337 acceptance is background, not a third rerun.

## Results

| World | First expansion | Occupied at day30 | Living cohorts | Accepted arrivals | Tracked losses | Living forms at day30 | Final biomass |
|---|---|---:|---:|---:|---:|---|---:|
|42, selected29254|day1 /4 nominal seconds|8|15|60|45|8mats,3cushions,1rosette,2ribbons,1canopy|0.1646155|
|2027, selected2542|day2 /8 nominal seconds|5|5|43|35|1mat,1cushion,3canopies|0.0431990|

Final biomass is the actual final-step total, not the daily log's sample just before the final tick. These are model biomass-density sums across patches, not a whole-world mass unit. Loss counters are bounded tracked lineage losses, not a complete death census or an establishment probability. Failed-capacity attempts are not arrivals. Actual relocation and grazing also occur, so arrival-minus-loss does not necessarily equal living cohort count.

Both survive and spread for 30 days. Neither result proves indefinite stability. Seed42 peaked around day15 then declined moderately; seed2027 grew to about0.106 at day15, then fell to0.0432 by day30. In2027 selected patch nutrients fell from0.02 to0.00209 while detritus accumulated, temperature stayed about294–295K, water rose to8.07m, and real grazing was recorded. Those observations suggest resource cycling/competition and light availability should be inspected, not a claim that nutrient shortage alone caused all deaths. It would be misleading to label the declining world simply “thriving.”

## Timing and visibility

Thirty days at Grow corresponds to **120 nominal simulation-paced seconds**, not a measured phone time. Native update means were26.084ms for42 and26.336ms for2027, roughly187.8/189.6 seconds of simulation-update wall time over7200 fixed-step harness updates, excluding initial generation, rendering, saves and shutdown. Both exceed a16.7ms60Hz budget before rendering. Maximum updates274.8ms/205.1ms. No phone FPS claim.

Final actual renderer reports5 visible occupied patches for42 (8 globally occupied),3 for2027 (5 globally occupied). Screenshots `results/seed-42-day30.png` and `seed-2027-day30.png` are native mobile-mode captures of the real final state. They use the normal tool bar/Seed mode because the simulation harness does not trigger the browser shell's Watch flow; do not treat that mode as the new user's post-seed Watch experience. The previously reviewed1337 compact Watch capture remains the direct Watch proof.

## Next bounded usability test, not a biology tuning request

1. Measure a **Fit living cluster** camera action in Watch against fixed founder-centered framing: occupied cells visible before/after, screen occupancy, and smallest form's pixel size, with no model change. Current images devote much of the screen to blank water; a user can miss real expansion beyond the initial camera.
2. Display current living patches and recent actual arrivals/losses alongside the existing biomass trend. A rising lifetime birth counter alone disguises the2027 decline and could feel like random disappearance. Use measured counts, not a success guarantee or a fabricated “established” stage.
3. Profile update phases before changing rates or clock multipliers. The current native update cost alone already exceeds60Hz; speeding the clock would not fix readability or sluggish interaction.

No production tuning was made. Save exact-roundtrip, invalid atomic rejection and transient reset tests pass in both worlds. Native process exit0 in both; existing allocator shutdown warnings remain. World water+vapor relative drift:2027 −0.004619% (absolute metric reported by log), within the already disclosed floating-point limitation. See source-commit.txt/source-hashes.txt and full logs for provenance. Source differs from earlier1337 only in production UI integration, self-neighbor propagule skip and removal of inactive hydro diagnostic fields; do not present them as perfectly identical-source replicates.

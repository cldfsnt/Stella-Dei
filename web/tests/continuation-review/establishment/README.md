# Actual-Planet daughter establishment baseline

## Finding

**Stable late succession is not established. A severe rare-daughter establishment bottleneck is demonstrated in the existing production scheduler.** This is not a request to force stronger competitors to win. It identifies a mechanism worth testing before changing ecology.

The real `Planet.simulateMicrobes` was run for 180 days on a controlled 19-cell graph, from an ordinary simple founder, at three PRNG seeds. After day 30, almost every daughter in stable habitats dies within one day despite abundant empty cohort slots. A separate funded-propagule contrast demonstrates that the existing grazing response can consume an entire rare daughter in one tick.

## Method and scope

`src/qa_establishment.zig` constructs a minimal real Planet with six symmetric ring neighbors per cell, 303K temperature, 1m water and alternating half-day sunlight/darkness. Each patch begins with nutrient 0.12. A finite shared atmosphere holds 10 carbon-equivalent units per cell for each CO2/O2 pool. The ordinary seed debits this inventory. The production scheduler performs physiology, relocation, randomized donor order, tiny propagule dispersal and larger local/neighbor reproduction. No production files are modified.

Treatments at seeds 42,1337,2027:
- 0: stable environment.
- 1: day60 clears every third patch, transferring living carbon into detritus and releasing bound nutrient.
- 2: day60–63 water depth is 8cm; afterwards 1m resumes.

All use 1,440-second simulation ticks. An additional seed42 mosaic run keeps six of19 patches at8cm/293K and the remainder at1m/303K, with the founder in a wet patch. An additional seed42 stable run uses 720-second ticks with identical simulated day/night periods. This is controlled topology/environment, not generated terrain or a full water/climate simulation. No claim of mobile rendering or performance follows.

Every daughter born after day30 is tracked by globally unique lineage ID. Global post-step matching distinguishes disappearance from relocation. Records include sampled peak mass, offspring, moves, age at death, birth mass and number of fully occupied neighboring patches. State sampled after the scheduler can miss a pre-reproduction peak because parent mass is immediately debited: `peak_ge002` is a lower bound, while an observed child with that parent ID proves reproduction. Birth-neighbor occupancy is measured at end of the birth step, not exact admission time. Pre-step eligible-parent/full-edge counters describe opportunities, not precise failed-call reasons. Young surviving cohorts at day180 are right-censored.

All steps check valid cells, nonnegative atmospheric pools, aggregate carbon and nutrient conservation within 0.001. No mutation is added outside ordinary production reproduction. No displaced lineage is silently replaced by a designated winner.

## Stable results at day180

| Seed | Postday30 daughters | Deaths within1day | Became parent | Sampled peak >=0.02 | Full cells at endpoint | Max generation |
|---|---:|---:|---:|---:|---:|---:|
| 42 | 31,002 | 30,920 | 19 | 15 | 0/19 | 5 |
| 1337 | 28,896 | 28,836 | 18 | 17 | 1/19 | 6 |
| 2027 | 29,824 | 29,824 | 0 | 0 | 0/19 | 5 |

Global ID tracking records 11/12/0 moves among these cohorts; moved organisms are not misclassified as deaths. The same persistent maximum generation is already present before late tracking. Thousands of newborns, mostly production-size 0.004, therefore do not imply successful replacement, establishment or continued deep ancestry.

At 720-second steps, seed42 still loses 28,394 of 28,449 postday30 daughters within one day (99.81%); only six become parents, endpoint full cells1/19 and maximum generation5. Exact populations differ, so the system is not step invariant. But the establishment bottleneck survives this half-step check.

Patch-clearing permits more late parents (64/47/30) and maximum generation7/7/6. The shallow-water shock permits74/92/55 late parents and maximum generation6/6/6. Both recover to19 occupied patches by day180. This is disturbance-enabled establishment/recolonization, **not evidence that a prescribed pioneer or stronger lineage wins**. Neither test alone proves the full desired succession cycle.

## Heterogeneous-habitat sanity check

One additional seed42 run uses the unchanged production scheduler with six8cm/293K pockets among thirteen1m/303K patches. Unlike its homogeneous counterpart, maximum observed generation progresses5 at day30 to7 at day60,8 at day100 and9 at day180. There are48 postday30 cohorts that become parents versus19 in the homogeneous control, and38 sampled peaks>=0.02 versus15. At day180 there are39 living cohorts in19 occupied patches, versus19 cohorts in19 patches for the homogeneous control. Thus late progression is possible in the current model and environmental variation matters; describing the system as universally generation-capped would be false.

Losses remain severe:14,716 of14,995 late daughters die within one day (98.14%). This one seed does not prove general niche coexistence, trait-specific causes, or stable pioneer-to-strong-competitor succession. The two habitat dimensions change together, so temperature versus water cannot be separated. Follow-up should trace surviving lineage traits by patch and repeat across seeds. The result weakens any argument to change grazing solely because a homogeneous crowded habitat excludes newcomers.

The isolated encounter-response candidate was also rejected, not shipped. See `REJECTED-ENCOUNTER.md` and its saved log for failed regression checks and absence of reliable succession improvement. Slower consumption alone is not a valid success criterion.

## Mechanistic contrast: funded rare offspring

`src/qa_grazing_establishment.zig` uses actual `propagate` to debit a donor and create a0.004 daughter beside an existing0.8 resident with feeding0.14. A copied control changes only resident feeding to zero. Both then use actual `step` at1440s,303K,1m, darkness, ample finite per-call resources.

- Feeding resident: daughter biomass0 after one tick; grazed carbon0.00399564.
- Feeding-zero resident: daughter0.00399565 after one tick and0.00374691 after one day; no grazing.
- Both preserve the carbon/nutrient ledger.

Setting feeding to zero also changes the resident's baseline mortality; this is not a whole-world knockout. Darkness removes photosynthetic-rate differences, and the measured grazing flux accounts for the missing daughter directly. The current uptake requests resident biomass ×3×feeding×days and then caps at total prey, so a rare target can be fully consumed regardless of scarcity. Here requested intake is approximately0.0056, larger than the entire daughter.

## Scheduler differences from the earlier ring probe

Production attempts0.004 propagules every tick when parent mass>=0.02 and earned credit>=0.01. A successful propagule immediately `continue`s, preceding0.01 local reproduction that requires mass>=0.03 and credit>=0.04. Frequent successful small dispersal can drain credit before the larger route. The earlier six-hour ring experiment used larger daughters and no actual relocation; its exact counts are not comparable.

This policy and the four-slot limit are potential secondary bottlenecks. Empty slots at late endpoints and enormous numbers of accepted tiny births show that hard slot capacity is not the sole cause in these controlled stable runs. Toughness/support currently grants no grazing armor. Newborns have zero earned credit; structure still carries costs and does not guarantee invasion.

## Next candidate evaluation

An isolated density-dependent feeding encounter/ingestion response is a reasonable mechanistic experiment, not an authorized conclusion that production should change. Compare survival-to-reproduction, age distribution, resident persistence, total grazing, carbon/oxygen use and actual competitive trait outcomes across multiple seeds and step sizes. Preserve resource constraints, no guaranteed winners, and disclose if the candidate only removes trophic pressure or still excludes rare invaders. Also compare larger versus tiny paid daughters and exact credit routing before blaming one term alone.

## Reproduction and saved evidence

With Zig0.13.0 from repository root (use absolute cache paths to avoid the known nested build-file cache issue):

```
zig build --build-file web/tests/lifecycle-build.zig -Dsource=src/qa_establishment.zig --cache-dir "$PWD/.zig-cache-establishment" --global-cache-dir "$PWD/.zig-cache-global"
zig test src/qa_grazing_establishment.zig --test-filter 'paid propagule faces'
```

`results.log` is the final eleven-run scheduler result, including imported core checks. `baseline-1440.log` retains the initial nine runs. `grazing-contrast.log` records the mechanism contrast. `build-first-failure.log` preserves the recoverable relative-cache failure with private absolute paths redacted. `SHA256SUMS` pins the actual production sources and probes. No production edits or deployment were performed by this investigation.

# Equal-stock multi-cycle trajectories: research, with an explicit failing audit

Only new `src/qa_energy_cycles.zig` and this evidence directory were added. Prior checkpoint assays, copied core and all production files unchanged. The copied actual shared-cell core and uncalibrated common-maintenance hypothesis are identical to the preceding energy-community experiment.

## Corrected comparison
72runs: basal0.2/0.6 ×slowactivity0.25/0.5/1 ×stablelight/alternatingdark/limiteddark ×sparse/crowded founders ×two slotorders. Forty days of2light/2dark cycles followed by8days uninterrupted light. Daily mass, maintenance, stress and resource observations:3456rows.

Total initial C and N now matched ACROSS densities, not only within competitive pairs. Normal totals10.8carbon-equivalent and0.18nutrient; limited0.85C/0.085N. Sparse founders0.02each and crowded0.4each. Missing bound stock is put into the initial free CO2/nutrient pool; O2 fixed10(normal)or0.01(limited). Actual f32 nutrient totals match targets within2e-8. This is deliberate initial resource partitioning, not repeated refill. Because living carbon represents prior reduction, matching C/N while holding O2fixed is a controlled inventory comparison, not a reconstructed geological history.

## Status: DO NOT CALL FULL SWEEP PASSED
All72runs complete and report errors; final test intentionally fails if any original conservation tolerance is exceeded. Four runs fail nutrient tolerance1e-5: basal0.2, equalactivity1, stablelight, both densities and both slots. Maximum nutrient error1.9566e-5; maximum Cerror in those runs8.422e-5 (below original1e-4). Original stopping failure ataboutday29 preserved in first-budget-failure.log.gz. No tolerance relaxed and no stock reset. Final log records budget_failures=4, BUILD_EXIT=1;65other tests pass, including neutralactivity exact production-core parity. This is a long-run numerical integration limitation, not evidence for a beneficial trait. All selected plotted0.6/activity0.5 scenarios meet original ledgers.

## Substantive outcome
Among24unequalactivity/environment/density settings (counting one slotorder), slow has greater living mass in2atday20, ZERO atday40 and ZERO after day48recovery. Thus the earlier20day slow advantage was transient, not demonstrated lasting dominance.

For basal0.6/activity0.5/initiallycrowded alternatingdark:
- Day20(enddark): fast0.11702128 vs slow0.14966847.
- Day38(endlight): fast0.50049280 vs slow0.22433592.
- Day40(enddark): fast0.13915645 vs slow0.11365298.
- Day48(after8lightdays): fast0.57329310 vs slow0.19915672.
- Cumulative maintenance at48: fast9.02443 vs slow3.23718kgC/m². Repeated fixedcarbon acquisition funds these repeated expenditures; no free biomass is added.

Slow has shallower dark losses and lower real demand, but faster acquisition recaptures shared resources and amplifies founders across cycles. Under limitedresources three slow combinations go extinct by48days, with no revival. Both advantages and costs are real within the assumed model; no outcome is forced. No offspring, mutation, movement, niche diversity or inherited persistence appears in these fixedcohort assays.

Slotorder differences remain numerical, maxliving2.3842e-7, within declared1e-5comparison. Original core adds f32 mortality/detritus by slot, so exact whole-state bitwise symmetry is not claimed.

## Explicit trajectory artifacts
`trajectories.png` and `.svg`:6panels (three resource/light settings ×two foundingdensities), basal0.6 and activity0.5. Shaded intervals are actual darkwindows; dashedday40 begins constantlight recovery. Actual pixels inspected, labels/caveats legible. `plot.py` recreates from `results.json.gz`. Graph labels explicitly note the overall sweep's4failed equalactivity controls. The graph does not pretend endpoint survival is evolutionary fitness.

## Inheritance feasibility AFTER outcomes
Actual core reproduction starts `var child=parent.*`, then funds child biomass from parent and mutates selected existing fields. A genuine metabolic-pace trait could technically be copied and mutated there, but the current external activity[slot] array must NEVER be used as inherited identity: slots change on death/movement and would silently swap phenotypes. Correct experimental integration needs a per-cohort trait or a lineage-keyed sidecar maintained through every birth, move, replacement and save. A new experimental per-cohort field is clearer than magical slot assignment, but production schema changes are not justified yet.

Existing `efficiency` is already inherited within0.5–1.3 and changes light acquisition, canopy shape and a nonrespiring uptake penalty. It is not equivalent to metabolic pace. Reusing it avoids a field but would redefine old organisms and visual semantics; need a separately declared efficiency-demand hypothesis, tests and migration policy. Current experiments cannot choose this without changing meaning.

Before a genuine heredity experiment:
1. Diagnose/fix the experimental common-maintenance+f32 nutrient accumulation so prolonged equaltrait controls meet declared accounting, rather than widening tests silently.
2. Add a copied experimental cohort field for pace, bounded>0; explicitly couple real uptake and respiration. Defaults apply only to experimental worlds, not silently existing saves.
3. Use actual donor-funded propagate/reproduce and mutation. Show child trait copied/mutated, tissue/resource funding, parentage and no resurrection; full slots and patch relocations cannot change a lineage's pace.
4. Measure descendant establishment and invasion from rarity across repeated environments, not just starting50:50mass or fixedfounder endpoint. Demonstrate sustained costs/benefits without demanding slow win.
5. Add resting state only separately, with paid transitions and actual ownership; current slowactive experiment is not dormancy.

The next useful candidate is a transparent experimental trait with measurable tradeoffs, NOT a promise of inevitable stronger late succession. Nothing in this checkpoint was shipped.

## Reproduce
Zig0.13.0: `zig test src/qa_energy_cycles.zig -O ReleaseSafe`. Expect current audit failure, not a green result. `run.log.gz`, `results.json.gz`, `first-budget-failure.log.gz`, source hashes and plotted trajectories preserve evidence. No commit/push/deploy performed by this worker.

## Lossless compact archive
The three raw evidence files are stored as `run.log.gz`, `first-budget-failure.log.gz` and `results.json.gz`, using gzip level 9 with deterministic `mtime=0`. Each archive was decompressed and checked byte-for-byte against its untracked original before the redundant uncompressed file was removed. `UNCOMPRESSED-SHA256SUMS` records the original byte hashes; `SHA256SUMS` covers the archives, source dependencies, this memo, plot source and existing figures. No rows or failures were removed.

Read logs with `gzip -dc web/tests/continuation-review/energy-cycles/run.log.gz`. Recreate the graph with `python3 web/tests/continuation-review/energy-cycles/plot.py` (requires matplotlib); it reads the compressed JSON directly. Validate the archived raw hashes from this directory with `for f in run.log first-budget-failure.log results.json; do gzip -dc "$f.gz" > "$f"; done; sha256sum -c UNCOMPRESSED-SHA256SUMS`. The audit remains **4/72 failed**, not a passing experiment.

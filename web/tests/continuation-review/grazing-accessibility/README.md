# Paid-support grazing accessibility: isolated research, not shipped

No production ecology, schema, graphics or UI changes. The helper and generated copied core are experimental. No commit, push or deploy by this worker.

## Hypothesis, not calibrated plant armor
Accessible prey carbon = fronds + support / (1 + k × inherited structure), for tested k=0,1,2,4. Only actual paid support receives reduced accessibility; fronds remain fully accessible. Zero support or zero structure yields no protection. Intake rate scales by accessible/total available prey, then simultaneous prey demands are distributed by accessible mass. This is a phenomenological handling-cost hypothesis, not a claim of real plant taxonomy or measured digestion.

The model is not immunity: at k<=4, even fully supportive tissue remains accessible. `graze` refuses k outside[0,4], invalid nonfinite inputs or invalid cells without mutation. Subnormal accessibility is floored at the smallest positive f32 so that a positive all-support input does not round to exactly zero accessibility; this does not claim meaningful grazing flux below the existing biological establishment cutoff. Tiny unresolved cohorts are still handled by the unchanged core.

Same existing growth penalties, structural respiration, canopy geometry, mortality, feeding investment and physiological rules. Carbon bookkeeping remains half consumed assimilated, one quarter respiration (finite oxygen bounded), one quarter detritus; associated nutrients return once. Support loss/gain is proportional as in existing core. This does not explicitly separate ingestion of fronds from stems: accessibility is a bulk handling coefficient, not selective tissue anatomy. No free defense from inherited structure alone, new resources, beneficial mutation or prescribed winner.

## How actual core physiology is used
`grazing-accessibility-prepare.py` generates an isolated copy of the production microbes module, replacing only graze dispatch with this helper and an explicit experiment-only enable switch. `step` still executes original mortality, growth, allocation, support costs and decay. Production files are untouched. An independent original copy is used for zero-coefficient grazing parity; compared field-by-field (not undefined struct padding).

## Executed
- Final primitive/control suite:34 tests including imported original microbial regressions. Support-required effect, immediate C/N receipts, oxygen cap including tiny oxygen, zero-oxygen/invalid atomic refusal, zero coefficient exact original results, combined tissue validity, empty-cell no resurrection, all-support/tiny accessibility and coefficient bound.
- Controlled60-day matrix:4coefficients ×2light levels (1/.2) ×4grazing investments (0/.1/.4/1) ×2initial resource budgets ×2producer slot positions =128cultures.1440-second core steps; no breeding or refills. Two assigned producer phenotypes differ only in inherited structure0/.7; both start0.2 biomass,0.04 actual support and organization.2. Third cohort always starts0.1 biomass, with tested feeding investment. A feeding0 third cohort is the no-grazing control, preserving initial biomass; positive feeding cohorts are mixotrophs, not animals. Rich starts free nutrient.12 and atmospheric carbon10; tight starts.005 and.02. Oxygen10 in both. All growth/feeding costs remain active; resources finite.
- Real evolved donors: production `Planet.simulateMicrobes` creates six extant donor phenotypes after180days across three19-cell worlds, seeds42/1337/2027, wet/shallow heterogeneous conditions. This is the actual spatial reproduction/mutation/movement scheduler with controlled habitat, not full hydrology. Extract largest living wet-origin and shallow-origin cohort, preserve all inherited traits and real support fraction.96matched reciprocal cultures:3seeds ×4coefficients ×2light ×grazing enabled/disabled ×2slot positions. Each60days with no reproduction in assay, equal.1 donor biomass each, free nutrient.12, carbon/O2 ten each,303K and1m water. Grazing-disabled arm is a deliberate mechanism-ablation control: original feeding costs remain. It is not a different evolved organism.

## Findings
- In all64distinct assigned-phenotype conditions (excluding slot duplicate), strong producer is extinct byday60. Weak producer survives16. Toughness defense did not outweigh existing costs here. This valid negative result was not tuned away.
- Primitive matched-prey control does show less immediate consumption of tough paid support. Long-run total consumption can increase because altered survival/growth changes later supply; reduced intake is not guaranteed benefit.
- Evolved seed42 shallow donor (generation5, feeding.09237, supportfraction.12243, structure.34228) wins with grazing but loses to wet donor without grazing. **That reversal already happens at k=0**, so it demonstrates existing real feeding strategy, not success of new protection.
- Across these evolved assays, changing k0→4 does not change final winner. Seeds1337/2027 wet donors win with grazing at both light levels; disabling grazing permits different coexistence amounts. Both slot orders agree within1e-5.
- Floating-point resource bounds: per-step carbon error <=3e-4 and nutrient <=3e-5 in60-day assays. Known baseline f32 accumulation exists: seed2027 k0 grazing bright case carbon error about−1.69e-4 and nutrient−1.19e-5, comparable at k4. This is not exact numerical closure or proof of arbitrary long-run stability. No tolerance was increased after a failure.

## Recommendation
Hold this as research, not a marketed new adaptation. Existing evolved grazing already creates meaningful competition and can be surfaced through discovery/inspection. New paid-support accessibility has a local handling effect, but the tested evidence does not establish a useful new ecological strategy or better gameplay. No wildfire, fire regrowth, drought-proof plants or animals are demonstrated.

## Reproduce
```
python3 web/tests/grazing-accessibility-prepare.py <isolated-src>
zig test <isolated-src>/main.zig -O ReleaseSafe
python3 web/tests/grazing-accessibility-prepare.py <isolated-evolved-src> --evolved
zig build --build-file web/tests/lifecycle-build.zig -Dsource=<isolated-evolved-src>/main.zig --cache-dir <absolute-cache> --global-cache-dir <absolute-global-cache>
```
Pinned Zig0.13.0. Use existing project's dependencies for lifecycle build. Initial test-only @bitCast of non-layout-guaranteed structs failed compilation; fixed with field-wise copying/comparison before successful runs. Final logs and source hashes accompany this report.

# Wet competition shows a relative canopy allocation cost

All36 preregistered runs completed,35 total tests including inherited core tests pass. Source hashes are unchanged from before execution; independent fire review accepted the design before running. No rate tuning, retries, parameter changes, reproduction, mutation, movement, refills or production edits. Every252 daily observation and36 endpoint is retained.

## Actual outcomes

In every unequal allocation run (A root0 / B root.25), A receives initial shared-light0.444503963 versus B0.418126583. Both began with exactly half the donor's biomass/support/credit/history. A eventually holds all surviving cohort biomass, independently of swapped slots and synthetic IDs.

| dt seconds | A share days1 /2 /3 | B first reaches zero, days | A final biomass kgC/m² |
|---|---|---:|---:|
|1440|.516710 /.572453 /.765016|3.5000|.13599910|
|720|.516836 /.573049 /.767818|3.4833|.13599916|
|360|.516900 /.573355 /.769260|3.4708|.13599904|

Slot swaps change some final biomass by approximately1.49e−8, not direction/fate. Identity swaps do not change measured outcomes. First-zero time is an observation, NOT a cause-of-death classification.

Equal-allocation controls (0/0 and.25/.25) remain exactly50/50 at each endpoint. Their final per-cohort biomass is identical between allocation treatments at a given dt: .0676486641 / .0678237751 / .0679107830 respectively. This negative/control result matters: the implemented opportunity cost is RELATIVE competitive light interception, not an absolute productivity penalty when all competitors allocate equally. Do not claim the test establishes a general energetic cost of roots beyond the model's unchanged support maintenance and canopy partition.

Actual feeding was retained. Aggregate grazing is approximately.292–.293kgC/m² over7days in unequal runs, so feeding/resource feedback can amplify initial light asymmetry. The experiment does not isolate a grazing-free canopy effect, assign per-cohort fixation from aggregate flux, or prove which process directly killed B. Finite nutrients become scarce (approximately1e−9 free nutrient at endpoints); finite gas pools remain nonnegative (CO2approximately.895). There is no scripted winner or winner assertion in the test.

## Budgets and scope

Max absolute carbon residual4.833636922e−6, nitrogen2.152052613e−7, water0; all below unchanged1e−4/1e−4/1e−9 limits from the previous assay. Initial total biomass/support/credit/history/nutrient/RNG preservation is asserted; every step validates cohorts, unchanged RNG and finite nonnegative gases. Not an exact-conservation claim for f32 biological bookkeeping.

Root478 is the source phenotype, not a new naturally evolved root lineage. IDs9001/9002 are explicitly prescribed comparison labels, with no claimed genealogy. Fully wet original surface705.580840907kg/m² gives approximately.70558m depth; temperature300K/light1 fixed. Water/vapor stay finite and unchanged because this assay invokes wet physiology without abiotic exchange or exposed demand. No soil, drought, recharge, climate, natural offspring, selection across generations, whole-world, browser or device result is implied.

This supplies the shared-resource competitive-cost evidence absent from the earlier single-colony assay. It complements, but does not substitute for, separate paid dry-survival/recovery tests and still-blocked physical-water integration gates. No production behavior or save schema changed.

Reproduce with pinned Zig0.13: `zig test src/qa_root_wet_competition.zig -O ReleaseSafe`. Source and input hashes, exact binary hash, all run/build logs, full compressed daily results and endpoint summary are included. Read PREREG.md for fixedmatrix design and independent review limitations.

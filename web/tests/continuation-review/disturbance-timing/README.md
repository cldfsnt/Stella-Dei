# Disturbance timing can reverse the surviving competitor

Source: qa_disturbance_timing.zig. Exit0 with final corrected minimum-bookkeeping. No production biological changes. Same methodology/limitations as ../disturbance/README.md, now compare a3-day exposure beginning day1 versus day10. Three180-day actual scheduler donor evolutions;96 controlled60-day pair assays (3seeds×2timings×4shocks×2habitats×2slotorders),288 recorded observations. Identical finite resources, actual M.step, no assay births or immigration. Every tick verifies state validity, nonnegative gases and carbon/nutrient ledgers. Imposed exposure is not a thermodynamically closed god-tool action or wildfire. Both timings' controls intentionally rerun.

## Observed result, not a programmed winner
In wet habitat, seeds1337/2027 untreated wet-origin cohorts displace shallow-origin rivals (.9394/.9414 versus0 by day60). Early day1 drying changes which survives: wet-origin0, shallow-origin.8680/.9059. Early combined drying+heat similarly allows the shallow-origin cohort to persist and later dominate. The same drying shock beginning day10, after competitive exclusion, leaves BOTH extinct; rewetting does not resurrect the eliminated competitor. Heat alone reduces biomass but does not change eventual winner in these runs.

Seed42's shallow-origin phenotype wins both habitats with/without either shock timing. That is a real exception, not excluded. Across shallow habitat cases the shallow-origin cohort survives in this fixture. Slot order does not change these conclusions.

Interpretation: disturbance can favor a preexisting resistant competitor, but it must still be present. Timing, inherited phenotype and local history matter. This is ecological sorting of actual evolved phenotypes; no new evolution during assays, no seedbank, no succession proof across many generations, no fire adaptation. A disturbance does not necessarily rejuvenate life. Next test is realistic funded immigration/rare establishment, not scripted replacement.

Reproduce: zig build --build-file web/tests/lifecycle-build.zig -Dsource=src/qa_disturbance_timing.zig --cache-dir <absolute> --global-cache-dir <absolute>.

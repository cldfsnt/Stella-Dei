# Ignition ecology: controlled negative result, not a gameplay feature

`src/qa_ignition_ecology.zig` copies the donor-generation scheduler and tracing from `qa_disturbance_timing.zig`; production is unchanged. Three 19-cell worlds (seeds42,1337,2027) evolve for180days through actual Planet.simulateMicrobes, 1440s ticks. Six largest extant donor phenotypes are extracted from wet/shallow zones, with lineage, generation and inherited traits logged. Donors are NOT synthetic fire-resistant designs.

## Assay
96 runs: 3 donor pairs × 2 pulse onsets (day1 or10) × 2 habitats (1m wet /0.08m shallow) × 2 cohort-slot arrangements ×4 treatments. Runs last60days. Matched initial biomass0.1 per donor, same donor support fraction, available nutrient0.12, explicitly assigned detritus0.25kgC/m², finite atmospheric carbon and oxygen inventories10kgC-equivalent/m² each. No resource replenishment/reset. Assigned detritus makes this a controlled experiment, not evidence that gameplay naturally supplies dry fuel.

Treatments:0 untouched;1 zero-depth drain for one day;2 same drain plus actual detritus_ignition primitive exactly once at onset;3 same drain plus externally supplied temperature perturbation matched to treatment2, retaining fuel/gases. The primitive is the real chemistry/ledger calculation underlying the Planet adapter, but this assay does NOT run the player action or full planetary hydrology. Temperatures are externally prescribed303K except the one-day matched pulse. Capacity400000J/m²/K and30MJ/kgC are declared gameplay parameters. Matching heat for a whole day and restoring303K are experimental climate interventions, not a closed energy system or a live thermal cooling trajectory.

Donor generation uses full spatial reproduction; transplant assays call Microbes.step only: **zero offspring or new mutations during these60days**, fixed-phenotype sorting. No seedbank, dormancy, resprouting or firearmor. Extinction tick logged; zero mass must stay zero thereafter. No living-tissue, nutrient or RNG change at ignition. Biomass may change subsequently through ordinary biology.

## Audit and results
All96 runs and imported unit tests pass (BUILD_EXIT=0).288 reported snapshots,96 extinction records. Slot swaps produce identical living mass. All24 burns checked actual fuel removal, finite O2 consumption, CO2 production and heat ledger directly. Carbon and nutrient checked every step; snapshot maximum absolute errors9.81e-6 and1.49e-6kg/m² respectively, below1e-4 acceptance. No global energy closure claimed.

At every reported snapshot, **ignition and its matched external-heat control have identical living masses**. They differ in detritus and gas inventories. Thus this assay does NOT demonstrate special fire response. Seed1337 and2027 donor winners differ between wet and shallow habitat; seed42 shallow-zone donor wins both. No treatment changes eventual winner. The late shallow seed2027 pulse reaches about+52.918K and modestly changes the surviving biomass/detritus trajectory; matching heat alone reproduces its living-mass effect. Earlier and less-hot pulses mostly converge. No forced winner required or coded.

Example seed2027/shallow/late day60: untreated living0.42314535, drain0.42312592, ignition0.42310610, matchedheat0.42310610kgC/m². Detritus respectively1.4776047,1.4364880,1.4160872,1.4208406. This is tiny long-term living separation, not a compelling new fire-adapted gameplay mechanic.

## Limits and next defensible step
This establishes finite accounting and a negative mechanistic contrast in these parameterized cells. It does not establish evolving terrestrial fire ecology. Investigate wetness/heat exposure trajectories and actual recruitment on full Planet before new biology; genuinely inherited reserves or recovery would require paid resources, mortality/inheritance and save tests rather than renaming structure as fire resistance. No game deployment or biology modification belongs to this checkpoint.

## Reproduction
From repository root:
```
zig build --build-file web/tests/lifecycle-build.zig -Dsource=src/qa_ignition_ecology.zig --cache-dir <absolute-cache> --global-cache-dir <absolute-global-cache>
```
Zig0.13.0, ReleaseSafe. `run.log` includes donor provenance, full scheduler lineage tracing, intervention rows, extinction times and imported unit-test output. `SHA256SUMS` records final fixture and production dependencies.

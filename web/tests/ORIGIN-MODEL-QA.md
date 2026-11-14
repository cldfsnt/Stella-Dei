# Origin model: implemented scope and controlled evidence

## Implemented production model

Origin is a separate optional microbial mode, not a claim of complete SimEarth-style macroevolution. Sandbox plant/rabbit biology remains unchanged. `Planet.beginOrigin` accepts only a fresh world without existing sandbox life; storage is allocated on demand through the live simulation arena. A sandbox never allocates or steps microbial arrays.

Each cell has at most two distinct microbial cohorts. Cohorts carry actual carbon biomass, inherited thermal optimum/light efficiency, lineage/parent IDs, generation and reproductive credit earned only through growth. A successful reproductive event transfers0.01kgC/m² from its parent, not free biomass. Full cohort slots reject incoming propagules without silent replacement or merging. All growth precedes dispersal, preventing newborns from growing/reproducing again because of grid order. This cap limits diversity and is an explicit first-increment simplification.

Natural free nutrient stock starts0.02kg/m²; growth binds0.1kg nutrient perkg carbon. Death releases bound nutrient and retains carbon as detritus. Aerobic detritus recycling is limited by available oxygen. Photosynthesis requires actual light, suitable water/temperature, available carbon and nutrients; carrying capacity bounds total living biomass1kgC/m². More efficient light use has a maintenance tradeoff. The model is simplified, not a complete biochemical or origin-of-life simulation.

Atmospheric quantities are averaged10^9kg gas per mesh point. Local microbial carbon iskgC/m². Production integration converts via point area and point count, using CO2:C:O2 mass ratios44:12:32. Fixation/recycling ledgers are totalkg carbon; explicit player-added nutrient has a totalkg input ledger. Seed actions introduce already-living colonies and reserve their biomass from the carbon/nutrient budgets; no abiogenesis is claimed.

Shallow habitat requires0.2–50m water and260–355K. Solar input follows actual `solarConstant` and geometric daylight, not the optional inspection lighting. UI tools seed/add nutrients only on deliberate taps; time-scale/frame rate do not repeatedly add organisms/resources. No plant or animal lineage is automatically unlocked or created. Current parent links identify ancestry but do not constitute an unlimited historical genealogy archive.

## Passed controlled tests

`zig test src/simulation/microbes.zig`:
- Carbon and nutrient accounting through growth, death, aerobic recycling and donor-funded transfer.
- Darkness, no carbon and drying cannot create photosynthetic growth.
- Two actual competing traits respond to thermal selection independent of cohort array order.
- Full cohort slots preserve existing populations/mass rather than replacing them.
- A genuinely generated mutant daughter increased its living share from5% to32.48% under330K selection over30days. The no-mutation control remained5%. Living mean thermal optimum shifted303.072→303.471K. This demonstrates inheritance plus selection in the simplified model, not speciation or progression into modern plants/animals.

Actual Planet integration: `zig build --build-file web/tests/lifecycle-build.zig -Dsource=src/qa_microbes.zig` ran100days in a controlled seven-cell environment using production `simulateMicrobes`, not a replacement ecology. Six reachable cells became colonized,11 daughter-colony events occurred, generation reached3, aggregate biomass1.2kgC/m². Relative atmospheric-plus-organic carbon error5.9e-8; nutrient error1.5e-8. All states remained valid; no plants or rabbits appeared. Setting actual solarConstant0 stopped further fixation.

Sandbox regression `qa_ecology.zig` remained passing:37days,35living rabbits,39births1106meals6deaths, healthy vegetation. New wet-habitat startup testing also found and corrected an existing geometry bug: initialization had added raw water mass to radius. Initial transformed points now match terrain-exaggerated upload geometry.

## Separate acceptance still required

Controlled evidence above is not full climate/water-coupled, browser or physical Android evidence. Actual rendered seed/growth/intervention, new-mode exact persistence, corruption rejection, old Sandbox save compatibility and startup/performance are handled by integration acceptance. Do not claim these passed from unit tests alone. New mode's initial atmosphere is inherited from the existing world generator; it is not a scientifically reconstructed primordial atmosphere.

## Coupled generated-world climate correction (2026-11-13)

Release was blocked after the first ordinary five-day test nearly extinguished
its starter (.02→.0001296 biomass, zero births). The controlled render demo alone
was not adequate gameplay evidence. An identical shallow, low-latitude habitat
with legacy equations reached 327 K and dried out; no biological tolerances were
expanded to mask this.

Origin now uses dimensionally consistent surface corrections, while Sandbox
retains its original expressions:
- Heat capacity adds actual water mass per cell area to the ground active layer.
  Water is capped at an explicit **50 m active mixed layer**, an approximation,
  not a comprehensive ocean model. Previously raw mass blended specific heat
  while total mass remained a 0.1 m ground slab.
- Height-limited water transport is height difference divided by km per mass,
  multiplied by a dimensionless timestep fraction and bounded by available
  shared water. The old expression multiplied by mass twice.
- Evaporation still uses the existing instantaneous saturation approximation;
  no claim of a physically complete climate or timestep-identical trajectories.

Pure surface_physics tests verify depth/grid invariance and closed two-cell
water+vapor conservation. Actual 40,962-cell, five-day totals separately show
float32 drift: 60-second steps lose 3.6704e-5 relative (0.00367%); 1440-second
steps lose 1.4159e-6 (0.000142%). This is small observed drift, not exact global
conservation. At normal speed corrected starter biomass .02→.035354 with one
real daughter lineage; fast speed .02→.102620 with one daughter. Neither result
establishes guaranteed spread or multicellular evolution.

Reproducible final production-focus gate:
```
python3 web/tests/egl-origin-coupled-prepare.py /tmp/stella-origin-final-src
zig build --build-file web/tests/egl-origin-build.zig -Dsource=/tmp/stella-origin-final-src/main.zig --prefix /tmp/stella-origin-final-out
STELLA_ORIGIN_COUPLED=1 STELLA_ORIGIN_WIDTH=390 /tmp/stella-origin-final-out/bin/stella-egl
# Add STELLA_ORIGIN_FAST=1 for five days at 1440-second updates.
```
Run from repository root for assets. The harness fixes only the new-world RNG
seed (1337), uses production Habitat selection and actual Seed click, then
normal update with full climate/water. It does not assign temperature, depth,
biomass or offspring. Save validation rejects corrupt shape without changes and
compares exact JSON after restoration. Native shutdown allocator leak remains
an existing caveat; this is EGL native mobile-branch proof, not physical Android.

Final current-source production Habitat→Seed gate **passed** (same real cell13596,
2.9297 m initially, latitude direction z=.2265). Normal five days yielded
.03535427 biomass, one daughter/gen1,1.45084 m water and289.506 K. Fast five days
.10261974 biomass, one daughter/gen1,2.25179 m and294.086 K. Both remain one
occupied cell: no claim of coupled-world spread. Both actual saves rejected a
corrupt shape without changing live state and restored byte-identical captured
JSON (21,459,887 /21,585,884 bytes). Production source was frozen after these
checks. Evidence logs and PNGs: `web/tests/evidence/origin-coupled`.

Sandbox 37-day controlled regression after the conditional physics integration
remains exactly35rabbits,39births,1106meals,6deaths and5.297848plant biomass.

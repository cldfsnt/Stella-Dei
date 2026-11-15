# Natural day60→90: existing grazing changes the community

**Isolated research only. No production changes or new traits.** One actual naturally evolved saved world, full coupled current Planet scheduler, two matched independently restored arms. Preregistration in PREREG.md preceded execution. The copied core adds one QA switch around the existing graze call; disabled arm retains all inherited feeding costs, growth, mortality, support, movement, reproduction/mutation and hydrology. No experimental realized-receipt/pace code imported. Exact source and local full-save hashes in provenance.json. Native engine, not browser or Android throughput evidence.

## Results

Both arms start64 colonies in37 patches, living biomass density sum2.591618, baseline IDs identical. All counts refer to cohorts, not species/individual animals. These photosynthetic microbial forms can also feed; no clean producer-versus-animal split is modeled.

|Day|Normal colonies / patches|No-grazing colonies / patches|Normal biomass sum|No-grazing biomass sum|
|---|---:|---:|---:|---:|
|60|64 /37|64 /37|2.591618|2.591618|
|63|67 /39|130 /38|2.556040|2.850161|
|70|56 /37|150 /39|2.422153|3.087243|
|80|44 /38|152 /38|2.178950|3.364880|
|90|41 /37|152 /38|2.009138|3.428123|

Atday90 normal grazing retains29 of64 initial IDs and12 living newly born IDs, after1,440 births. Disabled grazing retains62 initial and90 new IDs, after610 births. We scan the whole world, not only selected patches. Endpoint disappearance is not assigned a particular death cause. Intermediate lineage histories are not reconstructed.

**Slot saturation matters:** independently parsed final saves show all38 occupied patches in the no-grazing arm have4/4 slots full. Normal arm has35 singleton patches, one2-colony patch and one4-colony patch. Thus greater cumulative births with grazing does not mean healthier/more successful organisms; it accompanies lower standing population and turnover. Fewer births without grazing coexist with occupied reproduction destinations. This is a real mechanism effect in this particular model/world, not universal feeding fitness or calibrated natural ecology.

Density sums add per-patch kg C/m² and are not planet kilograms. Multiply by shared point area7,669,529,600m² for total mass. Support is already included in living biomass, not extra carbon.

## Actual30-day cumulative flows

|kg carbon|Normal|Grazing mechanism disabled|
|---|---:|---:|
|Fixed|111,122,847,092.653|115,900,083,909.151|
|Recycled, including respiration|121,443,581,780.047|112,473,237,869.815|
|Consumed by grazing|40,454,582,500.807|0|
|Grazing respiration|10,113,645,625.202|0|
|Movement respiration|10,090,767.658|1,873,828.077|

Existing grazing materially consumes tissue and feeds back into subsequent reproduction, survival and spatial slot occupancy. Both grazing counters stay exactly unchanged on every ablated tick. Final biomass-weighted feeding is .208675 versus .155849; this is composition after an intervention, not proof of selection strength or an optimum. Reproduction and mutation consume RNG differently once the populations diverge, so individuals do not receive paired identical stochastic histories. Patch coverage stays similar while local coexistence/count differs strongly.

## Validity and accounting

1,800×1,440second coupled steps per arm,3,600 total. Every tick validates every cell with production validCell and finite nonnegative global O2/CO2. Checkpoints validate unique living IDs, parent<child, and finite nonnegative liquid/vapor. Independently frozen serialized world starts exactly identical; original world restored exactly at end. Full final saves remain local. Neither assert means exact long-term resource closure.

Represented total carbon = (living+detritus)×area + globalCO2×12/44. Total nutrient = (free nutrient+living×production nutrient ratio)×area. Detritus nutrient was already released; support is a living subset. Residuals include existing f32 tissue/gas arithmetic and other full-model processes. No corrections or post-result tolerance changes:
- Normal final C residual **+34,014kg** from8.4272730588e15kg initial; N **−845.044kg** from6.2831852903e12kg.
- Disabled C **+22,975kg**; N **+3,853.026kg**.
- Total liquid+vapor residual normal **−69,050,176.693×10^9kg**, disabled **−69,049,367.277×10^9kg**, about42ppm over30days. Prior coupled-water drift remains unresolved; do not claim exact global conservation.

Full gases, water, support, nutrients, forms and all checkpoints retained in results.json. Exact biological receipts are not implied by large-reservoir relative residuals. No ecological winner was prescribed or coefficients tuned.

## Practical interpretation

Feeding is already consequential, not merely an inspector history label: in this one natural world it substantially reduces standing coexistence and increases replacement/turnover. The experiment does **not** justify disabling it in the game, adding defense bonuses, promising universal persistence, or calling these organisms evolved animals. A useful player-facing lesson is that crowded patches can change membership repeatedly even when occupied area barely changes; existing watch/inspect tools can reveal actual behavior. No new UI implemented here.

## Reproduction and limitations

Generate with `python3 web/tests/egl-grazing-coupled-prepare.py <isolated-src>`, build using egl-propagule-visual-build.zig and Zig0.13 ReleaseSafe, then run native binary from repository root with QA_PULSE_SAVE pointing at the hashed natural60-day60.json, STELLA_ORIGIN_COUPLED=1, STELLA_ORIGIN_FAST=1, STELLA_PRODUCER_LONG=1, STELLA_FORMS_SINGLE=1, STELLA_ORIGIN_WIDTH=390 and software EGL. No timing claim. Source-generated hashes pin the copy.

Final build/run exit0. Initial QA-only variable-shadow and module-doc placement compiler errors and wrong-working-directory asset lookup failure preserved separately; those were not completed runs. Inherited native GPA teardown leak warnings remain. Logs losslessly gzipped with mtime0 and verified after decompression. No live deployment.

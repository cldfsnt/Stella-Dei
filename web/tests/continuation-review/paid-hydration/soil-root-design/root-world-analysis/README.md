# Fixed actual-world root-only results: endpoint attribution

Read-only analysis of all five enabled arms, with all original final diagnostics retained in analysis.json. No model or inputs changed; no additional simulation advanced.

## Known founder is not exposed

At day60+1, patch12352 has standing depth0.704838824m, temperature295.862793K, and physically funded soil0.996995223kg/m². Founder478 biomass0.1217942983kgC/m² is identical in root0 and prescribedroot.25 arms. Reconstructed paid aboveground height is0.026408m versus0.019806m: both entirely submerged. All actual sampled cumulative root demand/paid/credits are0. Conductance1/10 therefore had no opportunity to differ. The soil is almost full, so this is not a failure to fund the focal substrate.

Do NOT conclude no global ecological effect: independent comparison finds13 other endpoint paths differ between root0 androot.25 (canopy/biological flux/gas coupling); k1/k10 match except saved conductance. The prescribed allocation has costs even when no root water flows. Family tracking records paid descendants but not a naturally evolved root trait or persistent land lineage.

## Global request deficit is dominated by deep-water representation

Actual global day60 infiltration3552.44756 versus39825.46467requested is8.92%; soil evaporation1.47730. The broad number is not representative of this shallow founder: its soil reaches99.6995% of capacity from zero with no refill.

Separate prospective endpoint probes evaluate ONLY the next infiltration source-removal arithmetic, without atmosphere or advancing a tick. They use actual saved liquid/soil/T and label the slight f64 conversion approximation explicitly. Day60 source-delivery ratios by depth are99.8826% below20cm,99.1263% from20cm–2m,97.7377% from2–100m, but0.9324% above100m. In the deepest bin36,254 warm positive requests have zero represented source debit. Max native source quantum is2.08618kg/m² there, larger than the entire1kg/m² soil capacity and much larger than a1/60kg/m² per-tick request. No fractional source credit was invented to conceal this limitation.

## Error attribution limits

The largest recorded residual is condensation stage2 (max0.99741kg/m² for day60, SUMABS10803.21 over2,457,720column updates). The soil infiltration stage maximum is1.04e-16; standing evaporation maximum1.5916e-5; soil evaporation maximum3.40397e-6. Thus calling the large residual new root/soil leakage would be incorrect. Large standing-pool f32 addition has up to half a native ULP of receiver rounding, consistent in scale with the condensation maximum. Existing legacy phase also casts standing/vapor to f32, but these logs do not contain a matched per-column legacy counterfactual, so they do NOT prove the exact legacy contribution. Keep all maxima and signs. Diagnostic sums are f64 endpoint estimates, not conservative exact-Fraction bounds or approval of a whole-engine precision budget.

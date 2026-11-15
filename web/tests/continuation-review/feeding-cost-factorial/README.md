# Existing inherited feeding has real benefits and costs, with different parent/family outcomes

**Isolated diagnostic only; no production change, new trait or UI.** Preregister fe3585d preceded execution. Four independently deep-restored copies of the same actual naturally evolved day60 world were advanced to day70 by the full current v54 coupled scheduler. All original phenotypes, resources and spatial positions were retained. The two QA switches disable grazing and/or the two existing feeding-specific costs. Cost-off is an intentionally unphysical mechanism ablation, not a proposal to remove costs in the game.

## Global outcomes

Initial world:64 cohorts,37 occupied patches, biomass-density sum2.591618. These are microbial cohorts, not plant/animal species or individuals. Density sums are not planet kilograms; multiply by shared native area7,669,529,600m² for mass.

|Arm|Day70 cohorts / patches|Biomass sum|Births since start|Fixed carbon kg|Consumed carbon kg|
|---|---:|---:|---:|---:|---:|
|Normal|56 /37|2.422195|532|41,684,562,927|16,393,382,785|
|Grazing off, costs retained|150 /39|3.087280|288|38,553,561,431|0|
|Costs off, grazing retained|53 /38|2.857912|613|46,047,419,369|18,657,435,471|
|Both off|152 /38|3.515690|327|41,856,539,134|0|

Removing feeding-specific costs increases final standing biomass by.435717 with grazing and.428411 without it. Thus these costs have a material effect in the actual coupled model; they are not merely descriptive traits. Grazing lowers standing biomass/coexistence in both comparisons while increasing births/turnover. Higher births alone are not greater establishment or ecosystem success. No outcome was prescribed, thresholds were not tuned after seeing results, and none justifies the unphysical cost-off state as a feature.

## Natural focal lineages: parent advantage is not family establishment

Focals were selected from the baseline census before outcomes, not transplanted or normalized. Rich root1092 (patch13670) and initially singleton root120 (patch12344) started in similar .33/.31m water at291.85/291.87K, but their size, support, feeding, mobility, efficiency and optimum differ. **Do not treat their difference as a controlled prey-only or causal single-trait comparison.** Baseline prey-rich/poor is not a maintained exposure; offspring, migration and losses change it.

|Arm|Rich1092 root mass / observed family mass|Poor120 root mass / observed family mass|120 observed new descendants / living family members at day70|
|---|---:|---:|---:|
|Normal|.014181 / .017655|.138236 / .138236|51 /1|
|Grazing off|.014992 / .022715|.106437 / .198221|10 /7|
|Costs off|absent /0|.201727 / .227317|60 /4|
|Both off|.019673 / .023133|.129587 / .192437|7 /7|

Normal root120 retains about30% more own biomass than in the matched grazing-disabled world, but its observed connected family retains about30% less. This is a meaningful whole-mechanism parent/descendant tradeoff, not proof that its own feeding allele alone caused the difference: grazing was disabled globally, changing competitors/resources and later random trajectories too. Its lifetime intake rises from.211193 to.385806 kg C/m² in normal versus remaining unchanged with grazing disabled. Root lifetime intake is not summed across offspring or treated as a per-patch flux.

In costs-off/grazing-on, rich root1092 autonomously moves from13670 to3431 by day61 and is absent at day62's checkpoint. Do not call this direct proof that reduced cost kills it or that predation caused its loss. At its moved location there is .274155 other living biomass on day61; its exposure is no longer the starting patch. All daily observations retained, including this inconvenient outcome.

Family maps contain the initial focal plus newly born IDs observed with a connected parent after each full coupled tick. Pre-existing relatives are excluded. A birth and loss entirely within one tick can be missed; these are **observed connected descendants**, not complete lifetime pedigrees. An absent root is represented by root_present=false, not by a fabricated live zero-valued phenotype. Once absent, measured_cell refers to its original patch, not its death location. Do not infer that all51 normal root120 descendants were eaten: movement, habitat and other losses were not cause-traced.

## Accounting / acceptance

2,400 coupled1440-second ticks total;44 global daily snapshots and88 focal rows. Production validCell and finite nonnegative global gases checked every tick; living unique IDs and parent ordering checked at checkpoints. Both grazing-disabled arms have exactly unchanged grazing and grazing-respiration counters every tick. Deep serialized starts match exactly; original world is restored exactly at end. All four full endpoint saves are local only, with hashes in execution.json. These structural gates are not assertions of exact long-run C/N/water closure.

|Arm|Final C residual kg|Final N residual kg|Water residual, units10^9kg|
|---|---:|---:|---:|
|Normal|+9,937|+749.509|−22,654,364.922|
|Grazing off|−12,527|+24.381|−22,654,364.917|
|Costs off|−22,709|+1,300.344|−22,654,363.929|
|Both off|−2,945|−689.602|−22,654,363.810|

Residuals include known f32 transactions and coupled hydrology; no compensator, resource top-up, relaxed tolerance or save-format change. Support is a living-carbon subset, detritus does not carry a second bound-N pool. Full gas/respiration/detritus/nutrient/water outputs are in results.json. Baseline source/save and copied-source hashes are in provenance.json; binary/log/endpoint hashes in execution.json. Build and run both exit0; inherited native GPA teardown warnings retained in lossless logs. This is native simulation evidence, not browser or hardware speed/graphics proof.

## Substantive implication / next narrow question

Existing feeding already provides a real resource-acquisition route and pays real physiological costs. Adding a generic fast/slow trait merely for variety is not justified by this result. A sharper autonomous-establishment question is **who is being consumed**. Current graze deliberately treats all other co-resident cohorts as food, including offspring and close relatives. The normal parent/family divergence makes a bounded ancestry-resolved grazing-flow audit worthwhile before changing dispersal, prey discrimination or feeding costs. That audit must record actual transactions, not infer causes from vanished IDs. No kin preference or prey-protection bonus is implemented or promised; such an alteration would be a new, separately tested biological rule.

## Reproduce

`python3 web/tests/egl-feeding-cost-prepare.py <isolated-src>` builds on the existing grazing/natural fixture preparers, copying production without editing it. Build with egl-propagule-visual-build.zig, Zig0.13 ReleaseSafe. Run from repo root with QA_PULSE_SAVE=<hashed natural60-day60.json>, STELLA_ORIGIN_COUPLED=1, STELLA_ORIGIN_FAST=1, STELLA_PRODUCER_LONG=1, STELLA_FORMS_SINGLE=1, STELLA_ORIGIN_WIDTH=390, LIBGL_ALWAYS_SOFTWARE=1, EGL_PLATFORM=surfaceless. No screenshot or graphics quality claim from this run.

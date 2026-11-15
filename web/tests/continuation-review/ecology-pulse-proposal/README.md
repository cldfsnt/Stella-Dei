# Next bounded gameplay step: watch an ecology pulse

Read-only review against source checkpoint `5f52002c7d80c61b02e91a69db85b6c6e273b22b` (v44). Proposal, not implemented or deployed. No benchmark run and no production changes.

## Recommendation
Expand the existing **Watch this patch · 10 seconds** rather than add another speculative physiology trait. The user wants visible spreading, competition, die-off and clear response to interventions. The current watch is excellent causal restraint but reports only grazing intake. A newly seeded, photosynthesizing patch can therefore report “No grazing intake recorded” while substantial real activity happens. That is truthful but unhelpful for the principal early-game question: “Is anything happening here?”

First implementation should report:
- actual carbon fixed by photosynthesis during the watch;
- actual carbon returned to the atmosphere by the watched patch's biological update;
- current living biomass versus start, explicitly **net patch change**, not growth;
- current resident colony count versus start, plus the bounded set of start IDs still present here;
- existing actual grazing intake and simulated elapsed time.

A compact HUD can lead with “Living biomass 0.032 → 0.039 kg C/m²; 2 → 3 colonies”, then actual fixation/intake. Detailed return-to-atmosphere number can remain in a result disclosure if the mobile HUD would overflow. Do not animate fake successful dispersal, label net changes as adaptation, or add another full-world scan. IDs should follow v44's exact-string formatting, not JS Number coercion of u64.

## Exact available seams and semantics
`Microbes.Flux` already supplies `fixed`, `recycled`, `grazed`, and `grazing_respired`. `Planet.simulateMicrobes` calls `Microbes.step` once per active cell and the current observer reads `flux.grazed` immediately afterward. `Flux.recycled` combines detritus oxidation, grazing respiration and support upkeep. It is NOT mortality, nutrients recycled, or solely live metabolism. A label such as “Biological carbon returned to air” is preferable to “Deaths” or “Colonies burned”. It excludes subsequent movement respiration, god-tool ignition, external carbon edits and physical gas redistribution. Either explicitly scope it to the biological update or add actual movement receipts separately; never silently present it as the full patch carbon ledger.

The existing observer calls `finishTick` BEFORE relocation and reproduction. Net living biomass/resident snapshots must instead finish after ALL scheduler phases, otherwise a tick's child arrivals and departures are omitted and reported duration is misleading for population state. The start snapshot belongs in `patchWatchStartForState`, after current world/selection/pause validation. End snapshots read only the watched cell's four slots once per tick. Births into a previously empty watched patch must still be captured even when it was skipped by the growth pass.

Keep original world/owner guards and ten-second deadline. Finish an already admitted indivisible tick, but do not admit a later tick after the deadline. Record both before/after from the same owner and selection; cancel on load, navigation, pause/menu/hidden-tab and explicit intervention. Do not turn a modal snapshot into automatic simulation control.

Start/end identities prove only occupancy change. A missing starting ID could have moved, died, or been replaced; do NOT call it dead. A new ID here could be a birth or a relocating existing cohort. Suggested copy: “1 starting colony still here; 2 different IDs now here.” This is optional detail, not a species counter. The simplest first release may omit ID comparisons and show only count/net biomass, retaining current lineage rows for inspection.

## Optional second step, not required for first release
Record successful scheduler events touching this one patch: local births, incoming paid offspring, outgoing paid offspring, and actual relocation in/out. Read the existing success branches only. Do not infer events from changes to global Stats.births or next_lineage; these count the whole world and include lineages that die. Do not call a local birth a dispersal arrival or count a same-cell parent debit as carbon export. Mortality attribution requires separate actual core receipts; existing failed_patches counts patches, and tracked propagule losses are deliberately incomplete. Defer universal “deaths” counters.

## Why not new resting physiology now
Prior null quiescence showed no honest survival benefit with equal mortality and paid conversion. Common maintenance assays require uncalibrated added active energy costs; equal-stock long cycles did not yield durable slow dominance. The corrected restricted accounting experiment is not the general core: it excludes offspring, support, grazing, motility and saves. The routing assay's larger funded offspring changed demographics but did not consistently improve reproductive establishment. None justifies a promised seed bank, fire armor or evolved winner. Existing paid support/light and shallow-habitat competition already produce genuine measurable differences, so making those outcomes legible is the nearer playable improvement.

## Required acceptance, without expensive exploratory runs
1. Extend pure observer tests with finite nonnegative flux validation, exact independent f64 sums, empty/no-step cases, interval deadline, overflow, owner mismatch and cancellation. Invalid data stops the observer, never changes world state.
2. Extend existing native patch-watch preparer using the preserved real 30-day save. For both naturally coexisting feeding patch and singleton/nonfeeding patch compare actual step receipts to an independent oracle, including fixed/recycled (zero is a valid observed result).
3. Observer-on/off arms start from the SAME immutable serialized baseline, run the same actual coupled ticks, and must end byte-identical, including RNG, resources and stats. Save schema unchanged. Add a known controlled empty-target arrival and relocation case solely to prove end-of-tick snapshot ordering; mark controlled fixtures as test arrangements, not evolved gameplay evidence.
4. Verify stopped snapshot stays frozen after more simulation. Start, cancel, replace world, stale expected selection, repeated watch and stale JS timer callbacks must not leak data from a newer world/watch.
5. JS tests for zero, positive fixation/no grazing, falling biomass despite fixation, large IDs, missing/invalid fields, and old callback cancellation. Do not use a growth arrow for biomass that decreased.
6. Mobile-width visual fixture at 390 px with maximum-length numbers and all optional lines. Ensure HUD does not cover primary controls; keep Stop immediately accessible. Native engine evidence is not real Android touch verification.
7. No allocations or whole-world scans introduced by observer. At most four-cohort snapshots once per admitted tick while active; disabled path remains a boolean guard. No benchmark claim is needed for this bounded telemetry change.

## Existing evidence used, not rerun
- `patch-watch/README.md`: exact natural positive grazing receipt 0.0014814876212767558 kg C/m² over 24 simulated hours; natural singleton correctly zero; observer-on/off serialized parity; native cancellation and JS fixture coverage.
- `routing-establishment/README.md`: 18 actual-scheduler runs; larger offspring not consistently better; late daughter losses remain severe.
- `energy-accounted-cycles/README.md`: restricted compensated fixed-cohort accounting, not a production inherited strategy; long-cycle limits retained.
- `quiescence/ENERGY-BUDGET-DECISION.md`: active/rest common-budget requirements and unresolved general-model integration.

Implementation ownership can be split narrowly: observer/native seam and harness versus shell formatting/controller tests. Parent should assign exact files before edits because performance work also touches Planet/main. Existing watch's successful cancellation and purity contract should be preserved, not replaced.

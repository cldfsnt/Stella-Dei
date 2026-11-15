# Fixed full-scheduler toughness mosaic: real cost and relative grazing protection

All four prescribed arms completed seven days (420×1440s) on the same actual warm day14 Sandbox world. Production unchanged. Toughness laws remain the frozen local candidate; no mutations, rate search, refill, new animals or extension. Two controls deliberately remove all 82 rabbits initially. This is an artificial causal ablation, not a resource-conserved player operation.

| Arm | Rabbits | Tender cover | Defended cover | Final rabbits | Births/deaths |
|---|---|---:|---:|---:|---:|
| A | original | 1.62256 | 1.48123 | 133 | 51/0 |
| B | original, reciprocal traits | 3.23283 | 1.17437 | 131 | 49/0 |
| C | removed, A traits | 46.92858 | 11.70689 | 0 | 0/0 |
| D | removed, B traits | 48.80910 | 11.29469 | 0 | 0/0 |

Initial cover was approximately30.85 per trait in all arms, 59 tender/58 defended patches. All117 positive patches were used, including unfavorable ones, with fixed cover-ranked reciprocal assignment. Exact distributions are retained in results.json.gz (lossless gzip). Defense is costly in both ungrazed controls and has consistent relative grazing protection in the matched comparisons below, but does not demonstrate absolute competitive dominance. Both grazed worlds lose most initial cover while rabbits continue increasing. No long-term persistence/coexistence conclusion, and no guarantee of future rabbit survival. The previously disclosed uniform d=.5 maintenance shortfall remains, not repaired by tuning.

## Actual inherited spatial events, not invented genealogies
Within the seven-day horizon A/B record24/25 actual offspring-placement events. Five/three defended placements use the existing 'vacant' branch, whose criterion is cover<1e-4, NOT necessarily exact zero. Tender placements in that branch are13/17. Other placements still use the unchanged thermal-fitness replacement rule. Exact-zero→positive transitions total7/9; positive→zero transitions9/7. These are distinct observables and must not be conflated. Sandbox has no lineage identity; this establishes copied patch-trait inheritance and spatial turnover, not natural evolution or comprehensive family trees. Post-endpoint continuation events are explicitly excluded from the event list.

No claim that toughness wins same-optimum occupied-patch competition: the unchanged replacement rule does not directly compare toughness fitness. Growth/propagule cost, thermal environment, spatial assignment and altered rabbit dynamics interact. Reciprocal outcomes differ substantially. This is useful evidence for a costly protective trait, not a justified production balance recommendation by itself. Next playable integration should not promise defense will save an island or label rendered silhouettes as new species.

## Food and state gates
Actual cover removed A/B93.36296/94.95427, actual satiety credits14004.30139/14242.99728, below150×removed throughout. Conservative receiver undercredit remains recorded; Sandbox cover/gases are phenomenological, not an exact elemental-carbon ledger. Every tick rabbit stock+births−deaths equals population. Full per-patch daily grazing/environment records, all28 daily summaries and all115 fixed-horizon placement events are retained.

Zero-trait ten-tick complete saved-state/RNG parity with a separately compiled production copy passes after removing ONLY the new zero toughness keys. No other normalization. Typed envelope `sandbox-toughness-v1`, law1, mutation=false retains all40,962 traits, including empty cells. Actual apply rejects unsupported law, mutation, Origin, NaN, out-of-range and disguised nonzero legacy state atomically. An empty-cell .25 trait survives capture/apply before restoring the unchanged arm. Each full endpoint round-trips exactly; uninterrupted versus reloaded ten-tick continuation is exact after a different prior rendered geometry/tilt. Original legacy input is restored exactly. These native checks do not constitute production save migration approval.

First compile failed because a test tried to mutate a const slice in a deep-owned parsed save. The fixture now explicitly casts that owned allocation for invalid-input tests; first failure is preserved. No model change followed outcomes. Full endpoints remain outside Git with SHA256/paths in provenance; compressed complete logs and copied-source hashes are committed. Reproduce using egl-toughness-mosaic-prepare.py and the existing EGL native build seam. QA_MOSAIC_RUN is required for four-arm activation. This is actual coupled native simulation, not browser/FPS proof or timestep-convergence evidence.

## Matched interaction clarification (read-only post-run analysis)

A/C and B/D initial full-state payloads differ ONLY in the rabbit list. Thus each phenotype has exactly matching initial cover, spatial assignment, temperature, traits, climate resources and RNG in its grazed/no-rabbit pair. Original initial differences between phenotypes are retained in matched-interaction.json, not normalized away or rebalanced.

| Reciprocal pair | Tender grazed / ungrazed cover | Defended grazed / ungrazed cover | Relative retention ratio |
|---|---:|---:|---:|
| A/C | 3.4575% | 12.6527% | 3.6595× |
| B/D | 6.6234% | 10.3975% | 1.5698× |

Defended plants retain a greater fraction of their own ungrazed counterfactual cover in BOTH reciprocal assignments: +9.1952 and +3.7741 percentage points. Dividing both endpoints by their own matched initial cover produces the same retention ratios because initial cover cancels within each pair. The first report emphasized final absolute abundance too strongly. These results do not reject defense; they support the intended costly relative protection, alongside the independently demonstrated direct handling mechanism.

This is a whole-system interaction, not a direct per-bite effect estimate or a fixed-grazer-pressure test. Rabbits move, reproduce, deplete food and modify the spatial trajectory; tender and defended plants share those consumers, and replacement/colonization changes occupied patches. Thermal optima, starting locations, illumination and water histories are not exchangeable between phenotypes, though reciprocal assignment reduces dependence on one allocation. Removing rabbits can also change subsequent plant/gas/environment dynamics. Two reciprocal assignments of ONE starting world are not independent worlds or statistical replication. The 1.57× versus 3.66× contrast exposes spatial sensitivity. No superiority, equilibrium, from-zero evolution or guaranteed island survival follows. No rerun, parameter change, extra biological arm or production edit was made for this clarification.

Lossless full results SHA256: `d965e2526c5ef53a280bfbc340a818124d0b31f43564f28b87e428d7b65ed61f`. Raw working copy remains at site-tmp/toughness-mosaic/results.json; prior Git history also retains it.

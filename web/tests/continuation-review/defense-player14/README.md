# Actual v69 Tender/Tough journey: 14 days, two reciprocal placements

Preregistered b942184; production model unchanged. Native coupled scheduler, not browser gameplay/FPS. Real Enable/select/Plant actions at the previously validated empty shallow sites26790/26788. Each arm adds external cover.35 to each patch, then no care. Same warm day14 world and82 rabbits. Assignments swapped, not independent worlds. Both840-tick arms and true10-tick uninterrupted/restored continuation passed; original complete save/RNG restored.

| At day14 | A:26790 tender,26788 tough | B:26790 tough,26788 tender |
|---|---:|---:|
| Tender founder cover | .72529 | 0 |
| Tough founder cover | .06093 | 0 |
| World cover, from62.40095 | 5.98921 | 6.16512 |
| Living vegetated patches, from119 | 113 | 122 |
| Defended occupied patches | 2 | 0 |
| Rabbits, from82 | 192 | 191 |
| Actual new rabbit births/deaths | 110/0 | 109/0 |
| Plant placement counter increment | 64 | 61 |
| Maximum living plant generation | 8 | 7 |

Tough cover declines in both locations from day1 while Tender initially grows. In B, Tender reaches.75329 at day7 but vanishes between daily samples11–12; Tough vanishes12–13. In A both persist through14. Traits at the two founder patches remain unchanged; these are patch histories, not individual lineage IDs. Two defended patches in A do not by themselves prove a known parent/child relationship. Daily zero-crossings total37 losses/31 gains in A and26/29 in B, a lower-resolution census, not complete per-tick mortality or recolonization ledger. No extension to force rabbit bust or vegetation recovery.

## Most useful next playable improvement
The strategy is not a guaranteed winner, and the spatial sensitivity is real. Current details expose toughness but do not tell the player why a selected patch is shrinking. A narrowly scoped **actual recent patch balance** (growth/physiology change, incoming spread, and actually grazed cover), recorded only for the watched Sandbox patch, would let the player distinguish defense cost from local grazing or water stress. This is a proposal, not implemented here. It should use actual stage receipts, clear on selection/load/world changes, and never infer grazing from a net decline. World defense totals being developed separately help locate survivors but do not explain a founder's loss.

No evidence here warrants changing growth/feeding coefficients. The daily snapshots lack per-patch grazing receipts, so the later disappearance is not labeled definitively as grazing. Temperatures stay near292.61/293.30K; complete water, traits and climate snapshots are retained for further attribution. Cover is the existing abstract Sandbox model, not a newly proven elemental conservation ledger. Existing mutation law remains enabled; no favorable mutations were prescribed beyond the two explicit founder traits.

## Reproduction
`egl-defense-player14-prepare.py` creates the isolated current-production copy; `defense-player14-qa.txt` fixes actions/horizon/assertions. `analyze-defense-player14.py` recreates summary. Compressed logs, source hashes and complete daily-summary retained here. Full30 daily snapshots and binary stay in `site-tmp/defense-player14`, each hashed in provenance; no huge plaintext snapshots committed. Both arms' day0 resource fields are unchanged by planting except the explicit founder cover/trait and opt-in config/actions already verified by final native release gate6b18d0b.

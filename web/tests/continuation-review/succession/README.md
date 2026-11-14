# Controlled multigeneration succession probe

## Conclusion first

**The requested stable-habitat succession is NOT demonstrated.** In three 180-day runs, inherited variation, competition, funded births and patch recolonization occur, but stable habitats do not consistently shift toward stronger/slower competitors. Maximum observed generation reaches 9 by day 30 and remains 9 through day 180 despite thousands of later funded births. This suggests a later-establishment bottleneck; it does not identify its cause.

A distinct, useful positive result is **shock selection among existing inherited variants**: a three-day shallow-water episode leaves survivors with greater biomass-weighted structure and organization. A no-reproduction-during-shock control confirms this is not solely new mutations during the shock. It is not fire resistance, dry-land establishment, or complete gameplay succession.

## Method

Production `simulation/microbes.zig` functions `seed`, `step`, and `reproduce` are imported directly by `src/qa_succession_probe.zig`. No production code is modified. Sixteen equal-area cells form a ring. One ordinary simple founder is seeded into cell 0; no designer toughness/organization traits are assigned. Each cell begins with finite carbon-equivalent atmospheric and oxygen pools of 10, plus nutrient 0.12. Seed mass is deducted from its atmosphere. Photosynthesis and recycling update the pools, and every step checks carbon, nutrient and cell invariants. Totals begin at 160 carbon and 1.92 nutrient; error tolerance is 0.001. Inputs use 303K, alternating half-day light/dark, normal depth 1m, and production 1,440-second timesteps.

Every six hours each pre-existing living cohort is offered one alternating ring neighbor using donor-funded `reproduce(..., true)`. Newly born cohorts cannot reproduce in the same sweep. This is a deliberately controlled dispersal scheduler, **not** the full Planet/ecology scheduler or actual-world climate. Reproduction uses 0.01 daughters, not 0.004 exploratory propagules. Fixed depth is an imposed experimental environment, not a water-conservation simulation.

Seeds: 42, 1337, 2027. Treatments:
- 0: stable wet habitat, mutation enabled.
- 1: same, but day 60 clears every third patch; living carbon becomes detritus and bound nutrients are released. No carbon is destroyed or free organisms added.
- 2: day 60 through day 63 depth is 8cm, then 1m resumes; mutation remains enabled.
- 3: stable habitat with mutation disabled (otherwise same scheduler).
- 4: same shallow-water shock, but reproduction is suspended only during the three shock days; existing variants alone face selection.

A reversed cell-iteration control for seed 42 stable habitat gives identical logged outcomes. This is one order control, not proof against all scheduling or cohort-slot biases.

## Results

All 16 controlled runs complete with invariants passing. In stable mutation-enabled runs, day-180 weighted structure is 0.01727 / 0.11627 / 0.05260 versus day-30 0.01941 / 0.10699 / 0.05543: no consistent toughening trend. Organization also does not show consistent late increase. Feeding evolves alongside these traits, so attributing success solely to physical structure would be unjustified.

Shallow-water shock with reproduction enabled changes weighted structure between day 60 and 63:
- Seed 42: 0.01889 to 0.08804; biomass 13.084 to 0.229.
- Seed 1337: 0.10968 to 0.20059; biomass 12.412 to 0.396.
- Seed 2027: 0.05419 to 0.11073; biomass 13.738 to 0.975.

With reproduction disabled during the shock, structure still rises to 0.08383 / 0.19905 / 0.10717. Occupied patches fall to 4 / 9 / 9. After reproduction and deep water resume, all regain 16 occupied patches by day 100. This supports differential persistence and recovery of pre-existing inherited variants, not new adaptation appearing by decree.

Patch-clearing treatments recover to 16 occupied patches by day 100 and permit another observed generation, but no consistent fast-pioneer advantage is established. This is recolonization, not the full requested reset-and-succession pattern.

No-mutation controls reach all 64 cohort slots with only 63 births, then remain locked. At day 180, 44,136 of 44,342 offers target full cells. Mutation-enabled runs have many successful births but maximum generation often stalls and feeding is substantial. Cohort capacity, offspring establishment and grazing need separate causal controls before changing ecology.

## Next experiment

Trace every daughter from birth through first growth, death or next reproduction, preserving parent traits, destination occupancy, grazing losses and stress. Compare ordinary production `propagate` scheduling with this ring scheduler. Run cohort-slot/permutation and feeding controls without removing resource costs. Only then decide whether stable succession is blocked by cohort-slot rules, small-propagule losses, grazing, or actual trait economics. No claimed winner should be hardcoded.

## Reproduction command and verification limits

With Zig 0.13.0, from repository root:

```
zig test src/qa_succession_probe.zig --test-filter 'paid multigeneration succession'
```

`results.log` records all snapshots and the passing test. `SHA256SUMS` identifies source and probe. This is an actual-core headless experiment, not rendered mobile gameplay, full-world evolution, natural species proof or a deployed feature.

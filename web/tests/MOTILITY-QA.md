# Motility candidate QA (v14 preserved)

Inherited mobility0–1 enables whole resident-cohort relocation to an adjacent
suitable wet patch with more actual competing prey and an empty cohortslot.
Source must also be habitable. No unrestricted search, overwriting or partial
clones. Migration preserves lineage/intake history, pays oxygen-limited carbon
respiration and returns bound nutrient at source. Higher maintenance and lower
photosynthesis impose ongoing cost. It is coarse-patch population movement,
not individual animal motion or a taxonomic unlock.

Cohort event fields: relocations,last_from,last_to,last_move_time in simulated
seconds, meaningful only after a real move. Reset on daughter birth. Same-tick
repeat movement blocked. Planet uses six stack neighbor records, not a world
scratch array. Stats track total relocation count and respired movementcarbon.
V5schema/mobile sparse serialization handled separately; old saves defaultnew
fields0, with explicit changed future dynamics.

Mechanism controls:32matched replicates of genuinely inherited motile grazers
have21survivors vs0immobile after30darkdays finding adjacent real prey.21moves,
no duplicate lineage. Following explicit4day daylight recovery,21survivors fund
inherited gen2offspring. Weak variants need not reproduce during darkness; no
respawn or forced success. Adjacency, unsuitablehabitat, oxygen and full-slot
refusal, conservation, benignphotosynthetic cost and event reset pass.

Actual Planet controlled100day integration: sixoccupiedpatches,385births/gen4,
carbonrelativeerror9.38e-7,nutrienterror4.47e-7. Updated ledger and same-tick tests passed. Actual generated-world rendered relocation, ordinary fullclimate and
v5save compatibility acceptance still pending; do not call allgamefunctions done.

Candidate /tmp/stella-recovery-20261113/Stella-Dei-motility shares immutableassets
anddeps by hardlinks to save disk. Sourcefiles copied independently. No edits to
hardlinked assets/deps. Prototype checkpoint remains in v14candidate prototypes.

Updated actualPlanet rerun passes with7naturalrelocations and20,023,991kgC
movement respiration. Every living movedcohort has correctdestination metadata,
unique lineage residency and no duplicate ghosts. Per-cohort move histories do
not exceed globalmove count. Same-tick repeat-hop test and newborn-history reset
are covered. Source frozen pending independentrender/save/ordinaryworld checks.

Fresh candidate Sandbox regression passes unchanged: 37 simulated days, 35 living
rabbits, 39 births, 1,106 meals, six deaths and plant biomass 5.297848.
See `evidence/motility/sandbox-regression.log`.

## Ordinary generated-world gate

Production Habitat → Seed on seed 1337, topology 6, then 20 days at the exposed
24 h/s setting (1,440 simulated seconds per update). No temperature, water,
light, nutrient, organism or event assignments in the harness.

- Biomass grew from 0.02 to 0.186327; three births, generation 1, four unique
  living lineages. One cohort actually grazed; planet intake 200,452,116 kg C.
- Two cohorts inherited mobility, but **no relocation occurred** in the isolated
  starter patch. Capability is not a promise of movement or an animal unlock.
- Full-world water + vapor relative drift: 1.007e-5. This is bounded numerical
  drift, not an exact full-climate conservation claim.
- Save v5: 12,246,222 bytes; malformed-state rejection left live state unchanged,
  and valid restore reproduced the exact captured JSON. Native peak RSS was
  227,060 KiB. The old shutdown allocator-leak warning remains.
- Native update mean 40.28 ms, maximum 1,051 ms on the shared test host. This is
  not a physical Android/browser performance measurement or a smooth-60-fps claim.
- Screenshots `ordinary-seeded.png` and `ordinary-day20.png` show the real mat;
  amber denotes recorded feeding, not motion. No new movement visual was faked.

The legacy `HOURLY hour=N` diagnostic label counts blocks of 60 updates; for
this fast run each block is one simulated day. The explicit `time` fields and
Day 20 screenshot establish the actual duration. Independent controlled
relocation/feeding screenshots and save migration acceptance are separate gates.

Default-speed check also passes: 7,200 updates of 60 simulated seconds, five
full-climate days. Biomass 0.02 → 0.0353616, one daughter, two unique living
lineages, no feeding or mobility variants yet and correctly zero feeding/movement
counters. Exact v5 save/restore and corrupt rejection pass (12,121,446 bytes).
Native peak RSS 226,672 KiB; update mean 37.77 ms, max 927.88 ms. Full-world
water/vapor relative drift 3.984e-5. Neither the existence nor timing of a new
capability is guaranteed. See `ordinary5days-default-speed.log`.

# Producer persistence contract (v6 candidate)

New writes use save version6 and Origin model revision5. All prior formats1–5
remain readable. Existing organism, lineage, climate, nutrient, carbon, PRNG,
feeding and movement values are restored without conversion. Old cohorts have
organization0 and support_mass0. Future simulation uses the new model; this is
not a promise of historical trajectory identity after advancing an old save.

`organization` must be finite in[0,0.7]. `support_mass` must be finite in
[0,biomass], a subset of existing biomass, never additional carbon. Validation
rejects invalid inputs rather than clamping or manufacturing support tissue.
Earlier format versions cannot claim nonzero new fields. No new Stats fields.

Sparse capture retains every noncanonical cohort using fieldwise bit equality
for floats. Thus negative zero and inactive history in new fields are retained,
not omitted by a biomass-only shortcut. Existing unique-slot/index validation
and full dense worst-case support remain unchanged.

`save_game.apply` still validates the entire save before any live data mutation;
allocation and topology preconditions precede commit. These two new scalars use
the existing exact cohort assignment, not a new mutation path.

Unit tests include actual v5-shaped wire with absent new fields; v6 sparse
roundtrip preserving feeding/motion/lineage/RNG; invalid, nonfinite and excessive
support; old-version contradictions; and signedzero preservation. Actual full
world migration and invalid-load/live-unchanged evidence is a separate gate,
not inferred from these DTO unit tests. Results will be recorded after execution.

Execution: schema suite29/29 passed against integrated fields (Zig0.13). Full-world gates remain separate.

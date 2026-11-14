# Producer persistence contract (v6)

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

## Verified acceptance

The final Zig 0.13 schema/model suite passes **34/34 tests**. Coverage includes
v5-shaped wire with absent new fields; v6 sparse roundtrip preserving feeding,
motion, lineage and RNG; invalid, nonfinite and excessive support; old-version
contradictions; and signed-zero preservation.

Actual engine tests independently restored a genuine historical v5 world through
production `replaceWorld`: all 40,962 cells, old cohort values, resources, RNG and
stats remained exact. Six feeding histories and one living movement history were
preserved; organization and support defaulted to zero. Invalid support greater
than biomass was rejected without changing the live world. The migrated v6
world roundtripped exactly.

A separate living v6 world contained four cohorts with nonzero support. After
explicitly clearing their support, loading restored the entire serialized world
exactly. This tests restoration of real support, not only zero defaults.

See [Producer actual-engine acceptance](PRODUCER-ENGINE-QA.md) for scenarios,
reproduction and limitations. These native results do not establish browser
storage durability or physical Android performance for this release.

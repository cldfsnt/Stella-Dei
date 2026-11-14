# Reserve save schema v7

Schema-only work in the isolated shore lab; not deployed.

- Version 7 captures inherited water retention and physiological water reserve through the generic cohort representation.
- Legacy versions 1–6 default absent fields to zero; legacy payloads carrying nonzero v7 fields are rejected rather than reinterpreted.
- Reserves must be finite, nonnegative and no larger than the model's actual `waterCapacity` plus 1e-5 kg/m² for proportional f32 transfer roundoff, matching runtime validity. Retention must be finite in [0,1]. A boundary test accepts +5e-6 and rejects +2e-5. This is numerical tolerance, not extra gameplay storage.
- Sparse slot indices, signed zero, lineage/history, carbon/nutrient fields, PRNG, environmental surface/vapor water and stats remain exact through roundtrip.
- Validation never repairs or mutates input. Existing `save_game.apply` validates before changing the live world; no integration code change was needed.

Two new tests cover a literal v6 producer wire migrated with zero water fields, and v7 exact sparse roundtrip plus invalid values/capacity/legacy-version rejection.

Final aggregate against real reserve implementation: **50/50 passed**, including all 15 schema tests and four new model water-ledger tests. Earlier depth-zero assertion failures were corrected by the model owner to distinguish external water from usable stored reserve. Native full-world v7 checks subsequently passed invalid-save rejection, unchanged state after rejection, and exact restoration in every completed100-day enabled/disabled comparison (single-founder and expanded-seeding, worlds1337 and1338). These are separate executed native checks, not inferred from unit tests. Independent numerical water-bridge review remains open; exact save restoration does not establish coupled water conservation.

The existing native migration fixture now asserts the current schema.VERSION instead of hardcoding version 6. Its v5 legacy-input validation remains unchanged.

## f64 reserves and precision carries (still unreleased version 7)

`Cohort.water_reserve` now roundtrips as f64. Both nonnegative cell precision remainders (`surface_water_carry`, `vapor_water_carry`, kg/m²) are preserved in dense capture, sparse capture, custom JSON and runtime reconstruction, including cells with no active cohorts. Legacy versions ≤6 default absent carries to zero and reject nonzero carries.

Each carry is validated against the corresponding saved f32 bulk water/vapor value using `water_precision.validCarry`. The area calculation deliberately matches `Planet.getMeanPointArea`, including rounding the calculated area to f32 before promoting to f64. This avoids disagreement at quantum boundaries. Carry must be finite, nonnegative and strictly below one next-f32 bulk quantum.

Tests preserve sub-quantum values exactly for zero and subnormal bulk water, ordinary vapor, and signed zero. Negative, infinite, NaN, equal-to-quantum, greater-than-quantum and incompatible legacy carries are rejected without changing the input.

Latest full schema/model/helper aggregate: **54/54 passed**. This supersedes the earlier 50-test result. Native weather/carry integration and full-world atomic save/load acceptance are separate parent-owned checks.

# Reserve save schema v7

Schema-only work in the isolated shore lab; not deployed.

- Version 7 captures inherited water retention and physiological water reserve through the generic cohort representation.
- Legacy versions 1–6 default absent fields to zero; legacy payloads carrying nonzero v7 fields are rejected rather than reinterpreted.
- Reserves must be finite, nonnegative and no larger than the model's actual `waterCapacity` plus 1e-5 kg/m² for proportional f32 transfer roundoff, matching runtime validity. Retention must be finite in [0,1]. A boundary test accepts +5e-6 and rejects +2e-5. This is numerical tolerance, not extra gameplay storage.
- Sparse slot indices, signed zero, lineage/history, carbon/nutrient fields, PRNG, environmental surface/vapor water and stats remain exact through roundtrip.
- Validation never repairs or mutates input. Existing `save_game.apply` validates before changing the live world; no integration code change was needed.

Two new tests cover a literal v6 producer wire migrated with zero water fields, and v7 exact sparse roundtrip plus invalid values/capacity/legacy-version rejection.

Final aggregate against real reserve implementation: **50/50 passed**, including all 15 schema tests and four new model water-ledger tests. Earlier depth-zero assertion failures were corrected by the model owner to distinguish external water from usable stored reserve. Native atomic save/load acceptance remains a separate full-world harness check; it is not claimed by the unit aggregate.

The existing native migration fixture now asserts the current schema.VERSION instead of hardcoding version 6. Its v5 legacy-input validation remains unchanged.

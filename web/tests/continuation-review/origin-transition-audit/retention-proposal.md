# Proposed minimal paid hydration transition (not implemented)

## Mechanism under review

Use one inherited retention-allocation scalar r in[0,1], default0. Actual retention carbon = existing paid support_mass*r; aboveground support = support_mass*(1−r). Total biomass and fronds do not increase, and all support retains existing respiration cost. Only aboveground support contributes the existing height/light-interception architecture. This makes water buffering compete with support's existing useful function, rather than a free protective bonus.

A finite retained-water reservoir, measured kg H2O/m², has capacity proportional to real retention tissue. A fixed candidate water:C capacity and evaporative-rate law must be preregistered before outcomes; neither is currently calibrated or approved. Hydration can permit temporary carbon acquisition/reduce desiccation stress on a dry surface, but cannot exceed the existing fully hydrated potential. Water loss progresses under drought; stored water never creates water, guarantees survival or resurrects dead tissue. Heat/freezing/deep-water restrictions remain. This is an aquatic-to-exposed-moist-surface hypothesis, NOT automatically vascular plants, roots or animals.

## Representation must be explicit

Planet liquid/vapor are f32 in10^9kg perpatch; organism stores are kg H2O/m². Convert via actual getMeanPointArea. Credit uptake from actual old−new represented liquid, never nominal requested subtraction; zero representable removal means zero credited body water. Receiver-limited transfers must not overdraw donors.

Tiny return/evaporation cannot simply be added to a huge f32 vapor pool and rounded away, or skipped in a way that makes organisms retain water forever. Proposed explicit f64 cell water-return escrow is a genuine nonliving, nonhydrating reservoir. Evaporation leaves organism water and enters escrow immediately; only representable funded transfers leave escrow for liquid/vapor. All water totals include escrow. Its direction/phase and physical availability must be specified; do not silently reuse it as hydration supply. This is a domain-state addition requiring approval, not a hidden numerical top-up. If this cannot be made sound within scope, stop rather than relaxing conservation or granting water.

## All lifecycle paths need closure

- Reproduction/propagation split finite body water with paid tissue; `child=parent.*` must NOT duplicate the reservoir. New allocation mutation may reduce capacity; overflow returns to explicit nonliving reservoir.
- Grazing, support maintenance, tissue mortality and final colony loss release corresponding retained water; no vanished water when a cohort is cleared.
- Existing whole-frond autonomous relocation leaves paid support behind: retention-bound water should stay/release at source, not teleport as if unsupported fronds carried roots. Whole-colony manual transport can move the bounded retained-water state, with full snapshot accounting.
- No intake from empty/dry/nonfinite sources, no capacity from zero support or zero allocation; no magical wetting from epsilon.

## Serializer/backward compatibility

Current saves use version6/model_revision5 and serialize Microbes.Cohort. A production candidate would require a new model/schema revision: old saves load allocation0, retained_water0, escrow0; future unknown versions rejected. Before emitting new saves, preserve old exact backup and verify explicit upgrade/roundtrip. Validate finiteness/nonnegativity, allocation bounds, capacity consistency and canonical empty cohort state. Sparse saves should not serialize artificial water on empty cohorts. Existing saved positions/IDs/parents/time/RNG remain intact; adding a mutation draw later intentionally changes future stochastic trajectories and must be disclosed, not advertised as bit-identical future history.

Dense in-memory storage matters: f64 body-water plus f32 allocation can add roughly16 bytes/cohort after alignment, about2.6MB on40,962×4slots; cell escrow adds~.33MB. Exact struct size and163,842-cell old-save memory must be measured before production. Sidecar experimental state avoids changing production now but does not eliminate this release decision.

## Exact bounded test plan before any production integration

1. **Material primitives:** zero/tiny/large f32 source reservoirs, negative/nonfinite refusal, receiver-rounding limits, repeated acquisition/evaporation/release, support shrinkage, death, both reproduction sizes, mutation-cap overflow, grazing and movement. Require atomic refusal and conserved explicit total water; retain v53's bounded C/N checks without claiming arbitrary-duration exactness. Zero r must reproduce original physiology, no water activity and no new RNG draws.
2. **One allocation, not a sweep:** proposed r0 versus r.25 on copies of the same actual natural supported phenotype ID478, retaining its real biomass/support/other traits. The new r assignment is explicitly an experimental hypothesis, not a naturally evolved trait or success story. A zero-support phenotype is a negative control.
3. **Four7-day exposure sequences:** continuously wet;1day wet then6dry;1wet/3dry/3rewet; all dry from empty internal stores. Same declared total available-water inventory; water removed from exposure is held in a separately accounted inaccessible control reservoir and rewetting returns that same water, not a refill. No free biomass/traits changed after start. Use actual core C/N/O2 physiology where possible, all8 outcomes retained. Rehydration can reverse stress before death, never resurrect extinct cohorts. No guaranteed persistence/crossover.
4. **Numerical/control gate:** 1hour and30minute timesteps on the same frozen8conditions, exact water ledger within a preregistered representational bound; directed receipt tests also execute under actual WASM target. No tolerance/rate tuning after failure.
5. Only if useful tradeoff and full accounting pass, design one actual coupled-world test with inherited mutation/paid tissues and correct save continuation. No production, automatic land unlock, new morphology label or rabbit conversion from the standalone assay.

A parent decision is needed on water-return escrow semantics, fixed capacity/evaporation hypothesis, and scope before code. This proposal is deliberately smaller than a soil ecosystem but still changes material representation; it is not a quick cosmetic patch.

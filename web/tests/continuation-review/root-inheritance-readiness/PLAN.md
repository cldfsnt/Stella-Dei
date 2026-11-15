# Root inheritance/progression readiness: source audit only

No new biology, mutation frequency, rate, schema or production code implemented. Physical-water integration remains a prerequisite. Current laboratory cohorts are prescribed phenotypes, not naturally accessible evolutionary variants. References: experimental/soil_physiology_core.zig, experimental/retention_mutation.zig, experimental/hydration_mutation_core.zig and production simulation/planet.zig. Source hashes recorded.

## What already exists and what does not

- `soil_physiology_core.reproduceSized` starts `child=parent.*`: root_fraction and retention allocation are inherited already. Child support is donor-funded proportionally; biomass/credit thresholds are checked before mutation, empty slot found before mutation, and failed full/capacity/insufficient-resource birth returns without consuming draws.
- Actual amount/thresholds remain: ordinary child.01, parent>=.03, credit>=.04; exploratory propagule.004, parent>=.02, credit>=.01. These values are existing code, not chosen by this audit. No reason to loosen them to produce roots.
- Six existing global mutation draws change optimum/efficiency/structure/feeding/mobility/organization and the established rare-tail law. **They never change root_fraction.** Beginning from canonical zero roots, this copied core cannot create a positive-root genotype by waiting. Its root-bearing laboratory outcomes therefore cannot be called natural evolution.
- The separate experimental retention mutation wrapper changes storage only. It is NOT wired into this soil physiology copy and its `[0,1]` clamp alone is insufficient when nonzero roots share the same paid support.
- Root fractions change allocations of existing support, not free root tissue. Positive genotype with zero support has zero paid roots/uptake. Preserving this developmental constraint is essential: genotype discovery, tissue growth, paid-water use, survival, birth and persistent establishment are separate milestones.

## Dry-gate audit: avoid blanket eligibility bypass

The core's early post-mortality `if !habitable continue` occurs at the end of that cohort loop; it does not globally skip the later growth loop. Later growth uses `max(photosyntheticHabitat, effectiveHydration)`, so a genuinely paid dry survivor can grow and earn reproduction credit. `reproduceSized` itself has no environment argument and no blanket wet check.

Production Planet's first exploratory propagation chooses any adjacent finite depth/temperature; it deliberately does NOT require aquatic habitat. After credit threshold, same-cell ordinary reproduction is tried without an aquatic check. Only the fallback ordinary reproduction into neighbors filters through aquatic `habitable`. Thus paid dry growth could, in a correctly integrated candidate, reproduce locally and send exploratory offspring without relaxing every aquatic gate. Existing autonomous relocation and grazing remain aquatic-gated; do not advertise dry grazing/animal mobility or modify those unrelated laws simply to make roots establish.

Required first lifecycle test after physical model passes: actual copied scheduler pays dry demand from finite owned water/soil, earns credit by real growth, then makes a donor-funded child with inherited roots. No injected credit, reserve, forced survival or manual clearing of full slots. Separately use controlled funded fixtures to prove failed/successful branch semantics. A valid zero-birth outcome is retained, not fixed by increasing resources or changing thresholds after the run.

## Minimal future mutation/config change

1. First prove mutate=false funded inheritance and lifecycle closure with positive prescribed roots; no mutation needed for this gate.
2. Add an explicit experimental root/allocation mutation law, disabled by default and persisted with its domain seed/version. Unknown/disguised configs reject atomically; legacy and Sandbox reset. Do not conflate it with water receipt policy, abiotic law or save format merely because all are new.
3. Use a separately domain-tagged deterministic lineage-keyed proposal stream (world/config seed,parentID,actual childID,generation), following the audited retention mechanism pattern, NOT a seventh draw from the established global genome RNG and NOT accidental reuse of correlated retention bits. Call only for a successful mutating birth after funding/slot checks. No fitness/environment/desired outcome inputs.
4. Preregister a small bounded signed step/probability before outcome trials; no numeric choice made here. At zero, negative proposals can be clipped/rejected while positive proposals must have nonzero probability. Record proposed, expressed and boundary-clipped counts separately. Do not wait for a chosen favorable child then claim unbiased accessibility.
5. Keep legacy mutate=false/failed/disabled outcomes and all six old draw advancement exactly unchanged. New enabled-law trajectories are intentionally different, not a backward-parity failure to hide.

## Shared support allocation is a coupled constraint

`validRoot` currently requires finite root_fraction>=0 and exact f64(root)+retention<=1. `abovegroundSupport` computes the remaining fraction in f32. A future mutation must validate the complete child BEFORE committing donor/resource changes, not create an invalid pair and rely on the next step to reject it.

Do not independently clamp both to[0,1]: root.75+retention.5 is invalid. Do not calculate `1-other` in f32 then assume its rounded upper endpoint satisfies the exact f64 sum. Validate represented fractions explicitly and bound canopy/root/storage paid tissue so rounding does not overallocate support.

A small coordinated allocation law is preferable to silently prioritizing storage then squeezing roots (or vice versa). For example, propose one selected allocation coordinate per mutation while holding the other fixed, then reject or conservatively bound invalid proposals against the remaining budget; this is a design option, not a chosen law. A joint vector proposal can instead reject the entire invalid proposal. Both produce boundary effects that need statistical tests. Sequential projection gives trait-order bias and must not be hidden. Existing retention-only law must keep its exact behavior when the new combined law is disabled; any enabled change needs an explicit new model version.

Changing fractions reallocates paid support; it does not buy new carbon. If storage capacity decreases, only actually transferred parental water is retained up to capacity and real excess must reach the declared physical destination. Current settleWater routes to experimental liquid_return; that old escrow is NOT approval to reintroduce a protected reservoir into the new soil model. Reproduction water fate must be aligned with the final physical authority before coupled testing. Roots do not transfer a patch's soil to a child. Manual whole-colony transfer carries owned stores only; soil remains at its patch. Support-shedding motility cannot carry nonexistent rooted tissue.

## Required tests before claims of progression

- Exact no-mutation inheritance, genuine parent/child IDs and generation, support/biomass/credit debit, water donation bounded by donor and capacity, no parent-capacity refill; same-cell and adjacent child, exhausted/full target, aliasing and failed birth atomicity.
- Root/storage corners0/1 and adjacent representable values, NaN/Inf/negative invalid states; sum validation before commit; capacity-shrink excess and dead/zero-support cohorts. No inequality-only test that overlooks actual receiver rounding.
- Fixed-seed large proposal counts: root0→positive accessibility, negative/interior directions, every selected coordinate, boundary expression/rejection, deterministic save/restart, identity vs slot dependence, no environment dependence. Legacy RNG count and unrelated old trait parity under disabled law.
- Actual successful births from root0 under predeclared seeds/time horizon without manual trait injection; count all attempts, expressed variants, actual paid root support, actual root-water receipts, lifetime, descendants and habitat. Do not call positive root genotype a land plant, successful adaptation or establishment by itself.
- Paid dry versus wet controlled populations only after water bridge/cold/evaporation/energy contracts pass. Preserve all zero-benefit, extinct and underwater-only outcomes. Current wet competition and separate dry/recharge laboratory results do not substitute for this inherited-lineage experiment.
- Full schema/capture/sparse roundtrip, true uninterrupted/restored continuation, reset/cancel, fixed save limits and actual native/WASM overhead. Mutation cost per actual successful birth is different from per-cell per-frame work; no broad hashing in every update.

Smallest honest progression claim after these gates: “A zero-root lineage produced a recorded positive-root child under the explicit enabled mutation law; that child's paid tissue and water transactions were traced.” Stronger claims need observed survival, funded descendants and replicated environmental comparisons. No guarantee that the trait will win or that a player will see it quickly.

# Independent retention mutation design review

Reviewed preregistration b6eb467 and current isolated draft. No production enablement or coefficient edits by reviewer. Statistical tests are owned by grazing_traits; this memo is not their result.

## Design boundaries

Domain-separated SHA256 uses a44-byte unambiguous fixed-width tuple:13-byte ASCII STELLA-RET-V1 padded with three zeros to16bytes, then seed/parent/child as little-endian u64 and generation as little-endian u32. Distinct valid tuples are unambiguous; duplicate tuples intentionally repeat proposals. Hash output is deterministic pseudorandomness, not proof of independence. Global child IDs are birth-order dependent: altering earlier history can alter later keys even for otherwise similar organisms. Identical world seed and lineage tuple across replayed worlds intentionally produces the same proposal. This is reproducibility, not a collision bug.

The1/64 event and ±1/32 proposal are symmetric in the interior, but realized change is not unbiased at bounds: zero has a modeled1/128 chance of becoming1/32 and otherwise remainszero. There is no favorable reroll. The distribution is an explicit game hypothesis, not calibrated biology. Statistical tolerances are plausibility gates only; do not retune the seed set or rate after observing survival.

The allocation reallocates existing paid support. Higher allocation sacrifices aboveground functions; increased capacity must remain empty until actual uptake. A zero-allocation parent's new positive mutant inherits no free water. Lower-capacity offspring must return inherited excess through the existing destination escrow settlement. No new carbon, support, resource-maintenance discounts or immunity is justified. Supportless offspring can carry a latent allocation trait without receiving usable capacity; water benefit still requires real support and water.

## Actual code issue caught before outcomes

The initial reproduceWithRetention draft accidentally used daughter amount.02/min_parent.05 instead of existing.01/.03 (credit.04). This would confound mutation with demographic policy. Owner corrected to.01/.03/.04 before the first test execution; original wrappers now pass null context and preserve their old amounts. The reviewer initially questioned the domain literal length, then independently checked and withdrew that concern:13bytes is correct. No hash-copy defect is claimed.

## Computational and save implications

The44-byte message plus SHA256 padding fits one64-byte compression block. Cost is incurred for EVERY successful mutate-enabled birth to decide whether it changes, not only1/64 mutation events. Failed eligibility/capacity checks and explicit nonmutating/disabled wrappers must not hash or consume legacy RNG. The isolated diff leaves the six old mutation draws in place and adds the hash after them. This protects the old random stream, not necessarily subsequent whole-world equality once altered phenotypes affect birth history.

No extra saved RNG cursor is needed, but enabling this law changes future trajectories. Saved seed, parent/child IDs and generation must remain exact integers. Model revision must explicitly distinguish enabled mutation from frozen-allocation experimentalv7/model6; existing saves must not silently adopt a different future law under the same revision. Native and WASM must agree on tuple bytes/digest; actual browser/WASM performance remains unmeasured. Do not describe one-block work as zero overhead without an actual birth-heavy test.

Independent Python hashlib vector: seed42,parent17,child123456,generation2 => SHA256 `22de0612c574954403e2b358218acc48a6d4e34ee6d3c6831faac4b81c93456c`. Sent to owner for a cross-implementation endian/domain check, beyond repeating the same implementation.

Recommended acceptance retains preregistered counts/sign/boundary tests, exact failed/disabled oldfields+RNG parity, successful old-field comparison excluding only new allocation and consequential water-capacity returns, parent allocation unchanged, actual funded same/cross-cell births, and explicit zero-start mutants with no prefilling. Mutation statistics do not establish selection, persistent land establishment or player-visible benefit. No new blocker remains in the corrected design beyond these pending gates.

## Independent funded-birth acceptance

Added qa_retention_mutation_audit.zig;70 total imported/local ReleaseSafe tests pass.8,192 successful funded births cover2,048 child IDs × same/cross-cell × propagule/daughter. Every old cohort field other than the deliberately new allocation/water effects, every statistic, nutrient/detritus and donor/destination RNG matches the unchanged continuous core exactly. Parent allocation/water stays unchanged relative to control. Child water never exceeds the original inherited amount or new capacity; lower-capacity excess matches extra destination liquid return. Total water matches within1e−15. The independent Python hashlib tuple vector also matches Zig exactly. This tests actual birth functions, not only standalone proposal statistics. It is not ecological selection or an arbitrary-duration budget proof. Exact reviewed candidate diff is retained.

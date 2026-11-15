# Conservative represented transfers without whole-step freezing

Design only. Preserve exact-or-refuse kernel and its negative outcomes as reference. Owner's repeated depletion fails at step27 because source withdrawal is representable but receiver increment is not, not because available water is zero.

## Concrete step27 witness

Soil=.0005644075936237503, vapor=.9994355924063762, requested=.00014110189840593756. Receiver-first downward represented credit=.00014110189840588205. Leave2^-54 kg/m² in physical soil. New soil=.0004233056952178682. Python Fraction verifies actual source decrement EXACTLY equals actual vapor increment. No water loss, numerical reservoir, biological coefficient or source replenishment is needed for this case.

## Proposed transfer primitive contract

For one finite source/receiver and finite nonnegative maximum demand, first cap demand to real source. Compute the greatest represented receiver increment no greater than that budget (directed downward, not nearest-up). Derive its actual increment, then require a represented source decrement exactly matching it. If not compatible, conservatively reduce to a common binary grid covering source and receiver endpoints and recheck. No unbounded search. If no positive common transfer exists, return successful zero-transfer with an explicit quantization status; keep all water in physical source. Never pretend the unmet requested amount transpired or hydrated anything.

A possible bounded construction uses the maximum source-decrement and receiver-increment ULP over the proposed interval. Flooring to that common power-of-two grid and checking both actual differences is conservative, but can reject more than the mathematically largest transfer near binade boundaries. Prefer correctness and recorded lost opportunity over unsupported maximality claims. Overflow/invalid input is distinct from a valid zero transferable amount. Mixed-scale sum/difference checks must retain the existing exact-arithmetic safeguards.

## Fairness and phase isolation

Do not iterate source-sharing cohorts one at a time. Snapshot root demands and soil once. Compute proportional allocations from a common available budget, quantize each conservatively with the same receiver-grid policy, canonical-sum actual allocations and apply the resulting aggregate physical transfer. Leave all unspent allocation in soil; never give leftovers to the first slot or a favored lineage. This can yield all-zero uptake when individual shares are too small, which is an explicit limitation rather than a free remedy. Exact individual receipt sum must match actual shared physical transfer; no unattributed evaporated amount should be manufactured to close that ledger.

Storage has separate owned sources, but a shared vapor receiver: plan all actual withdrawals against one frozen receiver scale and combine canonically, rather than granting the first slot a more favorable rounding window. Root receipts cover common demand first; store receipts only cover actual unmet demand.

Separate valid physical phases: infiltration, soil evaporation, roots/storage, drainage. An unrepresentable evaporation leg must not roll back representable infiltration or freeze ecology. Explicitly fix ordering; skipped evaporation can leave more water for roots, so this is a changed numerical policy requiring its own recorded identity. Invalid whole-state inputs can still refuse atomically. Derived support-partition errors are separate from water transactions; do not claim this change fixes every prior rejection.

## Limits and acceptance gates

No representation can add arbitrarily tiny water to a huge single f64 receiver. Zero transfer remains possible. Error here is unmet requested flow, not created/destroyed material: bound/report it in absolute units, and never assert small relative error when request is subquantum. A future higher-precision physical pool would have to participate fully in evaporation, hydrology, tools and saves, not act as protected escrow; that is outside this minimal proposal.

Before a replacement kernel: exact rational step27 proof; source/receiver binade boundaries and huge ratios; repeated tiny demands; all24 slot permutations; root+storage no-double-spend; nonnegative pools/capacity; valid zero-demand; per-leg skipped status and continued biology; full final ledgers. Compare refusal/skip and realized-flow distributions on actual non-dyadic phenotypes, not only dyadic favorable fixtures. No code or production approval in this document.

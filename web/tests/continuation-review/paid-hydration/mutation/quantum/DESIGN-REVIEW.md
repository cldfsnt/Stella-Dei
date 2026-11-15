# Numerical staging proposal, read-only review only

Exact endpoint calculation retained, not a new physiology fit. Key1 ID2003 has capacity3.005005964951124e−5kg/m², source smallestf32 debit3.1832542246137236e−5. Current take(requested) correctly returns0 rather than crediting nominal water. Key42 survivors havezero paid support/capacity; fixing source quantization would not grant them water.

Existing liquid_return is serialized f64 physical water debt, nonhydrating, flushed to f32 liquid at adapter entry/exit and in escrow-only empty patches. It cannot currently fund uptake directly. Simply debiting onequantum and immediately calling currentdeposit would restore the source before uptake, recreating the limitation. Simply counting escrow ashydration would fabricate organism access and violate ownership. Any new numeric staging requires an explicit model-law revision and tests, not a silent helper change.

Possible bounded transaction: flush permissible existing returns; form simultaneous deficits; use an explicitly charged actual f64 escrow withdrawal first; if deficient and source request unrepresentable, debit exactly one representable source quantum into liquid escrow, then fund only <=deficit grants. Unused water stays nonhydrating escrow and returns when representable. Water does not confer physiology until a paid transfer places it in cohort-owned storage. No extra tissue/capacity, no trait/probability changes. Charge receiver credits from ACTUAL source/escrow removal, not nominal subtraction. No fallback forzero source orzero demand; no repeated quantum staging while escrow can cover demand.

Risks requiring isolated proof:
- Escrow now acts as explicit transfer staging, not return-only; document semantics/model version. Must not silently treat all escrow as freewater.
- Deep-ocean f32 quantum may dwarf biological deficit; up toonequantum can temporarily be withheld from hydrological flow while remaining in counted physical escrow. This changes resolved depth byoneULP, not zero. Quantify it, do not call exact old-physics parity in enabled cells.
- A huge f64 escrow can itself have an unrepresentable requesteddebit; apply realized receipt rules there too, otherwise this repeats the original bug at64bit.
- New pending escrow must satisfy existing finite/schema bounds and survive exact roundtrip, death, migration and emptycell flush. No unsafe huge transient state madeunsavable.
- Simultaneous/permutation fairness, bounded allocation, zero-tissue/zero-mode unchanged, sourcepool extremes, ledger and exact oldfield/RNG disabled parity mandatory.
- No habitat benefit claim: ALL positive lineages in fixedtrial remained deeper than20cm. Better tiny uptake alone cannot demonstrate land adaptation.

No implementation, tuning or new run performed in this proposal.

## Review decision: direct escrow uptake rejected

The direct-escrow-uptake idea above is REJECTED, not approved for implementation: making a return-only pool consumable could create water protected from evaporation/advection/tools. Revised design consideration only: pay one actual source quantum in the current call, set usable grant budget to min(actual debit, total capacity deficit), allocate bounded proportional receipts, and leave ALL excess strictly nonhydrating under the existing return-to-physical-pool path. Never consume existing liquid_return directly. No code implements either proposal.

Read-only whole-world census (uniform actual native area 7,669,529,600m²) over natural60-day60 and all six fixed endpoint snapshots finds maximum downward source quantum 2.08617748864285kg/m² = 0.00208617748864285m water depth in every snapshot (example patch40859). This is a ~2.09mm upper bound for these snapshots, NOT a universal bound and NOT the amount every uptake would retain. ID2003's local quantum is only 3.1832542246137236e-5kg/m² (~31.8nm depth). Huge finite source/small-area combinations can be much larger or overflow; future candidate must refuse invalid transactions atomically, not clip grants or invent water.

Water− can lower the physical pool enough that previously unrepresentable nonhydrating excess becomes representable and returns as liquid. Existing deposit semantics therefore do not establish exact tool semantics. Any isolated test must explicitly measure pre/post edit physical pool plus nonhydrating residue, repeated cycles, actual maximum withheld depth, and exact ledger/roundtrip. No claim of perfect physical fidelity, land adaptation, or production readiness.

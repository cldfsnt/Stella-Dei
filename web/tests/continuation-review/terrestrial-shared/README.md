# Shared finite-soil demand: actual48-minute gate

All four fixed-input native arms completed, with exact original setup and old-arm records versus bb31977. No production changes.37 focused/imported tests passed. Independent exact Fraction receipt oracle passed. The read-only allocation trace had a compile-only format-brace failure, retained; no outcome-driven model revision.

| Law | Assigned root fraction | Final biomass kgC/m² | Final soil kg/m² |
|---|---:|---:|---:|
| Old atmospheric-first |0|0.003935461398|0|
| Old atmospheric-first |.25|0.003938490991|0|
| Shared, one-day substrate access |0|0.003935461398|0.016071830532|
| Shared, one-day substrate access |.25|0.003961284645|0.016071514912|

Initial biomass0.004483437631; all remain alive but declining. Root0/new retains physical soil yet has exactly the old root0 biomass, so environmental soil alone does not provide free physiology. Root.25/new receives actual source-and-receiver-funded hydration4.677001% then4.599651% of demand; total credited root water3.18354200095e−7kg/m². Its small improvement over the SAME paid-root old-law arm is an actual hydration response, not just the old geometry difference. This does not demonstrate growth, establishment, descendants or naturally evolved roots.

The one-day substrate access law replaces unlimited soil access to a whole-column deficit. It retains~96.72% of the tiny conditioned soil over48minutes. Capacity remains1mm and actual conditioning only0.0166mm; no hidden fill. Existing paid root/carbon/light/upkeep costs remain.

## Material audit

Each positive root step shares a single actual soil debit and vapor receipt with bare evaporation. Exact binary-rational checks establish:
- sum of all four root credits plus bare credit <= funded amount <= actual source debit;
- funded amount also <= actual represented vapor receipt;
- each h×demand <= actual root credit <= demand;
- actual cross-unit residual meets BOTH source-relative2^-20 and independently recomputed arithmetic envelope.

Two shared source transfers:2,107,689.934650kg and2,072,756.978378kg over the huge real patch. Residuals−1.7773e−5kg and−2.7909e−5kg; worst relative error1.3465e−11. These are whole shared soil transfers, NOT only root dose denominators. Root credits themselves are conservatively funded by both endpoints. No global water closure claim.

## Interpretation and remaining scope

This is the first actual exposed finite-soil physiological response in this sequence. It supports testing the declared mechanism, not shipping it. The model is an explicit uncalibrated game abstraction; no real soil hydraulic/latent-heat claim. All cohorts stay exactlydry at the surface. Root state is assigned, not evolved. Fixed single donor, tiny48minute interval, no7dayrun.

Receipts use pre-column cohort/depth/light and are consumed after vapor advection. Newly exposed roots from within-column standing depletion wait until next tick; that does not affect this alreadydry fixture. Five-way allocation is canonical and slot-symmetric, but biological ordering/source snapshot needs further review for general worlds.

The private QA law switch is NOT serialized. Existing version11 state-reload checks do not prove saved law persistence or genuine same-law continuation after process restart. No old-production trajectory equivalence or release migration is claimed. Proper opt-in model/schema lifecycle remains a promotion gate.

Reproduction: web/tests/egl-terrestrial-shared-prepare.py, same EGL build command/environment as terrestrial-two-tick, then web/tests/analyze-terrestrial-shared.py on run.log. Archives are deterministic gzip with decompression equality checked. Full generated source hashes are in shared-provenance.json.

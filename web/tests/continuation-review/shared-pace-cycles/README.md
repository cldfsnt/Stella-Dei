# Preregistered duration/rarity assay: FAILED conservation gate, incomplete

Plan/source frozen in0deb509. No physiology/tolerance adjustments after outcomes. First condition (rich, identicalpace1,5% initial, stablelight) passedday48 endpoint but failed original nutrient threshold at tick3000/day50. Reported Ndelta−1.000612974e−5 versus1e−5 limit, carbon drift4.80856e−5, swappedslots0. Thus the96run matrix DID NOT COMPLETE. No invasion/persistence conclusions may be taken from it. Initial failure and diagnostic reproduction retained.

## Attribution, not a relaxed pass
Separate diagnostic adds read-only precise(f64 sum of represented f32 fields) before/after maintenance and core ledger observations. Physiology remains identical. Sum of signed per-step changes exactly telescopes to final precise nutrient delta (observed residual0).

Atday56:
- Rate0/no additional maintenance: preciseNdelta−5.4919553e−6, entirely core. Sum absolute per-step core changes6.3646017e−6.
- Rate.2: preciseNdelta−1.1338902e−5; maintenance contribution−2.7201521e−9, core−1.1336182e−5. Sum absolute maintenance changes2.5782414e−7 and core1.2085281e−5 gives empirical accumulated bound1.2343106e−5.
- Direct original production step, identicalpace and no addedmaintenance, reportedNdelta−5.4985285e−6, agreeing with no-maintenance copiedcore to reporting precision.

At failingtick3000 preciseNdelta is−9.9977975e−6 while f32 nutrientTotal reports−1.0006130e−5: reporting rounding crosses the threshold slightly earlier, but precise ledger STILL exceeds it byday56. Merely changing the reporting sum would not fix this assay.

The added maintenance ledger is not responsible for the main loss. Existing core finite-precision operations exhibit cumulative drift even without added maintenance; the changed growth/respiration trajectory amplifies it. These stage sums localize error, not a proof that every individual core operation is correctly rounded or a mathematical arbitrary-run error bound. Do NOT reinterpret failed tolerance as passed.65 diagnostic/imported tests passed; this does not validate the stopped matrix.

Next step requires a separately reviewed numeric-accounting correction or independently justified error model with exact-operation bounds, followed by the original fixed matrix. No production/schema change, no rare/extinction outcome claim. Source and full logs preserved, logs losslessly gzipped with decompressed hashes.

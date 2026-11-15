# Isolated f64 bridge gate
Candidate/protocol55c486d. No production or scheduler integration, no new ecological outcomes or rate changes. Replaces only archived vapor-bridge acceptance arithmetic with conservative f64 bounds; source removal, represented receiver and downward-funded credit remain unchanged. f128 reference retained only for tests.

## Final results
- All30 actual daylight receipt endpoints/paid/funded values bit-identical to archived f128 reference.
-6326 fixed probes:2918 positive transfers,3398 zero/refused outcomes,10 invalid/overflow nulls.
- Exact binary Fraction oracle validates every positive actual debit<=request, funded credit<=actual source AND receiver, and BOTH existing budgets:2^-20 actual source relative and arithmetic ULP envelope.
- Maximum observed relative error8.695067e−7, below2^-20≈9.536743e−7. This maximum includes adversarial values, not typical daylight dosing.
- Reference accepted2924 positive transfers;6 extra conservative refusals arise only in fixed subnormal/extremely tiny physical-mass probes. No changed positive endpoints/credits among shared accepted cases. All6 remain unchanged pools; no retry/topup/escrow.
-3 tests pass in ReleaseSafe and ReleaseFast; complete emitted logs byte-identical. Includes invalid finite/range handling and exactzero no-op.

## Implementation boundary
TwoDiff retains represented source/receiver increments. Outward-rounded f64 intervals bound their physical kg products; upper residual is tested against LOWER bounds on the original two allowances. Nonfinite or unresolved positive bounds refuse. No runtime f128, heap allocation or exact-lattice search in candidate. Imported physical_water_f64 likewise uses f64; reference/test executable intentionally still includes f128 for comparison. Runtime cost not benchmarked, no device/performance claim.

Theoretical conservatism is supported by direct source reasoning and this bounded exact oracle, not a formal proof over every f64 input. f64 authority is not global climate conservation. No change to soil law, physics, seed/mutation behavior or production save schema.

## Retained first failures
Initial test compilation failed from a missing nested-loop terminator, corrected without algorithm change. First exact oracle then caught a real maxfinite boundary issue: lower(infinity) became maxfinite, masking an infinite adjacent ULP and accepting a case where the reference refused. Fixed with explicit finite ULP checks and nonfinite-preserving lower(); added exact regression. First Safe/Fast logs retained.

After that fix, oracle row-count assertion found two rows prefixed by Zig's test name; parser now recognizes BRIDGE within those lines. All6326 rows are checked, including row0, not silently sampled. No biological rerun or threshold changes.

Conclusion: this finite candidate clears the first bounded integration gate and preserves all observed daylight doses. Next integration/save/mutation/runtime gates remain separate; this checkpoint does not expose a beta or approve shipping.

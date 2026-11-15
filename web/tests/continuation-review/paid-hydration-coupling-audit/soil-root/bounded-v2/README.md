# Independent bounded v2 audit: initial checkpoint

3000 generated scalar/scatter/gather cases over scale2^-1000…2^1000, all24 permutations each, pass bitwise identity-slot fairness and exact Python Fraction global/per-cohort physical ledgers. No material leak found in these sampled inputs. Source at least one meaningful transfer in all3000. These are helper tests, not actual coupled biology or proof of universal correctness.

A separate behavioral witness fails inactive-cohort independence: gather(sources=[1,1e100,0,0], target=0, wanted=[1,0,0,0]) returns0 to the active source, while replacing unused source1e100 by0 returns1. All sources currently contribute sourceGrid even when wanted=0, artificially blocking unrelated participants. Owner notified before acceptance; preserve initial data/log. Fix should validate all sources but include only positive requested participants in grid selection, then repeat tests. No slot-priority leftover allocation recommended.

## Corrected acceptance

Owner filters inactive sources from the shared grid after validating all inputs. Independent inactive-source witness now returns1 both with/without unused huge source; test now asserts this regression. All3000 helper outputs remain byte-identical to initial sampled run and exact Fraction checker passes. Final source hashes retained.

Additional independent full-kernel qa_soil_root_v2_audit.zig reuses the original4000 mixed ample/scarce conditions and24 permutations, changing only kernel import and expectation that an unrepresentable evaporation leg no longer refuses the whole valid step. All4000 accepted versus original2322accepted/1678refused, with exact Fraction global/per-store/no-double-spend ledgers. Invalid, zero demand and direct root+storage gates still pass. Raw accepted records compressed. These are sampled numerical tests, not real climate/native-unit or organism-growth results. Invalid original inputs still refuse; valid skipped transfers leave water at source. Original frozen exact oracle and initial inactive-source witness remain archived.

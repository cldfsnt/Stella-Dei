# Remaining transaction boundary checks

Pre-outcome scope: actual production Planet.seedEligibility/seedMicrobes and auto_seed transaction in a QA-only four-point view of a loaded world. Vertices and all fields read by seeding have consistent length four, so mean area and shared gas scaling use four. No solver/topology/rendering inference from this reduced geometry.

Two fixed cases: (0) ample gas, a first resident paid with seedMicrobes in cell0, then all four eligible points seeded once; (1) same paid resident and four eligible points, shared CO2 initialized to a density that casts to the smallest positive f32. This is an explicit numerical exhaustion boundary, not ordinary gameplay scarcity. One resident remains unchanged; three free slots remain before the operation. All cells otherwise initialized using actual initialized(seed), warm temperature and1m water.

Initial resources are synthetic fixture inputs, never edits to a player's world. Test actual direct sequential reference against staged transaction, count and skip breakdown, unchanged planning/cancel and restoration of original complete save. No physiological evolution or performance benchmark. Source-paid semantics are those of existing seedMicrobes; exact real-number chemical conservation is not inferred from equality, especially subnormal nutrient/gas rounding.

Reason for numerical boundary: seed has no minimum positive amount, and each seed consumes at most the per-column average carbon availability while reducing global average by1/N. Ordinary real-number shared carbon remains positive over one N-point pass; resource_skips from exhausted global carbon therefore require finite-precision availability reaching zero. This test does not claim broad in-game exhaustion coverage.

# Declared basal geometry prototype: focused gates pass

Separate `site-tmp/origin-basal/src`, generated from frozen `origin-land-beta/src`. No production/shared-tree changes or whole-world run. Supersedes the held support-only geometry draft, not any saved law1 world.

## Explicit modeling assumption

Law2 fixes illustrative material density100 kg C/m³. Basal metres = live projected carbon kg C/m² / density; exposure height=max(basal, existing architecture). This is not empirical calibration. f64 geometry avoids underflow from valid tiny f32 biomass; zero/nonfinite biomass is ineligible. No body-height epsilon. Immersion and root exposed fraction use the SAME geometry helper, complementary for identical state/depth. Existing architectural aerial-stress term is retained separately; this is not a wholesale morphology replacement.

At fixed positive biomass, support→0 and root fraction→1 now have continuous immersion. Density controls10/100/1000 are fixed sensitivity checks, not alternative selected winners. For .1kgC/m² zero architecture, basal heights are10/1/.1mm; at .1mm water, immersion is about .01/.1/1 respectively. Architecture-dominant cases are invariant. Results do not establish survival or ecological fitness.

Only the opted-in copied physiology receives the immersion correction. Full immersion interpolates old composed mortality to existing wet mortality and raises existing photosynthetic habitat to immersion. Existing root-funded hydration, thermal/depth gates, light/C/N/space budgets, support upkeep, actual root-tissue capacity and biomass establishment cutoff remain. Root phase input still precedes column evaporation/condensation while biology sees final depth; shared geometry does NOT fix that separate phase-snapshot issue.

## Identity and persistence

Experimental schema9 / `origin_land_beta_v2` requires `physiology_law:2`. Schema8 / v1 requires law1. Missing field defaults1; law1 writer omits it, retaining old config fields. Unknown laws and disguised old identities reject in validation. Existing Origin revision5 retained. Copied capture chooses correct version/format and apply restores validated config unchanged. No public activation/new-world UI; original generation still defaults law1.

Focused schema serialize/parse/validate tests passed including law2 full typed equality, unknown/disguised rejection and old law1 omission/default restore. This is NOT yet actual native Save.apply/new-process continuation proof; those remain gates before a coupled trial/promotion.

## Executed gates

ReleaseSafe lifecycle-build, both exit0:
- `src/simulation/qa_immersion.zig`: initial focused controls plus basal sensitivity tests and imported unchanged core tests.
- `src/save_schema.zig`: existing schema/core tests plus experimental identity roundtrip tests.

Law1 step compared full serialized cells/RNG against frozen original core across96 depth/temperature/root combinations. Other checks: dry response unchanged, cold/deep/nonfinite enhancement refusal, positive/zero body geometry, adjacent height boundary, support subnormal/1e-12 and root1-ULP→1, dark wet-mortality equality, zero-carbon fixation refusal, recycled nutrient budget, empty soil refusal and submerged zero-root-demand. Zero initial mineral nutrient is not zero available nutrient because mortality recycles tissue; test uses total live+mineral nitrogen bound. No runtime benchmark or survival claim.

Reproduce with `web/tests/origin-basal-prepare.py <frozen-source> <new-absent-directory>`, then `zig build --build-file web/tests/lifecycle-build.zig -Dsource=<copy>/simulation/qa_immersion.zig` and separately copied save_schema. Exact copied source hashes and logs retained here. Existing held failure evidence remains unchanged.

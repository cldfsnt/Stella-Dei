# Corrected near-zero contact review

Read-only review of isolated v28 model, no main/frozen evidence edits.

PASS: protection-weighted geometric/baseline contact resolves both previously
identified zero-water and vanishing-support discontinuities. Original probe
now yields exactly0.09371546 biomass at both0m and1nm after1440s. At1µm it is
0.093715504, approaching dry continuously rather than receiving full protection.

Independent structure0.9 support sweep0/1e-15/1e-12 at0,1nm,1mm,5cm,19cm yields
identical f32 outcomes. At1e-9support differences remain rounding-scale. Model
29/29 tests reproduced.240 alternating dry/1nm steps end biomass0 with carbon
residual3.12e-8kgC/m² and nutrient residual−5.96e-7kg/m².

No new local ledger or continuity blocker found. Production remains unchanged.
The correction intentionally alters shallow survival; earlier paired evidence
must not be relabeled unchanged. Rerun both worlds and controls as planned.

Guidance helper uses actual per-cohort photosynthetic habitat, does not mutate
or infer guaranteed growth. Recommend visible text explicitly includes drying
stress and decline, rather than suggesting only light/resources govern growth.
Tiny positive habitat factor can still yield zero fixation after maintenance.

Temperature scope: strict<=273.15K fixation guard is intentional; mortality
retains a hard frozen/nonfrozen phase boundary and grazing/movement retain old
aquatic260K gate. This is not a globally corrected freeze/ecology system.

Legacy tradeoff caveat: at structure0.9 without support,5cm dark mortality can
exceed exact-dry mortality, because old dry structure resistance is stronger than
unprotected film mortality. The blend is continuous, but water isn't universally
beneficial for every inherited phenotype. This is not an introduced ledger bug;
do not promise monotonically better survival with more water.

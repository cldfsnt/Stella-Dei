# Internal hydration vanishes at any positive surface depth

Independent conceptual gate, not a water-ownership defect. No physiology coefficients or source laws changed. The fixture funds identical retained water through actual simultaneousUptake, charges the same one-hour evaporation, and passes the resulting fraction to the unchanged experimental core in each one-step snapshot. This is an isolated boundary diagnostic, not a coupled environmental history. Zero-h comparisons intentionally disable internal physiological benefit without changing the recorded paid store.

Actual donor phenotype478 starts at .12940502 kgC/m². Paid post-evaporation retained water=.04296942498386129 kg/m², capacity fraction=.9892532. Temperature300K, full light, finite C/O2 budgets10, one3600s core step:

| Surface depth | Internal fraction | Final biomass | Fixed carbon |
|---|---:|---:|---:|
| Exactly0m | .9892532 | .13705248 | .008727476 |
| 0.000001m (1micrometre) | .9892532 | .10878893 | 0 |
| Exactly0m | 0 | .10878879 | 0 |
| 0.000001m | 0 | .10878893 | 0 |

An arbitrarily small positive film disables the internal benefit because both mortality and growth use `env.depth_km==0`. The hydrated final-biomass jump is .02826355 kgC/m², about20.6% of the exactly-dry result. The disabled control is continuous at this scale. All38 imported/local tests pass, but this passing diagnostic explicitly exposes a model discontinuity; it is not acceptance of the physiology.

## Smallest continuous candidate (proposal, not implemented)

Retain the current paid hydration fraction h and all existing coefficients. For finite nonnegative depth and the existing temperature bounds, replace the exact-zero enable switch with:

`h_effective = h * (1 - aquaticSubmergence(depth))`

Here aquaticSubmergence is the existing smoothstep between15cm and20cm, not a newly selected threshold. Keep current mortality interpolation and exposure multiplier using h_effective, and the existing `max(external_photosynthetic_habitat, h_effective)` rule. Thus the dry endpoint is unchanged; tiny positive film does not discard paid internal water; fully aquatic response remains legacy; h=0 preserves legacy everywhere. The max has a possible derivative kink but no value discontinuity. This is a minimal continuity repair hypothesis, not calibrated physiology or a claim of additive unlimited benefit.

Acceptance should first establish 0→small-positive convergence,15/20cm endpoint continuity, h=0 exact legacy behavior, fully aquatic exact behavior, no water receipt change, and bounded effective habitat≤1. Retain existing temperature/deep-water exclusions; do not use internal water to remove heat/freezing/deep-ocean restrictions. Test both ownership and physiological timing after mortality before any full-world claim. No coefficient search or favorable-outcome tuning is justified by this audit.

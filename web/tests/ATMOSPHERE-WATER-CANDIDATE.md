# Isolated atmospheric water candidate

Not yet production or a physically complete weather simulation. Unchanged biology,
energy input and climate temperature calculation. No latent-heat budget.

## Correction

* Conservative local evaporation relaxation toward the actual saturation deficit,
  capped by liquid available; time constant 1 day. No evaporation from frozen cells.
* Condensation only of actual supersaturation, relaxation time 1 hour. Frozen
  condensate remains in the existing temperature-interpreted surface ice reservoir.
* Rain diagnostic uses correctly weighted daily-rate EMA (1 day).
* Globally joined phase pass precedes immutable-source moisture advection.
  Advection follows tangent velocity and projected displacement in km/s and km,
  with exponential donor budget. Zero wind moves nothing.
* Gather-only writes avoid atmospheric neighbor-write races. Mesh construction
  inserts symmetric unique neighbors; pentagon self fillers have zero edge rate.
* Reuses stale newWaterMass as coefficient scratch until next liquid copy. Saves
  read current waterMass, not scratch. No new persisted field.

## Verification

Six standalone tests pass. `results/atmosphere-water-unit.log` records 1, 60, 360,
1440 second runs. Pure f64 phase/exchange conserves mass to roundoff. Coupled
one-day liquid deviation versus 1-second reference is <=0.170/2000 mass units at
1440 seconds; this is splitting error, not exact timestep independence.

Four-cell production-style f32 gather has bounded nonnegative donor budgets but
is NOT exactly conserving after float storage: one-day relative drift at dt1 is
7.72e-5 (0.00772%), dt60 1.29e-6, dt360 2.40e-7, dt1440 zero in this fixture.
Retained mass is computed in f64 immediately before final gather, avoiding an
extra f32 rounding. No global correction or hidden mass balancing is applied.

WASM ReleaseSafe compilation passed including gather precision refinement.
Full browser packaging and native whole-world acceptance pending.
Existing surface liquid scatter and per-step velocity drag are unchanged and
prevent claiming a strictly conserved or timestep-independent whole planet.
Reserve/carry candidate must be merged separately, preserving biohooks.

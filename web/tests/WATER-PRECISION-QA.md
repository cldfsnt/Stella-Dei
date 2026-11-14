# Biological water bridge precision (experimental)

The first reserve prototype was not numerically conservative at biological scale.
The existing hydrology uses f32 fields in billions of kg, while tissue water is
kg/m². Adding a tiny biological debit directly to bulk water loses significant
bits. At 15 m depth and 1-second timesteps over three days, the old bridge gained
5.53 kg/m², or 234% of the final living reserve. At 60 seconds it lost 0.107 kg/m²;
at 50 m and 60 seconds it lost about 0.49 kg/m² (45% of living reserve).
A separate f32 physiological reserve also drifted about 0.009 kg/m².

## Corrected representation

Physiological reserves and water fluxes are f64. Every microbial cell also stores
nonnegative f64 liquid/vapor **numerical carries** in kg/m², each strictly below
one representable f32 bulk quantum. These are not biological or soil reservoirs.
The bulk representation rounds down and the carry retains the remainder. The
supply budget includes the liquid carry; vapor never supplies biological uptake.
Climate processes bulk until microbial reconciliation; carry-only cells are
therefore processed even when no organisms remain.

Fine water editing, basin creation and wave redistribution normalize existing
carries after direct bulk edits, including while paused. This changes only the
representation of edited bulk plus its preexisting remainder. Old worlds default
to zero carry and zero physiological reserve.

Water-limited carbon allocation rounds down to representable f32 carbon when
needed, preventing a final-ulp overdraft. Carbon/traits remain f32.

## Tests completed

- 39/39 bridge/helper/model tests passed (including signed-zero compatibility).
- 55/55 schema/helper/model tests passed.
- Actual microbial step plus the exact helper used by Planet was run at 0.02, 15
  and 50 m depth, with 1, 60 and 1440-second timesteps for three days; includes
  reproduction, daylight cycling and cold exposure.
- Maximum corrected ledger deviation across these nine combinations:
  **2.18e-11 kg/m²**. At 15 m/1 s, final error was -1.82e-12 kg/m², instead of
  +5.53 kg/m². Tests enforce absolute error below 1e-7 kg/m², not an ocean-relative
  tolerance that hides biological errors.
- Tracked runoff removes raw liquid/vapor after day one while retaining carries;
  the remaining system conserves through 1000 days and eventual drought death.
- Zero/subnormal bulk, carry-only empty cells, overflow/nonfinite/negative input,
  atomic transfer rejection and exact sparse save defaults/roundtrip are covered.

These are biological-bridge tests, not proof that the preexisting climate solver
is exactly conservative. Corrected native results and independent action/helper review are reported below. Earlier shoreline results used the pre-correction prototype.

## Corrected native coupled-world run

World1337, eight explicit Seeds across seven patches, one15m basin, one diagnostic
shelf edit on day20, 25% neighbor-first paid dispersal, no subsequent irrigation:
at day100 four protected shore cohorts remain, biomass0.073297136kgC/m² and
stored water1.97821446694kg/m². A naturally generated protected descendant146
arrived after shelf conversion on day63.3 and subsequently grew/bred. Version7
invalid-save rejection, unchanged state on rejection and exact restoration all
pass. Immediate paused fine-drain, Make Pond and wave saves all validate canonical
carries. Existing native teardown allocation warnings remain.

Independent paused-action tests pass (pond5/5 and god42/42 before the additional
signed-zero test). They cover representation preservation, untouched cells,
stale actions and old-world zero-carry no-op. Review caught signed-negative-zero
bulk compatibility, fixed in the helper and covered by a regression. Final schema
aggregate is55/55. This correction does not alter positive-water native behavior.

Matched reserve-disabled corrected native control completed100days: shore biomass and reserves are zero. It also passes exact save restoration and all three paused-action save checks. Full climate
water output includes tissue reserves and carries, but explicit player edits and
the existing climate solver prevent treating that total as a closed exact ledger.

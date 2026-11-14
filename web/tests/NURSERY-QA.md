# Explicit shallow nursery

Integrated in v20. This adds an explicit Origin-only action; existing 15 m basin remains unchanged. It does not seed, warm, change traits, run time, or replenish automatically.

The action shapes at most 19 unique cells: selected center is 10 m above the reservoir floor and contains 5 m water; first-ring neighbors contain 15 m water; outer dry rim is at least 17 m above reservoir floor and above neighboring external surfaces. Center and reservoir therefore share the same intended initial waterline, within f32 elevation precision. Existing terrain/water in the footprint is replaced explicitly. Repeat applies the same geometry without cumulatively raising the center; selected center contributes its elevation minus 10 m to the floor calculation.

API: PlayState.makeSelectedNursery(expected_point), browser stella_make_nursery(expected_point). Return positive affected patch count or -1 with no mutation. Guard exact current selection, Origin mode, finite elevations/water/conversion and bounded footprint. All checks precede changes.

Suggested label: “Shape shallow nursery”; disclosure: “5 m center + 15 m surrounding reservoir; changes terrain and water. Seed separately. No automatic refill.” Keep “Shape 15 m basin” as separate option.

Tests: `zig test src/pond_action.zig` passes 2/2, exercising original pond, shallow center/common waterline, reservoir, dry rim, untouched outside, repeatability, stale selection and NaN-outside atomic rejection. Actual API 30-day acceptance completed: one explicit seed, normal Grow, 53 paid arrivals, 24 tracked losses, 11 inhabited patches, 26 cohorts across five aquatic forms. Final biomass 0.202930898 kgC/m² summed over cells; final selected depth 8.544176 m. Exact save roundtrip and invalid-save atomic rejection passed. Native final-day render shows six visible inhabited patches. This is not proof that every world/cell thrives.

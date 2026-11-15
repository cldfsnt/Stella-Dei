# Current living growth-form navigation

`stella_visit_growth_form(expected_world:u32,form:u32)->i32`:1focused,0no current living match,−1unavailable/wrong mode,−2stale world or blocking UI/Advance,−3invalid enum,−4unsafe geometry/viewport. Existing enum IDs mat0,cushion1,rosette2,ribbon3,branching4,canopy5 appear as form_id in each sorted census row. This is current morphology, not species.

One synchronous on-demand O(cells×4) scan, no perframe scan or allocations. Nearest angular safe candidate to target camera; equal scores retain first cell/slot. Valid current positive biomass/identity/finite phenotype only; polar/invalid geometry cannot be focused. All refusal paths precede mutation. Success selects actual patch, frames at existing close distance radius+200, clears destructive tool through existing watchLife (not simulation Watch), preserves pause and all simulation resources/RNG/time. Main saves retain existing schema.

Pin.focused is exactu64 lineage and focused_form is expected enum, both ephemeral. Selected-only glyph/title use that actual living cohort; minority form is not presented as dominant. Peek names visited form and percent of patch biomass. Every draw revalidates identity/form; death/reclassification/selection elsewhere clears focus. All other glyphs preserve dominant selection and draw count. Details retains actual four cohorts/IDs.

Same native patch applied to separate Wetlands copied tree through growth-form-preview.patch plus new helper and required export. No copied physiology/factory/save authority replaced. Pure helper/peek tests passed; native actual7day mixed-patch acceptance required separately, not inferred from helper tests.

Native Details correction: actual mobile Details now calls the same validated focusedCohort before choosing the displayed identity/traits. A valid explicit visit shows that cohort's current form and its own biomass, never the patch total as the minority amount. Without valid focus it retains maximum-biomass colony selection and aggregate patch biomass, now labeled Patch biomass rather than hardcoded Microbial mat. This fixes a native-panel mismatch not covered by the HTML four-cohort snapshot.

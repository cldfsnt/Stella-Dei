# Functional colonial producers: isolated prototype

Status: five fresh Zig tests pass. This module is not imported by the game,
not in a save schema, and has no rendered/world acceptance yet. Existing
microbes, Sandbox and saves are untouched.

## Why this is a progression step

A lineage can allocate actual new carbon to support tissue and photosynthetic
fronds. These are separate conserved pools. Support raises the collecting tissue
in a shared water column. Higher fronds absorb some finite incoming light before
lower mats; equal-height colonies share a layer, including when carbon/nutrients
are scarce. Support itself does not photosynthesize and has higher maintenance
cost. No taxonomic label, timer, research-point payment or automatic unlock is
used. This is a simplified functional colonial producer, not a simulation of the
historical origin of multicellularity or a claim that a true plant evolved.

A zero-support founder produces donor-funded propagules with inherited allocation
variation. Daughters initially receive the donor's actual tissue proportions;
new structure must then be grown, not created by the mutation event. A tested
organized daughter establishes and funds a second-generation propagule.

## Player-relevant tradeoff

- In open clear water, a flat mat grows faster because it avoids support cost.
- In crowded water, raised collecting tissue gains light at lower mats' expense.
- Lowering water exposes tissue; disturbance breaks more tall tissue. Damage
  becomes detritus and releases bound nutrient, rather than disappearing.
- Restoring conditions permits recovery from surviving tissue, without reseeding
  or a guaranteed-survival branch.

Future UI should show fronds only when actual support/frond pools exist. A marker
can illustrate their structure at map scale, but must not imply individual-scale
geometry. Life details should show collecting/support mass, intercepted light,
maintenance and damage. Current tests do not establish that this is readable or
fun in the full game; that is a separate acceptance gate.

## Accounting and controls

Units: kg C/m² in tissue/detritus/available carbon; bound nutrient is 0.1 times
living carbon. Photosynthetic fixation and respiration exchange carbon and
oxygen-equivalent capacity. Total light absorption is capped by incoming light;
fixation is capped by absorbed light, carbon and nutrient. A four-cohort fixture
bounds work. Carbon and nutrient errors remain below 1e-10 in the test cases.
Same-height light and oxygen-limited maintenance share resources without array
priority. Vertical priority is intentional ecological competition.

Fresh results (`colonial-tests.log`):
- Zero-support founder: three funded daughters, actual inherited support develops.
- Open-water 20-day mechanism control: organized biomass 1.4666, flat 1.9013.
- Same-column crowded control: organized 1.4666, lower flat mat 0.05447.
- Exposure/disturbance: 1.0081 → 0.007631 living carbon; restored conditions
  recover to 1.4043, with damage recycled and resource ledgers preserved.
- Actual inherited allocation 0.016375, not preassigned high structure: organized
  descendant 2.6289 versus support-disabled matched descendant 2.5084 after 30
  days of controlled competition. It funds a generation-2 descendant with real
  support tissue. This is controlled establishment, not ordinary-world evidence.

An initial 0.3 m optical attenuation length made support beneficial even in the
open-water control; it failed the intended cost/benefit test. The present explicit
3 m attenuation assumption produces the intended tradeoff. These are authored
gameplay parameters, not empirically calibrated biology. No full-climate tuning
or production model change has been made.

## Before integration

1. Confirm timestep and sparse-resource stability, realistic extinction/recovery
   cases, and that mutation/competition works across more than one fixed seed.
2. Decide explicit relationship to current cohorts/feeding: support may be harder
   to consume, but adding free armor or duplicating biomass is not acceptable.
3. Preserve old save values with a separate opt-in model revision/default zero
   tissue; never convert existing biomass into a new class silently.
4. Run actual generated-world and player water/shading interventions, render actual
   tissue/competition, test mobile readability, then consider integration.

No publication or repository push was attempted by this worker. Small files are
kept locally for the coordinator's authorized checkpoint workflow.

## Second gate: extinction, diversity and time steps

Eight fresh tests now pass. A uniform 0.0025 kg C/m² resolution floor (one quarter
of a propagule, matching the current production model) recycles sub-resolution
living tissue into detritus and releases its bound nutrient before clearing the
slot. This is explicitly a coarse-population resolution rule, not proof of a
biological minimum population. It applies to every lineage; no winner is chosen.
Three small occupied slots clear conservatively, and a surviving donor can fund a
new daughter in the freed slot with a new lineage ID. No carbon is created and
extinction counters increment only once.

Severe exposure can extinguish the colony entirely. Restoring water/light does
not resurrect it. A carbon/nutrient/oxygen-depleted control does not gain organic
carbon. Thirty-two independent founder PRNG seeds produce offspring in all 32
cases; 30 develop actual inherited support in this bounded habitat, two do not.
This is not a universal innovation guarantee. Carbon/nutrient and unique living
lineage checks pass throughout.

Twenty-day step-size controls at 60, 1,440 and 3,600 simulated seconds end at
biomass 1.4645084, 1.4648403 and 1.4653580 respectively (largest difference about
0.058%). Carbon error is at most 9.63e-13. These are isolated biological controls,
not a claim that full-world climate is timestep invariant.

## Concrete integration proposal (not implemented)

Create a separate producer candidate from the latest verified runtime. Preserve
`Cohort.biomass` as TOTAL living carbon so all existing world/accounting paths keep
one source of truth. Add two explicit fields:

- `organization: f32 = 0`, inherited target allocation [0, 0.7]. Do not repurpose
  the existing `structure` trait, whose drying effect must remain identifiable.
- `support_mass: f32 = 0`, a SUBSET of biomass, constrained to [0, biomass].
  Photosynthetic tissue is derived as biomass minus support_mass. Never add the
  support field to total carbon a second time.

New fixed/assimilated carbon is partitioned by organization. Mortality and grazing
remove support proportionally with the rest of consumed tissue; structural carbon
is not free armor. Maintenance of support pays extra oxygen-limited respiratory
carbon. This keeps the current food web functional and provides a new tradeoff
rather than replacing consumers. Donor-funded fragments inherit proportional real
tissue and a mutated target allocation; no tissue appears solely due to mutation.

Attached structure must have an explicit motility cost: a moving lineage leaves
its support carbon as detritus at the source (releasing its bound nutrient), and
moves only surviving non-support biomass. Require the remaining fragment to meet
establishment resolution; otherwise reject movement. This is a coarse attachment
mechanism, not individual plant locomotion. Re-evaluate movement food/space/cost
against the actual fragment; use shared eligibility so the UI explains it.

In cells with expressed support, compute four bounded vertical light layers from
actual support/frond pools. Equal-height cohorts share finite absorbed light and
scarce resource budgets. Production tuning must respect its existing 1 kg C/m²
capacity, nutrient and atmospheric flux units; the prototype's larger fixture
biomass cannot simply be copied into a real world. Keep zero-support baseline
cells on the old path during the first compatibility gate, then document any
model-revision change to future dynamics explicitly.

Save upgrade defaults both fields to zero, preserving every old biomass and trait
value without silently classifying old organisms. Validate the subset relation;
serialize actual tissue and lineage state. Add no new global taxonomy/unlock.

First playable acceptance: seed real simple life, wait for actual inherited
support, establish a neighboring competitor using existing tools, observe light
competition, lower/restore water and show damage/recovery or honest extinction.
Rendered branched/frond glyphs must depend on positive actual support AND collecting
tissue, with Life labels such as 'attached photosynthetic colony'. Show support
cost/light capture and explain that this is a functional precursor, not a true
plant species. Include actual full-world save roundtrip, old microbe/Sandbox
regressions, consumer/movement conservation and mobile playtest before publication.

This is a bounded next implementation, not another indefinite research phase.
The unresolved production parameters are explicitly a gate for integration tests;
no runtime, schema, glyph or automatic class change has been made in this prototype.

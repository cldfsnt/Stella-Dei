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

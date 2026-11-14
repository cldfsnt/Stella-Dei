Experimental merge based on deployed master92f96487fcc0114371a56b9743d6c77566841925. Production untouched. Keeps exact corrected atmosphere/nursery/Watch/snapshot APIs and current exploratory propagation, adds reviewed precision reserves and schema7. No policy/tuning changes.
Base Planet SHA256 b0b4ea3c226559ff6862c9dfc3e3c7530ac1334160e877729e0e08714cdea631

## Passing unit checks
Schema/model59, bridge43, god48, nursery/pond9, atmosphere6. The atmospheric
module and Planet's phase/advection code are exact v20; only the biological
environment/precision bridge and paired action carry hooks are added.

## Completed real one-founder nursery path
Actual Focus/Make Nursery/Seed callbacks, ONE ordinary Seed, normal Grow
(6 simulated hours/second), no later watering/biological assignments:
at day30 (120 simulated play seconds) 7 occupied patches, 11 living cohorts,
4 forms (mat4/cushion3/rosette3/canopy1), biomass0.0830432144 versus initial0.02.
41 funded arrivals; 31 tracked arrivals subsequently lost. Growth is not
universal success and loss counters remain honest. Nursery shaping is invoked
twice in harness to test repeatability before time advances; no second Seed and
no subsequent care.

Version7 invalid-save rejection, unchanged state on rejection, exact restoration
and immediate paused nursery-save canonical validation pass. Existing native
teardown allocation warnings remain. Native legacyv6 migration and paused
fine-drain/wave checks are pending in an extended harness.

## Shore comparison pending
Both reserve-enabled and disabled full engine100d runs are underway under v20
climate, ordinary expanded eight Seeds and a SINGLE diagnostic shelf editday20.
No automatic refills/assigned traits. The shelf is not an accessible UI feature
and is not deployment-ready. Daily lineage/patch data distinguish existing
residents from later colonization; don't infer establishment from body reserve
alone. Generated test code logs true zero-surface-water fixation separately.

## Native migration and direct actions completed
Actual deployed v20 30-day v6 fixture (40962 cells) loads with all existing
cohorts/resources/RNG/stats unchanged; reserve, retention and both carries
default exactly0. Surface/vapor arrays are unchanged. Subsequent v7 save/apply
is exact. The native harness must pump pending render jobs before replacing
world state; the corrected harness does so.
Immediate paused0m target, Nursery and wave all pass canonical save validation.

## Re-wetting shelf comparison completed (not drought proof)
Expanded eight-Seed100d, actual new v20 climate, same day20 .15m shelf:
- ON: depth0.6769347m, biomass0.01836093, reserve0.410971019kg/m².
- OFF: depth0.6772665m, biomass0.049347144, reserve0.
Both exact native saves and paused nursery checks pass. No zero-surface fixation
was observed. Byday21 the shelf already has0.338m water; it becomes ordinary
aquatic habitat, not a persistent drought test.
Atday20 ON contains four residents (3,77,19,25). The day100 survivor2600 first
appears on shelfday71 with parent346 observed in neighboring13598. This is new
colonization, but into a re-wetted aquatic site, not proof of dry-land evolution.

## Matched saved-world dry-edge10d
Both replay the identical actual v6 nursery30d save. Existing four founder
lineages/traits match exactly. One wet simulation hour lets ON take real surface
water; OFF remains uncharged. Global biological water ledger:
taken4.1618453025 − returned0.0311895755 − evaporated0.0073114192
= bodywater4.1233443078kg/m²-sum, error0.
Select actual populated neighbor13598, raise once above max neighboring
waterline by requested0.5m (actual0.48828125m due terrain f32 precision), set0m
once. No biological edits or later care.

ON day1 biomass0.00323462 versus OFF0.00296253. Both re-wet to~0.222m byday1
and~0.51m byday10. ON final biomass0.038776364/water0.854849487; OFF0.041660395.
Only20 vs21 dry ticks (~2 simulated hours), with zero fixation while surface
water is zero. ON final biological ledger error5.68e-14kg/m²-sum; OFF0.
Both exact saves and paused0m/Nursery/wave checks pass.

No meaningful sustained drought advantage is demonstrated. Per-edge liquid and
phase condensation/evaporation diagnostics are next to identify re-wetting
sources before any taller explicit plateau test. No physiology tuning and no
new shoreline UI has been added.

## Re-wetting source measured, not assumed
A one-day matched stress replay records actual per-edge liquid transfers and
the phase function's evaporation/condensation. Cell13598 has:
- Liquid inflow: **0m**.
- Liquid outflow:0.0411480m (observed bulk flow change -0.0411479m).
- Condensation:0.3490594m; evaporation:0.0859563m.
- Observed net phase addition:0.2631031m.
- Interstep post-hydrology net addition:~0.00044535m, consistent with returned
  biological water being a small contributor, not the dominant source.
- Final depth:0.2224016m.

The existing phenomenological atmospheric column rains heavily at this site.
Raising the edge0.5m already prevents neighboring liquid inflow. Raising5m
would not remove atmospheric condensation, so no taller plateau test or tuning
was used simply to force a drought success. This local accounting does not claim
the entire preexisting liquid solver is perfect or real-world meteorology.

Candidate is stable in tested scenarios but has NOT demonstrated meaningful
drought-resilient shoreline gameplay under v20 climate. Keep experimental. Next
sound investigation is an actual naturally drier location/exposure, or a clearly
disclosed environmental action with its physical water/energy accounting, not
altering traits/mortality just to force the desired ending.

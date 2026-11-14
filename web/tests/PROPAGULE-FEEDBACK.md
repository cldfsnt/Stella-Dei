# Actual arrival / tracked-loss feedback (isolated candidate)

No animation creates life. The model calls Tracker.arrived only after accepting
a paid propagule. Failure events require an actual lost cohort with the same
lineage and destination, still present in the bounded observation tracker. There is no arbitrary time
expiry; an evicted/untracked loss is not recorded. Neither is called failed establishment. Movement forgets
the pending arrival rather than inventing mortality. These receipts establish
arrival or loss only, not successful adaptation or long-term establishment.

The tracker bounds both pending lineages and events to32. Renderer consumes each
serial once, discards offscreen events, and shows at most12 recent pulses for1.6
real seconds independent of simulation pace. Cyan diamonds mean arrival; amber
crosses mean tracked colony lost. A tiny legend distinguishes them from green
+ actionable Seed targets. A loss replaces that lineage's still-visible arrival
pulse. Neither leaves a ghost living plant. No full-screen flash or strobing.

Five pure tests cover bounded eviction, valid tracked loss only, older tracked losses,
real-time pulse expiry, newest12 receipts, and replacement of arrival on failure.
The native visual fixture follows the camera to the first actual events generated
by the ordinary coupled single-founder shallow nursery run. It never assigns
biomass, births, survival, event receipts, or trait upgrades to manufacture success.

The observation tracker and visual pool are session-only and intentionally not
serialized. Loading a save resets them; serial regression also clears the pool.

Actual native capture observed a paid arrival at day1.129 (lineage2,17884→17886)
and an actual loss at day4.917 (lineage3,17884→4496). Reviewed cyan diamond and
amber X rendering. Camera follows events for visual QA; the unchanged-camera
ecological comparison is a separate test. Final wording is tracked colony lost,
not failed establishment; the tracker has no time expiry, only bounded eviction.

Final Inspect-mode capture removes placement targets and fixes the fixture camera
orbit scale. Actual arrival day1.129 shows two mats; first tracked loss day4.725
shows an amber X alongside actual surviving/other cohorts and distinct inherited
forms. The X refers to one tracked lineage, not extinction of the whole cell.
The run uses the explicit experimental shallow-nursery scenario; clean production
15m-basin ecological performance must be tested separately. No nursery geometry
change is included in the clean visual overlay. Eight-day native run exits0 and
save/restore checks pass, with the existing GPA shutdown leak diagnostic.

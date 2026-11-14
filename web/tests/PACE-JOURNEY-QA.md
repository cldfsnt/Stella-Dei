# Pacing, live journey and deliberate pond action

New worlds start at Grow (6 simulated hours/second) instead of the previous
browser 1 h/s. Pace cycles Grow → Fast → Slow (6/24/1 h/s). These are existing
supported rates; no biological clock, mutation rate, maximum speed or physics
step has been increased. Initial Origin pause and saved pace/pause are preserved.
The button uses names with feedback describing simulated days per real second.

A small header button links directly to the current next step. Its three-second
read-only refresh derives Origin stages from current living biomass, living
descendants, actual support-bearing forms, diversity and occupied patches.
Stages regress after extinction; no unlock, reward or organism is manufactured.
This is guidance, not evidence of fun or complete progression.

Shape basin + add water is an explicit one-time player intervention from Life
snapshot. The shared native handler validates the expected selected cell and
whole footprint before changing terrain. Center+immediate neighbors become a
flat shallow floor; the second ring becomes a dry raised rim. At most 19 cells
are edited. The floor is raised to at least bordering exterior water surfaces,
then the rim is at least 17 m above the floor. The floor receives 15 m water and
the rim is drained. Existing high rim terrain remains high. An unchanged world
produces identical terrain/water on repeated calls. No life or temperature field
is injected, and no automatic refill is installed. Simulation may change depths.
The prior depth-only action failed an actual-world survival test, so its 'pond'
label was removed and replaced by this genuinely contained terrain action.

Life snapshot now names each living cohort's actual aquatic growth form, through
the same producerForm function as the simulation/visual classification.

Executed focused checks: mobile_guidance tests 3/3; pond_action 1/1;
habitat_feedback plus imported production-model tests 25/25; shell tests include
live-goal regression/fallback/open, pond success and stale/sandbox rejections.
Joint compiled actual-engine UI and pond ecology runs are integration gates,
not established by these unit tests. No physical Android measurement is claimed.

Final depth adjustment: 3 m retained basin evaporated by about day 17 in the coupled-world test, with extinction by day 19. The explicit basin action now supplies 15 m once with a 17 m rim; sustained viability is subject to the new coupled-world run, not asserted by unit tests. It writes validated water mass directly because the separate fine-depth editor intentionally remains capped at 5 m. No hidden refill was added.

# v21 · fast-forward and clear feedback

Explicit Speed / fast-forward panel offers requested 1, 6 and 24 simulated hours
per wall second. It shows measured achieved speed separately and never unpauses
when changing target. Legacy/custom saved speeds display Custom, not a false preset.

Physics uses fixed 1440-second ticks independent of requested speed, recomputing
solar phase and game time each tick. At most two ticks per frame; no second tick
after the scheduling budget is spent. An indivisible tick can exceed that budget.
No high-speed water/rabbit skipping. Background gaps, pause, menus and loads clear
pending demand; visual time never advances beyond executed physics.

Actual native rendered wall tests achieved about 0.96 / 5.56 / 8.35 hours per
second at the three targets. This is a real but hardware-limited fast-forward,
not a promise of 24h/s or Android performance. See speed-adapter/REPORT.md for
resource/finite checks, identical-physics hashes, saved-world experiments,
callback and rabbit food/breeding regression evidence. Fixed steps change old
stochastic trajectories; no trajectory equivalence with v20 is claimed.

Compact Watch now explains cyan arrivals / amber tracked losses (not every
death), shows since-load session counts, and preserves lifetime births outside
Watch. Counts are capped only for display at 999+, not in simulation. These are
observations, not fake effects. Loaded saves reset transient observations.

Rabbit lighting now transforms local normals into world space for existing
uniform-scale entity transforms; native paired rendering demonstrates the fix.
No Blender assets or new material pipeline are claimed.

No schema7/reserves, fire button, or completed terrestrial evolution is included.
The camera Fit life prototype is separate. Site remains owner-private. Existing
browser-local save/backup limitations and native shutdown leak diagnostic remain.

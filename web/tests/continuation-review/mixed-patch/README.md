# Natural mixed-patch observation, two consecutive simulated days

Production unchanged. Isolated current engine loaded preserved naturally generated 30-day QA world, selected existing patch13594 without changing organisms/resources, then ran two consecutive windows of60 real Planet.simulate ticks at dt1440seconds. Each window is24 simulated hours. This is a native EGL/software-renderer scheduler correctness replay, NOT10real seconds, achieved24h/s performance, a browser interaction test, or Android verification. Selection only is QA-directed. Full current world state after each observer-on window exactly equals a restored same-baseline observer-off replay; next window starts from that identical result. Actual watch fixed/recycled/grazed totals exactly equal independently instrumented real Microbes.step flux sums. End membership exactly matches actual post-scheduler cell.

Four original colonies persist through both windows; no birth/arrival/disappearance in this patch. Endpoint carbon biomass kg C/m²:

|ID|day30|day31|day32|
|---|---|---|---|
|34|.00549095|.00564292|.00580305|
|20|.01787373|.01569785|.01721414|
|21|.00443487|.00445770|.00448136|
|24|.00315428|.00312216|.00309084|

ID34 has feeding .02485, the others0. ID21 has slightly higher efficiency1.04917 and actual support .00012354 initially; ID24 structure .07911 but zero support. Correlated optima differ, too. No trait was assigned for this assay. Day1/day2 fixed=.00749131/.00720357, biological return=.00415484/.00428228, grazing=.000427304/.000439304 kg C/m². Return does not include all movement/god processes; not a complete local budget. ID20 reverses loss to gain: a one-window rank is not a stable winner. Watch endpoints cannot attribute each change to specific causes. This demonstrates meaningful real simultaneous gains/losses and nonzero feeding, NOT universal stronger succession, causal benefit of any trait, or unbounded diversity.

Temperature294.258→294.290→294.321K, local nutrient .0185047→.0183080→.0181411. Logged water is raw engine waterMass, not labelled depth. Natural conditions evolve; no fixed light/resource control, and no claim the different fluxes isolate competition causality. Existing UI can accurately show these distinct changes without inventing new organisms or scripted outcomes.

Build/run exit0; inherited native GPA teardown leaks remain, not leak-clean. Initial compile failed only because a fixture variable shadowed an existing name; corrected and original error retained. No source physics edits. Exact JSON endpoints and full compressed native output retained. Source copied before concurrent Watch-toolbar implementation.

Reproduce: python3 web/tests/egl-mixed-patch-prepare.py <isolated-dir>; build with web/tests/egl-propagule-visual-build.zig -Dsource=<isolated-dir>/main.zig. Run from repository with LIBGL_ALWAYS_SOFTWARE=1 STELLA_ORIGIN_COUPLED=1 STELLA_ORIGIN_FAST=1 STELLA_PRODUCER_LONG=1 STELLA_FORMS_SINGLE=1 STELLA_ORIGIN_WIDTH=390 QA_PULSE_SAVE=<preserved-natural-world> STELLA_EGL_CAPTURE_PREFIX=<temporary-prefix> <binary>. QA save stays local, not uploaded.

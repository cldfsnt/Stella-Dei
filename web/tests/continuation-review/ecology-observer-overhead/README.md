# v63 observer native sanity gate

One predeclared ABBA run, no repeats: disabled/enabled/enabled/disabled. Real natural-day60 world,40,962 cells; each arm restores the identical owned save then12 warmup and60 timed1440s coupled steps. Full saved endpoints including RNG are exactly equal across all four arms; original restored. Timing includes actual Planet.simulate and gameTime only, excludes rendering/census/serialization. CPU window explicitly released by sibling after its separate scans.

Disabled QA path skips physiologyDeaths as well as observer record bookkeeping; preexisting before_cohorts remains in both. Tiny call/guard overhead remains on the disabled path, so this is not literal zero-hook compilation. Source/math/biology otherwise unchanged; no production patch.

Off mean9.455/8.054ms, on9.109/7.975ms per step. Off medians9.139/7.922ms, on7.855/7.918ms (see exact JSON). Enabled totals are3.65% and0.98% lower in the two directional comparisons, but this is noise, NOT a performance improvement. One enabled tick reached58.56ms; order/OS jitter is material. No repeatable >5% slowdown identified. This small fixed sample does not establish an overhead upper confidence bound, browser/device FPS, frame responsiveness, or cost in dense worlds. No followup sweep or production optimization justified.

Copied-source native EGL initializes the actual engine; no graphics calls in measured loops. Preparer exact-source guard initially failed before compile due to whitespace/operator spelling and was corrected to match existing saturating accumulation; no outcome was run with the failed preparer. Binary/input/source hashes retained. Model observer-on/off correctness had also passed the independent ecology-cue native gate.

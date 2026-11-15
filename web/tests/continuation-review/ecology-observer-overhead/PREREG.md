# Bounded native observer overhead sanity

One fixed ABBA sequence: observer disabled, enabled, enabled, disabled. The same frozen actual natural-day60 world (40,962 cells) is restored independently before each arm;12 actual coupled ticks warm up, then60 ticks at1440s each are timed. Timing covers Planet.simulate and gameTime increment only. No frame rendering, census query, save serialization or stdout inside timed intervals. Complete saved state/RNG at every endpoint must match the first arm, and original input must be restored afterward.

QA-only copied Planet guards physiologyDeaths when observer disabled; the preexisting before_cohorts snapshot stays in both arms. The Observer.enabled false branch still executes the small public call/guard; this is not a literal binary with every hook removed. No production changes. Report individual means/medians, paired spread and pooled descriptive ratio, not a significance/device-FPS claim. An apparent >5% repeatable increase in both directional comparisons merits further review; a noisy/small result does not justify another sweep. No additional favorable repeats.

Native EGL fixture used only to initialize the actual saved world. No graphics work in measured blocks. Coordinator and sibling compilers must be idle during the four measured arms. Existing exact native observer/model acceptance remains the correctness baseline.

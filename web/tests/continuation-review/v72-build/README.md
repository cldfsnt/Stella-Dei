# v72 Inspect-to-Watch transition

The actual native baseline proved that native Inspect left open beneath the HTML Life panel blocked both ordinary and explicitly resumed Watch. Fix 0389740 prepares a private watch baseline, then only on success commits the watch and closes native Inspect. Ordinary Watch never resumes pause; checked Watch resumes only with explicit authorization. Escape/Climate remain blockers. Generic dialog close and god actions do not dismiss native Inspect. Failure preserves pause, selection and prior watch.

Native acceptance 4802a03 covers actual rendered glyph pick and both pause states, stale world/selection, Escape/Climate, invalid population, actual watched tick, repeated start and cancellation. Full saved state/RNG unchanged except explicitly requested pause resume; original restored. No physiology or renderer changes.

Full JavaScript/build status and unchanged source/artifact hashes are recorded in provenance.json. No deployment in this checkpoint; wait for verified fork source. No fresh browser/device performance claim.

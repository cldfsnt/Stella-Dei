# Truthful last water-step feedback

Production successful Water− receipt now uses actual represented removal and remaining selected-patch depth. Text is stored in a PlayState-owned128-byte buffer, never a dangling stack slice. Example: `Patch last step: -1.00m; depth16.47m` (formatter inserts space after depth). Last step explicitly excludes accumulated held-gesture totals. Existing refusal text remains unchanged. Positive depths/removals below.01m display<0.01, not zero; huge finite numbers use bounded scientific notation; invalid formatting inputs have safe unknown fallback.

Eight Zig tests pass: actual brush tap, shallow depletion, dry refusal, held step, gesture parity, invalid/precision refusals, tiny/huge format cases. Native320px actual paired30day-world one-tap acceptance passes independently deep-frozen full non-water save identity, same ecology outcomes as original paired assay, readable screenshot. No browser/device performance claim.

Successful save_game.apply clears transient last-action feedback and timer, alongside old god receipt, so loading another world cannot display stale step text. Native invalid-version failed-load leaves feedback/timer unchanged; successful restore empties both. No save schema or biology changes. Known inherited native GPA teardown leak warning remains documented; not leak-free proof.

Reproduce via egl-water-paired-prepare.py and same env/build recipe as sibling water-paired/README.md, at STELLA_ORIGIN_WIDTH=320. run-load.log is final source acceptance; initial run.log predates only stale-load guard. Logs losslessly gz archived withmtime0 and decompression verified.

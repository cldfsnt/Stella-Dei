# Earned-fuel player route, v63 audit and small improvement

## Verified blocker
Actual current native discovery in two immutable saved worlds,81 chunks each, zero dry fuel sites. Sunlit14 had19 wet fuel patches. Old finder chose maximum detritus at29254,4.1520333m deep, about5 ordinary Water− taps. Earned shallow fuel existed, so this was unnecessary repetitive intervention, not missing biology/fuel. Natural60 had63 wet fuel sites and already chose a one-tap patch. Complete biology/save/RNG unchanged by finding after restoring only documented view fields; original save restored.

## Small change
Keep first already-dry burnable site preferred. Otherwise choose wet fuel by fewest nominal ceil(depth metres) taps, then more fuel, then stable index. Dry-but-blocked fuel is a separate last fallback, never mislabeled wet. Conversion checked once per chunk; finite water/fuel/geometry and final current preview remain guarded. No automatic draining, ignition, new fuel or biology. UI says 'About', up to1m each, external removal, drying can harm colonies, pause first, rounding/running water can change estimate. No exact universal edit count claim.

Pure tests cover0/near1/exact1/above1/deep/nonfinite, same-bucket fuel/index ties and separate blocked fallback. Shell tests verify single target read, same boundaries, blocked ignition and explicit intervention/refill warning. Production code797f612; only subsequent fixture const correction.

## Actual player route acceptance
Sunlit14: selected10071,0.086113624m, .027227182kgC/m² dead carbon. This is not the absolute shallowest site: it wins the one-tap bucket by more fuel. One real Water− removes660.451 native water units (each1e9kg), then successful existing ignition burns208,819,677.82316208kgC and raises temperature2.116607666K.
Natural60: selected13668 unchanged,0.3546412m, .35300344kgC/m². One real Water− removes2719.9312 native units, burn2,707,370,349.5254517kgC, temperature+27.441894531K. These large totals reflect coarse planetary patch area, not a small real fire.
Both: wet attempted ignition refuses without changes; intentional drain changes only selected water; preview pure; preview/direct old ignition/actual Play ignition receipts and full physics match exactly; burned save reload exact; full original restored. No growth followup, wildfire, guaranteed recovery or evolutionary claim. Old gas/heat bounded residual accounting unchanged.

## User steps
Origin with naturally earned dead carbon → Pause → More → God tools → Find dead organic matter. Search returns to planet. Reopen God tools to read current water/estimated taps; close, use Water− deliberately at selected patch. Reopen God tools → Refresh if needed → Ignite detritus. Successful action closes the sheet and shows the real ember/heat receipt. Draining and ignition remain separate choices; pause avoids hydrology refilling between steps. No existing world is remodeled on load.

## Reproduction / limits
Generators egl-fire-route-audit-prepare.py and egl-fire-route-player-prepare.py; Zig0.13 ReleaseSafe egl-propagule-visual-build.zig. QA_PULSE_SAVE selects hashed input; STELLA_ORIGIN_COUPLED=1 STELLA_ORIGIN_FAST=1 STELLA_ORIGIN_WIDTH=390, LIBGL_ALWAYS_SOFTWARE=1 EGL_PLATFORM=surfaceless. Both final runs exit0; all59 public exports exact. Native software EGL, not actual browser/device proof. Explicit QA exit skips inherited teardown. Retained preliminary compile errors: local wet/dry name collision, then const-required water_check declaration; only fixture fixes. Old complete logs and final complete logs gzip-preserved. Screenshots inspected separately before release.

# Phase-receipt risk and proposed final-demand contract

Read-only research proposal; no code, run or change to historical law1/law2. Source locations refer to frozen `site-tmp/origin-basal/src`, hashes in source-sha256.json.

## Current mismatch

`simulation/shared_soil.zig:13–28` calculates source-funded credits and `h=credit/pre-column demand`. `planet.zig:1386–1391` supplies the pre-column environment and saves only root_h, while capillary processing changes standing water. `planet.zig:1762–1765` supplies final depth to physiology. `microbes.zig:145–164` uses the old ratio with final-depth immersion and cohorts after upkeep/mortality.

Thus a drying column can make the old hydration fraction too generous for final exposed-tissue demand, even though every physical transfer was paid correctly. In the reported 1mm-water case, depth changes .9904mm→.175mm. For an illustrative exactly1mm body, exposed fraction changes .0096→.825 (~86x). This ratio is explanatory, NOT a measured demand/error ratio for the actual cohort; real geometry, tissue, light and domain eligibility must be used. Wetting can instead leave paid water with no final root benefit.

Current law2 outcomes must retain this limitation: paid receipts alone do not establish that their stored hydration signals fund final-state demand. Do not rewrite the historical law or retroactively reinterpret survival as a corrected-law result.

## Proposed new-law contract, not implemented

- Carry actual source-funded credit in kg water/m², replacing transient `[4]f32` root_h with `[4]f64` credit. At40962 patches the incremental allocation is655392bytes, about.625MiB. No separate persistent physical reservoir.
- Compute demand against the final environment and a declared physiological cohort snapshot. Use shared demand/geometry definitions, unchanged temperature/domain gates and conservative rounded division to derive h, bounded0..1.
- Zero final demand gives zero ROOT signal, including fully submerged tissue. Immersion may still supply wet physiology. Invalid/nonliving/ineligible recipients get zero signal.
- Both mortality relief and growth response refer to ONE funded interval allowance, not two separately spendable credits. If different physiological stages use changed tissue/demand, their signal must remain bounded by the same allowance; a larger applicable demand reduces h. Do not reuse the amount as another physical withdrawal or as two independent full-interval water budgets.
- Credit represents water already transferred from soil to vapor. No refund, carry-forward, hidden soil/plant reservoir or double-counting in world inventory. Unused allowance expires.
- Reset credits before every column phase and after load/world reset. Bind ownership to the source cohort/slot for that step. Physiology currently precedes relocation/birth, but any future reordering must invalidate stale credit rather than transfer it to a newborn/replacement. Read/save/render must not consume or rearm it.
- Preserve law1/law2 identities and trajectories; this correction requires a separately explicit experimental law identity and actual save/restart tests before use.

## Bounded future gates

Unchanged phase state recovers old funded ratio; drying increases demand and lowers signal; wetting to zero demand yields no root signal; cold/empty/dead/replaced recipients cannot reuse credit. Assert conservatively `h*applicable_interval_demand <= actual_credit` and finite/nonnegative physical source/receiver receipts. Test endpoint/reset/new-process behavior and no credit leakage across tick/recipient boundaries. No hydrology reorder or rate tuning is implied. Implementation waits for the current fixed law2 trial checkpoint.

Geometry nuance: basal thickness uses whole projected living carbon, including allocated root/support. Density100kgC/m³ is an illustrative cohort geometry assumption, not anatomically calibrated aboveground volume. This limitation does not silently change the fixed tested contract.

# Measure gameplay without Speed dialog

Explicit opt-in10-second measurement closes the dialog and shows a small nonmodal countdown/Cancel status. It never opens a dialog on completion. A deep-copied in-memory result is shown when Speed is next opened. One retained result, no growing history, persistence, telemetry or upload. Existing live diagnostic details remain independently opt-in.

## Honest result semantics
Displayed whole-run achieved speed is (final gameTime − initial gameTime) / actual monotonic elapsed seconds /3600, in simulated hours per real second. gameTime is seconds (physics increments1440s/tick). The retained frame/physics/render/stage timings are explicitly the latest≤60-frame block from the run, NOT a10-second aggregate. Render call is not GPU time and frame intervals are not touch latency. Timer delay is included in actual elapsed time; a polling gap>2s aborts rather than calling suspension gameplay.

## Lifecycle
Start resets diagnostics, ignoring a prior sample's stale interrupted flag. A native paused/menu frame marks interruption even if the user closes it between JS polls. A volatile wrapping u32 generation changes on new world/successful load; it is not persisted or used by simulation. New/load resets diagnostics. More/Speed reopen, hidden tab, pause/native menus, speed change, unavailable/session-changed data and polling gaps cancel. Prior retained result survives cancellation or repeated starts until a new run successfully completes. Previous-world samples are labeled. Queued close/toggle events caused by starting do not accidentally stop the run. Ordinary later UI is unmeasured unless user opens live diagnostics. Explicit new-start failure stops any prior live measurement immediately.

## Passed
- Six native metric unit tests, including enable/reset/interruption and world generation.
- Deterministic JS controller tests:10.25s actual elapsed, immutable result, pause/menu/session/world/speed interruptions, polling gap, prior stale interrupted flag, repeat/cancel and prior-result preservation.
- Real production shell handlers under VM:10.5s completion, delayed close/toggle preservation, no automatic modal, reopen labels, cancel/hidden/More/paused refusal, prior-world label; all prior tests pass.
- Full WASM build passed. Final JS helper tests passed after adding polling-gap guard; final helper copied into isolated dist (same packaging step).
- Actual generated-world native callbacks exited0: enable/read/disable preserves complete8,867,927-byte save (Wyhash7bf3835fa4fd5a13) and clock exactly. Extreme finite-field metadata serializes valid1126-byte JSON into2048-byte buffer, including max u32 generation, max finite simulated time/target, large counters/context/stage timings. State restored byte-identically afterward. Existing unrelated allocator teardown warning remains.
- Final main main.zig/performance_details.zig/play.zig were compared byte-for-byte to this tested candidate and match. Root's final shader is additional; this worker did not rerun full combined shader gameplay. Parent owns final combined WASM gate.

## Limits
Actual browser visual check remains unavailable (known socket restriction); no new browser retry. Timed behavior uses clock fixtures, not an Android benchmark. The small countdown overlay still exists during gameplay; no claim that Speed was causing Todd's stalls or that this tool removes all rendering overhead.

## Reproduce final-main callback gate
STELLA_SOURCE_ROOT=<main> python3 qa/prepare.py <workspace-output>
Build <workspace-output>/main.zig using main/web/tests/egl-origin-build.zig with workspace-local prefix/cache/TMPDIR; run QA_PERFORMANCE=1 STELLA_ORIGIN_FAST=1 binary from main assets cwd. See results/native-callbacks.log. All work was isolated; no main edits by this worker.

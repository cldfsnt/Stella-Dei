# Native explicit advance candidate contract

Candidate, not deployed. Independent real-world exported/native acceptance and browser UI verification are separate gates. Controller lives in src/advance_day.zig, never save schema. No physics formula, timestep or biology change.

## Entry points
All return JSON strings:
- stella_advance_start(expected_world:u32)
- stella_advance_status()
- stella_advance_cancel(token:u32)
- stella_advance_environment(visible:i32,context_ok:i32)
- stella_advance_dismiss(token:u32)

Status: ok, available, token, world, phase(idle/running/redraw/done/cancelled), busy, running, redraw_pending, waiting_for_view, completed,total60,seconds=completed×1440,reason,paused,redraw_complete,recovery_required,recovery_save_allowed,dismissed,input_blocked,visible,context_ok. Start refusal retains old ticket and returns okfalse; it must not be mistaken for a newly completed old ticket. Tokens monotonic nonzero, no wrap.

Start requires paused Origin, matching current world, finite representable time/pace, no native menu, visible/validcontext and no existing job/latch/recovery. It never unpauses or changes requestedpace. Stops transient patchwatch and manualtransport tickets/performance measurement explicitly. Sixty unchanged1440second coupled ticks, atmostone per browsercallback. Normal simulation demand suppressed/reset. Callback world/owner/pause/pace/clock/menu mismatch or>2second/nonfinite gap cancels before further work. Completedtime and biology retained; no rollback/catch-up. Final actual render+swap precedes terminal status. No normal physics in pendingredraw.

DOM must own opaque hide-globe presentation, not depend on preserved WebGL buffer. Native mutatingexports, save/load, GLFWmouse/key and camera/UI dispatch are blocked. Readonly snapshots remain available. Successfulterminaldismiss requires exactticket; inputblocks persist until dismissed AND neutralheldleft/right/middle/W/S. Native UIcomponent states and pointer target cleared before resuming. Old pause is never restored into a changedworld. Successfulsaveapply/worldchange invalidates activejob; failedsaveapply does not.

## Permanent context-loss recovery

Genuine contextloss permanently sets recovery_required until reload. Phasecancelled,busyfalse,runningfalse,redraw_completefalse,inputblockedtrue. Contextrestored event is NOT evidence that existing renderer resources were rebuilt. advanceFrame consumes callbacks without falling through to normalrender/physics. All starts/dismissals/gameplay/loads remainblocked.

Only recovery_save_allowed permits existing stella_save path: same planetowner/world, pausedOrigin, unchangedrequestedpace and currenttime exactly start+completedticks. That path serializes/writes existing state without pumping jobs or rendering. Return0 means filesystemwrite only; shell must complete FS.syncfs(false) before durable-save claim/reload advice. Unsafecontext returns−4, writefailure−2. No ability to restore/render is claimed; completedmodel remains memory until saved/reload. If world/owner/clock changed, saferecovery-save is refused rather than writing an unrelated snapshot.

## Unit gate

10 ReleaseSafe tests pass (6 controller plus4 importedclock): exact60ticks/pause/pace/redrawbarrier, partialcancel/visibility, stale-world and paused-start atomicrefusal, backgroundgap, stickycontextloss, tokenexhaustion, explicitterminaldismiss+neutralinput, and saferecovery-save restrictions. These use mockphysics to isolate lifecycle and are not actual-engine proof. See independent nativefixture for resource/ID/fullsave parity. No claim of browser FPS or cancellation inside indivisiblephysicsstep. The benchmark-only earlier evidence supports potential optionalrender savings, not a promised completion duration.

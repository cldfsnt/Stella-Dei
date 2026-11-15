# Sampled global community status — candidate

Not a live-release claim. Native acceptance is documented below after the original candidate description.

The existing periodic goal-stage inspection now computes current positive finite, nonzero-ID colony and occupied-patch counts in the same pass. Original journey classification still uses its existing biomass>0.001 threshold. Counts include smaller positive living cohorts and are not cumulative births or arrivals. The resulting transient sample is keyed by world serial, storage identity and simulation time. Rendering only formats this fixed-size sample; no new per-frame world traversal occurs.

Before the first valid sample, across world/storage changes or rewind, the footer reads Global count pending. Observed empty populations explicitly show zero. Successful save application clears the transient sample after its validation/allocation boundary; failed apply paths do not touch it. Cache is not part of saved ecology. No-pin Watch replaces the session-counter line with Last count; pinned local inspection and the tracked-event legend are unchanged.

Unit acceptance: Zig0.13.0 ReleaseSafe, community_sample.zig1test passed, habitat_feedback.zig36tests passed (including imported existing microbial regression tests). Test commands: zig test src/community_sample.zig -O ReleaseSafe; zig test src/habitat_feedback.zig -O ReleaseSafe. Logs and source hashes correspond to this candidate. No FPS or complete-game claim.

# Actual native sampled global Watch status

Both320×700 and390×700 native EGL llvmpipe runs exit0. Preserved actual natural60-day world contains64living colonies/37occupiedpatches; the sampled HUD shows exactly that and remains legible atbothwidths. Contact sheet and individual screenshots inspected. No biological assignments; loaded real savedworld. Native browser-policy proxy, not Android/WebGL or actual screenreader proof.

Checks: before first scan pending; genuine fresh empty world records knownzero; sampleOriginCommunity records64/37; immediate serialized fullsave bytes frozen BEFORE sample+render equal separately serialized bytes afterward. Pin13596 retains local footer ‘Top mat28% · observing over0.0d’, sharebar, Details/Dismiss, rather than global status. Pin render also leaves full serialized world unchanged. Invalid radius save.apply refuses and preserves sample/fullworld; successful apply of independently parsed frozen baseline clears sample. Source sample stores runtime world/storage/time only, no savefields. Visual contexts use explicit FindLife framing before frozen parity baseline; neither framing nor selection is claimed byte-identical to unframed camera.

The helper native fixture invokes sampleOriginCommunity directly, so does not establish real-browser3second polling timing. Main's JS/native helper tests separately cover integration. No production source edits by this worker. Build source hashes and local QA save digest retained. Inherited native teardown GPA leak warning remains; no leak-clean claim.

Reproduce: egl-community-sample-prepare.py into isolated source, egl-propagule-visual-build.zig -Dsource=<copy>/main.zig, QA_PULSE_SAVE=<natural60-day60.json>, QA_COMMUNITY_PREFIX=<captureprefix>, STELLA_ORIGIN_WIDTH=320 or390, LIBGL_ALWAYS_SOFTWARE=1, STELLA_ORIGIN_COUPLED=1 STELLA_ORIGIN_FAST=1 STELLA_PRODUCER_LONG=1 STELLA_FORMS_SINGLE=1. Runtime is only fixture acceptance, not a throughput benchmark.

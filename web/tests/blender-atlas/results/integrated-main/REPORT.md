# Final integrated-main smoke

Production source includes Blender atlas, owned wind cache, and typed Fitlife
failure reasons. SHA256 manifests distinguish original source and native QA copy.
The QA copy substitutes native mobile UI/audio/event-loop support, without
changing ecology, camera algorithm, resources or renderer code.

Integration issue caught before release: regenerated atlas patch accidentally
included a reverse Fitlife typed-reason hunk. Initial combined compile failed
on missing fitLivingClusterResult. Parent restored typed reason method; atlas
archive patch now explicitly omits every Fitlife hunk. Final QA preparation
asserts method exists. This failure is not counted as a passing inventory/test.

The test loads actual saved day30 world42, pauses, selects Watch, invokes Fitlife,
compares full save state after normalizing camera only, and verifies all8 real
occupied centroid Inspect callbacks. Then it performs three actual new-world
PlayState transitions, checking atlas transient fields reset while cached GL
texture remains alive and NanoVG handle remains identical. No biological
state is injected. Viewports320x700 and800x400.

Native shutdown GPA warnings are an existing issue, not proof of no leaks.
Atlas-specific GPU ownership is checked explicitly. No real-phone performance
or browser-playback claim. Source production files are not modified by QA.

Final source also includes pace's fallible optional NanoVG registration, copied
only after renderer/play freeze. Native lifecycle fixture pumps pending normal
jobs before synchronous setState teardown. Without that native pump, an earlier
intermediate run blocked waiting for a queued job; it was stopped and not counted
as passing lifecycle proof. This is a harness adjustment, not a production fix.

## Final outcome: PASS
Both320x700 and800x400 exit0. Day30 resource/state hashc957a0149e8f9813,
8 actual living Inspect targets correct, same pause/pace/time, idempotent repeated
Fitlife. Three new-world transitions per viewport preserve identical alive GL
texture and NanoVG handle while transient atlas fields reset. Both final PNGs
reviewed:8 distinguishable visible colony patches; no toolbar/footer clipping
or apparent transparent halo. Source/test manifests and logs are alongside.

Final original source hashes (full values in SOURCE-HASHES.txt):
main0d621c0f, play7e518aef, renderer e569bee7, planet f8b4c492.

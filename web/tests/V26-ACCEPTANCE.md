# v26 render-work checkpoint

## Disabled atmosphere work
The final composite now reconstructs atmosphere rays only when atmosphere is enabled. Browser atmosphere is already disabled; bloom, animal drawing, tone mapping and framebuffer resolution are unchanged. The empty-bloom guard is not broadened.

Same-binary native checks preserve byte-identical pixels for all five maps with atmosphere on/off, visible rabbits, real HDR sun, bright-to-normal transitions and day/night changes, at 390×700 and 920×700. Model state is unchanged. A synchronized final-composite bracket shows roughly 0.6–1.5 ms less completed work on the native test driver; it changes pipeline scheduling and is not a hardware GPU timer or normal frame measurement. The effect is modest and does not explain or promise to cure the reported 68 ms mobile render call.

## Verification limits
Native software GL and fixed fixtures are not Android Brave acceptance. The two user phone screenshots show different worlds/scenes and are not a controlled comparison. Frame/submission timing includes possible driver waits. Existing unrelated native shutdown allocator warning remains disclosed. No scene quality reduction, whole-world O(1) claim, reserve migration or completed terrestrial evolution claim is made.

## Per-program uniform locations
A bounded inline cache retains at most 32 names of up to 64 bytes per linked program. Missing uniforms (-1) are cached; capacity/oversized names retain the original GL path. No allocations or global reused-handle cache. All setters borrow owned programs. Relinking clears locations. Replacement begins empty; successful reload replaces the old batch, while failed reload cleans up candidates and retains old programs. This does not implement missing WebGL context restoration.

Actual native combined shader/cache tests at 390×700 and 920×700 eliminate 416 repeated GL location queries over eight guarded frames, or 472 with active bloom, after warmup. Framebuffer pixels and full saves remain exact. Missing uniforms, relink, delete, successful reload and failed-reload rollback pass. Query reduction is not a proportional frame-time or phone speed claim.

## Actual scene and stage diagnostics
Local opt-in diagnostics now show the actual last rendered world/map, canvas/framebuffer dimensions, bloom/composite passes, daylight/camera mode and animals. Stage-call averages separate scene, postprocess and UI; terrain upload is explicitly included within scene. These are submission/wall times including driver waits, not GPU timers. No forced synchronization or quality reduction is introduced. Context is last-frame, while timing uses bounded blocks, not one synchronized snapshot.

Five helper tests, actual Origin/Sandbox/map context checks, shell validation and export bounds pass. The 2048-byte JSON buffer holds the 984-byte worst-finite fixture. WASM timer bridge was compiled, linked and executed through Node with finite nonzero readings; that is not Android graphics testing. Closing or hiding stops/resets diagnostics.

## Final combined source gate
The final current-tree shader/cache/context build passes all root JavaScript suites, two uniform helper tests, five metrics helper tests, full WASM packaging, and native guarded/active-bloom pixel, save and program-lifecycle checks. Independent context clock regression retains identical physics hashes for all requested rates, pause/reset behavior and exact save restore. Tests intentionally log malformed-shader failures to verify rollback; those expected fixture errors are not runtime failures.

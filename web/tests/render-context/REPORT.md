# Opt-in actual render context and stage-call diagnostics

Production-only patch: render-context.patch. No main edits. Applies cleanly against v25 plus current uniform aliases. Baseline files retained separately to avoid reversing unrelated work.

## What is measured
Only enabled while the existing Performance details section is open. Actual Play.render captures world/map, canvas dimensions, scene framebuffer dimensions, bloom-active flag, actual bloom/composite pass counts, daylight/orbit state, animal count and camera/planet radius. This is labeled LAST render setup, not averaged historical timing. Camera invalidity is explicit and cannot serialize NaN.

Four bounded per-window stage sums/maxima: terrain upload, scene draw, postprocess, and UI/overlays. Scene draw INCLUDES terrain upload, so the UI explicitly calls upload included; they must not be added as disjoint costs. Post timer starts after the scene framebuffer is finished and ends at Play.render return, before the main UI block. UI includes startUI, renderUI/overlays and endUI submission. Stage calls are CPU wall time including any driver waits, NOT GPU timestamps. No forced GPU synchronization or frame-quality change is added.

Timer type is compile-time selected: wasm uses existing emscripten_get_now, native uses std.time.Timer. Disabled measurement does not start timers. Samples retain the existing60-frame bounded/reset behavior; no network or save-state additions.

## Verification
- Five module unit tests pass, including disabled behavior, finite input filtering, bounded stage blocks and context reset.
- Actual worst-finite export serialization uses984 bytes of expanded2048-byte buffer and parses. Static context labels, finite camera fallback and nonnegative finite metrics bound variable content.
- Native timer smoke passes.
- Actual wasm32-emscripten timer object compiled, linked with emcc and executed through Node WASM;10 finite/nonnegative nonzero readings confirm clock bridge operation. This is clock validation, not browser graphics performance.
- Native actual scene smoke exit0: Origin Normal stable orbit reports390×700 canvas/scene and0 bloom passes; Sandbox rabbit reports5 passes and1 animal; Temperature label updates. Every stage records positive call time. JSON snapshot parses with context and stages. Closing diagnostics resets/stops metrics/context.
- Shell validation accepts correct metadata, labels inclusive upload, and rejects invalid dimensions, bloom counts and NaN values; legacy snapshots can show a waiting/unavailable context without inventing data.

Failed intermediate QA logs retained: first preparer followed a symlink and copied baseline performance module; local copied preparation chain fixed it. Second native link exposed unused union browser branch; final compile-time clock type removes that native reference while preserving working WASM bridge. Existing unrelated native allocator shutdown warning remains.

No claims are made about the unseen guard/map/camera in the phone screenshot. This patch supplies that missing evidence. Stage timings can overlap driver waits and must not be interpreted as separate GPU costs.

Final supplemental clock/save smoke also exits0: all three speed targets retain physical hash d523353839672a4; actual pause/rate/background/menu/load callbacks and invalid-save/no-mutation/exact restore pass (8,734,640 bytes). Native and WASM clock/serialization fixtures remain separate from timing claims. Final module tests rerun after compile-time clock selection: all5 pass.

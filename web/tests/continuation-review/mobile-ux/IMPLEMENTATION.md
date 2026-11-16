# Mobile navigation implementation checkpoint

Isolated tree: `site-tmp/mobile-ux`, copied from final unified-ui web and unified-game native source. No Site, physics, schema or saved-namespace changes.

One dock: Play/Pause, Speed, Seed, God, Stats, World. Uniform bottom sheets replace the hidden group tabs and independent header. Actual resource/token/save/import controllers keep their element identities. Native bridge ownership is separate, transient and independently tested; standalone native UI remains available.

Primary God water/terrain/heat/fire/wave actions are direct. Explicit brush chip has Explore cancellation, not a second toolbar. Native state determines pause/tool status; changing sheets does not silently change the selected brush. Insets derive from actual visible overlays and dock safe-area height. Native feedback is surfaced as temporary HTML notice.

One modal at a time. Cancellation runs synchronously before hiding; stale asynchronous close events cannot cancel a newly reopened plan. Busy storage keeps its sheet visible. World import cancellation is requested on dismiss. Advance cannot be replaced/dismissed by ordinary navigation. Exact confirmations remain in the existing controllers.

Visible Stats retains sampled population and observed births/deaths/window or unavailable warmup; detail prose folds. World local-save/no-cloud warning stays visible, laws/help fold. Old saved worlds retain rules; no automatic conversion or save is introduced.

Verification: 222 existing frontend tests pass;10 navigation/modal tests pass. First regression failure retained: missing isolated build dependencies and intentionally changed native rabbit bottom-bound assertion, repaired without removing rendering checks. Real browser DOM review is documented separately; native rendering/API and final compiled artifact gates remain pending at this checkpoint.

Final frontend gate:232/232tests (222preserved regression +10actual navigation/modal-wrapper tests). Designer and storage reviewer independently accepted synchronous cancellation, busy Close/Escape and delayed reopen protection. World Advanced exposes existing native settings with Save-first warning, preserving Sandbox route rather than removing it. Persistent dock uses static translucent fill/border, no continuous animation or backdrop blur.

Final reachability audit restored all existing tool routes0–6: Explore0; God Water±1/2, Raise/Lower5/6; Origin Seed→Choose seed patch3 preserves actual green target hints; Sandbox Seed→Plants3/Rabbits4; Origin God→Nutrients4. Mode-specific buttons reread actual mode and world before dispatch and refuse stale/unknown labels after load. No new tool semantics. Final suite233/233 (222existing +11focused). A completed pre-whitelist build is retained as superseded and is not the final release artifact.

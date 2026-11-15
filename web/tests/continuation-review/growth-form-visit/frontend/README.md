# Final growth-form visitor frontend gate

Both final built artifacts passed actual Node-instantiated Emscripten Module checks: `_stella_visit_growth_form` is exported and returns -1 before world initialization. Wetlands additionally retains both factory/snapshot exports, unavailable snapshot and factory refusal. No game world was initialized or mutated by this export check.

The exact minified outer-HTML controller was executed with DOM mocks for each artifact: six rows, zero-count disabled, sampled world/form arguments [42,2], successful navigation messaging/close, stale refusal without close, and collapsed-panel cancellation. This is **outerHTML mock interaction proof, not an actual browser layout/render or WebGL gameplay test**. `world-ecology.js` is byte-identical between source and both artifacts. Full source frontend suite: 116 tests passed.

Harness-only initial failures were retained here as a description: quoted-id regex rejected valid unquoted minified attributes; minifier moved event registrations after the named function; expanding extraction exposed a mock addEventListener that overwrote dialog.close; source visibility listener required a document listener mock. Corrected harness only. Both final artifact runs then passed. No game artifact was altered to satisfy the harness.

Namespace/disclosure assertions passed: main retains /saves; preview has only /wetlands-saves, isolated welcome key, bottom:auto and closed-visible disclosure CSS, and controller loads before its mount. Both contain visibility-change census cancellation (minifier relocates this listener). No live Site changes, GPU retries or device-performance claims.

`hashes.json` records raw build inputs before release-owner label/link-only packaging. Subsequent published HTML hashes must be recorded separately; WASM/controller hashes remain authoritative here. Native current-cohort/picking/full-state acceptance is separate evidence 7f2d420, not inferred from these mocks.

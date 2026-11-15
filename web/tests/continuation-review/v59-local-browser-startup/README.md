# Actual local cloud-browser startup check

2026-11-15 about11:51UTC. This is an observed real browser attempt, not native EGL or the mock habitat fixture.

An existing Chrome tab at localhost4173/habitat-fixture was explicitly MOCK responses only. CLI loopback4187 and a separately attached worker4188 returned ERR_CONNECTION_REFUSED in Chrome despite retained CLI sessions; those servers were stopped. This was connection isolation, not bot detection, and no network/security settings or private Site authentication was changed.

Through the documented native terminal UI, the authorized local web/dist path was verified and Python's standard HTTP server was started on127.0.0.1:4189 only. Chrome tab12 loaded the actual page: Ready. Tap Play to start. Clicking Play changed the page to Reload to try again and Startup failed. Diagnostics showed Audio memory bridge ready; WASM ready; error: WindowCreationFailed twice. Browser console independently showed the same application error. This establishes successful local serving/WASM load and failed graphics-window startup, not its cause. No browser gameplay, successful rendering, device performance or user-device reproduction is claimed.

Both local index.wasm and index.js match the saved v59 deployment archive byte-for-byte (hashes in provenance.json). The source commit for that archive is b079fc14781c05cca62b02610e28d1e348fc76ff. Local shell is the existing web/dist shell; no experimental liquid/root code was served.

Private host remains v59 and unchanged. Native-terminal loopback server remains available for the next bounded context-creation diagnostic. No extra retry, browser flags, permissions, auth bypass or public exposure was attempted. Local browser tab12 was retained as observed failure evidence; no user handoff requested.

## Independent context creation controls

A separate local-only diagnostic page from aa0393f was opened in Chrome tab13 and all four buttons clicked once. Matching game WebGL2 options, default WebGL2, default WebGL1 and minimum-buffer WebGL2 all returned null with GL_VENDOR=Disabled, GL_RENDERER=Disabled and BindToCurrentSequence failed. Exact displayed error/results are transcribed in observed-context-results.json. Thus inability to create graphics contexts is independently reproduced in this cloud browser, without game code. This does not establish why its GPU/context service is disabled, nor imply failure on Todd's device. No permissions, flags, drivers or security settings changed. Stop repeated startup attempts here; retain native/standalone-WASM limitations.

The local diagnostic is NOT part of the release manifest and must not be published accidentally from web/dist. Native terminal server at4189 is still available for controlled follow-up; no public exposure.

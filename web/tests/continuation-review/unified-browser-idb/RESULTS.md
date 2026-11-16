# Real browser IndexedDB integration check

2026-11-16 UTC. Supported `sites-preview` served the isolated QA at http://127.0.0.1:4173/. Chrome CUA clicked **Run real IndexedDB tests**, then **Reload and verify durable results**. Both reported PASS.

Run namespace: `stella-unified-idb-qa-dee8e8ad-7a00-4f92-aec2-115e6dd0b9e0`. All databases were fresh QA-prefixed names; real game saves were never addressed.

Verified real IndexedDB readonly legacy discovery/export; abort on absent database upgrade without creating that database; actual controller cancellation; exact source bytes including maximum-u64 value; durable current checkpoint before mocked native apply; unchanged source and canonical saved world; all durable expectations again after browser page reload. Event order: mount-canonical, populate, stella_recovery_prepare, sync, stella_recovery_apply, stella_recovery_cancel.

Source bytes: `{"version":11,"seed":18446744073709551615,"id":"18446744073709551615"}`.
Canonical bytes: `{"version":13,"name":"saved old world"}`.
Current checkpoint SHA256: `dbefcc4294424354d29be6d90eb4e614cf26774c28ae6a35e2c54ffc13263764`.
Source SHA256: `2f2d6de75da01334087ae57cd8551fd584638074176d8d96816d51ed1845e8d7`.

Limitations: native world apply is explicitly mocked in this browser harness; separate actual native transition tests establish engine behavior. WebGL2 was freshly tested in the cloud browser and failed with GL_VENDOR/GL_RENDERER Disabled and BindToCurrentSequence failed. This is not browser-rendered gameplay, Android/laptop performance, or a full Emscripten startup claim. Screenshot output exceeded tool context; no screenshot artifact is claimed.

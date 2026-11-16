# Independent unified storage acceptance

Controller checkpoint: 5d28346. Eleven Node adversarial tests pass. The fixture uses real asynchronous promises, microtasks and SHA-256 but mocked IndexedDB, Emscripten FS and native exports. This is not a browser IDBFS or native schema acceptance claim.

Covered: read-only legacy discovery without mounting or upgrading legacy databases; byte-exact export including integers above JS safe range; absent database abort; successful Wind11 import preserves original source and canonical bytes while durably staging the exact hash-addressed backup; repeated import, Save and Load refuse while busy; cancellation, hidden page, stale world and changed source during checkpoint prevent native apply; unknown12/16 refuse; failed Save prevents destructive populating Load/import; quota failure after serialization leaves unsynced RAM distinct from intact durable original, and successful Save retry commits it.

Source audit identified an owned-lock release gap in nested recovery. The owner fixed inner `finally` to release only unowned locks. The independent microtask test verifies Save cannot enter between nested recovery completion and outer import completion. The first retained log is a QA fixture setup failure (Node crypto getter), not a reproduction of the former controller bug.

Missing-database handle cleanup was suggested to owner; absence test proves no database creation, not close-event cleanup. Canonical-present startup UX, real schema validation, actual native recovery and cross-tab browser behavior remain separate gates.

Run: `node --test web/tests/unified-storage-independent.test.cjs`.

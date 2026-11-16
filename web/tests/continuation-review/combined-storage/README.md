# Combined Wetlands storage boundary (isolated frontend candidate)

Owned source: web/combined-storage.js. Adapted from reviewed wind-storage, but all file/mount/backup access is exclusively /wetlands-saves. No root/Wind fallback or automatic world conversion/reset. Every save requires readWriterIdentity and native stella_save_expected(world,writer), allowing actual writers7/8/9/10/13 only; missing guarded API never falls back to stella_save.

Before a13 write, the latest saved bytes with a bounded recognized version1..10 are preserved, not an unrelated earlier classic save. First immutable world.pre-v13.json is retained; a distinct later oldsave gets world.pre-v13.sha256-<exact bytes digest>.json. Existing hash path must match exactly. Temp and renamed destination are read back before durable sync; destination is checked again afterward. Unknown/opaque/11/12 inputs, missing/invalid hash, corrupt files, quota/read/write errors, changed world/writer or changed prior bytes refuse before native serialization. Matching RAM-only backups are always resynced. Existing pre-v7 backup policy is retained and never reused as pre-v13 permission. Current13 repeats need no new pre13 backup. No cleanup or restore UI is claimed.

19 focused tests pass using an actual asynchronous mockedFS with independent RAM/durable maps, read/write/rename corruption and sync failures. Coverage includes all historical writer versions, latest-byte protection, second distinct backup/dedup/collision, quota retry, hash failure, async identity/byte changes, native-6 wrong-writer rejection, loaded13/normal repeat saves, namespace isolation and real Combined.create fresh flow. Corrupt write, quota and native-6 all leave factory count0 and prior durable bytes unchanged; cancellation performs neither save nor reset.

This is mocked browser-storage correctness, not IndexedDB/device/browser-render proof. Native public guarded writer contract is separately tested by native owner97f3b78. Storage state reports combinedBackup; callers must supply authoritative readWriterIdentity from stella_combined_snapshot. Existing createStorage callers without it must be adapted, not silently allowed to use unguarded writing.

No copied shell, native source, build or deployment changed by this worker. Source tests run with node --test web/tests/combined-storage.test.cjs and use parent-owned web/combined-world.js only for integration checks.

## Copied legacy regression adapters
`prepare-combined-storage-regressions.py` adapts only root-wind-ui/web/tests/{storage,storage-upgrade,save-size-safety}.test.cjs. All original assertions retained. Supported current writers forward `_stella_save_expected` to the original mock native behavior with explicit expected world/writer assertions and authoritative identity. Historical writer6 cases cannot truthfully test combined (minimum writer7), so those three cases explicitly load unchanged original stella-storage.js, with only a mock FS namespace proxy. They are labeled LEGACY-REFERENCE ONLY in logs; source SHA is recorded in legacy-reference.json. This is not reported as combined writer6 support. All three copied suites pass.

The module now skips the asynchronous pre-v13 helper altogether for writers other than13, preserving ordinary historical save scheduling while retaining expected-writer and exact prior-byte checks. All19 focused combined tests still pass. Copying the final module into the isolated test tree was required to exercise the final implementation; no shell/controller edits were made.

### Explicit incompatible-preview rejection

The load path now reads only the saved version header after storage population and before calling the native loader. Version 11 is named as standalone Wind and version 12 as research preview; the message directs use of the original preview and states that the current world is unchanged. The same explicit explanation precedes a refused pre-v13 write. No import conversion, reset, deletion, or automatic navigation is attempted. Unknown other headers still go through native load validation.

All 21 focused tests and all three copied regression suites pass. Added tests verify zero native load/save/factory calls, unchanged current writer identity and saved bytes for both rejected versions. Copied `stella-storage.js`, `combined-storage.js`, and the focused test mirror this exact source. This remains mocked-FS evidence, not browser rendering or actual IndexedDB proof.

### Readable version6 is not writer6

A new focused test exercises the actual combined storage module (not the legacy reference) with version6 bytes: Load invokes the native loader once and succeeds, without a reset or write. A following current-writer7 Save waits for the exact version6 pre-v7 backup to sync, then calls the guarded writer7. The durable backup retains the exact original bytes. All22 focused tests pass. This proves the frontend storage routing and backup contract using mocked native/FS operations; actual native schema compatibility is a separate native gate. Only the candidate test was copied; built artifact source was not changed.

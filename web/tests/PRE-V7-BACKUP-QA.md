# Browser pre-v7 save protection

Isolated storage-module patch, not yet activated in a production shell.

## Activation

Only the v7 candidate should call:

```js
createStellaStorage(Module, feedback, {targetSchemaVersion: 7})
```

Default/v6 callers retain their old behavior. This patch deliberately does not infer schema version from deployment labels or hardwire an upgrade into every future caller.

## Safety sequence

Before a v7 save can call the native serializer, the module checks at most 256 bytes of the existing file's header. A confidently v7 file needs no legacy backup. Any legacy/unknown/nonstandard header is preserved conservatively as exact bytes in `world.pre-v7.json`. It writes a temporary file then renames it, and awaits successful `syncfs(false)` before native serialization may overwrite the canonical save.

An existing backup is never replaced. It must be readable and must be successfully synced by this instance before it is trusted. A backup left in memory by a failed sync does not authorize an overwrite on retry. Backup failures abort before the native writer and explicitly report that the previous save was not replaced. The normal busy/storage-operation gate spans backup and world-save syncs.

The returned state includes backup status, durability, and known legacy version (null for unknown headers). Success feedback explains that the backup is local to this browser and that automatic restore is unavailable. No restore UI, import/export, cloud backup or automatic rollback is provided. A game-code rollback does not make v7 bytes loadable in v6; restoring the retained pre-upgrade file requires a separate explicit validated restore workflow.

## Verified

- Existing `storage.test.cjs` passes unchanged: initialize, busy dedup, save durability feedback, quota/serialization/load errors and unavailable storage.
- New `storage-upgrade.test.cjs` passes: exact byte preservation, backup sync before serialization, immutable later backups, retry after quota failure, existing backup sync, v7/new-world skips, v6 opt-out, bounded unknown/opaque headers, read/write errors, final-save quota failure, invalid load without restore, and state snapshot immutability.
- Tests use a deterministic in-memory FS/durable-store mock. Actual browser IDBFS integration remains a candidate release check.
- The isolated lab's unrelated `shell.test.cjs` currently fails an existing CSS regex expecting `origin-starter` max-height 130px. That test stubs storage rather than importing this module; no shell or CSS files were edited in this task.

## Concurrency boundary

This preserves the existing single-instance busy gate. It does not add an origin-wide multi-tab lock; IDBFS was not previously a safe concurrent multi-tab writer. Do not claim cross-tab atomic backup creation or cloud durability. Origin Web Locks and a separate restore/export flow are possible later bounded changes.

## v20 schema-6 climate preservation opt-in

Use `createStellaStorage(Module, feedback, {preserveLegacyThroughVersion:6})`
for a climate update that still writes schema 6. This protects existing <=6 or
unknown-header bytes once, using the same stable `world.pre-v7.json` backup
filename. The filename is historical, not a claim that runtime schema is 7.
The prior `{targetSchemaVersion:7}` option maps to the same boundary. Known
versions above 6 need no legacy backup. No automatic restore is added.
Tests cover both existing v6 and unknown bytes, durable-before-overwrite ordering,
continued v6 serialization, and immutable backup on a second v6 save.

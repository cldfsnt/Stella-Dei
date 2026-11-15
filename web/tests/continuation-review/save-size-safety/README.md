# Bounded production save-file safety candidate

## Why

The production reader accepts at most128MiB, but the previous writer could replace `world.json` with a larger valid JSON file that the reader subsequently refuses. The experimental hydration schema audit demonstrated the **existing v6** legal dense maximum-grid cohort payload alone can exceed this limit. This fix does not promote hydration or change schema/version/biology.

## Change

- `save_io.max_save_bytes` is the single128MiB read/write limit.
- A streaming byte-budget adapter wraps the buffered file writer. It rejects an over-budget write with `SaveTooLarge` before accepting those bytes; subtraction avoids integer overflow.
- Serialization and flush must finish before closing/renaming the temporary file. On serialization, size, flush or rename failure, the file closes and bounded temporary cleanup is attempted. The existing canonical path is never renamed/replaced on refusal.
- No duplicate whole-world JSON allocation is added. Existing capture allocations and browser backups remain unchanged. Cleanup is best-effort if filesystem deletion itself fails; any leftover temporary is bounded by the limit.
- Both regular and graphics-context recovery save exports return−5 for oversize,−2 for other serialization/I/O failures. Storage feedback and the recovery overlay explicitly say the previous save was not replaced and current progress remains only in memory. No automatic reload, shrink, resampling, or save migration.
- A successful native write is still not browser durability: existing `FS.syncfs(false)` completion remains required. A backup may be synchronized before a refused canonical write under the existing legacy backup policy.

## Gates

-5/5 ReleaseSafe native helper tests: exact boundary and normal-byte parity (including UTF8/escaping); overflow and zero budget; partial sink failure without overcount; old canonical retained/temp removed on overflow; successful exact-limit replacement/read; opening and rename failures; injected partial serialization output failure with canonical preservation and cleanup.
-66/66 existing/new Node test files pass. New checks distinguish oversized vs generic failure, no post-refusal durability sync, cleared error on subsequent success, both native export mappings and recovery inline message dependency.
- Actual saved-world native export gate is delegated independently and pending at this checkpoint. No browser IndexedDB failure/Android hardware claim.
- Initial fifth-test compile failure retained: arbitrary injected error was outside Zig JSON's declared output error set. Corrected test injection to the supported `InputOutput` error; production code unchanged.

## Reproduce

```
$ZIG test src/save_io.zig -O ReleaseSafe
node --test web/tests/*.test.cjs
```

Production schema remains6. Existing saves are read unchanged; only explicit Save invokes bounded serialization. Oversized saves cannot be made loadable merely by changing a UI message; the refusal deliberately preserves the previous usable save instead.

# Experimental hydration version-7 serialization gate

## Scope and result

**103/103 ReleaseSafe native tests pass. Production remains version 6 and unchanged.** This is a generated experimental copy of the real `save_schema.zig`, using a frozen copy of the lifecycle worker's current types/functions. It is not a deployed format, native `save_game.apply` integration, browser persistence proof, or approval of the developing physiology.

Contract: cohort `retention_allocation:f32=0`, `stored_water:f64=0`; cell `liquid_return:f64=0`, `vapor_return:f64=0`. Water and return pools are kg/m²; returns are nonhydrating. Mutation is not introduced by this fixture. Source hashes are in `provenance.json`; the frozen imported core avoids racing later worker edits.

## Verified

- Old v2–v6 missing hydration fields parse to exact zeros. v2 keeps its two-slot wire shape and pads runtime to four slots. Old IDs, tissue, resources and RNG remain unchanged.
- Nonzero new trait or return pools disguised under an old version are rejected. The same version guard covers stored water. Existing legacy-feature and invalid sparse index/duplicate tests remain intact.
- `SavedCell.capture`, custom JSON writer, `runtime`, and `captureSparse` all preserve both return pools and cohort water. Sparse empty escrow-only cells survive roundtrip without inventing a cohort. Zero return keys are omitted from JSON.
- NaN reserve, out-of-range allocation, overcapacity reserve, dead biomass with reserve, negative/infinite escrows and negative reserve reject before the **experimental validate-then-assignment** destination changes. This is not actual native save-apply failure/allocator coverage.
- Parsing a legacy v6 document leaves its version and original input bytes unchanged. Production read/load source remains read/parse/apply only; no real saved file was opened for writing.
- Existing full schema and imported core regression tests run too; their inclusion is regression support, not proof of new lifecycle correctness.

## Sizes and explicit limits

- Native measured Cohort96B, Cell416B. Relative to production80/336, +80B/cell: 3,276,960B at40,962 and13,107,360B at163,842. This excludes parse/capture/backup/pending-preview copies; WASM layout and browser peak remain unmeasured.
- Four long-ID/large-field cohort payload fixture:1,894 bytes,6,298 bytes below the8,192-byte Life buffer. **Payload only:** no integrated envelope/export test or mathematical maximum proof.
- A valid four-occupied-cohort cell serializes to1,601 old bytes vs1,900 proposed bytes. At163,842 cells, the cell-array-only lower bounds are262,474,884 old bytes vs311,463,642 new bytes (+48,988,758), before climate arrays and envelope. Even existing format exceeds128MiB for this legal dense population. This is a measured counterexample, not a worst-case bound; sparse encoding cannot eliminate genuinely occupied cohorts.
- Existing `save_game.write` streams to temporary file then renames, with no128MiB size check. Existing `read` caps at128MiB. **Inherited write/read asymmetry remains unresolved.** Before integration, add an explicit bounded/counting writer or coherent revised format/limit with atomic refusal before replacing the canonical save, and test allocation/stream failures. Do not shorten valid state to pass a size gate.
- Existing sparse40k saves are not rewritten. Futurev7 must retain the old file until explicit Save, retain durable legacy backup semantics, and disclose that an older build may not read newer saves. An actual old-file preservation/backup failure gate remains required at native integration.

## Reproduce

From repo root:

```
python3 web/tests/prepare-hydration-schema.py
$ZIG build --build-file web/tests/lifecycle-build.zig --cache-dir "$ABSOLUTE_QA_CACHE" -Dsource=src/qa_hydration_schema.zig --summary all
```

Generator reads the current lifecycle experiment; rerunning updates its frozen provenance, so compare hashes before attributing a result to this checkpoint. No main/build/save_game production edits. Initial harness failures retained: relative build cache resolved twice; a truncated frozen core omitted helper definitions below its tests. Both were fixture construction issues, corrected by absolute cache and full frozen copy, not by weakening checks.

## Remaining gates

Actual lifecycle zero-water/RNG parity; all donor-funded water fates; real area-scaled hydrology totals and rounding; inherited allocation stream; actualv7 native save/load/failedapply/backup/oldformat rollback and maximum-size refusal; full Life envelope+WASM layout/peak. Do not claim land adaptation or completed migration from this schema fixture.

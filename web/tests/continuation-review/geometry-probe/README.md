# Exact terrain-upload cache: research and unapplied candidate

Status: isolated native proxy accepted; production patch NOT applied. Four cache-module unit tests pass and `git apply --check` passed against the sparse-index checkout. The proposed production wrapper adds defensive keys and allocation fallback beyond the tested prototype; an integrated build and review remain required before shipping.

## Method and limits

Real engine, generated natural 30-day QA save and early seeded world, 40,962 cells, 1366×768 EGL llvmpipe. Actual pre-pump/update/post-pump/render/finish ordering. This is neither an Android/browser test nor a hardware laptop GPU benchmark. Fixed frame delta does not establish achieved browser simulation pace. See laptop-render provenance and preparer for cache/source validation.

The initial baseline/candidate logs retained a native-only atmosphere upload. Corrected browser-policy runs omit that block because production WASM already omits it. Do not attribute its removal to the candidate.

`browser-baseline` and `browser-candidate` are preserved failed QA runs: the obsolete assertion compared the padding of a 16-byte three-float vector. `browser-check-*` correctly compare the three float components, not undefined padding. No failed run is acceptance evidence.

## Accepted prototype results

24 invalidation cases (12 each early/cached30d): Normal/Wind/Temperature/WaterVapor/Rainfall/Normal mode sequence, actual raise/lower controls, tilt change, queued normal work followed by two edits, queued work followed by load, and same-geometry reload. Every settled cell normal matches fresh calculation component-bitwise. All 24 complete saved-world hashes match baseline. All 30 settled images (24 cases plus 6 pace scenes) match byte-for-byte. Image hashes and case comparisons are in parity.json; bulky PPMs stay local.

Unchanged frames transfer 491,544 instead of 1,474,632 subdata bytes: exactly 983,088 fewer bytes, without geometry/graphics reduction. Dynamic attributes are still uploaded. Normal work is requested for changed geometry rather than every tenth unchanged upload.

Timing is noisy and does NOT prove a guaranteed speedup. Corrected cached30d total frame milliseconds, baseline/candidate: paused 19.9922/20.7282; Grow 24.3742/21.3554; target24 33.5666/31.1982. Host outliers included a 217.99ms baseline update. Earlier paired research suggested modest 1–2ms gains, not a dramatic fix. Retain exact-work reduction as the defensible result.

## Candidate design and review notes

`production-candidate.patch` is narrow and includes a new `src/terrain_upload_cache.zig`; it must not replace the whole Planet file. It was generated against the parent's sparse-index modifications. Recheck application before applying.

- Only WASM uses cache observation; native uses the unchanged legacy path and allocates no snapshot.
- Arena-owned independent elevation snapshot costs 4 bytes/cell: 163,848 bytes (~160KiB) here. It is not serialized. Wind may overwrite bufData, so that scratch buffer cannot be the snapshot.
- Exact O(N) byte comparison plus tilt/radius bits, immutable-topology pointer and destination VBO identity. This is not an O(1) simulation claim.
- Changed geometry requests the existing cooperative normal job. Its completion marks normals dirty, ensuring a second upload even if elevations are unchanged. Queued edit/load behavior is tested in the cooperative single-thread browser scheduling proxy; no new worker concurrency is introduced.
- Allocation failure or unexpected length change disables caching and retains legacy upload/scheduling behavior, with no allocation retry storm. All dynamic temperature/water/vegetation/Wind work is unchanged.
- Empty/failed cache falls back; changed values including signed zero invalidate. Topology vertices are immutable during a Planet's lifetime; pointer key covers replacement.
- Existing native harness allocator teardown warnings remain; this is not a clean whole-game leak certification.

No production promotion, push, or deployment was performed by this worker.

# v45 integrated terrain-upload cache acceptance: HOLD

No production change. The actual previously proposed `terrain_upload_cache.zig` module and production patch were applied only inside the generated source copy. The browser architecture gate was replaced by a runtime environment toggle solely for same-binary native A/B. This tests the candidate's actual allocation fallback/key/dirty wrapper, not the earlier simplified prototype.

Native browser-policy EGL llvmpipe at 1366×768 / 40,962 cells. Cooperatively pumped jobs, current v45 source, frozen early and natural30day QA saves. It is not Android, browser WASM or Todd's laptop GPU. No user saves involved. Source hashes explicitly record allowed QA checkpoint differences (diagnostics/pulse observation/label/sparse traversal changes); unmatched engine hashes fail preparation.

## Correctness
- 24 invalidation cases match full saved states and fresh normals component-bitwise: map switching including Wind scratch reuse, raise/lower, tilt, queued edits, queued load, same load, on both early and30day worlds.
- All30 settled PPMs match byte-for-byte (hashes in results.json; bulky files local).
- All18 complete saved-state hashes match across three paired timing runs.
- UI and mesh quality unchanged; biology/RNG/order unchanged. Terrain subdata remains exactly983,088 bytes/frame smaller on unchanged geometry (1,474,632→491,544).
- Initial build failed because old QA helper used prototype `.qa_valid`; helper was corrected to `.terrainUploadCache.valid`. Preserved failed build is obsolete fixture evidence, not an accepted production failure.

## Timing: no robust general benefit

Three paired runs, alternating order for second pair;12 warmups/60frames per pace. Total-frame medians in ms, baseline→candidate:

| World | Paused | Grow6 target |24 target |
|---|---:|---:|---:|
| Early |15.689→15.583|19.141→17.365|26.422→25.485|
| Natural30day |16.950→17.171|19.945→20.014|28.367→28.564|

Established render+finish medians are also slightly worse:16.808→17.170,17.270→17.509,18.165→18.523ms. These small differences are within host timing variability, not proof of regression; neither do they demonstrate a dependable gain. Exact work avoided is real, but this proxy does not justify shipping160KiB of extra snapshot storage and invalidation complexity for a broad speedup claim.

Recommendation: HOLD candidate. Existing geometry proof remains useful if actual browser/device telemetry later identifies upload/normal-job overhead. Do not claim an optimization was deployed, that all runtime normal timing is pixel-identical during edits (screenshots are settled), or that native tests establish device gains. Existing allocator teardown warnings persist; no whole-game leak certification.

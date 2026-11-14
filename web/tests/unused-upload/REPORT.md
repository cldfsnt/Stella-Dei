# Avoid rebuilding/streaming unused browser atmosphere geometry

## Narrow scope and consumer proof
Production patch changes one existing block guard in Planet.upload: execute atmosphereMesh buffer rebuild/upload only on non-wasm targets. Browser Play.renderScene already never calls renderWater. Repository reference scan finds atmosphereMesh only in Planet generation, this upload, renderWater and teardown; no physics, save, input or other draw consumer. Native keeps the original upload and renderWater path. Resource generation and teardown remain unchanged. No quality/resolution reduction, no new memory or geometry cache.

The shared bufData array is scratch for uploads only; all terrain position/normal and map/vegetation values are overwritten/uploaded before the omitted block. transformedPoints and normals are still updated. The omission changes no physics or saved state. Subsequent rendering binds its own VAOs/buffers; paired actual pixels verify no lost binding side effect.

Avoided per rendered frame: one glBufferData and 4-float rebuild per atmosphere vertex. Exactly655,392 bytes at40,962 points;2,621,472 bytes at163,842 points. This is avoided streaming, not released GPU allocation or reduced simulation memory.

## Initial native correctness/performance
Native browser-style same-binary toggles pass all5 maps with atmosphere shader off/on, a visibly rendered rabbit, HDR sun peak9.96875, bright return/day-night transitions, and full serialized state unchanged. This forced atmosphere shader test does not claim native cloud-mesh draw testing; production native guard still always executes original code.

Four-second ABBA windows at390×700:
- Original medians15.34/14.93ms vs skipped14.15/14.33ms.
- Original unused block call averaged0.161/0.170ms; skipped counters are exactly zero uploads/bytes.
- Original maxima142.26/106.75ms vs skipped110.17/98.87ms in this run only.
Native llvmpipe timings are noisy and cannot establish Android gain or consistent tail improvement. Total-frame changes exceed directly measured block cost; do not attribute all of that difference causally. This is not a demonstrated solution to a68ms render-call stall. Actual device stage diagnostics will identify whether upload contributes materially.

## Completed regression and wider repeat
Actual clock/save run with skip enabled exits0. All three targets retain six-tick physical hash d523353839672a4; pause/rate/background/menu/load invariants and invalid-save/no-mutation/exact restore pass (8,734,640 bytes).

At920×700, all paired pixels/model checks again pass. Four-second ABBA original medians27.45/28.47ms vs skipped26.57/28.28ms. Original p9536.38/42.71ms vs skipped37.33/43.47ms; original maxima114.95/67.36ms vs skipped93.67/141.25ms. This wider repeat does NOT establish tail improvement. Original block call averaged0.299/0.128ms; skip remains zero calls/bytes. Existing allocator shutdown warning remains unrelated.

Recommendation: safe, narrowly justified removal of unused browser work, worth a later checkpoint after integrated/WASM validation. Treat the reduced buffer streaming as the firm result; actual phone performance benefit remains unverified. Do not fold it into v26 before its independent acceptance if that delays the completed milestone. Main unchanged, no deployment.

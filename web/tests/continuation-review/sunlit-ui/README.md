# Sunlit / Deep nursery UI candidate

Sunlit is the primary starter choice. Existing native prepare API preserves 0=Pond and 1=Deep nursery; additive 2=Sunlit nursery returns kind sunlit_nursery. No export signature, save format, automatic world edit or seeding changes.

Sunlit requires 5 m center and neighboring floor; Deep requires 5 m center and 15 m neighboring floor. Both retain bounded actual footprint and dry raised rim risk. Dialog explicitly offers each preview, says Sunlit trades a smaller water buffer for more light, and does not guarantee growth. Changes require paused Origin and a fresh one-use explicit Apply. Switching shape revalidates the original cell AND world; it cannot silently bind a different loaded planet with the same cell. Existing status/stale/context/visibility/close/load/advance guards remain.

68 full JavaScript tests pass, including both shapes, legacy boolean call compatibility, no automatic application or seed, exact receipt shape/depth validation, and same-cell/new-world refusal. Malformed/changed execute receipts remain unknown rather than falsely claiming failure. Tests do not prove browser graphics or device behavior.

Mock fixture: run prepare-habitat-ui-fixture.py with destination and this directory's mock-native.js. It uses actual shell/controller files with an explicit UI FIXTURE ONLY banner and 358 px panel. It does not simulate a world. Browser review, if performed, is reported separately by coordinator. The old habitat-ui historical mock is preserved unchanged.

Native action/Plan tests and natural-world comparison belong to the native owner; one fixed trial is not a universal ecological benefit or evolution claim. Combined release build is recorded separately once complete. No deployment by this worker.

Final combined pinned-toolchain WASM build exits0 (atmosphere cleanup plus native Sunlit and final shell). Final full JS68/68 passes. Independent UI review caught stale Find habitat guidance; corrected to Sunlit5m / optional Deep15m and asserted. First added assertion was outside its async fixture scope and failed ReferenceError; preserved log, moved inside the existing fixture, all assertions retained. No application defect inferred from that setup failure.

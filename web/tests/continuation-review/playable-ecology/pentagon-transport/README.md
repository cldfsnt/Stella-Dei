# Pentagon transport destination fix

Native options previously emitted self-padding from pentagonal Planet adjacency. The unchanged browser validator rejects self-neighbors, so one such entry invalidated the whole panel. Actual 40,962-cell graph has 12 self-padded rows. Read-only reproduction: row 0 raw options invalid; its five real neighbors valid.

`manual_transport.options` now skips self and out-of-range indices, and deduplicates while preserving first occurrence. No model, save schema, RNG or transfer semantics change. Browser validation remains strict.

Validation: ReleaseSafe new native QA 35 tests pass; existing session QA 56 pass; colony-transport JS 12 pass. Native cases use exact actual graph rows 0 and 12, verify five/six ordered destinations, duplicate/invalid/all-self handling, complete cohort/RNG and environment/state preservation. These are focused native mocks of the actual options API and JS controller tests, not browser gameplay or full Planet rendering tests.

Reproduce: `zig test src/qa_transport_neighbors.zig -O ReleaseSafe`; `zig test src/qa_manual_transport_session.zig -O ReleaseSafe`; `node --test web/tests/colony-transport.test.cjs`.

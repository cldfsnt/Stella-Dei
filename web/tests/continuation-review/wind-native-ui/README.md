# Isolated wind public native candidate (not published)

Reapply `wind-native-ui-prepare.py <copied-root>` once after the frozen wind-core preparer. Only copied main/Play plus read-only wind_view and build exports change. Production and Wetlands are untouched. Physics remains the separate fixed QA source.

Read-only snapshot uses exact u64 lineage strings, selected living aerial allocations, current world serial, and writer version 7 (classic), 11 (enabled Origin), or 0 (unavailable/invalid configuration). Focused ReleaseSafe snapshot/writer tests passed; first test-only float-literal compilation failure retained. Native full-game public flow acceptance remains pending, not implied by these tests.

Fresh factory consumes a one-shot startWindNext flag. initWithTopology explicitly uses false; loading restores saved configuration through the validated adapter. Existing Mode is Navigate/Paint, not ecological mode conversion. Existing Sandbox menu creates a new Planet, so no existing wind genes are silently discarded by an in-place mode switch. Explicit new-world replacement remains a destructive user choice, requiring the frontend warning.

Pioneer is actual seedPioneer funding, world/selected-point guarded; success1, ordinary refusal0, unavailable-1, stale-2, busy-3. No bulk Pioneer UI claim. Snapshot allocations report traits, not actual flights.

Expected save checks world and writer after the cooperative task pump immediately before serialization, without another pump; mismatch-6, existing recovery/save errors retained. JS must finish durable backup and subsequent save sync. No successful durable save is implied by the native write result alone.

# Browser control-flow check, 2026-11-15

Managed preview of the actual production shell at a374px dialog width. The WASM script was removed; mocked Module replies were explicitly labelled UI FIXTURE ONLY, not gameplay. This test does not establish real WebGL/Android behavior or engine availability.

Observed through supported cloud-browser controls:
- Open Life in this patch: Find recorded feeding is visible immediately near Close, not buried beneath cohort details.
- Search pending: Find disabled, Cancel search visible, progress text wraps inside374px panel. Screenshot inspected; neither button clipped.
- Cancel: Find re-enabled, Cancel hidden, 'Search cancelled; no life changed.' visible.
- Repeat search then Close: modal closes. Reopen via Inspect: no stale Searching state, cancellation message remains.
- Explicit fixture success mode then Find: modal closes, focus returns to canvas; feedback reads 'Lineage28 has recorded intake0.00726kg C/m². Past feeding, not eating now. Reopen Life snapshot to inspect.' The numbers came from mocked snapshot data, not this browser's gameplay.

The separate native-run.log/native-found.png demonstrate actual natural-world discovery and camera/pointer behavior. Browser fixture is complementary UI evidence only. Preview stopped after testing. No user save was opened or changed.

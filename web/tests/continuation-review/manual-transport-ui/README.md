# Whole-colony transport UI candidate

Actual production controller and shell, not deployed by this worker. Native engine/API and actual-world acceptance are separately owned.

- Collapsed God tools section; explicitly requires paused Origin; no automatic pause/resume.
- Frozen bounded options: at most four sources and six real neighbors. Exact lineage IDs remain decimal strings, including IDs above JavaScript's exact integer range.
- Choosing a source exposes neighboring destinations. Cards show biomass, included support, form and inherited trait values; destinations show actual depth, temperature, occupancy and biomass capacity. No habitat suitability claim.
- Review is separate from explicit final Move whole colony. Prepare must match displayed identity, biomass/support/credit, traits, destination environment/occupancy exactly. Mismatch cancels the one-use native ticket, not silently refreshes it.
- Execution validates native receipt fields rather than manufacturing success from the requested ticket. Lost or malformed post-action receipts advise inspecting both patches, not automatic retry.
- Close, collapse, tab hiding, load attempts, and stale world/selection/pause/status cancel. Lightweight native status polling only while this section and God dialog are open; no UI mesh scans.
- Session receipt is ephemeral, cleared on cancel/close/refresh/load. Clearly manual intervention, not natural birth, movement or evolution. No survival guarantee.

`node --test web/tests/*.test.cjs`: 35/35 pass, including eleven new controller/DOM tests. Logs preserved in js.log. Tests cover exact long IDs, invalid/nonfinite options, paused guard, stale preview fields, capacity, one-use execution, native cancellation, malformed results and lifecycle closure. Mock tests do not prove native biology or graphics.

Prepared separate supported-preview fixture from actual shell + controller with explicit '358px panel · mock engine' heading, four 20-digit IDs and six neighbors. No browser inspection performed by this worker. Parent owns CUA review. This is not a physical-phone viewport or real-game browser proof.

Explicit Inspect destination is available only following a verified move. The native owner validates its last receipt plus current identity; the UI validates returned world/cell/string ID then opens a fresh Life snapshot. No automatic camera, pause or time changes. JS tests cover explicit-only invocation and stale refusal. Actual native acceptance remains separate.

Parent CUA checked the 358px mock-engine panel: refresh → source → neighbor → Review → Move → Inspect succeeded with exact long ID. It found unnecessary scrolling from expanded unselected cards. Follow-up compacts sources/destinations after selection, provides Change buttons that consume any pending ticket, and hides cards during final review. These revisions pass full 35-test Node gate, including 4→1/6→1 cards and stale-ticket invalidation; repeat CUA pending. Life summary now shows the validated actual patch number.

Parent repeated CUA after compaction: verified 4→1 source cards, 6→1 destination cards, concise Review, Change destination removes the final Move and invalidates review; rechoose → Review → Move → Inspect showed Patch 20 and the exact long ID. This remains a 358px panel with mocked engine, not real mobile/native environment rendering. The mock Life snapshot retained a 1 m placeholder while the chosen destination card showed 0.5 m; therefore it does not prove environment consistency. Separate actual-native acceptance owns that proof. No further production edits after this review.

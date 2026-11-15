# Manual transport ownership gate, isolated

Production manual_transfer_core.zig copied with exactly one import remapped to hydration_lifecycle_core.zig. Reverse-remap byte equality asserted; hashes saved. No algorithm edits, API/UI integration or production change.

37 ReleaseSafe tests passed (including imported core). Exact expected state differs only in two cohort slots: whole stored water/allocation accompanies the moved cohort; source and destination liquid/vapor escrows stay. Duplicate execution, changed stored water/allocation/escrows, invalid overcapacity/NaN/negative escrow and full target reject without mutation. Includes full serialized before/after oracle for invalid NaN cases rather than NaN equality.

This tests copied core against mock planet ownership/adjacency, not actual browser exports, variable-area transport or schema. Those remain separate gates. Existing history and pause/ticket checks are unchanged production code. Initial compile-only mock visibility error retained.

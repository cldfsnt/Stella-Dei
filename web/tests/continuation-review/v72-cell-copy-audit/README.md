# Read-only v72 Cell-copy audit

Remaining borrowed-beta main368B memcpy is startup restore: immediately after `SavedCell.runtime`, before simulation/timing. A second368B copy inside SavedCell.runtime returns its value. These are not per-tick opportunities.

For the actual v72 baseline archive, metadata-only relink preserves every non-custom WASM section exactly. Final compiled main has one320B cohort-array copy in its simulation path. Retained object DWARF identifies its source exactly: **microbes.zig:144**, the potential-growth read loop `for(cell.cohorts,0..) |c,i|`. This is not the simultaneous grazing snapshot or physiology-death history snapshot. It follows mortality and precedes potential computation; only the separate potentials array is written within the loop.

A narrow prospective change is iterating `&cell.cohorts` with the same value capture, avoiding the whole-array value snapshot while preserving each c and all arithmetic. No source edit or benchmark performed. Compiled-copy disappearance and full saved-state/RNG/grazing/history parity would be required before any production claim.

Magnitude matters: this loop runs active cells, not every empty cell.37 occupied cells imply11,840 copied bytes/tick, versus the beta's30MB/tick. A substantial live gameplay speedup is not established; many populated cells would be needed before large traffic. No blind pointer conversion across all helpers is justified.

Other inspected paths: biomass/carbon are inlined without a separate whole336B Cell memcpy in this scheduler artifact. producerLightShares is used by selected-summary snapshot, not the actual scheduler. validCell has a320B array copy at line246 but is save validation here, outside timed simulation. This headless artifact does not prove absence of copies in every full UI/render callsite.

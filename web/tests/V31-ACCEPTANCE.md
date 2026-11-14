# v31: living traits at a glance

Life inspection now has a compact selected-patch card showing each living lineage's existing growth-form name and actual thin-water capability. This exposes real trait/tissue changes even in the ordinary deep nursery, without changing the simulation or forcing an intervention.

Potential requires inherited structure AND actual living support tissue. “Compatible here” additionally requires current nonfrozen shallow liquid and the model's habitat suitability. It is not a claim that the cohort is currently fixing carbon, growing, surviving, or establishing on dry land. The 15–20 cm aquatic transition is not mislabeled an evolved capability in use. Measured biomass trend remains separate.

The card contains at most four rows, is refreshed explicitly with Life inspection, clears on empty/unavailable patches, and retains existing map forms. No global scans, new art, camera moves, automatic modal, timer unlock, schema fields or telemetry were added.

## Executed checks
- 32 helper/model tests cover depth boundaries, frozen/dry states, inherited structure without tissue, tissue without structure, support loss, and read-only state.
- Production shell tests cover repeated open/refresh/close, form names, current labels and clearing stale rows; the integrated seven-suite JavaScript run passes.
- Actual native generated-world export called three times yields valid2,462-byte JSON within8,192-byte capacity and four cohort trait records. The complete8,867,927-byte save remains byte-identical (Wyhash7bf3835fa4fd5a13). Final integrated main/helper engine files match the tested candidate exactly.
- Final integrated full WASM packaging passed. The earlier native relative-cache path failure and corrected success are retained.

This is not an Android/browser visual acceptance or a new ecological establishment result. Known unrelated native teardown allocator warning remains. v30 ecology and v29 performance controls are preserved.

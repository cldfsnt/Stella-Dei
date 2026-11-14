# v32: colony watch and Sandbox Scorch

Two bounded gameplay improvements. Neither creates new species, wildfire simulation or automatic evolutionary milestones.

## Watch colony peek
Tap a colony in Origin Watch/Inspect mode to pin its patch in the existing bottom information area. A compact bar shows actual biomass shares of up to four living lineages; colors use the map's thermal-trait palette, not fitness. The dominant lineage's biomass change is measured against the pin-time baseline after at least two simulated days. Steady means within1%; a changed dominant lineage is called turnover, not mutation or proof of competitive selection.

The footer remains the same height. Details and Dismiss have44px targets. Dismiss restores the global Day/footer; Details opens existing patch inspection and explains the bar. There are no global scans, automatic camera moves, extra event cues or simulation changes. Existing arrivals/losses remain visible. Load or rewind clears the transient pin; observations are not serialized.

Actual native replay of an existing30-day world advanced120 fixed steps (two simulated days) at three viewport sizes. Four current cohorts had55.44%,9.86%,16.31%,18.38% biomass shares; the same dominant lineage's biomass fell. The UI correctly reports this without attributing cause. Read/pin/render save invariance, pointer Details/Close/Dismiss, pause preservation and load reset pass. Native screenshots demonstrate layout, not Android browser performance.

## Scorch: an explicit Sandbox intervention
God tools offers Scorch only in Sandbox. It destroys75% of the selected dry patch's existing vegetation cover and adds up to40°C external heat, capped at500K. The warning explicitly says heat can kill rabbits and recovery is not guaranteed. A brief charcoal mark and receipt describe the accepted action. Wet, stale, Origin, invalid, empty and numerical-precision cases reject without resource changes; rejected/invalid actions clear the transient effect.

This is NOT combustion: Sandbox cover is dimensionless and fuel moisture is not modeled. There is no invented atmospheric-carbon ledger, fire-resistance trait, seedbank, animal escape or guaranteed regeneration. Actual Origin fire remains unimplemented rather than assuming wet tissue is dry fuel.

Controlled actual-engine contrasts show existing consequences: a rabbit at275K survives after Scorch but receives less food (satiety67.14 versus89.64 control); at295K, the added heat crosses the existing333.15K thermal death threshold. Existing vegetation can regrow under explicitly favorable controlled conditions (cover0.2→0.709 over one day); this is not a promise of recovery in an uncontrolled climate. Receipts report cover percentage points removed and actual external heat.

Native exported callback, visible portrait scar, rejection/effect reset, save reload, rabbit contrasts and ordinary vegetation update pass. A centered landscape target was correctly clipped beneath toolbar bounds, so no off-target or always-visible scar is claimed. Harness alias, stale-fixture and busy-world restore failures were diagnosed and retained; normal job draining and serialized reload fixed the test sequence, not production guards.

## Limits and combined release gate
Known native teardown allocator warning remains. No actual Android/browser visual or frame-performance acceptance is claimed. Final combined current-tree tests/build and source hashes are recorded with the integration evidence before deployment. v31 Living traits and earlier ecology/performance features are retained.

## Final integrated results
Final combined source passes seven JavaScript suites, full WASM packaging,31 colony-peek/helper tests,36 action/imported-model tests and39 visual/imported-model tests. Actual combined native Peek gates pass at320×700,390×700 and700×390; real pointer Details/Close/Dismiss, pause preservation, load reset and full-save observation invariance pass. The combined Scorch callback/rabbit/save/effect gates pass in portrait and landscape. Source hashes are captured in the integration reports and unchanged during testing. No biology was injected into the saved-world Peek replay; Scorch's controlled mechanism fixtures are clearly distinguished from natural play.

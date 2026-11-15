# Post-water edit observation candidate

After a successful nonzero selected-patch fine-water or target-depth edit, an inline action offers Watch this patch, or explicitly Resume & watch this patch when paused. Refused/zero edits do not arm it. The edit receipt records world and patch identity; the click rereads the current snapshot and native code checks identity again. A newly paused world requires a newly labelled explicit resume click. Observation starts at the click AFTER the edit, not before intervention; simulation may already have run. Subsequent changes do not establish causation.

The new native checked-start seam restores the exact prior pause and Watch record on failed start. It never changes speed. Existing ordinary Watch remains pause-preserving. Dialog close/cancel, refresh, another edit and load clear the inline action. No automatic observation, additional ecological resources or god-tool chain is introduced.

## Verification

Production shell mock tests pass paused/running flows, stale same-index world and changed selection, newly paused relabel, zero/refused fine edits, zero target edit, close/cancel/load and no redundant success toast. Existing eight observation-controller tests pass. Native checked-start acceptance is separately owned by the actual-game worker and is not asserted complete by this checkpoint.

Parent performed CUA interaction on the current production shell with mock WASM values: paused edit→Resume & watch and running edit→Watch passed. Browser viewport was1343px wide with a450px dialog, NOT a phone viewport or real-game/runtime verification. A stale pre-refresh preview tab was corrected by reload; it was not a production failure. Visual review found the success toast overlapped the Watching HUD; this revision removes that redundant toast, leaving the pre-click caveat and actual observation HUD. The toast-removal regression is unit-tested; no new CUA screenshot is claimed here.

Existing stella-competition-preview metadata was preserved. The preview uses current shell/controller files with an explicit UI FIXTURE ONLY banner and mock data; no live game deployment was performed. Source hashes record this candidate.

## Complete JavaScript gate follow-up

The first full glob run exposed two isolated test fixtures that extracted handlers without their new real clearWaterWatch helper. No production assertion was removed. Both fixtures now evaluate the actual helper/declaration block, and the watch fixture supplies/executes real registered dialog-close behavior. Additional assertions verify the real inline nodes are cleared. `node --test web/tests/*.test.cjs` now passes24/24 tests, zero failures. This is fixture dependency repair, not evidence of a production runtime failure.

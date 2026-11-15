# Final selected footprint and close BFS regression gate

Supersedes the selected-only scale checkpoint with stronger overlap/picking acceptance; earlier failures remain immutable.

Review found14px ordinary distance decluttering insufficient for an enlarged selected glyph. Final selected-pair exclusion uses actual22×41up/9down conservative rectangles at each glyph's own scale. Ordinary/ordinary distance rule remains unchanged. Adds bounded64f32 scales+64bool flags (~320stackbytes), no allocations or particles.

First pure vertical-overlap fixture at y125 actually left a4.9px gap, so correctly failed the assertion; corrected test coordinate to y118, no algorithm/tolerance change.9 tests pass including source classifier, all selected index order cases0–64, margins, overlap geometry and selected center/four body edges against nearby rejected/accepted targets.

Then strict actual native edge assertions exposed close-view priority bug: original BFS begins cameraGroundPoint, not necessarily selected patch. In actual saved world, selected204 projects center while cameraGroundPoint12344 due elevated geometry. New overlap rule could suppress selected204 after an earlier nearby glyph. Final fix draws a bounded selected prepass in close mode, does NOT expand its neighbors there, and retains original BFS discovery/expansion. The duplicate selected index expands its ordinary neighbors before skipping only its duplicate drawing. Other traversal order is unchanged. Close maximum512 neighbors plus one selected prepass; glyph cap64 unchanged. Wide traversal retains selected-first permutation.

Actual strict native gates pass390/320 close and default2.5-radius globe, plus unchanged naturalday30 no-history/mixed/dominant controls. Selected204 baseline root204/left13593/right12397 becomes204/204/204; mixed13596 similarly becomes its own center/edges. Old failure logs retained. Candidate selected glyph required present, and actual center/left/right body samples required exact target. Every selected back-face test creates no target. Matched full saved state after equivalent rendering is exact and original input restores in all5runs. No seeding/god targeting code changed.

Final320globe mixed and320close dominant captures visually inspected: white brackets and producer forms remain readable; nearby body glyphs are omitted to protect selected, but their real living ground footprints remain. This is selected-patch legibility only, not all distant populations, current eating or animal evolution. Final log label is actual_saved_world; day30time2592000 and day60time5184000. Native software/browser-policy proxy, no device/WebGL claim.

66 existing JS suites pass. Production renderSprouts is byte-exact to tested candidate path after removing only QA switch/old path; helper byte-identical. Provenance records frozen source hashes. All logs retained including inherited teardown diagnostic. Coordinator owns final WASM/build/deployment.

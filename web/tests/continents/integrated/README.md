# Integrated Continents menu/load native acceptance

Tested current integrated source with diagnostics, before deployment. No production source changes were made by this QA pass. Exact source, harness and asset SHA256 manifests accompany this report; source-manifest SHA256 is f38a2a7d4db98e375314bdafeb2fd575780bbaf5aac028b6bdea8671712c2f00. Main, PlayState, menu, Planet and save adapter hashes remained unchanged through completion.

Both tests PASS:
- Origin390×700: real pointer presses/releases select Continents, Random, Continents, then Origin.
- Sandbox640×360: same selection sequence, then Sandbox and Create my planet.
- Both assert initial Random, reversible choices and no world reset on selection.
- Both load the existing30-day schema6 Origin fixture while Continents remains selected, compare complete canonical captured JSON byte-for-byte, then reload the newly created mode and compare its entire saved JSON byte-for-byte.
- All resources, water, vapor, terrain, traits, organisms, counters, serialized RNG/view/time fields remain exact. Schema remains6; loaded inventory is not recomputed from the menu preset.

Native harness uses the browser's cooperative EventLoop semantics at a quiescent frame boundary, not the desktop asynchronous updater. The browser menu branch and actual ui.button pointer handling are rendered. Screenshots confirm no clipped menu labels at both viewport sizes. Native EGL is not an Android/WebGL device test. The known pre-existing allocator leak at shutdown remains and this is not a clean sanitizer result.

Reproduce with web/tests/egl-world-menu-prepare.py, egl-world-menu-build.zig and egl-world-menu-shim.c. QA_SANDBOX=1 chooses Sandbox, otherwise Origin. STELLA_ORIGIN_WIDTH/HEIGHT set dimensions; QA_EXISTING_SAVE selects the existing Origin fixture. Raw captures and full native logs were retained locally; checked-in logs contain relevant assertion results only.

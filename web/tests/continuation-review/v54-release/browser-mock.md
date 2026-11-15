# Actual browser control flow, mocked native engine

2026-11-15, supported Sites preview and cloud Chrome tab7, actual shell/controller with mock native callbacks. Desktop viewport only; not Android, actual WebGL engine, ecological progress, or real persistent-save evidence.

Initial run found real browser receiver bug: passing raw setInterval/clearInterval as object methods caused Illegal invocation before native start. Fixed by global arrow wrappers (0e2e260), then reloaded and retested.

Observed after fix: explicit paused start; 7/60=2.8hours; Cancel keeps partial count and withholds Return during pending redraw; explicit final redraw permits Return; repeated start;60/60 reports restoring rather than completion until final redraw; malformed status holds opaque overlay, restored valid response resumes receipt; final completion returns after checked dismiss/neutral mock callback. Context loss at7steps stops and exposes save/reload recovery; context-restored does not clear recovery or offer Return. Mock save rejection displayed failure/in-memory warning; mock delayed success displayed saved only after promise resolved. No actual IDB durability established by mock.

Screenshot inspected opaque full-viewport readable overlay, ordinary controls inaccessible. Identified contradictory generic wait-for-redraw subtitle during permanent recovery and requested correction. Native audit separately identified swallowed release events; UI fix/test pending at time of this note. Final independent native acceptance and final build remain release gates.

Final recheck after c00d614: reloaded actual mock shell, started, injected context loss, verified generic final-redraw subtitle now absent and explicit reload/save warning remains. Release-event propagation is covered by focused JS tests/native latch acceptance, not claimed measured through real browser GLFW in this mock. Final JavaScript suite54 tests passes. Integrated WASM rebuild pending final passive glyph redraw b7df233.

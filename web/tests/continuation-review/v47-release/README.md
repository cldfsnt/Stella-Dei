# Colony endpoint detail integration

Extends Watch this patch with an optional collapsed Individual colony changes section after observation stops/completes. Active watching keeps it hidden. Exact decimal IDs and start/end biomass show net change or presence only at one endpoint; no inferred death or cause. Four members per endpoint, at most eight compared identifiers. No biology, RNG, save format, new timers or full-world scans.

The retained panel is height-limited and scrollable; a new watch, failed start or snapshot-less error clears previous details. Formatter uses textContent, not interpreted HTML. Unit/controller/UI regression checks pass; all existing JavaScript test files pass. Two Zig serialization/capture tests pass. Real Emscripten WebAssembly build passes.

Actual native scheduler proof is archived in ../colony-watch: funded birth, 64 movement cases, exact independent natural-world endpoint arrays and complete observer-on/off saved-world parity. Those fixtures are not Android/laptop gameplay evidence. Cloud browser actual game remains WindowCreationFailed as previously recorded; UI fixture inspection for this new fold remains pending. No deployment claimed here.

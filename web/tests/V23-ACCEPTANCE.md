# v23 · Sculpted life and faster worlds

## Real art, same organisms
Six original Blender-authored aquatic forms are baked into one camera-facing
atlas. Form choice and thermal-lineage tint still come from real inherited
cohort state; this is not new taxonomy or a terrestrial-evolution claim.
Raised/layered canopy and flat mat remain distinct. Existing colony count caps,
Inspect roots and feedback overlays remain. Missing, corrupt or incorrectly
sized artwork falls back to existing vectors. Fresh rejected textures are freed;
valid shared textures keep renderer ownership. NanoVG registration allocation failure also falls back safely, with a successful later retry verified. Runtime atlas is576×384 RGBA,
0.844 MiB decoded, not six live complex 3D models. Editable Blender source and
reproducible generator are saved under assets-src/aquatic-forms.

Twelve isolated native actual-saved-world comparisons cover two worlds, three
viewports and vector/atlas modes. Full resource hashes, pause/time, visible
patches and every Inspect target remain unchanged. Native fixture tests also
cover heat feedback, invalid artwork, repeated invalid loads and valid caching.

## Faster without skipping physics
Wind tangent vectors are computed once per cell per physical step rather than
repeatedly for every edge. Edge calculations, rounding and summation order stay
unchanged. The owned transient scratch cache uses491,544 bytes on40,962cells,
is not saved and falls back to original calculations if allocation fails.

An1800-tick/30-day paired test produced identical full saved-world hashes with
cache and forced-allocation-failure baseline. Poisoned cache after load refreshes
before use. Alternating grid replacements and isolated Planet allocation/free
balance pass. Measured native Fast was16.53 simulatedhours/second in the owned
candidate repeat versus9.66 in the earlier baseline. This is not a guaranteed
speedup, Android benchmark or smooth-frame claim; achieved-rate UI stays honest.

## Feedback and limits
Fit nearby life now distinguishes Origin-only, small canvas, polar, invalid and
no-nearby-life cases instead of giving misleading panning advice.
The first combined build caught an accidentally reversed Fit-feedback patch;
it was restored before any publication, and final combined checks were rerun.

No reserves/schema7, Continents menu or terrestrial ecology is included here.
Existing native shutdown leak diagnostic remains. Real-device browser profiling
is still unavailable; native/EGL evidence and successful WASM packaging are not
claimed as an Android runtime test. See blender-atlas and performance QA reports.

Final integrated native smoke: actual world42 at320portrait/800landscape, identical resource hashc957a0149e8f9813 and8/8 Inspect targets. Three new-world transitions each reuse live texture/handle. Final clock/save smoke preserves identical hashes across all speed targets.

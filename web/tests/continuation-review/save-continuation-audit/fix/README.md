# CPU-only load-geometry repair acceptance

Production candidate changes only Planet and save_game. A shared inline terrainPoint helper preserves the old upload expression and optimized float mode. refreshTransformedPoints applies that expression synchronously on load after elevation/axial tilt restoration. It allocates nothing, starts no jobs, calls no GL, consumes no RNG and changes no saved field. Rendering continues to use its existing single loop and the same point helper; no extra full render pass is introduced. No schema bump.

Actual native EGL gate passed:
- Four tilts(-45,0,23.5,90) plus an actual terrain brush edit: every three-component f32 bit pattern for all40,962 vertices matches the frozen pre-fix upload expression, then actual upload. Undefined vector padding is not compared.
- Same legitimate prior-world tilt/terrain witness now produces exact complete one-tick state with and without a subsequent upload. Both fixed outputs also exactly match the ORIGINAL correctly refreshed control:SHA256b48e0789e3d13eced64242b3aebea55493f45982dab631ab2c69f4b010760ad2. No normalization.
- Same-geometry uninterrupted10ticks versus restored10ticks is exact; invalid save validation preserves full serialized state and all geometry component bits.
- Original full save restored, existing native originSaveCheck invalid-load/exact-restore assertions pass.49/49 existing save/core tests pass.
- Production Planet exactly equals tested copied Planet after removing only QA-only frozen oracle; save_game byte-identical. production-match.json pins hashes.

The first fixed-fixture compile failed because QA main used an unavailable Vec3 alias; corrected to derive the actual array element type. No production correction or assertion weakening was needed. Failure retained. Existing GPA teardown diagnostic retained; no memory-leak fix claim.

Callers of save_game.apply already must finish pending jobs; replaceWorld checks normal job completion and browser load pumps outstanding jobs. The new helper does not add a graphics or normal-job dependency. Existing native multithreaded physics concerns are outside this change. Native proof is not an Android/browser execution claim; final WASM build remains coordinator-owned.

Reproduction: run web/tests/egl-load-geometry-fixed-prepare.py on an isolated directory, build with egl-propagule-visual-build.zig, then run with QA_PULSE_SAVE=natural60-day60.json, STELLA_ORIGIN_COUPLED=1, STELLA_ORIGIN_FAST=1, STELLA_ORIGIN_WIDTH=390, LIBGL_ALWAYS_SOFTWARE=1. Original failing witness is pinned at ab30649; current source intentionally fixes it. Large raw snapshots remain local, only compact hashes/results committed.

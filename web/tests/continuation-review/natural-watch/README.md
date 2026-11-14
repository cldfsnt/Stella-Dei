# Actual coupled nursery and rendered observation acceptance

One ordinary starter seed, production nursery API, real coupled PlayState.update for30 simulated days. No assigned organisms/traits, no auto-care and no experimental grazing model. The native adapter uses mobile UI branches, offline audio and EGL rather than Android/WebGL. Original runtime source is unchanged.

Observed final world:40962cells,10occupied patches,48paid arrivals,31tracked colony losses, maximum extant generation3, biomass-density sum0.200586kgC/m² summed across patches (not a world total mass). Six cohorts hold actual support tissue and seven have recorded feeding. No rabbits or Sandbox vegetation exist in this Origin run. Find returned success, framed10visible living glyphs, all10actual pointer root checks selected their intended cells. Inspection preserved serialized Origin biological data and simulation time/pace/pause. Exact save roundtrip and invalid-save rejection passed.

`final.png` is the actual day30 renderer frame, not a synthetic ecology fixture. It was visually inspected: distinct raised forms and mats, arrival/loss markers, readable portrait controls/footer. Root picks occur after this frame; they were asserted against actual renderer target records. The previous glyph fixture additionally tests body offsets. A loss marker can coexist with living cohorts in the same patch.

Native shutdown still reports the pre-existing allocator leak. Sparse rendering in this accelerated harness is not a mobile frame-rate measurement. Browser graphics-context startup and Android device acceptance remain unverified. This is not proof of full evolution into plants and animals or long-term ecosystem stability.

## Reproduce

```sh
python web/tests/egl-nursery-watch-prepare.py <absolute-isolated-source>
zig build --build-file web/tests/egl-propagule-visual-build.zig -Dsource=<absolute-isolated-source>/main.zig --cache-dir <absolute-cache> --global-cache-dir <absolute-global-cache>
MESA_SHADER_CACHE_DIR=<cache> STELLA_ORIGIN_COUPLED=1 STELLA_ORIGIN_FAST=1 STELLA_PRODUCER_LONG=1 STELLA_DIAGNOSTIC_DAYS=30 STELLA_FORMS_SINGLE=1 STELLA_ORIGIN_WIDTH=390 STELLA_EGL_CAPTURE_PREFIX=<capture-prefix> STELLA_EGL_SAVE_PATH=<test-save> web/tests/zig-out/bin/stella-egl
```

Use Zig0.13.0 and existing vendored dependencies. Run binary from repository root so assets resolve. Initial harness compilation mistakes (const qualification and save-schema field name) were corrected before this passing run; no production logic was changed.

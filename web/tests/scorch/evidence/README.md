# Isolated Sandbox Scorch candidate

Base fork master v30 2af9c4d. No production edits or deployment. Apply scorch-v30.patch narrowly; full source copies are review evidence, NOT wholesale replacements for v31 UI.

See SCORCH-QA.md for verified mechanics, real native callback/animal/recovery/save results and limitations. Scorch is external cover destruction and heat, not fire chemistry. No Origin combustion, inferred moisture, seedbank, new schema or fire-adaptation claims.

Native harness files belong under web/tests in an isolated copy with assets/deps. Run egl-scorch-prepare.py to absolute tmp/native-src, build egl-world-menu-build.zig with absolute source/prefix/cache paths using Zig0.13. Environment: QA_SANDBOX=1, QA_EXISTING_SAVE=/path/to/old-schema6.json, STELLA_EGL_CAPTURE_PREFIX=/workspace/output/prefix, LIBGL_ALWAYS_SOFTWARE=1, EGL_PLATFORM=surfaceless; widths390/640 and heights700/360. Old fixture retained locally in stella-shore-visibility/tmp/schema6-world.json. Larger binary/assets are reproducible and excluded.

Portrait scar verified; landscape centered patch obscured by existing toolbar exclusion, not moved artificially. Browser/mobile visual execution still absent. Known native shutdown allocator warning remains. Failed harness runs preserved and explained in QA; final runs exit0.

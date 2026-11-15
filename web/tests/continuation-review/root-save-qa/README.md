# Experimental root-only persistence: actual native acceptance

No production/schema promotion. Reusable `root-only-save-patch.py` modifies only generated save_schema/save_game. `egl-root-save-qa.py` copies the complete candidate independently and injects QA main; it restores the exact production pond export inherited incorrectly by the older fixture chain. Owner's candidate/main is not modified by this acceptance fixture.

## Contract

Schema10/model9 Origin root_config is required. Enabled law1 accepts conductance1 or10 and exactly one finite0..1kg/m² soil density per cell. Disabled canonical law0/conductance1 has no serialized soil material or nonzero root fraction. Legacy<=6 rejects disguised new config/soil/root material and initializes disabled/zero. Schemas7–9 and unknown storage/mutation fields reject, never silently discard. Sandbox/legacy apply resets root model. All validation and allocations precede committed state mutation; old saved files are not rewritten on load.

## Actual test results

ReleaseSafe native EGL acceptance exit0 on the frozen production day60 input. Initial native run lacked assets in its isolated working directory and exited FileNotFound before the gate; retained first-run log. Read-only existing asset symlink corrected that fixture setup. Preliminary compile predated exact pond restoration; only final build executed acceptance.

For ownership testing only, a real resident lineage478 is prescribed root allocation.25 and its patch soil.125kg/m². This is not natural evolution, funded soil creation or an ecology success claim.

- Enabled capture→decoded apply preserves complete serialized bytes exactly.
- Ten actual full Planet.simulate ticks at1440seconds uninterrupted versus restoring the same enabled endpoint then running ten ticks: complete serialized state identical. No camera/model field stripping. Raw snapshots retained locally with hashes and lengths in provenance.
- Seven actual apply refusals leave complete active state unchanged: unsupported version9, unknown root law, unknown conductance, wrong soil length, NaN soil, disabled config with physical soil, legacy version disguised with new material/config.
- All six frozen schema8 retention endpoints rejected through real schema parse/apply path, preserving the current world byte-for-byte. No dropping their retained water/config.
- Sandbox apply clears root configuration/soil; actual raw v6 input also resets disabled. Reapplying the original captured disabled world restores exact bytes.
- Existing actual Origin save check passes: invalid refusal, exact restore, transient observer reset. Its old `save_schema_unchanged` label is inherited fixture text, NOT a claim this experimental schema is unchanged. Inherited final GPA teardown diagnostic retained, process exit0.

No browser/IndexedDB/device test. No new global rates, roots mutation, storage, lifecycle water claim, save-size/performance claim or release approval. Real physical-model acceptance and supported source-law review remain separate owner gates.

## Reproduction

Apply `python3 web/tests/root-only-save-patch.py <generated-root-src>` once after owner's generator. Then `python3 web/tests/egl-root-save-qa.py <generated-root-src> <independent-src>`.

Build with Zig0.13.0, `zig build --build-file web/tests/egl-propagule-visual-build.zig --cache-dir <cache> --prefix <bin> -Dsource=<independent-src>/main.zig`.

Run from isolated directory with read-only `assets` link, LIBGL_ALWAYS_SOFTWARE=1, EGL_PLATFORM=surfaceless, STELLA_ORIGIN_COUPLED=1, STELLA_ORIGIN_FAST=1, STELLA_ORIGIN_WIDTH=390, QA_PULSE_SAVE pointing to natural60-day60.json, QA_REJECTED_DIR to frozen retention-coupled, and STELLA_EGL_CAPTURE_PREFIX to that isolated directory. Input hashes are preserved; no source worlds modified.

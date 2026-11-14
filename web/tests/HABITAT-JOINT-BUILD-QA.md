# Habitat joint browser build acceptance

Final label: **Build v16 · habitat care**. Zig 0.13.0 and Emscripten 3.1.64
build succeeds. All ten frozen model, shader, UI, build and persistence inputs
matched their pre-build hashes after completion.

- WASM validates with all **19** expected game exports, including
  `stella_set_water_target` and `stella_adjust_water`.
- Runtime, touch and storage JavaScript syntax checks pass.
- All four shell/storage/touch/harness test files pass, including target-depth
  scope, invalid input and optional one-time habitat-care help.
- Unchanged schema 6 persistence/model regression suite passes **34/34**.
  The persistence adapter and schema are byte-identical to the producer release.

Runtime package: **66392539 bytes**.

WASM SHA-256: `b55563acd1047cb69dee12c235ef3051aca8d412ff52554bb7cca724436f5aec`.

HTML SHA-256: `1218a0cb897d0282c0eadf1be1f345ab9dccbc16bffe4169d6fcfa2ffc796443`.

Shell source SHA-256: `0100142d9357d4a0c48a6825f22b2c76781e2b7a2fae86e92f6cec6a40524d86`.

See [Habitat map](../../docs/HABITAT-MAP.md) for the separate actual native
320/390px rendering and control gates, and [Habitat care](HABITAT-CARE-QA.md)
for long-running player-intervention outcomes and limits. These results are not
inferred from compilation. Fine target water changes only the selected patch;
help does not promise automatic refill or guaranteed evolution.

No physical Android FPS or browser graphics result is claimed by this build
verification. Native rendered checks and mocked browser layout checks have
different scopes; neither substitutes for physical-device playtesting.

The initial shell-preprocessor failure on a new CSS selector was corrected
before the final successful build; the failed artifact was not accepted.

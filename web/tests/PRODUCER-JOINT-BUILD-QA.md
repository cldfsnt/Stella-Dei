# Producer joint browser build acceptance

Final integrated model, persistence, native UI and HTML shell built successfully
with Zig 0.13.0 and Emscripten 3.1.64. Source hashes were checked before and after
the build; no frozen input changed during compilation.

- WASM validation passes; all 18 expected `stella_*` exports exist, including
  `stella_adjust_water`.
- JavaScript syntax checks pass for the runtime, touch controls and storage.
- All four JavaScript test files pass: shell, storage, touch and harness mode.
- The final schema/model regression suite passes 34/34 tests.
- Small positive support/height values remain visible rather than rounding to
  zero. Nonzero water changes below 0.01 m are distinguished from no change.

The runtime package totals **66,388,502 bytes**. Its WASM is 1,208,218 bytes:
`1c3ba62eaf4c9ff8a313839ce94cca8a1f8cbc9e913fe905279c89f162b8fdc7`.
Final HTML SHA-256:
`f82e824412b5866f70e7c9f879ef01353bc7f3edda046a554afc5db0f8a52906`.

See [Producer actual-engine acceptance](PRODUCER-ENGINE-QA.md) for actual
legacy migration, nonzero-support restoration, ordinary-world outcomes,
controlled inheritance, native portrait rendering and water interventions.
These are separate gates, not inferred from a successful build.

This verification did not measure Android FPS or verify browser graphics on a
physical phone. A successful build and native rendering are not substitutes for
those checks. Existing native teardown leak warnings are not resolved here.

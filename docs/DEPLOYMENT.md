# Browser deployment and recovery

## Verified source and build

The browser/mobile port uses Zig 0.13.0 and Emscripten 3.1.64. Build with `web/build.sh`. Keep the exact source revision available together with the executable under GPL-3.0.

The production source milestone at `7cd26361b9c343220a6999a8af33b0cb639b3e0a` was rebuilt after restoring the official toolchains. Shell, touch, storage and JavaScript syntax checks passed; the generated WASM validated and included required application exports.

## Small runtime package

Publish only the generated runtime, original asset chunks, LICENSE, and lightweight source/verification notices. The executable needs:

- `index.html`, `index.js`, `index.wasm`
- all `assets-*.bin` chunks produced by the build
- `touch-controls.js`, `stella-storage.js`, `gameplay-harness.js`
- `LICENSE`
- `source.html` with an exact corresponding-source commit and source archive link
- `qa.html` with precise verification limits
- optionally a public-safe build manifest containing source revision and file hashes

Do not include old source archives, caches, private hosting configuration in public source, credentials, personal metadata or test fixtures containing internal paths. Preserve project access settings when replacing an existing deployment.

A runtime-only package of 66,396,160 bytes successfully deployed after an earlier 182,067,200-byte archive repeatedly failed with a generic hosting-provider error. No individual file exceeded the documented per-file limit. The smaller package is a verified successful workaround, not proof that total size was the root cause.

## Verify before claiming live

Record the saved version and successful deployment. Fetch the deployed build metadata, HTML and WASM using the hosting service's supported access method, and compare their hashes with the local candidate. Never publish service-access credentials.

For the source milestone above, the verified runtime hashes were:

- HTML: `b8caddb52c65db96a7648f120f3df003fd2de09c1d12c395b9b4a84cb242140f`
- WASM: `9a3898d9de39abe697eb98340693252b5f6673a230c3aba90072ee5696249b5c`

These identify that build only; a later rebuild can differ.

## Verification boundary

The managed cloud browser loaded assets and WASM but failed at graphics-window creation with `WindowCreationFailed`. Native software-rendered engine tests and successful hosting do not establish Android performance or end-to-end browser gameplay. Preserve that distinction in release notes.

Keep previous saved deployments for rollback. Save source changes and reproducible tests to the authorized repository at meaningful checkpoints before relying on an ephemeral execution workspace.

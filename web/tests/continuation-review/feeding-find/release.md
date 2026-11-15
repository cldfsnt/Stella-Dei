# v41 release validation
Pinned Zig 0.13.0 / Emscripten 3.1.64 web build completed successfully. Generated JS syntax check passed, new stella_find_feeding export present. Final seven JavaScript suites passed. Existing 47 save-schema tests and real native world acceptance are recorded separately. No save schema or ecology change. Browser control flow tested with explicitly mocked WASM; actual game rendered/tested natively. Android and live WebGL gameplay not verified.

Built output SHA-256:
09f9f71c4bff5601ceedbfef859580733aad9a118fd79f6a8428c11fd878406e  index.html
6bb88b37435192014d72fa2af3f42bbedf725d18539165dd440c685dbdbeefed  index.js
57dba0dc9562ef638d6e9545289da5ff3003454ecae058f7e5a70cae4cb90d11  index.wasm

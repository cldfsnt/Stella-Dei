# Isolated Wetlands preview build

Final full WASM/HTML/assets build passed (exit 0), including the final isolated welcome key. All 111 copied JavaScript tests passed. Initial optional-module/mock and storage namespace fixture failures are retained; fixes are frontend-only. Frozen engine source manifest matches every original listed source hash.

This is the separate `site-tmp/wetlands-preview` project, not a production or root Site build. New native exports and `/wetlands-saves` paths are isolated; no deployment performed. Full source and artifact hashes are in provenance.json. No browser GPU/device performance claim. Actual native gameplay acceptance and independent final Module proof are separate release gates and are not inferred from compilation.

Toolchain: Zig 0.13.0 wasm32-emscripten ReleaseSafe; Emscripten 3.1.64 with -O2, WebGL2, debug=false, 128 MiB initial linear memory, 8 MiB stack, memory growth enabled. Exact build.sh is source-hashed. Source-manifest aggregate hash is recorded in provenance.json.

Parity scope: prior canonical controls compare reference/candidate within native and separately within WASM, including same-target saved continuations. This build proof does not establish native-to-WASM cross-platform bit identity. Native full-game acceptance is a separate sibling gate; Node export checks do not establish browser rendering or GPU functionality.

## Final disclosure-only rebuild

After ee98afd, the isolated HTML was rebuilt successfully with the compact, reopenable disclosure CSS. `disclosure-final-provenance.json` supersedes earlier HTML artifact hashes; all native source hashes and WASM bytes remain unchanged. HTML SHA-256: 2657c135cd317519ff4368770bcaa7bad1bc12f64be1be655c1bbbac50fe9ff2. Independent native full-player/save/continuation proof is saved separately at fda412a/5a356be. Browser DOM collapse/reopen verification is delegated separately, not inferred from this build.

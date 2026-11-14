# Per-linked-program uniform-location cache

## Implementation
A small inline cache belongs to each ShaderProgram: 32 entries with up to 64 bytes of owned name content and signed GL locations. Missing uniforms (-1) are cached without changing the subsequent GL uniform call. Full cache and oversized names use the original lookup path. No allocations/OOM branches, global map, retained external name pointers, or cross-context IDs.

All uniform setters now borrow the actual program through pointers. Nine minimal render aliases in play/main_menu (including entity) likewise borrow renderer fields instead of copying the cache. Read-only attach/use borrow pointers too. Creation/replacement starts empty; each link attempt clears its program cache, including failed link. Program teardown clears cache and deletes the GL object. Renderer teardown deletes its six owned programs. Reload creates all replacements first; only a successful full batch replaces/deletes the old six. Error defers release newly created programs if a later stage fails. Partial program creation errors clean up the program created by that constructor.

Context assumption: the engine currently creates these objects in one GL context and does not implement in-place WebGL context restoration. Fresh renderer/program construction starts fresh caches; this change does not add context-loss restoration or make stale GL objects usable. No global numeric-handle cache can accidentally survive a new context or reused GL ID.

## Verification so far
- Two pure cache tests pass: owned name bytes, exact names, -1, clear, program separation, 32-slot overflow and oversized-name fallback.
- Actual native 390×700 paused Origin draw: eight warmed frames have 416 original glGetUniformLocation calls vs zero cache lookups. RGBA framebuffer hashes exactly match (a1bdaaa8ed90dcc9); complete saved-world bytes unchanged. No claim of proportional speedup or actual Android timings.
- Actual GL missing uniform caches -1; relink invalidates and repeats lookup; deletion removes program; renderer reload preserves framebuffer pixels.
- Intentional malformed reload: five newly created programs cleaned up, old program IDs retained. An empty program link also fails and clears stale cached entries. Expected shader errors are logged; test exits 0.
- Existing unrelated allocator teardown warning persists.

Final combined shader+cache evidence will be appended after native acceptance completes. Main never edited by this worker. uniform-cache.patch contains only renderer cache/ownership, pointer aliases, and helper module; no shader changes.

## Reproduce
Set STELLA_SOURCE_ROOT to a source tree containing the candidate and run qa/prepare.py with a workspace-local output directory. Build its main.zig using source web/tests/egl-origin-build.zig. Run from source repo assets cwd with QA_UNIFORM=1, QA_BAD_SHADERS=<output-parent>/bad-shaders, STELLA_ORIGIN_FAST=1. STELLA_ORIGIN_WIDTH controls width. Preparation injects only test lookup counters/bypass and creates an isolated malformed shader fixture. Source cache behavior remains unchanged.

## Final combined result
Accepted postprocess shader (SHA256 c951c29e8f60aa8348a0c2b31c7875fba1848c65456935bd71f0b84594997472) plus uniform-cache candidate passed native ReleaseSafe acceptance at 390×700 and 920×700. Both runs exited 0. Eight warmed guarded frames: 416 lookups → 0. Eight forced active-bloom-path frames: 472 → 0. Cached/uncached RGBA pixels were exactly identical in each path, and saved world stayed unchanged. Pixel hashes: 390 a1bdaaa8ed90dcc9; 920 ee58b8503c79479f. Both resolutions passed missing-uniform, relink, deletion, failed reload rollback/cleanup, successful reload pixel equality, and subsequent zero-lookup warmed frame checks. See results/combined-390.log and combined-920.log. No frame-time or Android improvement claim is made from these query counts.

Frozen patch SHA256: 4caa1376d1d6312daaee90185c66d390283b025a49554b02be07960cdd9073d2.

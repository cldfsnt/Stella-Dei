# v27 · Less unused graphics traffic

The browser no longer rebuilds or streams the atmosphere mesh that its renderer never draws. The native renderer retains its original upload. Terrain positions/normals, climate maps, visible water presentation, animals, bloom and framebuffer resolution are unchanged. No new cache or allocation is added.

Firm reduction: one unused buffer upload and 655,392 bytes per rendered frame at 40,962 cells (2,621,472 bytes at high detail). This is less streaming, not freed GPU memory or a promise of a corresponding speedup.

Same-binary native browser-style checks preserve exact pixels across all five maps, atmosphere shader on/off, visible rabbit, real HDR sun and lighting transitions. Serialized world state and clock/save/pause regressions remain unchanged. Native timings show small/noisy average gains with mixed tails; this is not an Android benchmark or a demonstrated fix for the reported 68 ms render call. Local render-stage diagnostics remain available for actual device evidence.

No save-schema migration, water-reserve model or unreviewed shoreline UI ships here. Known unrelated native allocator shutdown warning remains disclosed. Final integrated checks and full WASM packaging are release gates.

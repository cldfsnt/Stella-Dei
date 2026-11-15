# All-point resource-paid auto-seed: actual native acceptance

Final `release.log.gz` passes on the actual Sunlit day14 world (40,962 patches; 54 living colonies initially), using production source checkpoint `2c7e0e2`. No biology, terrain, water, mutation or save-schema change was made by this operation.

## Verified outcomes
- All initially eligible points scanned in 81 bounded chunks: 7,933 eligible, 7,933 real resource-paid seeds, 33,029 ineligible, zero resource/identity skips. No visible-only filter or arbitrary count cap.
- Complete applied save/RNG exactly matches direct sequential calls to the existing `Planet.seedMicrobes` on the initially eligible IDs. Planning leaves live state unchanged; duplicate apply is inert.
- Cancel before Apply, stale source/world/time/unpause/load, one-byte allocator OOM, and invalid cell after an eligible cell all preserve the corresponding live state. The invalid-cell test retains the deliberately invalid input, then restores the valid original.
- Save/reload is exact. Ten actual coupled ticks (four simulated hours) produce 0 natural births and 5 physiological colony deaths, independently reconciling 7,987 to 7,982 living colonies. True uninterrupted versus restored continuation matches exactly. Original pre-seed state is restored at completion.
- Screenshot `recent-footer.png` displays the actual observed ‘4.0h: 0 births · 5 colony deaths’. This is not the visual tracked-loss counter. Native recent footer is bounded/read-only; detailed Community retains physiological scope.

## Practical limits
Final native diagnostic timings: snapshot 11.79 ms, maximum 512-point chunk 1.91 ms, atomic commit 7.18 ms; snapshot allocation 28,018,008 bytes. These are execution diagnostics, NOT controlled browser/mobile frame or speed claims. A separate reviewer performance experiment used natural60 and 2,365 seeds, not this 7,933-seed world.

The fixture has zero initially partially occupied eligible points; that predicate is shared with existing seed eligibility, but partial-slot behavior is not established by this world alone. No funding exhaustion occurred here. Large seeded populations may run slower and may die. Apply has no built-in undo: Save first; loading the prior save restores it. File snapshots and hashes are retained outside Git; this gate does not exercise browser IDBFS persistence.

## Reproduction and provenance
Generator: `web/tests/egl-auto-seed-prepare.py`; native build seam: `web/tests/egl-propagule-visual-build.zig`. Input and immutable before/after paths plus hashes are in provenance.json. The copied public-export audit and source hashes are preserved. All build/run/unit logs, including the earlier recent-mode census test failure and its subsequent correction, are retained compressed. Final gate exits explicitly after restoration, so it makes no inherited teardown/leak-check claim. Raw large snapshots and native binaries are not committed.

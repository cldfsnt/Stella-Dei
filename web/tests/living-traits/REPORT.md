# Living traits: selected-patch capability card

Isolated source snapshot of current corrected-film main. No production edits, deployment, simulation changes, schema changes, RNG calls, global scans or telemetry.

Four changed files: src/main.zig, src/producer_habitat.zig, web/shell.html, web/tests/shell.test.cjs.

The Life snapshot's four tissue records now include read-only model-derived living_traits: film_potential, film_compatible_now, habitat_factor. Potential requires both actual paid support and inherited structure on living tissue. Compatible-here requires actual model suitability in >0–15cm liquid water; the 15–20cm partial aquatic transition is not falsely labeled an evolved capability in use. Compatibility is not measured uptake or positive net growth.

A compact card above detailed cohort rows lists lineage, existing growth-form name, and current capability. Existing map silhouettes are unchanged; no new art or renderer overhead. This can reveal potential in the ordinary 5m nursery before an explicit player experiment. Existing measured biomass trend remains separate. Four rows maximum, no automatic modal, camera change, timer or progress unlock. Reopens/refreshes replace the snapshot; empty/unavailable snapshots hide and clear the card.

Validation:
- 32 helper/model tests pass. Added exact 15/20cm boundaries, frozen/dry, trait-without-support, support-without-trait, support loss, and source-cohort equality.
- Production shell VM tests pass, including three open/refresh/close repetitions, current form labels and stale-row clearing.
- Native generated-world snapshot/save-invariance gate: see results/native-callbacks.log when complete.
- Browser visual check not performed (known browser OS socket restriction). No Android performance or screenshot claim.
- First native build failed from relative cache path resolution; retried with absolute cache paths. This was test invocation, not source failure.

Measurements are current potential/compatibility, not evidence of selection, inherited ancestry history, terrestrial plants, measured photosynthesis or successful establishment. Existing shell measurement controls preserved.

## Final actual-engine gate
Native ReleaseSafe build passed. Generated-world snapshot export called three times:
2462 bytes each within8192-byte buffer, valid JSON with four per-cohort trait records.
Complete serialized save before/after remained byte-identical:8,867,927 bytes,
Wyhash7bf3835fa4fd5a13. Exit0. Existing unrelated allocator teardown leak warning
remains; this is not a leak-free claim. Native availability shim bypasses only browser
export guard, so this is actual export/model QA, not browser runtime verification.

Patch SHA256:
c1700bf079c82eba16699313baded1ffaa02ee5e54ab67a0c2c48d7b01970a2a

Reproduce preparation:
STELLA_SOURCE_ROOT=/absolute/source python3 qa/prepare.py /absolute/generated-src
Build using source web/tests/egl-origin-build.zig with absolute source/cache paths.
Run from repo with QA_LIVING_TRAITS=1 STELLA_ORIGIN_WIDTH=390 STELLA_ORIGIN_FAST=1.

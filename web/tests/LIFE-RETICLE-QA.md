# Recovered v13 Life/reticle QA

These results were rerun on the recovered workspace. They are not inherited
passes from the disconnected/lost computer.

## Fresh executed evidence
- Shell VM regression passes: Life open/close/refresh, no runtime, Sandbox,
  empty cohorts, malformed JSON, literal unsafe strings, large parent IDs,
  optional structure and biological-light labels. Uses textContent, no HTML injection.
- Actual native engine at320x700 and390x700, real MainMenu Origin click and Seed
  action on normal generated habitat. Paused state and seed20261113 match the
  before/after visual variants. Only the test copy can enable old-ring baseline.
- All4 native runs succeeded. Actual read-only export contains4 slots, one live
  seeded lineage1/parent0 with0.02kgC/m², structure0,20°C,2.441m water,
  nutrient0.018kg/m² and biological light0. The lit viewing aid is not biology.
- Toggling stableDaylight produced byte-identical complete snapshot JSON.
- Reviewed fresh320/390 after screenshots and320 before screenshot: compact32px
  selection corners replace the large yellow ring; actual seeded mat is legible.
  It is a selection indicator, not a claim about brush radius or organism size.
- Evidence in `evidence/reticle-life-recovered` includes PNGs, logs and actual JSON.

The recovered host default native target hit LLVM AVX512/evex512 failure;
explicit `-Dcpu=x86_64_v3` recovered the build without model/source semantics changes.
Reproduce with `egl-life-visual-prepare.py`, `egl-origin-menu-build.zig` and the
v3 CPU option. `QA_WIDTH=320/390 QA_HEIGHT=700`; set `STELLA_VISUAL_BASELINE=1`
only for the old-ring comparison. Test-only native bridge removes the browser
platform gate from read-only web exports; production guards remain unchanged.

Actual HTML Life-sheet visual/scroll/touch review belongs to integration preview.
Native EGL is not proof of physical Android WebGL performance. No new taxonomic
class, full historical tree, unbounded memory, evolution to plants or animals,
or long-term survival is claimed by this presentation layer.

## Managed-browser HTML dialog QA (fresh recovery)

Executed official sites-preview + CUA Chrome on an isolated /workspace preview copy. Actual built WASM initializes, but Play produces `WindowCreationFailed` in this cloud browser. No browser gameplay claim.

Then used the production shell with the actual native-export JSON fixture (explicit MOCK banner), inside a 320x700 iframe. Verified More → Life, readable wrapped conditions/cohort/biological light, Refresh, vertical scrolling to glossary/history caveat, sticky Close, close focus returning to More, and reopen. No horizontal clipping observed. At 390x700 repeated with explicitly synthetic four-cohort stress fixture derived from the real JSON: all four rows reachable through scrolling, sticky Close remained accessible, Refresh and Close passed. Screenshots visually reviewed in CUA output. Production source was not modified for fixture; no synthetic data is shipped. These are HTML layout/control checks, not physical Android performance or browser simulation proof.

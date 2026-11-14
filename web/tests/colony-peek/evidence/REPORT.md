# Watch: pinned colony peek

Isolated from current main, no production edits or deployment. Changes only play.zig,
save_game.zig (transient reset), and new pure colony_peek.zig.

## What changes
A deliberate Watch+Inspect tap pins that patch, instead of immediately covering the
planet with native Surface details. Existing84px footer becomes a compact observation:
largest living cohort's expressed form, its actual share of local living biomass,
and same-lineage biomass change since the tap. A four-cohort stacked share bar uses
the existing map thermal palette (NOT fitness); separators distinguish equal-color
cohorts, and largest share has an outline. Exact current lineage details remain
available through existing Surface details / Life snapshot.

Details and Dismiss each have44px height. Details reuses native Surface inspection;
a short key explains bar/color. Dismiss restores the original Day/global counters.
Existing arrival trails, loss crosses and legend above footer are preserved.
No added area covers the planet. Pin is independent of subsequent cursor/pan position.
Tools exits clear it; new worlds start empty; load explicitly clears it.
No painting/touch handler changes outside Watch+Inspect.

## Honest observation model
Only four current cohorts and one four-cohort baseline, exactu64 lineage identities.
Shares are biomass fractions, not success, fertility or fitness. Baseline is pinned
time, not a sliding window. Wait at least two simulated days before reporting a
same-lineage increase/decrease. Steady means within1% of baseline biomass.
Dominant-lineage change reports turnover, not mutation, adaptation, selection or a
causal competition claim; remains changed until repinned. Empty/lost colonies cannot
be described as growing. Invalid times/time rewind reset. Existing data is read only.
No RNG, model edits, assets, global scans, additional events or telemetry.

## Executed validation
31 pure/helper model tests passed, including actual shares, same-lineage increase/
decrease, turnover, empty/replaced/invalid cohorts, no input mutation and rewind.
Native actual saved30day world42, then120 real fixed-step updates (two simulated days):
lineage1 biomass0.021936815, share55.44127%; other lineages25/15/39 shares
9.86457%,16.31063%,18.38353%. Correctly reports same-lineage biomass down.
This is current corrected-film engine advancing an existing saved world, not an
injected ecology or visual-only demonstration. No claim of cause or guaranteed fate.

Before actual simulation advance, pin/read/render kept complete serialized save
byte-identical at each viewport. World-load transient reset passed.
Initial native captures320×700,390×700,700×390 showed ten/ten/seven actual visible
living markers. Actual real pointer press/release Details/Close/Dismiss tested.
Final refreshed capture/log status recorded below.

Known limit: nativeEGL/mobile path, not actualAndroid browser performance. No new
Chromium attempt (known OS socket block). Existing unrelated allocator teardown
warning occurs at exit0; not a leak-free claim. No WASM run by this worker yet.

## Final gate (all final source)
Native ReleaseSafe rebuilt final time-window/color/key/separator refinements.
All three runs exit0, all pointer Details/Close/Dismiss assertions and load resets pass.
Final PNG evidence: results/{320,390,landscape}/peek-006.png.
320/390 portrait and700×390 landscape visually inspected. Footer remains84px,
buttons44px, no new overlap with above-footer event cue. Final label reads
“Top mat55% · biomass down over2.0d”; no rate or causal claim.

Exact full-save invariance before ecology advances:
320:10,780,377 bytes, Wyhash3f6c2f301fa7cd2e
390:10,780,363 bytes, Wyhashd753c639f8207afd
landscape:10,780,370 bytes, Wyhashf2d07435ee21d802
Viewport-specific camera state explains different complete-save hashes.
After two actual simulation days all viewport runs have identical reported cohort
biomass/shares. No state change attributed to peek. Snapshot reads do not alter time,
resources, cohort IDs or RNG. Main/default files untouched.

Patch SHA256 c34e3ac63886214d7c54917ceea3f9e4675c319726abfa866bd5e271f3d959b8.
qa/prepare.py uses STELLA_SOURCE_ROOT and current shipped nursery/fit QA dependencies.
qa/replay.part loads QA_REPLAY_SAVE (tested /tmp/v20-seed-42.json), actual oldworld
world42 center29254. STELLA_ORIGIN_WIDTH/HEIGHT choose captured viewport.

# Blender aquatic-form atlas prototype (isolated)

Original procedural Blender artwork for the six existing aquatic architecture
classes: mat, cushion, rosette, ribbon, branching, canopy. These are not taxonomy,
terrestrial trees or proof of evolved organisms. Runtime chooses the exact
existing Microbes.producerForm of the actual dominant living cohort and uses
actual biomass/visibility/decluttering. Existing thermal-lineage palette is
multiplied through NanoVG image paint; no arbitrary form-based color trait.

Reproduce with installed Blender4.3.2:
  blender --background --factory-startup --python build_forms.py
  python3 package_atlas.py

No downloaded art/fonts/models. Existing repository GPLv3 and credits unchanged;
new original scripts/art are intended for this GPLv3 project. Source .blend and
procedural recipe retained. Cycles32CPU samples, transparent RGBA, fixed camera
and lighting. Blender build lacks OpenImageDenoise, so denoising deliberately off.

Artifacts: aquatic-forms.blend; six renders/; geometry-report.json; packed
576x384 aquatic-forms-atlas.png; legibility-sheet.png at40/32/25pixel tiles.
Alpha-bounds normalized to172px inside192px tiles, bottom-root anchored at182px.
Geometry144–780 triangles per archetype is baked OFFLINE, not sent to the game.

Runtime scope: one RGBA atlas884736 bytes (0.844MiB), no mipmaps; at most64 visible
colonies from existing cap, up to3 sprite rectangles each for existing dense
biomass groups. These are quad counts, not measured drawcalls. Actual framecost
still needs mobile profiling. No 3D mesh/terrain pipeline or engine rewrite.
Sprites are camera-facing screen-space schematics, not volumetric submerged
models; existing hemisphere/viewport/LOD filtering remains. Water draws before
UI markers, effects after plants. Fixed baked light is illustrative, not part of
photosynthesis or actual sunlight. Asset loaded once; missing/corrupt/wrong-size
atlas retains existing vector forms instead of crashing.

Native fixture explicitly seeds six synthetic trait combinations in real cells
only to compare rendered forms. It is NOT evidence of evolution. Same fixedworld,
camera, pause and contents in before/after; different shader/model state is not
used to make the atlas look better. Additional actual root-picking/heat receipt
and fallback checks are recorded separately. No main source changes or deploy.

## Verified candidate QA (2026-11-14)
Native build and ReleaseSafe WASM build passed. Final same-world paired image:
results/stella-atlas-native-comparison.png (vectors left, atlas right). The six
fixture forms remain recognizable, with noticeably faceted volume; canopy and
mat still have similar low profiles at this angle, so this is an art improvement,
not a claim that every small form is easier to identify than the vector version.
RGB-only four-pixel transparent edge bleed avoids dark filtering fringes; alpha
is unchanged. No opaque tile rectangle or apparent halo in reviewed native images.

All six native runs completed: original vectors, atlas, actual heat-receipt
overlay, missing asset, corrupt asset, wrong-size asset. Each verified a click at
the projected root selects the same real cell, paused=true and simulated_time=0.
This tests the ROOT, not an expanded full-sprite hit area. Actual heat overlay
stays above the sprite, with an honest heat receipt and no asserted casualties.
Asset failures warn once and continue with vectors. Original asset restored and
byte-compared after failure tests. Existing shutdown GPA leak diagnostics remain.

Runtime source tested SHA256:
15ad7d8f6eb5943f95e9bded4ccc9686a8ce660b1789fce1beeba007aeab82bf
Atlas SHA256:
9da31521a93267e6a334ae74c450b6e5a3a89cf24b1e88bb404eec8049e4a7e5

runtime-atlas.patch contains ONLY fields, loader, sprite drawing and callsites;
it explicitly excludes newer production Fitlife code. git apply --check passed
against current main, but it has NOT been applied. Copy the PNG into assets and
rebuild normal embedded assets when integrating. Keep source scripts/blend and
license with the checkpoint. Native fixture scripts live in game/web/tests.

Remaining acceptance: real-phone graphics/frame cost and touch interaction,
current Fitlife integration, and actual evolved-world comparison (not the
synthetic six-form fixture). Sprite overlap/decluttering is existing behavior.
The fixed baked art lighting is not a dynamic simulation sun. No deployment.

## v22 actual-world acceptance
Newest replay baseline is commit7a1a51a, without changing main. Six paired cases
use actual saved day30 worlds42/2027 at320×700,390×700,800×400, without injected
forms. Vector versus atlas has identical camera/distance/time/pause/pace,
8/8 visible patches for42 and5/5 for2027 after Fitlife. Every projected living
cell centroid passes the real pointer/Inspect callbacks. Full state/resource
hash remains42=c957a0149e8f9813 and2027=d5cab3d03314df03 after normalizing only
camera changes. Evidence and original save SHA256s in results/actual-fit/.
Raised, staggered canopy collector pads now differ from mat in actual evolved
world2027; branching remains separately covered by the synthetic six-form test.
Art is a schematic form interpretation, not a new morphology/physiology trait.

Reviewed actual portrait and landscape pairs: no clipping or halo, patch counts
unchanged, readable mat/cushion/rosette/ribbon/canopy silhouettes. Phone frame
cost is unmeasured. The palette remains actual thermal lineage tint; amber dots
remain actual existing feeding indicators, not new art-derived status.

The loader now explicitly gl.deleteTextures ONLY for a freshly unregistered
rejected texture (before cache insertion or NanoVG registration), since existing
Texture.deinit is a TODO. Native diagnostics assert GL texture exists before
and does not exist after each deletion. Three repeated wrong-size loads pass;
repeated valid cached lookup passes without deletion. Shared cache is untouched.
This correction was included in the narrow runtime patch and subsequently integrated in v23.

qa/prepare.py reproduces Fitlife native replay and adds native-only ownership
assertions. STELLA_ATLAS_BASELINE=1 selects original vector comparison;
QA_REPEAT_ATLAS_LOAD=1 retries loader each rendered frame for ownership checks.
The PNG has a base64 transport copy aquatic-forms-atlas.png.b64; full .blend,
procedural build_forms.py and package_atlas.py remain the editable source.

Full current-v22 web/build.sh Emscripten+static packaging passes. Initial isolated
run lacked root LICENSE copy (packaging only); copied unchanged upstream LICENSE
and reran successfully. Final index.js preload entry /assets/aquatic-forms-atlas.png
is bytes546..170043. Reassembled assets-*.bin slice byte-compares equal to final
PNG SHA2563aaec4b988f0d12d5401d081eaa7899f04f76a18d07827723c0b764ee47b42d6.
Proof JSON saved with actual-fit results. Final WASM1276223bytes. This is packaging
verification, not a claim of browser WebGL playback or Android profiling.


## Integrated v23 acceptance
Integrated main passed actual world42 at320portrait and800landscape with identical resources, eight Inspect hits, pause/time preserved and three new-world texture-cache reuse transitions each. Final fallible NanoVG registration has injected-allocation-failure coverage under ../atlas-registration. Earlier first combined build caught a reversed Fit-feedback patch; restored before final tests/publication. Phone performance remains unmeasured. Source/generator is now assets-src/aquatic-forms; runtime PNG assets/aquatic-forms-atlas.png.

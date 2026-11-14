# Original aquatic archetype art

Six Blender-authored forms express the existing inherited producer morphology:
mat, cushion, rosette, ribbon, branching and canopy. They are aquatic forms, not
new taxonomic species or proof of terrestrial evolution. Original procedural
meshes/materials; no third-party art. Distributed under the repository GPL-3.0.

Regenerate with Blender 4.3.2:

    blender -b --python assets-src/aquatic-forms/build_forms.py
    python3 assets-src/aquatic-forms/package_atlas.py

Packaging requires Pillow, NumPy and SciPy. It trims alpha bounds, retains a
consistent root anchor, and bleeds only transparent RGB to avoid sampling halos.
Output is assets/aquatic-forms-atlas.png, embedded by the normal web build.
The .blend is editable source; geometry-report.json records source triangles,
not runtime polygon counts. Runtime uses a single 576×384 RGBA image atlas,
0.844 MiB decoded; existing colony cap remains64. The image is camera-facing,
not a live 3D mesh. Lighting is baked; lineage tint remains simulation-derived.

See web/tests/blender-atlas for actual native comparisons and limitations.

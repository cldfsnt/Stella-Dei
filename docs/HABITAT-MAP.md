# Habitat map context

Browser Habitat focus uses 900 km surface-relative context rather than 300 km. On a 40,962-cell, radius 5,000 km world, this shows roughly eight cell scales across a 390×700 portrait, instead of 2.7. User zoom remains available; desktop camera behavior is unchanged.

Normal browser map view uses faint 1 km contours and colors derived from interpolated real vertex terrain altitude, existing water, vegetation and temperature. Vertex altitude avoids chord-sag errors from taking the radius after interpolation. This adds no terrain resolution, texture assets or fabricated ecology. Heatmaps and desktop rendering retain their original branches. Biology markers remain bounded fixed-screen-size schematic icons, not physical spatial footprints.

## Acceptance

The integrated native EGL build rendered normal and temperature views at both 320×700 and 390×700. Actual callbacks picked the same central cell, set its water to 3 m, rejected stale selection and invalid 6 m targets without mutation, applied +0.1/-0.1 m edits, and zoomed out/back. The Life snapshot export left microbial cells, statistics, gases, time and selection unchanged; display-light changes did not alter exported simulation light. The normal view shows useful surrounding coastline/elevation context and readable controls at both widths. The uniform initial temperature heatmap remains uniform, without normal-view contours.

The actual EGL ES3 shader pair compiled and linked. These are native software-rendered acceptance checks, not physical Android performance or browser WebGL proof. The harness still emits an existing GPA teardown leak warning; it is not a memory-clean certification. HTML target-water controls are checked separately from these native callbacks.

Public reproducers: `web/tests/egl-habitat-map-prepare.py` and `web/tests/gles-terrain-check.py`. Run the latter with the shader directory as its argument. The native preparer extends the existing Life visual harness in an isolated source copy. Browser packaging/build checks remain a separate gate before publication.

# Fixed local hydraulic expression probe, no model patch

Use all unique directed neighbor edges in the same three frozen worlds. Reproduce current scalar f32 operations elevation+(mass*km_per_mass), subtraction/routing and height-limited single-edge proposal with fixed sharefraction0.0048 (dt1440, one illustrative subdivision). This is a local arithmetic proxy, not actual scheduler aggregate transfer: in-engine source scratch state and SIMD no-self-vector guards also matter.

Compare f64 difference-before-add on EXACT SAME represented f32 elevations and depths, with same mass/shared cap. No new physical precision or water invented. Record route/sign disagreement and proposed transfer differences, separated shallow source<0.2m and all edges.

Fixed positive synthetic source-depth additions1,2,5cm: first convert to native mass and roundf32, then currentf32depth. Distinguish lost at source-mass representation, represented depth change lost in radius-scale head sum, and visible transfer effect after shared cap. No negative/clipped perturbations or after-result threshold changes. Also use a plainly synthetic equal-terrain/equal-depth pair at fixed12352 scale as an explanatory boundary witness, not actual habitat discovery.

No world reruns, biological changes, persistent modification, or assumption that numerical sensitivity alone fixes topology/habitat. Preserve zero-effect cases and coarse terrain limitations.

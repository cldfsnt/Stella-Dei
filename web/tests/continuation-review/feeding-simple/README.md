# Attribution: marker work, not selection correctness

All native actual-world gates pass, exact full-save equality across all modes and original restore, selected root/body edges, back-face exclusion and64glyph cap. This run retains native per-draw diagnostics; do not infer shipped-web cost from it. A follow-up convex candidate explicitly switches both arms to shipped debug=false.

Median ms per paused presentation frame, modes0=v57,1=v58,2=selection-correct v58 with original dot(attribution only),3=concave12vertex outlined band:

- Close mixed:12.255 /14.103 /11.655 /13.590.
- Close dominant:12.388 /14.715 /11.666 /13.786.
- Globe mixed:14.197 /14.274 /14.070 /14.941.
- Globe dominant:13.464 /13.649 /12.830 /13.116.

Selection-only keeps v58 emitted glyph counts and picking yet returns near/below v57 timings in both close scenes. This implicates history-marker rendering rather than selection-priority mechanics in measured cost. Concave band helps only modestly, with mixed globe results; do not promote from this alone. Actual close candidate capture inspected: history band/ring distinction and producer forms clear, but performance merits another bounded candidate. No production edits. All trial rows, hashes, compressed full logs, preregistered order and time window preserved. Same native EGL limitations as prior regression report; no Android/laptop/WebGL or running-simulation speed claim.

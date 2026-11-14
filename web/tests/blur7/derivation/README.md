# Seven-sample blur feasibility, analysis only

Existing blur: center0.227027, plus/minus1.5*0.1945946,3*0.1216216,4.5*0.054054,6*0.016216. For a pixel-center sample and linear filtering, the positive-side integer coefficients are .0972973,.0972973,.1216216,.027027,.027027,.016216.

Combine adjacent discrete terms:
- offset1.5 weight.1945946 (unchanged)
- offset3.181818059504092 weight.1486486
- offset5.37499710935874 weight.043243
with mirrored negatives and unchanged center. This is7 rather than9 texture samples, preserving mathematical convolution. Total kernel weight .9999994 is deliberately unchanged; normalizing would alter existing output.

Clamp-to-edge does not invalidate this linear grouping: extend discrete samples with endpoint values first, then interpolation distributes over their weighted sum. Exact Fraction reference confirms equality on2340 deterministic random HDR cases with lengths1,2,3,4,5,6,7,8,17,64, including all edge centers. kernel.py/proof.txt reproduce.

This assumes exact pixel centers in a same-size fullscreen pass, GL_LINEAR sampling and the existing CLAMP_TO_EDGE. It does not prove GPU equivalence: actual interpolator weight precision, normalized coordinate rounding, arithmetic ordering and intermediate half-float quantization may differ. Multiple4-pass propagation must be measured, not just one horizontal pass. No production or shader changes made.

Next isolated experiment should compare original/candidate on HDR impulses at every boundary/axis, checkerboards, gradients and constant sources; record intermediate float max/RMS error and final display-byte changed-count/max, across390x700/920x700 plus tiny/odd sizes. Include real bright sun/rabbits, maps and bright transitions. Only then paired ABBA stage timings and user-visible judgment, explicitly not claiming bit-exact if differences exist. No reduction in resolution, pass count or effects. Four blur passes go36→28 texture fetches per pixel, not a prediction of22% frame speed improvement; total post includes extraction/composite and driver waits.

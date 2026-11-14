# Seven-tap full-resolution blur candidate

Isolated against v28; no main edits or publication. Only drawBlurredTexture changes. Same full-size HDR targets, four blur passes, extraction/composite, bloom eligibility, atmosphere, effects and simulation. No claim of bit-exact HDR or mobile speed.

## Derivation
Existing positive discrete coefficients after linear interpolation: [.0972973,.0972973,.1216216,.027027,.027027,.016216]. Combine adjacent1–2,3–4,5–6 into weights .1945946,.1486486,.043243 at offsets1.5,3.181818059504092,5.37499710935874. Mirror negatives; unchanged center.227027. Sum.9999994 deliberately preserved. Clamp extension preserves mathematical linearity. Exact rational2340case derivation in derivation/. Actual GPU interpolation, half-float storage and arithmetic ordering differ.

## Real GL synthetic evidence
qa/synthetic.py creates surfaceless desktop GL llvmpipe. Actual RGBA16F/HALF-FLOAT-equivalent storage, GL_LINEAR/CLAMP_TO_EDGE, four alternating passes read back each intermediate float result, then actual original tone-map composite to RGBA8. Same shaders as game; fullscreen triangle instead of game's quad. No real WebGL/phone driver claim.

First36cases: sizes1x1,2x3,7x9,31x33,390x700,920x700; constant/checker/ramp/edge/impulse/fractional-position impulse; HDRpeak10. Composite over original input. Final display bytes exact; HDRmax.00390625.
Expanded144cases: same shapes/sizes, peaks1.01/2/10/100, sensitive black composite base. Five cases differ in final display,33 RGB components total, maximum1/255; largest12components out of1,092,000 in390x700 ramp. Intermediate/final HDRmax.03125 atpeak100; maximum fourth-pass RMS.000124781. This is small rounding, NOT exact equivalence. Script asserts final max<=1; JSON preserves all per-pass errors. First script retained separately. Mathematical nonnegative symmetric kernel prevents new support/ringing, but platform precision still needs integrated browser review.

## Actual game paired visual/model evidence
Native build exit0; both390x700 and920x700 initial and repeat processes exit0. Same-binary shader swaps across ten map/atmosphere combinations, visible-rabbit fixture (adding rabbit changes pixels), actual HDRsunpeak9.96875, bright return and day/night. Every paired display framebuffer is byte-identical (changed=0,max=0,RMS=0). Serialized model unchanged. Sun original/candidate PNGs manually inspected: identical halo, edge and background appearance. Map pixel equality provides exact checked-frame evidence; initial generic capture rabbit-map.png is a pre-fixture startup frame, not claimed rabbit screenshot. No whole-game completeness claim.

## Timing, not a phone promise
Two2-second ABBA windows per size, same binary and scene, final glFinish each frame. Native llvmpipe software renderer, CPU submission and wait wall time, not hardware GPU timestamps. Paused Sandbox Normal stable orbit, one rabbit; full bloom. Shared machine/order noise remains.
390 initial original medians14.46/14.37ms vs candidate13.46/12.55; repeat15.54/14.90 vs13.49/14.34.
920 initial28.26/33.52 vs24.85/25.42; repeat29.60/28.31 vs26.00/26.14.
All paired-window medians favor candidate, supporting useful native throughput improvement. Tails do NOT consistently improve:920repeat candidatep95=49.5/68.7ms versus original42.3/37.8ms, maximum111.7ms candidate vs83.8ms original. Do not promise smooth frames,22% game speedup, or Android gain. Nine→seven samples is22% fewer blur fetches, not22% less total work.

## Scope, reproducibility and remaining gates
Patch/hash in HASHES.txt. qa/prepare.py uses actual checkout, copies frozen baseline/candidate shaders, adds runtime swaps and readback only in isolated copy. Build via web/tests/egl-origin-build.zig. QA_SB_SHADER=1, deterministic seed42 and forms single; STELLA_ORIGIN_WIDTH=920 selects wide case. Workspace capture directory must exist. qa/README.md details commands. Existing native shutdown GPA warning remains. Two initial QA compile errors (unused hash vars, const deinit receiver) fixed; logs retained. Production shader untouched by these fixes.

Recommend narrow candidate for integration given exact actual-game display frames, negligible bounded synthetic display difference and repeated lower native medians. Still require full WASM compile, integrated current-tree pixel/model/clock/save gate and live browser check. No code weakening of eligibility/quality or simulation.

Final packaging adds requested derivation comment and removes unused BLUR_KERNEL_SIZE macro. No other shader tokens changed; tested-before-comment shader retained. Final commented shader synthetic144case rerun passes same error bounds. Native actual-game binary tested pre-comment version; integrated gate should compile final shader. Frozen baseline.fs SHA c951c29e8f60aa8348a0c2b31c7875fba1848c65456935bd71f0b84594997472 is always copied by QA, regardless of checkout's current candidate.

## Additional real OpenGL ES3 evidence (important platform caveat)
Static glslangValidator unavailable; not installed/bypassed. qa/synthetic-es300.py instead creates actual OpenGL ES3.2 Mesa25.0.7 llvmpipe context, compiles adapted ESSL300 shaders, usesRGBA16F targets and checks GL errors after readbacks. First ES fixture failed because RGBA8 texture was incorrectly allocated withFLOAT type; corrected toUNSIGNED_BYTE, failure retained. This was a QA format mismatch, not production shader failure.

ES300 precision produces MORE differences than desktop330:144cases pass maxdisplay1/255,50cases change,156,306RGBcomponents total. Worst single case44,283/1,932,000RGBcomponents=2.29% (920x700 ramp). HDRmax and worst fourth-pass RMS.1875 arise in1x1constant100; tone-mapped display remains identical there. Do not quote desktop33changedcomponents as an ES/phone result. Real ES3 context still is NOT a browser/WebGL implementation or Todd's GPU.

Reviewed920x700 ES ramp original/candidate, threshold-edge glow original/candidate and fractional impulse original/candidate at normal scale: no discernible added banding or halo-shape artifact. A64xamplified difference image exposes sparse patterned1-level quantization on ramp; it is not visually exact. These results support negligible tested display error, not universal equivalence. Selected originals/candidates/difference PNGs included. Current additional actual-game ESSL300-adaptation test status is recorded in integrated report separately.

Supplemental actual-game ESSL300 adaptation completed after integrated gate:390and920 processes exit0, browserRGBA16F/depth32F formats on desktopGL context. Maps differ by only1–4components at390, sun48components390/46at920, all max1/255; no discernible halo change in viewed original/candidate sunPNG. Night pixels exact, model unchanged. This is additional precision evidence, not actualWebGL gameplay. Integrated report/logs preserve exact scope. No known shader/runtime failure remains.

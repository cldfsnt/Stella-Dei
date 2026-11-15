# Opt-in 3D resolution: measured quality/performance tradeoff

Isolated experiment, not automatically selected. Sharp100% remains default. Reduced75% and Low50% change only scene/bloom framebuffer pixel dimensions; final HDR composition, NanoVG controls, text and colony glyphs remain at the original canvas size. Simulation terrain grid, ecology and save schema are unchanged. Browser currently uses stage CSS-pixel dimensions already, not an inflated devicePixelRatio buffer. No preexisting user-facing resolution control was found.

## Measured result

Native EGL llvmpipe browser-policy proxy, current v45 engine, 40,962 terrain cells. Early nursery and naturally established30day QA world. Three repeats per100/75/50% at1366×768 and390×700; alternate order in second repeat.12 warmups+60frames for paused/Grow6/target24. Not Android, browser WASM or hardware laptop measurements; fixed input delta isn't measured browser achieved pace.

Established laptop total frame medians (100/75/50%): paused16.484/14.172/13.090ms; Grow19.387/17.677/16.115ms; target24 27.979/24.328/22.972ms. Render+finish target24:17.712/14.481/12.746ms. Mobile390×700 gains smaller: Grow10.515/9.990/9.382ms; target24 18.052/16.822/16.843ms. This setting helps pixel-bound rendering, not expensive simulation or arbitrary stalls. Full results include all conditions, not only favorable rows.

All72 lower-scale-vs-sharp complete-world hash comparisons and216 ray-picking comparisons match. Dimension unit test covers1pixel and prevents zero-sized targets. `comparison.png` was visually inspected: unchanged crisp UI/glyphs, visibly softer/jaggier terrain edges at lower resolution. This is an explicit quality tradeoff, not pixel-equivalent optimization. Existing GPA teardown warnings persist.

Prior sharp screenshot comparison against an older *different* geometry acceptance sequence matched4/6. That old sequence exercised intervening terrain/queued-load fixtures before its cached-world capture, so it is not a controlled default comparison. Do not use it as proof either way. Same-run runtime100→75→50→100 acceptance is recorded separately below.

## Candidate API and limits

Unapplied candidate/production.patch adds session-only shared render_scale module, Sharp100 default, invalid inputs rejected, dimensions bounded>=1 using wide integer arithmetic. Setter accepts100/75/50, returns1 accepted or0 invalid/no active world, and marks active diagnostics interrupted on real changes. Getter reports current session choice. It is not saved in planets or disk and does not unpause/advance simulation.

Framebuffers still use the existing allocation/error path (`catch unreachable` on failure); this work does not add graceful GPU allocation fallback. Switching scale may cause a one-frame allocation hitch. Native viewport acceptance uses a logical resized viewport inside fixed EGL storage, not a browser window/context-loss test. Actual browser export/control integration and build remain main-thread work.

## Runtime candidate acceptance completed

32 actual FBO cases: early and natural30day, logical viewport1366×768→390×700→700×390→1366×768, each100→75→50→100. Actual scene dimensions match the module; canvas/UI dimensions stay unchanged by scale. Complete saved state and three ray picks per case match across scales. All8 restored100 screenshots are byte-identical to initial100 in the same viewport/world group. Two pure module tests pass, including invalid values, signed-independent dimension bounds,1pixel and integer overflow boundaries. The signed export rejects negative values before conversion; no active world returns0.

The initial runtime fixture build used signed GLFW dimensions and failed compilation; corrected explicit casts only in fixture. Failed build retained for provenance. No production code was applied by this worker. Main thread owns applying the patch, adding the two Emscripten exports, browser UI tests and deployment. Tests do not validate actual browser context loss or guarantee GPU allocation recovery.

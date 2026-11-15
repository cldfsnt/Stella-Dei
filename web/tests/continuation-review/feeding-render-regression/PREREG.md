# v57/v58 paused presentation-frame regression proxy

Compare exact released renderSprouts bodies b308b37 / be1abc8 in one existing EGL browser-policy native harness; all other code is identical frozen QA base. This is a narrow renderer change regression test, not an entire-release benchmark. Actual natural-day60 input is restored independently for every arm. Actual living mixed and dominant patches are used, not invented cohorts.

390x700, close and default2.5radius globe views. Each patch/view has six arms alternating false,true,true,false,false,true. Each arm has20 warmup and120 timed real cooperative pump/render/gl.finish/swap frames. Simulation is paused: no update/physics speed claim. Console, JSON, screenshots and target assertions are outside measured loop. First12 shim captures happen before measurement. Exact paired full-save equality and original restore remain required; images deliberately differ because this is the released readability feature. At most64glyphs, selected root/edge picks and back-face rejection retain prior acceptance.

Report per-frame times and all paired variation, not just best run. Native software EGL is not browser WebGL, laptop or Android evidence. No fixed-device FPS assertion or automatic regression cutoff from these noisy proxies. No production edits.

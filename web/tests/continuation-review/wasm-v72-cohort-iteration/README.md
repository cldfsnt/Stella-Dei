# Live-v72 cohort-loop copy: correctness passes, performance held

One isolated change iterates `&cell.cohorts` rather than the cohort array value in the photosynthesis-potential loop. Each cohort is still a value capture; no genuine simultaneous snapshot changed. Production remains untouched.

## Fixed correctness

All 34 imported microbe tests pass. On both inputs, baseline/candidate complete serialized state including RNG is byte-identical after 72 actual scheduler ticks. Each arm independently passes new-Node-process 72+10 versus uninterrupted 82 ticks. Timed endpoints also equal those gated hashes.

The dense input is a genuine player Auto-seed intervention: 54 prior survivors plus 7,933 resource-paid seeds, not a naturally evolved population. Initial living/occupied/active counts are 7,987/7,949/7,952; after72 they are13,430/8,548/9,357. The early archived natural30 input starts18/10/11 and ends22/13/15. `active` means living or positive detritus. Inputs are imported into current v72, not asserted to be unbroken current-model natural trajectories.

DWARF archive disassembly proves the exact 320-byte memcpy at microbes.zig:144 is absent in candidate. Validation/serialization copies remain. `copy-proof.json` deliberately retains surrounding broad 320-constant matches, including offsets that are not memcpy lengths; it is not a count of all runtime copies. Final linked WASM contexts are also retained.

## One fixed ABBA, no gain

Each process runs12 warmup ticks then60 timed full Planet.simulate ticks. Startup, parsing, saving, rendering and restart tests are outside the timer. No instrumentation or repeated favorable screen. Both workers explicitly released CPU; a process check found no compiler/native/profile jobs before execution. Timing:2026-11-15 19:44:01.004–19:44:18.772 UTC.

Dense paid population: baseline23.563643 versus candidate24.306151 ms/tick median, **+3.15%**. Early sparse:18.122739 versus19.547300, **+7.86%**. Pair ordering is noisy (one candidate faster than its adjacent baseline in each scenario); this small screen does not establish a robust slowdown either. It establishes **no demonstrated speedup**, despite verified copy elimination. Hold production promotion. No further variants/repeats in this pass.

These are actual Node/V8 WASM scheduler measurements, not browser rendering or mobile/device performance. All samples and negative results retained.

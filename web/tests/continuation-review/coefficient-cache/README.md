# Exact atmospheric relaxation cache (research only)

This is an isolated copied-source candidate, not a released production change. It memoizes only relaxation(dt, 1 / total_rate), keyed by the exact f64 bits of both arguments. Current vapor mass still enters the original multiply/divide and f32 downward donor bound on every call. It does not freeze geometry, wind, transport rates, biology or timesteps. Invalid inputs retain the original return behavior; allocation failure falls back to the original computation. Payload is 24 bytes/cell, approximately 0.94 MiB at 40,962 cells.

Three alternating baseline/candidate native EGL runs used the same naturally evolved 30-day, 40,962-cell world and 60 actual 1,440-second updates after 12 warmups. Median update time was 9.8590 → 9.4475 ms (4.17% lower); one of three pairs was slower. The targeted coefficient stage median was 0.7158 → 0.3114 ms/tick. Cache hits were 2,432,280 / 2,457,660 (98.97%). These are software-GL native proxy timings, not a phone/browser speed promise or a universal major improvement.

All nine serialized whole-world comparisons were byte-identical: ordinary measured run, real raise-terrain action, axial tilt, water adjustment, save restoration, changed timestep, changed rotation period, explicitly perturbed wind, and another save restoration. The perturbation fixtures deliberately exercise inputs rather than assert that every input must change every local key. Full-state hash pairs are in final-parity.log.gz. No target-total corrections or widened tolerances.

Native helper comparisons: 300,252 exact f32 cases plus six atmospheric regression tests passed. Freestanding wasm32 ReleaseSafe helper: 101,048 exact f32 cases passed, including zero, negative, extreme, NaN and infinity values. This tests actual WASM numerical behavior, not browser performance.

## Early/cold gate

A separate fresh-world pair skipped all warmup frames and included cold initialization. Both early and 30-day complete serialized states were byte-identical. Early hit rate was only 694,377 / 2,457,660 (28.25%); mean update was 9.4148 → 9.6057 ms (+2.0% in one pair). First update was 18.3940 → 10.4690 ms, so this run did not expose an allocation spike. The same naturally developed world at 30 days measured 9.5870 → 8.9954 ms (−6.2%), with 98.97% hits. This single additional pair is a correctness/cold-behavior gate, not a precise regression estimate. Process maximum RSS was 219,280 → 220,540 KiB (+1.23 MiB).

Recommendation: retain as a candidate, not an automatic production promotion. Mature-world savings are modest and early low-hit operation can add overhead. Repeat representative early and browser workloads before deciding the tradeoff. Existing native allocator shutdown diagnostics remain visible in logs.

## Reproduction

Freeze the v44 source (5f52002) and run `egl-cpu-resolution-prepare.py` to create an instrumented base source. `egl-cpu-coefficient-prepare.py BASE CANDIDATE` creates the isolated cache copy. Apply `egl-cpu-coefficient-replay-prepare.py` to each to create replay sources; build each with `egl-propagule-visual-build.zig` and its `-Dsource` argument. The runners here accept one absolute work directory containing `replay-base-build/bin/stella-egl`, `replay-coefficient-build/bin/stella-egl`, and `save.json` (the actual 30-day generated save). `run-established.py` performs three alternating pairs and all eight perturbations. `run-cold.py` generates independent fresh worlds with no loaded save and checks early plus 30-day states.

The WASM source fragment imports the generated helper; build it as wasm32-freestanding ReleaseSafe with no entry and exported `parity_run` / `parity_count`. It is numerical acceptance, not a rendered WASM timing measurement. Source hashes below pin the actual frozen tested copies. No production source or save schema was modified.


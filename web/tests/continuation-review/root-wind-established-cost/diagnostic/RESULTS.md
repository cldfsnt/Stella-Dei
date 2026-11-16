# One bounded stage attribution pair

Coordinator-approved one off→enabled pair on exact seed1337 inputs,72steps (12warm/60measured), 2026-11-16 00:54:29–00:54:35 UTC. No per-cell clock calls; one tick-level boundary around each phase and one around entire birth/routing pass. No model arithmetic change. Both full endpoint hashes exactly match uninstrumented accepted references. No repeats.

| Stage | off ms/tick | enabled ms/tick | difference |
|---|---:|---:|---:|
|temperature|2.24994|2.48940|+.23947|
|liquid/wind|3.30033|3.70830|+.40797|
|land phase/transport|20.73082|23.78762|+3.05679|
|misc/rabbits|.00070|.00085|+.00015|
|microbes total|.90720|1.38951|+.48232|
|birth/routing (subset of microbes)|.01258|.02206|+.00948|
|total|27.19489|31.38221|+4.18731|

Do not sum the birth subset twice. Direct birth/routing is too small in this diagnostic to explain the measured total difference. Largest difference is in shared land column/transport, with increases elsewhere too. Inputs initially differ only genetic allocation/wind config; their biology and atmospheric/resource trajectories then diverge, so shared source does not imply identical operands. This evidence cannot establish whether variability, changed physical operands or compiled/JIT behavior explains the remaining cost.

Instrumentation changes generated code. Totals are19.29% and15.52% below the earlier accepted off/enabled medians, respectively, despite adding clocks: simple subtraction is NOT a reliable instrumentation-overhead estimate. This pair is distribution evidence only, not a new performance pass or replacement for the retained +10.25% original seed1337 result. No optimization justified solely by this pair.

Work populations/serials/full stats remain in ../endpoint-census.json and frozen inputs.json. Seed1337:123initial live; off128/enabled124 final, off1/enabled0 positive-root final. Enabled opportunity serial75→91 (16opportunities, not launches); observed routing elapsed is a whole-pass subset, not per-launch latency. No per-cell work counter was invented.

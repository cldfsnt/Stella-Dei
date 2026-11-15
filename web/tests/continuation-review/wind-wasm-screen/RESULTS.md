# Actual WASM wind screen: mixed cost, correctness passed

One preregistered 12-process ABBA window, 2026-11-15 22:06:11.720–22:06:35.744 UTC. Both sibling workers explicitly released CPU before start and held heavy jobs; completion released them. No favorable reruns. Zig0.13.0 wasm32 Emscripten ReleaseSafe, single_threaded/cooperative Loop; emcc3.1.64 -O2; Node24.22.1 on this cloud host. Exact flags are in build-wasm-wind-screen.sh. This does not measure browser rendering or device FPS.

| Fixed scenario | Baseline median ms/tick | Candidate median | Change |
|---|---:|---:|---:|
| Legacy Origin day30, wind off |17.6366|18.0426|+2.30%|
| Legacy Sandbox82 rabbits, wind off |27.1959|29.5525|+8.67%|
| Actual paid-Pioneer day3, enabled |17.5423|18.3570|+4.64%|

Every process restores its immutable input;12 warmup plus60 timed complete Planet.simulate steps and clock increments. Restore/parse/serialization excluded. All timed endpoints exactly match untimed gate hashes. Substantial ordering/host variation prevents clean attribution or a speed claim. Sandbox candidate27.744/31.362 exceeded both baseline27.497/26.895 in this sample: a practical overhead caution, not silently declared a pass. Coordinator review required before promotion; no additional optimization or repeat authorized here.

Off scenarios have raw-byte-identical complete saved baseline/candidate endpoints including RNG. All six source/input combinations pass zero semantic restoration and fresh-process72+10==82 raw-byte equality. Old schema6 zero-capture normalization is explicitly documented in prereg addendum and first failure retained. No native↔WASM bit identity claim.

Enabled scenario is the genuine205-paid-founder experiment day3,216 living cohorts. Wind opportunity serial85→131 during72 steps. Its baseline is an explicit projection to classic version7 removing only wind config and aerial allocation, not a claim the enabled ecology should remain identical. Enabled has its own full restart/state gates. Thus enabled timing measures total coupled practical cost relative to that counterfactual, not isolated kernel overhead or equal trajectories.

WASM layout: Cohort80→88bytes; Cell336→368; Planet2936→2960. Origin cell arrays13,763,232→15,074,016bytes: +1,310,784bytes (1.25MiB), plus24bytes Planet config. Sandbox has no allocated microbe cell array here, though compiled struct/code differ. No new per-tick heap scratch was added by wind route or packet helpers. Existing staging Auto-seed can duplicate the larger cell array twice, adding2,621,568bytes above its old staging cost; it is not running during this screen. These are model-layout figures, not measured process RSS/browser memory. Raw binary/input/source/output hashes are retained; source/runtime archive includes the exact compiled copies. No rejected live-loop/hoist optimization included.

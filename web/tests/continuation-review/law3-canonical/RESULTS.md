# Canonical law3 + borrowed Cell: integrity passes, bounded cost measured

No production edits/deployment. Reproducible copies combine frozen final-demand law3 (012cd08) with ONLY patch-origin-land-borrowed.py (28854f1). Exact comparison confirms only planet/shared_soil/capillary_bucket differ between A/B. Rejected live-loop, environment-skip and coefficient-hoist variants are absent. Both use original hydrology/physiology parameters and explicit saved identities.

## Correctness

Actual wasm32 ReleaseSafe Planet.simulate, width4, cooperative event loop. Zero-tick typed captures agree with inputs; allowed normalization is legacy version7/default serialization and empty cohort representation, not physics. A/B output bytes match for earlyoff, earlylaw3, populatedlaw3 and historical laws1/2. Both law3 scenarios pass fresh-process72+2vs74 byte equality in each build. All timed72tick endpoints match their own correctness outputs exactly.

Actual native borrowed fullsavedstates/RNG match frozen unborrowed native4tick outputs for laws1/2/3, legacy and actual day30/100mm. This is same-target parity; no cross-SIMD native/WASM equivalence claim. Existing law3 native reset/ownership/2+2 gates remain separately preserved.

## Fixed screen (all12 runs retained)

One preregistered ABBA per input, freshprocess restore,12warmup+60timed1440s ticks. Complete simulation+clock increment only; parse/load and serialization excluded. Window2026-11-15T20:16:49.964153Z–20:17:20.186373Z, otherworkers reserved read-only; exit0 collected before CPU release. No repeats.

| Scenario | Frozen unborrowed median ms/tick | Canonical borrowed | Difference |
|---|---:|---:|---:|
| Genuine early/default empty, betaoff |13.4954|13.7111|+1.60%, mixed |
| Early empty, explicit law3 |35.4140|30.0747|−15.08%, bothB belowbothA |
| Actual day30/law3/100mm |34.4187|34.0786|−0.99%, mixed |

Earlybeta shows reduced cost from borrowing; populated-world improvement is not established by this small noisy screen. No universal speedup, frame/FPS, browserGPU or phone/laptop claim. Absolute beta simulation cost remains substantial; these equivalent-law A/B comparisons are not an ecological parity or total-cost comparison against productionv72. Earlyoff and earlybeta medians also differ in law and resulting trajectory, not just implementation.

## Memory

40962patches, Cell368bytes/Cohort88bytes; dense Cell array15,074,016bytes (~14.375MiB) in this loader, even empty. Enabledbeta extra arrays: soil327,696; authoritativevapor327,696; newvapor327,696; coefficient327,696; amounts1,310,784; lineageowners1,310,784 bytes. Total3,932,352bytes (~3.75018MiB). Amount+owner increment over original f32rootratios is1,966,176bytes (~1.87509MiB). Betaoff allocates none of these beta arrays. These figures exclude existing common engine/mesh/render allocations.

Final WASM linear-heap capacity stayed134,217,728bytes (128MiB initial allocation) for all measured scenarios/builds. This includes input/graph parsing, retained source JSON and output serialization. It is capacity, NOT live game memory or peak device RAM; no fullrenderer present.

## Existing compiled Environment cost inspection, no new variant/run

Native DWARF reports Environment104bytes/alignment8, optionalEnvironment112bytes. The existing WASM object materializes Environment fields on the column stack at offsets1608..1712 before shared_soil.stepBorrowed call0x87a9. This includes the now-large environment structure despite borrowed Cell. No standalone104-byte memcpy in that hot call path was identified: the three literal104-byte memcpy sites found belong to JSON parse/stringify outside timed simulation. Scalar load/store work is plausible; no attribution percentage or confirmed optimization benefit inferred. Excerpts retained. A future readonly receipt reference might reduce copying but is NOT included here.

All actual snapshots remain under site-tmp/law3-canonical with hashes in proof; scripts, source/artifact hashes, complete logs and all timing rows retained in repository. This checkpoint prepares potential separately authorized preview work only.

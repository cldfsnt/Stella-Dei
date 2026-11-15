# Compact immutable liquid transport: actual-WASM decision gate

Status: protocol frozen before any new WASM compact-solver outcomes. Coordinator approved numerical/performance limits in principle; this document makes units, acceptance and stop rules explicit. Production/live game remain unchanged. Previous three native variants remain held; these are new-target measurements, not relabeled native successes.

## Fixed model and inputs

Use the already tested compact helper `src/experimental/liquid_gather_compact.zig`, unchanged arithmetic: immutable f32 donor masses, identical existing f32 absolute heads, f32 outgoing edges, fixed-order f64 destination gather, f32 final pools. All cells including SIMD tails participate. Unique reciprocal edges, explicit self/duplicate masks, donor-bounded flow and original factor/cap remain. No relative-head precision change, optional roots, vapor migration, validation-hoist candidate, rate tuning or additional optimization bundled.

Actual production WASM Planet/EventLoop harness from afe9e62 supplies real coupled temperature/wind/atmosphere/microbes. Only Origin liquid scatter is replaced; Sandbox retains the original path. Fixed actual40,962-cell day30/day60/day90 snapshots and topology are the same hashed inputs from that profile. Source and graphs pinned before builds. Use wasm32-emscripten Zig0.13 ReleaseSafe, single-threaded, emcc-O2/Node. Native prior results are context, not the performance comparator. No browser/GPU/device claim.

## Hard correctness gates

1. Topology range/reciprocity and same-count changed-graph rebuild; duplicate/self rules; tails; no offset-alias acceptance; finite/nonnegative outputs; exact summed unique outgoing f32 edges≤immutable donor. Invalid topology/inputs fail closed before authoritative swap (scratch is not promised atomic on late failure).
2. Each actual directed edge incurs equal exact debt and credit once, using the identical represented f32 value. Independent offline dyadic-integer oracle reconstructs all incoming adjacency, rather than trusting destination loops. Forward/reverse source traversal and compact/reference helper parity required on supported controls, including signed zero, tiny/huge mixed pools and zero flow. No renormalization or target-total topups.
3. Candidate diagnostics must produce identical full saved endpoints to uninstrumented candidate. Zero-tick input restoration parity inherited/rechecked. Save schema6/model5 remains unchanged and validates all outputs. Same candidate whole-state70tick result must equal60tick endpoint serialized and reloaded into a NEW Node process then10ticks (same initial inputs/geometry). This tests the QA loader with actual production schema, not browser IndexedDB/UI. Do not require candidate and old-law biology/water endpoints to match.
4. All three real worlds run60×1440seconds. Preserve original inputs and baseline results. Audit every liquid step independently of atmosphere; global coupled water drift is reported separately, not assigned wholly to liquid.

## Numerical units and acceptance

Native pool/edge unit is10^9kg. Multiply absolute inventory residuals by1e9 for kg. Equivalent local water depth is error_native×1e9/(actual_patch_area_m2×1000) meters, using actual Planet mean area; this is an equivalent layer, not a hydrology/weather claim. Sum-of-depths is not a single patch depth.

For each destination define exact dyadic x_i=M_i−Σout_i+Σin_i from immutable represented f32 values. Let a_i be the actual pre-cast f64 gather accumulator, o_i the final f32 output, and e_i=o_i−x_i. S_i=M_i+Σout_i+Σin_i. With u64=2^-53 and gamma12=12u64/(1−12u64), require:

- |a_i−x_i|≤gamma12×S_i (at most six subtractions and six additions).
- |e_i|≤B_i=0.5ULP32(a_i)+gamma12×S_i. For zero/subnormal a_i, half-spacing is2^-150 native units. No user-selected epsilon or tolerance expansion after results.

Record E=Σe_i (signed), A=Σ|e_i|, B=ΣB_i per step, cumulative A/B and maximum local ratio. Report all absolute kg, local equivalent-depth maxima, inventory-normalized errors using that step's pre-liquid inventory, and throughput-normalized errors using gross one-way transfer T=Σunique_directed_edges flow. When T=0, require unchanged pools, report ratio not applicable rather than hide it behind an arbitrary denominator. Pure synthetic tiny-flow tests may expose limited precision without changing thresholds or claiming all small flows resolve.

Practical real-world improvement gate: for EACH fixed world, D_candidate=Σ_steps |Σ_i e_it| must be at most0.5×D_legacy, where legacy D is independently measured exact pre/post liquid inventory difference under actual WASM scatter. This is ≥50% reduction in accumulated absolute per-step global drift, not a global signed cancellation test. A is separately required to satisfy the analytic envelope; do not call D the per-cell SUMABS. Report legacy/candidate signed cumulative residuals and coupled-stage drift separately.

Resolution warning only, not an automatic game failure: count every positive-incident-flow cell/step with B_i>(Σout_i+Σin_i)/128, including affected tiny-flow mass and local depth. This engineering7-useful-bit target is not calibrated biology. Coordinator-approved pre-outcome engineering cap: cumulative A/T≤1e-3 for each real-world horizon, with T counted once per directed edge. This is a practical movement-accuracy bound, not a gamma-derived or biologically calibrated law. Local errors may be nonzero and still acceptable within the declared binary-precision budget; no absolute-zero paralysis or hidden correction.

## Fixed performance decision

After numerical/helper/restart gates: three alternating baseline/candidate pairs per world,18 fresh-process executions, each60 unchanged1440second steps from the same original snapshot. Use uninstrumented full Planet.simulate, no diagnostic trace/ledger I/O; exclude restore/serialize. Record first tick separately and remaining59 average, as in the existing WASM profile. Include all records and raw ranges. No favorable repeats. Stage instrumented timing is not the decision metric.

Accept bounded correctness cost only if EVERY world has candidate remaining-step median≤1.05×baseline, AND geometric mean of the three median ratios≤1.03. This is permission for a small measured cost in exchange for improved transport accounting, not a speedup requirement or claim. Failure/inconclusive noisy boundaries mean HOLD and explicit review, not automatic repeated testing. First-tick allocation cost and memory overhead must also be disclosed, not excluded from the report.

## Predeclared longer gate and gameplay interpretation

Only if all60tick numerical/restart/performance gates pass, run420ticks (seven simulated days) on the SAME three worlds, numerical diagnostics and serialized420+10 vs430tick process-reload continuation. No additional performance repetitions. Apply the same analytic envelope, hard validity gates and ≥50%D improvement comparison to matched legacy420tick controls. Preserve all endpoint ecology counts/biomass/lineage losses and altered habitats. Different legitimate ecological trajectories are expected from removing lane/tail/order-dependent water transport; no natural survival/adaptation/land-life upgrade is inferred.

Passing this research gate does not deploy. Coordinator reviews source lifetime/invalidation, compatibility, cost and ecological deltas before any production decision. If short gate fails, stop longer gate and save the useful negative result.

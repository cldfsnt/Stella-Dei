# Independent actual WASM60tick numerical gate: HOLD

All three completed candidate and baseline binary traces audited, no sampling:40962cells×60ticks×3worlds=7,373,160 candidate cell-steps. All trace hashes match producer controls.json. Header count/ticks/area and exact60frame lengths checked; actual area7669529600m². All40962 helper graph rows independently equal Planet enum graph remapped[0,3,1,4,2,5] for PRIVATE helper edges; Planet topology remains unchanged. No second remap in oracle.

All finite/nonnegative, sourcebudget, self/duplicateedge, per-cell f64gamma12, half-f32cast and combined-operation envelopes PASS. These are ordinary bounded floating errors, not evidence of a duplicate-edge ownership defect. Nevertheless the prospectively frozen traffic-relative practical gate FAILS every world:

| Initial world | A=sumabs cell error, native | T=one-way transfer, native | A/T | D candidate/legacy |
|---|---:|---:|---:|---:|
|day30|1807675.1940542124|101874660.09957686|1.774411%|.091878795|
|day60|1861791.4722844013|124977373.89115967|1.489703%|.085391948|
|day90|1866010.7887555335|139588364.13970375|1.336795%|.085264141|

Native mass units are10^9kg, not kg/m². D=sum absolute global per-step drift improves90.81–91.47%, satisfying≥50% reduction. A/T remains13.37–17.74times the approved0.1% cap. Do not substitute D for A or use global inventory to waive the failure. Maximum cell-equivalent depth error~.00103029m (~1.03mm), using actual patch area. Sum derived bounds~4.267–4.269million native per60steps; A remains within them.

Local B>incident/128 warnings:1682992/1696494/1678642 cell-steps. Positive intended NET incoming balance with unchanged represented pool:10649/14116/16377. These are numerical local-resolution diagnostics, not counts of individual blocked edge transfers, deaths, or failed births. Warnings alone are not the failure criterion; aggregate A/T is.

Every oracle invocation returned2 as designed for practical failure and wrote complete output. The enclosing shell loop finally returned1 because its last conditional `[ code = 1 ] && break` was false; no oracle structural exception occurred. No tolerance changed, no extra repetitions, no timing or420tick follow-up warranted by this failed gate. No production changes.

Producer independently reports plain/trace output equality, complete original baseline equality, zero-tick restoration and genuine new-process60+10 versus70 continuation equality. Those controls are in its own evidence; this independent checkpoint verifies actual binary hashes against that manifest and audits the numerical traces, not a duplicate engine run.

Reproduce each day D:
`python web/tests/liquid-wasm-oracle.py --graph ../site-tmp/liquid-gather-wasm/helper-graph.json --candidate ../site-tmp/liquid-gather-wasm/candidate-dayD.bin --baseline ../site-tmp/liquid-gather-wasm/baseline-dayD.bin --output audit-dayD.json`

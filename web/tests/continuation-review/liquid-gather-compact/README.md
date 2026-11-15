# Compact working-set variant: exact model, still slower

Approved single variant after LLVM inspection6e8104f: store already-computedf32 edge flows asf32, widen exactly at the samef64 subtract/add positions; compute identicalf32 heads once in existing finite-input pass and reuse. No relative-head formula, rate, cap, target selection, summation order, physical ownership or schema change. Dynamic invalid guards remain. Cache lifecycle and prepared immutable-array contract unchanged.

Independent3test gate proves exact widened edges, outputs and both ledger fields versus cachedreference for mixedscales/signedzero/three timesteps/forward-reverse/duplicate-self-tail/changedgraphreprepare and alias refusals. Three actual frozenworld runs passed complete endpoint and true uninterrupted/restored continuation equality before timing. All18 subsequent timing runs repeat those same-version exact checks. No fresh-process restart or browser claim.

Native scratch falls from102 to82bytes/patch:4,178,124→3,358,884bytes at40962nodes. Head is recalculated every step, not stale cross-tick authority. Invalid-input failure may alter non-authoritative scratch but never commits output to current world. Memory saving is not a speed result.

## Fixed timing results: HOLD

Three alternating pairs perworld,60actual1440second ticks; startup/render/serialization outside timer, cold scratch construction inside firsttick. Siblings/coordinator explicitly released CPU. No extra favorable repeats.

|World|Baseline median ms/tick|Compact median|Change|
|---|---:|---:|---:|
|day30|7.792967183|8.778697483|+12.65%|
|day60|7.762431233|8.852862967|+14.05%|
|day90|8.00293555|8.812970283|+10.12%|

Every pair slower: day30+12.65/+11.66/+12.01%;day60+28.15/+14.05/+5.19%;day90+9.88/+10.12/+8.21%. Do not compare across earlier timing windows to manufacture an optimization benefit. Nativeproxy only, not deviceFPS. The correct immutable solver changes genuine hydraulic work versus legacy omitted/order-dependent transfers; it is not currently a performance fix.

No promotion. Numerical residuals and ecological changes remain identical to prior immutablegather; they require separate release interpretation, not a relaxed tolerance because signed drift improved. Earlier failedtiming variants retained. No production edit or live deployment.

# Minimal exact protective-state compaction

Independent isolated copy of frozen graded-protection/graded-world physiology (owner4f59b75, raw6eed35d). No owner source, model coefficients, live runtime or product schema edited.

## Result

Original104-byte Cohort /432-byte Cell becomes96/400. Live no-protection layout is88/368. Replacing the two recovery-state fields (f32 elapsed +bool) with one f32 clock avoids padding without quantizing any trait or arbitrary elapsed-time value:

- clock−1: metabolically ACTIVE, protective_rest=false, recovery0.
- finite clock≥0: protective_rest=true, same exact f32 elapsed recovery.
- birth/death/empty default uses−1; movement copies the entire state.
- other negative values, NaN and infinities are rejected by QA's decoding validator. Product validation must enforce this itself; legacy validCell does not know new fields.

A finite clock may exceed7200 because the old law adds dt while below7200 and wakes on the NEXT favorable interval. Do not cap or quantize during an equivalence change. This prototype preserves that ordering exactly. Recovery reset outside favorable range remains0 while resting, not−1.

At40962cells, one core cell array shrinks1,310,784bytes versus the104-byte prototype, halving incremental storage over live88-byte cohorts from2,621,568 to1,310,784bytes. This is layout accounting, not measured total runtime memory or speed.

## Exact focused controls

73 tests pass (four focused plus imported suites).32 combinations of enabled/off, investment0/1⁄32/.5/1 and dt.125/60/1440/7200 each run180 actual physiology intervals across cold, warm recovery, heat and lethal extremes. Every decoded cohort field, nutrient/detritus, RNG, actual entry payment and Flux is exact at every interval. Midpoint research JSON roundtrip retains compact state exactly and continuation stays equal. Actual paid birth inherits investment and resets clock; partial resting movement preserves identity/recovery and paid movement results exactly. Invalid clock domains refused. Original parser syntax compile failure is retained; no discarded ecology or timing runs.

This is **pure actual-core equivalence and research JSON**, not full Planet scheduler/product save/recovery or empirical performance proof. Existing research fullworld sidecar still uses rest+recovery; no production format assigned.

## Practical production recommendation

Use the compact scalar pair if integration proceeds. Keep protective investment separate from structure: structure already changes growth, baseline dry/wet mortality and geometry; reusing it would couple independent costs and change the tested strategy, not merely save memory. Do not hide that change as optimization.

An external optional state table can preserve88-byte cohorts only by moving investment and clock out, but then every birth/transport/death, lineage identity, stale slot and save path needs synchronized ownership and lookups. That is a larger correctness/cost risk than this8-byte inline increment. Avoid it for the minimal first version.

Compute concern remains the extra pre-column protectBefore call/4slot scan on every patch, plus activity checks; compaction does not prove those free. Production should gate disabled law outside added work where possible, retain exact old floating arithmetic/default omission, and avoid an additional full-world pass. Cell layout/code generation may still affect off-path speed.

## Bounded cost gate when integrated source freezes

Recommend two fixed same-input comparisons: historical live runtime versus candidate disabled on one established wire13 world; original104-byte prototype versus compact96 on one already-completed protected world with exact decoded state/flux/RNG and restart first. Each one-process warmA/B+ABBA72tick blocks (12warm+60timed), no repeats, exclusive CPU window. Roughly8 measured blocks total and tens of seconds to a minute after builds; actual cost unknown until measured. No new ecology selection, benchmark during owner work, blanket speed or device claim. Await integrated source/save contract rather than patching unowned product code now.

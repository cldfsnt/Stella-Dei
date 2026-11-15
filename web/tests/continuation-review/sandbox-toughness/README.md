# Prescribed costly toughness: real local tradeoff, not a stable ecosystem

Frozen2afdecb matrix completed: baseline6controls and candidate12arms, each14days, dt1440/720/360. Both test processes exit0, actual production biology copied with narrow candidate diff. No production/save/schema change. All84 zero-trait daily records and6 complete old-field/RNG endpoints are exactly equal to the unchanged baseline. Trait inheritance preserves original thermal draw; no toughness mutations. Source/receipt/final-fragment/property checks pass.

## Observed cost and conditional benefit
Atdt1440, ungrazed day1cover4.14787(d0) versus1.07280(d.5): genuinely slower gross growth/spread. Both saturate near7byday14, so endpointalone would hide the cost. With two starting rabbits, day14cover6.34730vs6.53551 (+2.97%); rabbits23vs9, cover consumed15.7613vs8.42533. Rabbits fed from actual cover debit with conservative satiety credit. This is a coupled food/demographic feedback, not equal-consumer-pressure resistance measurement.

Atdt720 day14grazedcover6.34886vs6.55582; atdt3606.38105vs6.56001. Same qualitative direction, but exact numerical/timestep convergence is NOT established. Allcases retain7plant patches, no actual local extinctions, no rabbitdeaths byday14. Separate repeated hungry-foraging gate exhausts a defended patch: no immortal floor. These favorable seven-patch results do not establish island persistence, invasibility or coexistence.

## Critical energetic limitation, not tuned away
For d=.5, maximum acquisition=.144cover/day BEFORE density response, exactly nominal maintenance need21.6satiety/day dividedby150. Atcover1, densityresponse1/1.1 reduces maximum to19.636satiety/day, BELOW maintenance21.6, even before reproductioncost. Thus a uniform d.5 world cannot sustain rabbits indefinitely under this law. Nine rabbits atday14 are a transient outcome. Approximate necessary bound atcover1 is d<=.40909, ignoring reproduction and feeding-stop behavior. We did NOT change d/rates or extend horizon after discovering this. A diverse tender/defended mosaic is a meaningful later test; a uniformly defended ecosystem should not be marketed as balanced.

## Interpretation and open gates
This justifies investigating a distinct costly strategy, not release. Occupied-patch replacement still uses thermalfitness; same-optimum toughness does not invade occupied space through a new artificial score. No competitive selection/coexistence claim. Future spatial turnover must be tracked separately from prescribeduniform-arm cost/benefit.

Existing plant brush retains old plantTraits even on zero-cover cells. These controlled fixtures set initial genotypes explicitly and do not exercise the brush. Before any promotion, decide whether painting a truly empty patch resets foundertraits or deliberately revives its stale genotype; do not silently call it ancestry. Existing-livepatch behavior and old-save rules need explicit tests.

All cover/gas semantics remain Sandbox phenomenology, not closed elemental mass. Growth cost scales gross production only; losses are unchanged. Offspring cover comes from existing model, not a newly proven donor carbon budget. All actual bite credits are bounded by150×representedcoverremoved; maximum cumulative relative undercredit in results.json. Baseline/instrumented source observations are identical, and no additional RNG draws were introduced.

## Reproduce
Generator web/tests/sandbox-toughness-prepare.py creates separate baseline/candidate src copies. Run Zig0.13 ReleaseSafe with web/tests/lifecycle-build.zig and -Dsource=<copy>/qa_sandbox_toughness.zig, absolutecache paths. Analysis web/tests/analyze-sandbox-toughness.py requires both raw logs, recomputes exactzero-trait comparisons and preserves all168candidate daily records. Compressed complete logs include unrelated imported baseline tests; no discarded failures or selected winning runs. No renderer/save/fullclimate test here. Geometry, inputstock, temperature/light and14day cap are fixed in PREREG.md. No newexperiment starts from this report alone.

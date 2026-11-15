# Proposed isolated costly toughness law, not production

One new continuous Plant.toughness:f32 in[0,1]. This is a simplified handling-resistance surrogate, not botanical calibration, woody forest identity, nutrient-quality model or Origin land evolution. Default0. Existing cover remains fully edible, mortality can remove it and local extinction stays possible.

## First fixed candidate (review before implementation)
Let d=toughness. Positive plant gross production is multiplied by(1-d); existing respiration, unsuitable-climate mortality, flooding, light and CO2 gates stay unchanged. In grow, scale ONLY the positive fitness/light*6/day term, not the whole net rate, otherwise defense would subsidize mortality.

Neighbor propagule cover addition is multiplied by(1-parent.d); do not change thermal replacement thresholds or add biomass, donor grants or new dispersion. Existing Sandbox propagation is phenomenological cover, not donor-conserved elemental mass. State that limitation, do not label this a closed carbon budget.

Rabbit maximum acquisition rate becomes old maximum/(1+2*d), retaining the existing density-response, hunger ceiling, actual represented cover debit and conservative150*debit satiety. All tissue remains edible. Final-fragment consumption must also fit this REDUCED time budget; no bypass at tiny cover. For d=.5, gross growth/propagule production halve and handling capacity halves. This symmetry is a transparent first engineering hypothesis, not an empirical fit. No rate/coefficient tuning after outcomes.

Defense0 must take the exact original code path for growth, spread and feeding, preserving old outputs and RNG. Initial experiment uses prescribed d0/.5 in copied actual core, mutation disabled. No favorable mutation or thermal optimum assignment. Hungry movement remains unchanged in this FIRST test; explicitly observe possible attraction to dense but hard-to-eat patches rather than quietly giving rabbits new strategic knowledge. If that produces a concrete trap, report it before a separate behavior hypothesis.

## Bounded paired assay to review
Use a controlled seven-patch actual-engine habitat from qa_ecology, fixed thermal parameters from the existing warm fixture, identical initial cover/food and rabbit state. Explicit external setup, no midrun refill/temperature rescue. Four arms: d0 vsd.5, each with no rabbits versus fixed grazing pressure. Fixed14days, dt1440/720/360 (12runs), same seed1337; no later extension. Include separate zero-cover/final-fragment and sustained-heavy-graze tests to prove no invulnerability. Log cover, propagule establishment, actual bite debits/credits, rabbits/births/deaths, extinction/recolonization, thermal losses and timestep effects. Keep negative results.

Expected direction is a TEST, not an acceptance requirement: defended plants should sacrifice ungrazed expansion and may fare better under grazing; too little advantage, universal inferiority, universal superiority or no coexistence all remain possible. Fair paired pre-state and resource bounds are acceptance requirements, not a desired winner. Only after source/accounting/disabled gates and an interpretable cost-benefit result, consider one fixed actual-world paired continuation from the already frozen warm day14 save. No broad seed/rate search.

## Inheritance and saved-world obligations
Ecology.offspring must copy d then vary it in a separately declared later phase. Preserve the original optimum draw exactly; a subsequent draw from its existing local per-birth PRNG can provide reproducible variation without touching the global world's RNG, but it is pseudorandom, not mathematically independent. Freeze rarity/step/boundary policy before a from-zero trial. Mutation is disabled during the first prescribed tradeoff assay. No natural-evolution claim before an actual from-zero inherited-variation experiment.

One f32 adds about163,848bytes for40,962plant entries (verify struct alignment/build), plus serialized JSON cost. No per-frame allocation, f128 ledger, climate array rewrite or protected water pool. Save schema currently aliases Plant, so validate finite d[0,1], require explicit supported experimental model identity, default legacy imports0 with feature disabled, reject disguised unsupported nonzero ownership before mutation, preserve Sandbox/Origin reset behavior and no automatic save migration. A later actual capture/load/true continuation test must persist both law/config and trait, not merely JSON bytes. Do not pick a production schema revision in this proposal.

No code or production/save changes until reviewed. The current warm-world recovery and all earlier negative worlds remain evidence, not targets to overwrite.

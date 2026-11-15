# Bounded search-mechanic and feasibility review (no new runs)

Scope: frozen law3 Wetlands equations, actual524 observations and fixed950dccb paired diagnostic. No source/parameter/runtime changes. Natural day7→21 results are pending and must be considered before another intervention.

## Mutation search is asymmetric across traits

`simulation/root_mutation.zig:proposal/allocation` has only symmetric±1/32 proposals at1/64 births, clipped[0,1], from the independent lineage-keyed root stream. `microbes.zig:rareMutation/applyRareMutation` instead has a1/512 event across SIX other traits and replaces one ordinary mutation with a symmetric1–<3× step. Each individual general trait's tail probability is about1/3072, not1/512. Roots are not in that selection. Seven net positive root increments separate1/32 from1/4; this is an ancestry distance, not an expected elapsed time.

A symmetric, environment-independent larger-root tail is defensible as an explicit game search mechanic, not evidence of evolutionary realism or a remedy guaranteed to establish land life. Existing paid support is repartitioned: root allocation neither adds biomass nor support nor water, and reduces aboveground geometry/protection/canopy opportunity. Clipping creates boundary expression bias even with symmetric proposals; mutations at0 can be invisible and at1 cannot increase. Rare larger negative changes and their costs must remain.

Do not silently copy the six-trait aggregate1/512 rate as a per-root rate, which would give roots about six times each existing trait's rare-event opportunity. An exact rate/magnitude/replacement rule needs a predeclared new law and explicit approval, not selection after seeing survival. Prefer an independently domain-tagged event stream and replace, rather than add to, the ordinary proposal on tail events. Keep law1 completely unchanged, including other traits' draws and counters; do not add roots to the old six-way selector.

## Resource-based bounds

Write B=live carbon density, S=paid support density, q=S/B, r=root fraction, w=soil kg/m² (bounded0..1), L=surface light, x=exposed fraction, and Δ=days. In a constant warm dry interval, before sharing/rounding:

- Root supply ≤10 S r w Δ kg water/m².
- Demand =0.1(B−S)(0.5+0.5L)xΔ kg water/m².
- Thus h≤min(1,100 q r w/[(1−q)(0.5+0.5L)x]). Law3's actual credit and max(entry,current) denominator can only tighten this envelope; dynamic phase exposure must not be substituted silently.
- Root spending plus bare evaporation cannot exceed soil debit. Photosynthetic carbon gain is capped by potential, remaining patch space, available carbon, and nutrient/0.1; support respiration is oxygen-capacity bounded. Larger root share does not create any of those resources.

For actual524 at the first dry consumption record, q=.0231174, L=.942339, efficiency=.984780, r=1/32, x=1. Even w=1 permits h≈.076147; prescribedr=1/4 permits only≈.609174. Full hydration would need r≈.4104 at maximumsoil, and even r=1 cannot reach it when soil<.4104 with this fixed paid-support ratio. These are conditional bounds, not proposed parameter targets.

Structure s lowers dry mortality4−3.3s/day but costs photosynthetic multiplier1−.5s; total support still costs about.12S/day. Ignoring competition, nighttime, finite carbon/nutrient/space, thermal mismatch and aerial exposure gives an optimistic continuous-rate balance per livecarbon:

`(1−q)*max(0,3*h*L*e*(1−.5s)−.15e²) − [(4−3.3s)*(1−h)+(.04+.1s)*h] − .12q`.

This is an algebraic envelope, NOT a full scheduler prediction or exact discrete timestep update. For the same q/L/e and r=.25, its break-even h is≈.6195 at actuals=.02019 (above the .6092 maximum),≈.5802 ats=.5, and≈.4401 ats=1. The latter two require w at least≈.953 and≈.722 respectively even in this favorable envelope. At naturalr=1/32 and s=1, the photosynthetic rate remains zero at this light because the efficiency cost exceeds hydrated production. More structure alone cannot solve this example.

Therefore the equations do not provide a blanket impossibility proof for jointly higher structure and roots, but their favorable region is narrow and resource-dependent. Positive optimistic capacity is NOT proof of a sustainable24h strategy: soil depletion, darkness, competition, geometric exposure, growth-paid support history and the .0025 establishment cutoff remain. Structure is inherited protection with a growth cost, not extra paid tissue; r is a fraction of actual support, not a fraction of totalcarbon. Higher organization would need real growth to pay for more S.

The actual paired diagnostic is consistent: r=.25 raised firstcredit8× and reduced aboveground support22.58%, but biomass still declined and the lineage died at8h instead of2.8h, with no offspring. This shows a genuine benefit plus remaining limits; it does not show that root mutation accessibility is the sole obstacle. The corrected law3 credit computation passes funding/ownership/restart gates; demand/conductance remain declared model assumptions, not empirically validated biology.

## Save/reproducibility contract if a tail is approved

Use a new root_mutation law identity, not a new hidden behavior under law1 or a changed physiology3 label. Persist the root mutation law, enabled flag and fullu64 stream seed alongside existing hydrology/physiology identity and all actual root traits; widen experimental compatibility only under an explicit version/format gate so old readers reject unknown semantics. Keep historical schema/law1 captures and runs unchanged. Existing saved worlds must remain law1 unless an explicit experimental migration changes only identity/config; no automatic import upgrade. New-world opt-in/default policy must be stated.

Require exact old-law/no-tail RNG/state trajectories, fixed independent event vectors (including maxu64), positive/negative and boundary-expression counts, failed-birth atomicity/no newstream draw requirements, actual funded offspring copying, invalid-load atomicity, and fresh-process continuation after both ordinary and tail births. No receipt/owner arrays or per-cell memory increase is needed; work occurs only at successful mutating births. Do not infer zero performance cost without checking implementation.

## One next action after natural day21

First use that already-running result to count actual successful mutating births, root-step opportunities and occupied root/structure combinations. If larger allocations remain unvisited, propose ONE isolated, explicitly new-law rare-root-tail pilot paired against the unchanged mutator on the same saved world/horizon, after the fixed event/save gates above. Predeclare the tail probability/magnitude before outcomes, retain losses and absent establishment, and measure visited genotypes plus paid costs rather than declare success by survival alone. Do not tune demand/conductance or repeat the paid-allocation sweep. If the natural run already visits substantial roots yet still fails, the search rationale weakens; report that instead of automatically adding the tail.

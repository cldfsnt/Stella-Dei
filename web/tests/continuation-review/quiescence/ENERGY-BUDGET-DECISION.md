# Decision: specify shared maintenance before adding a persistence advantage

**Proposal only; no primitive, production or null-assay changes.** The null assay already demonstrated that moving biomass into an inactive pool with the same mortality and paid conversion does not create drought or heat survival. Do not change this negative evidence.

## What is actually missing
Current Microbes.step charges support tissue respiration from finite O2. The growth-rate term `-0.15*efficiency²` reduces potential uptake; it does not respire existing active biomass or generate a maintenance deficit. Unstructured colonies therefore lack explicit baseline energetic expenditure. When oxygen is absent, support respiration is scaled to zero without an additional unmet-maintenance consequence. Ordinary mortality still applies, so this is not literally immortal tissue, but oxygen scarcity can remove that maintenance cost. Copying this pattern into a resting trait would be an inadequate energy model.

No physiology calibration is available here for ATP requirements, anaerobic metabolism, repair or desiccation envelopes. A new mortality constant selected to make the resting phenotype win would not be evidence of evolved persistence. Thus this step is a bounded simulation hypothesis for review, not scientifically validated biology.

## Smallest common-budget hypothesis
Initially restrict to the same unstructured, nonfeeding, nonmoving phenotype as the null adapter. Do not add seedbanks, immunity, reserves, new taxa or multiple energy substrates.

Let A and R be the disjoint active and resting living carbon masses. Both count toward occupancy and bound nutrient. Each requires positive daily maintenance: active rate mA and resting rate mR, with 0 < mR <= mA. Dormancy hypothesis is reduced metabolic demand, not reduced heat/drought mortality. Rest has zero fixation, grazing and earned reproduction credit. Existing paid entry/wake transfers and limited conversion rates remain; treatment assignment is not inherited evolution until actual lineage tests exist.

For one bounded timestep dt (days), maintenance carbon demands can use analytic finite loss:
- DA = A*(1-exp(-mA*dt)); DR = R*(1-exp(-mR*dt)).
- Shared available oxygen is expressed in carbon-equivalent units. Allocate it proportionally to demand, NOT active-first/rest-first: f = min(1, O2_available/(DA+DR)).
- Respire paid carbon f*DA and f*DR. Remove it from the appropriate living compartments; add exactly corresponding CO2 and return bound nutrient once. O2 decreases by the same carbon-equivalent amount.

These carbon quantities are a bookkeeping proxy for maintenance energy, not ATP molecules or measured bioenergetic efficiency. Positive demand does not itself remove unpaid carbon.

### Essential unmet-demand rule
A model that simply skips respiration when O2 runs out is rejected. Explicitly expose unmet maintenance fraction u = 1-f (when demand positive). A bounded experimental option is an added stress hazard proportional to u, applied equally per living mass in both pools, with a declared maximum hazard. Under complete oxygen absence both pools face the SAME maximum energy-deficit hazard: neither becomes immune merely by having a smaller positive rate. Stress mortality becomes detritus and returns bound nutrients, NOT CO2; it must not consume unavailable oxygen.

This hazard is a phenomenological hypothesis requiring calibration/sensitivity analysis, not an established ATP mechanism. A future accumulated stress/debt model could model delayed failure, but adds a save state and recovery physiology; defer it rather than label an arbitrary accumulator ATP.

Baseline thermal/dry mortality remains the actual core response for both pools. Lower respiration can help preserve tissue during long nonproductive periods with oxygen, but does not stop heat/dry death. No fire-event branch or automatic beneficial response.

## Timing and accounting decisions before implementation
1. Do not layer baseline active respiration blindly on top of the existing growth-rate penalty. Determine whether the latter is an uptake efficiency penalty or intended maintenance, document that distinction, and calibrate common baseline cost. Otherwise the active phenotype is deliberately double-charged.
2. Full model must give one finite O2 budget to basal/support/grazing/decay processes, with documented priorities or proportional allocation. No compartment may reuse the original oxygen allowance. Newly photosynthetically produced oxygen must become available on a defined timestep boundary, not arbitrarily early for one slot. The restricted prototype can exclude support/grazing but must still book detritus decay.
3. Respiration and mortality both remove actual represented tissue. f32 rounding must use represented removed carbon for receipts, bound O2 overspend and reject/retain tiny unrepresentable changes. Numerical tolerance should be derived and logged, not increased until tests pass.
4. Shared occupancy is active+rest+support, not separate1-unit capacities. Starvation cannot free a compartment without sending its carbon and nutrients somewhere.
5. An isolated sidecar cannot settle the existing independent0.0025 cutoff: a genuine cohort must own both pools and die only under a declared total-living/establishment rule. No restoring cleared IDs. If both pools reach zero, no reactivation.

## Bounded experimental matrix (before any schema or live change)
Use common finite initial biomass, nutrient, carbon and oxygen. Include stable light/wet, natural day/night cycles, progressively longer darkness, fully dry and thermal extremes. Include zero O2/dark, low O2, and O2-rich controls. No refill except explicitly declared light-driven fixation; measured O2 production is not a hidden initial gas subsidy.

Start with null controls: mR=mA, no special deficit tolerance and identical traits. Then sweep a small documented ratio set (e.g.1,1/2,1/4) and positive common rates for sensitivity, WITHOUT choosing a preferred setting because it produces the desired winner. Entry/wake cost and lost uptake should be separately toggled to diagnose mechanism; free-entry controls are diagnostic only, never a shippable strategy.

Acceptance requires:
- Each-step C/N/O2/CO2 receipts, death destination, failed/unrepresentable operations and nonnegative bounds; extended numeric drift compared with core-only control.
- Zero O2 does not eliminate deficit stress; zero biomass remains extinct; no nutrient creation during repeated transfers/death.
- Active resting-rest swaps give same resource allocations; no ordering-derived survival advantage.
- Stable favorable environment exposes the cost of resting, while any persistence benefit in unfavorable periods is explained by delivered maintenance, paid living tissue and actual delayed recovery, not a preset mortality bonus.
- No universal winner required. If none of the chosen conditions produces a meaningful advantage, report that; do not tune a hidden bonus.
- Full scheduler with actual inherited propensity, funded offspring, movement, predation and multispecies competition only after the primitive and single-cell experiments are valid. Preserve all old-world migrations and publish nothing experimental as gameplay.

## Playable goal and go/no-go
The potentially playable strategy is **fast active expansion versus slower, paid resting investment during nonproductive periods**, visibly showing active/resting biomass and delayed return. It is NOT fire resistance, real seed ecology or a promise that resting wins. A minimal common maintenance/deficit model is plausible engineering work, but empirical constants and integration policy remain unresolved. Keep current live biology unchanged while profiling and usability improvements can deliver real benefits independently.

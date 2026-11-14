# Shared relocation explanations

This change is confined to the separate responsiveness/usability candidate.
It adds no traits or altered probabilities. Actual `relocate` calls the same
read-only `evaluateRelocation` used by on-demand player feedback.

`Planet.microbeRelocationOpportunity(index, cohort_slot, game_time)` builds the
same six actual neighbor/environment records used by simulation and returns:

- `reason`: invalid, no_living_cohort, no_grazing, no_mobility,
  source_unsuitable, already_moved, no_suitable_neighbor, no_better_prey,
  no_capacity, insufficient_oxygen, or eligible.
- Optional destination, slot and respiratory carbon cost, when a candidate exists.

Suitable source/neighbor means the model's actual temperature and water bounds.
Better prey means neighboring living biomass exceeds other biomass at source by
more than 0.005 kg C/m². Capacity requires an empty cohort slot and total biomass
at most 1 after arrival. Movement consumes oxygen and respired carbon. Eligible
is only an opportunity: the time-dependent random move can still fail, and other
cohorts/environment can change before the next step. Feedback never advances
randomness, moves a cohort or changes resources.

Fourteen fresh model tests pass, including all explanations, unchanged state,
actual cost agreement, no duplicate lineage, controlled benefit and inherited
births, and existing grazing conservation/step-size tests. Actual Planet
regression is separately logged when complete. Native/browser layout acceptance
belongs to the UI worker; this document makes no browser-performance claim.

Actual Planet 100-day regression passes unchanged: 385 births, generation 4,
seven natural relocations, movement respiration 20,023,990.7759 kg C. Carbon
relative error 9.379e-7 and nutrient error 4.470e-7 remain bounded. Calling the
new explanation for every cell/cohort leaves all cells and statistics exactly
unchanged. See `evidence/responsiveness/eligibility-planet.log`.

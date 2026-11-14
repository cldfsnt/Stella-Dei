# Isolated next capability: inherited grazing

Production v13 remains untouched. This prototype adds feeding allocation0–1 to
real donor-funded offspring, mutating symmetrically by at most.1. It reduces
photosynthetic capacity and increases maintenance. Feeding consumes only OTHER
living cohorts. Simultaneous demand prevents loop-order predation advantage.
Half consumed carbon is assimilated, one quarter respired with explicit oxygen
budget, one quarter enters detritus. Nutrient in both waste streams is recycled.
Respiration and detritus decay share the same finite oxygen budget.

This is an authored mixotrophic grazing strategy, not yet an animal, taxonomic
species or scientific reconstruction of evolutionary history. No timer unlock.
The cell-scale mixing approximation allows competing lineages to encounter one
another; spatial pursuit and prey preference are not implemented.

Tests: actual daughter with feeding.08097 grows.01→.03207 in18darkdays while
feeding-disabled control declines to.00419 and prey-free to.00362. It consumes
.08250prey carbon and funds real gen2 inheriting feeding. Carbon/nutrient mass
balance, simultaneous order invariance, bounded capture and oxygen limitation
pass. Equal nutrient-replete comparison demonstrates photosynthetic cost.
120day day/night web test includes actual births and checks accounting.

Still needs independent review, fullworld/resource-budget integration and
playability evidence before any production change. Prototype source and fresh
logs should be checkpointed frequently.

# v44: distinguish identifiers from diversity

Todd reported seeing “variation 20599.” Current source has no literal variation
label, so its exact screen field cannot be identified without a screenshot.
Serial lineage IDs and cumulative births were plausible sources of confusion.

HUD now says Births since start. Inspect and snapshot distinguish Colony ID,
parent ID and Generation. Help explicitly says IDs are serial identifiers, not
numbers of living colonies/species, and births include colonies that later died.
The local count includes every finite positive-biomass cohort consistently,
including tiny colonies previously hidden by a display-only threshold.

No global population scan, phenotypic merging, variety cap, simulation formula,
randomness, save field or rendering geometry was changed. Four cohort slots per
cell remain the current storage model. A high historical ID alone is not a
large active population or a growing ancestor registry.

Validation: 14 reported JS/shell tests pass. New fixture covers ID20599, parent
and generation, tiny positive biomass, zero/singular/plural local count, and
snapshot immutability. The real-world30day QA example had48 births but only18
living cohorts in10 patches; it is not Todd's world. These tests establish text
and data semantics, not the identity of the number in his reported screen.

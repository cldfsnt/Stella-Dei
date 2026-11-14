# Organized producer implementation candidate

Development only until actual-world, rendered intervention and save gates pass.
No claim of true plants, multicellular speciation or a guaranteed innovation.

## Conserved tissue

Total living carbon remains `biomass`; `support_mass` is a subset, not extra
carbon. Frond mass is the difference. Inherited `organization` allocates new
fixed/assimilated carbon to support. Daughters receive donor-funded proportional
tissue. Mutation changes future allocation, not existing tissue. Old save fields
are preserved, with both new fields zero.

Support consumes extra oxygen-limited maintenance carbon (0.12/day). Mortality
and grazing remove support proportionally; it is not free armor. Exposed height
above water adds damage; ordinary dry-habitat mortality also applies. Movement
sheds support into source detritus and releases its bound nutrient, then moves
only the surviving frond fragment. The shared eligibility predicate rejects a
fragment below resolution after respiratory cost. Identity is not duplicated.

## Continuous light competition

An initial implementation switched every cohort in a cell to a different 3 m
attenuation/linear uptake model as soon as any support existed. Review correctly
identified an unacceptable discontinuity. That branch was removed before final
ordinary acceptance. It was checkpointed only as development work.

Current code retains the existing 20 m attenuation and phenomenological uptake
response. Actual frond mass supplies an unshaded growth budget. Smooth bounded
height weights redistribute that same budget between competitors; support cannot
increase total unshaded production merely by existing. In open water it costs
collecting mass and maintenance; in a crowded patch it can gain a larger share.
There is no hard top-layer ordering or infinitesimal cell-wide model switch.
The separate instantaneous light-share helper distributes a finite absorbed light
pool; it is potential interception, not a stored measurement of fixed carbon.

## Fresh pure gates

18 tests pass. A 1e-10 support perturbation leaves total fixation and a neighbor's
biomass within 1e-7 of zero-support baseline. All original grazing and motion
controls still pass. Production controls after ten days:

- Open support 0.9491554 versus open flat 0.9868515 biomass.
- Crowded support 0.72340095 versus lower flat 0.2393979.
- 21 of 32 founder seeds express actual inherited support within the controlled
  thirty-day scenario. Eleven do not; innovation is not promised.
- Carbon/nutrient conservation passes through growth, grazing, daughter creation
  and support-shedding relocation. Support remains within total biomass.

The isolated earlier prototype's optical constants/results are not the current
production model. Actual full-world climate and mobile screenshots are separate
acceptance evidence. Fine-water intervention is explicitly player-added/removed
water, not part of a closed-world conservation test.

Final numeric gate: 19 model tests pass. All-support colonies (zero collecting
mass), daughter partitioning, maintenance and grazing preserve the strict subset
constraint despite f32 rounding. Subset clamps adjust tissue classification only;
they do not alter total biomass/carbon. A support-only cohort cannot relocate as
an established collecting fragment. Existing capacity rejection remains intact.

Actual controlled Planet 100-day integration passes with real daughters and
support, no Sandbox plants/rabbits spawned, conserved carbon/nutrient ledgers,
real grazing/relocation and a fine-water +0.1/-0.1 m roundtrip. See the actual
Planet log for measured counts. This controlled fixture is not a claim that the
ordinary generated seed necessarily develops organization in twenty days.

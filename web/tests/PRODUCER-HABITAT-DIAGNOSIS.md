# Actual habitat diagnosis and sustained organization

Frozen biological model, seed 1337, full generated-world climate. No organism,
trait, biomass, support, temperature or sunlight assignments in these runs.
Extra founders are explicit resource-paid Seed actions, not evolved daughters.

## Why the unmanaged neighbor habitats failed

Three adjacent dry patches were raised to at least 1.5 m with 45 actual +0.1 m
water actions, then seeded through the real tool callback. Patch 3420 fell to
0.195 m on day 1 and 0.016 m on day 2. Patch 13598 fell below 0.2 m by day 3.
Patch 13594 supported a real organized daughter, lineage 8, then dried below its
habitable range by day 10. These are hydrology/establishment failures.

The original center remained warm and wet. Its organized lineage 11 grew to
0.01810 biomass on day 10, but declined to 0.00740 on day 20 while grazer lineage 9
accumulated real intake; by day 25 only that grazer remained. Resource competition
and grazing are implicated, not a blanket thermal-fitness problem. The current
local-first reproduction rule also delays adjacent dispersal until local slots
are full; repeated local offspring consumption can prevent that opportunity.
This is a diagnostic mechanism lead, not proof that every failure has one cause.

## Explicit managed-water comparison

Same initial player seeding/habitat setup, with a once-per-simulated-day check:
when any of the seven local patches is below 0.3 m, apply real +0.1 m actions until
it is at least 0.5 m. This is an external player intervention schedule in a test,
NOT a hidden game automation or a claim that water is conserved with additions.

- Unwatered 40-day run: no living support-bearing lineage remains.
- Managed 40-day run: two remain, support sum 0.00825274 kg C/m² across patches.
  It used 200 precision-water actions in 50 intervention events.
- Managed 100-day replay: two remain, support sum 0.01676711, total biomass
  0.18095162. It used 500 precision-water actions after the initial 45.
- At day 100, generation-2 lineage 13 lives at a neighboring patch with biomass
  0.1570513 and support 0.0141500. Its actual generation-3 daughter 56 lives in
  the original patch with biomass 0.0239003 and support 0.0026171.
- These are organized photosynthetic/grazing colonies, not true plants or animals.
  Four real relocations occurred; existing support shedding/regrowth semantics
  apply. No organism was respawned or assigned organization.
- The final 12,255,188-byte v6 state passed invalid-save rejection and exact
  restoration. The genuine compressed state and day-100 screenshot are retained as private test evidence, not published in this repository.

## Usability conclusion

This establishes a sustained environmental opportunity without changing biology.
It does NOT make 500 taps acceptable gameplay. The next isolated habitat candidate
will test ordinary coarse Water+ and an explicit selected-depth action to reduce
input burden. Neither automatically refills water. The day-100 schematic is also
small and needs clearer visual separation from a mat/feeding marker, without
inventing extra biological mass or a taxonomic unlock.

Evidence is in `evidence/producer-diagnostic/`. The diagnostic generator is
`egl-producer-diagnostic-prepare.py`; it makes an isolated test copy. Biological
source remains frozen. The existing native shutdown allocation warning persists.

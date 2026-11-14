# Explicit habitat maintenance comparison

Biology is unchanged from the frozen producer model. All runs use generated seed
1337 and full climate, actual initial Seed, then three additional resource-paid
neighbor Seed actions and 45 initial fine-water actions to establish shallow
habitat. No traits, support, living biomass, temperature or sunlight are assigned.
The test checks once per simulated day and invokes an actual player action when
one of seven local patches is below 0.3 m. This schedule is a harness scenario,
not automatic watering added to the game.

## Actual 100-day results

| Maintenance action | Actions after setup | Living support-bearing cohorts | Support sum | Total biomass |
|---|---:|---:|---:|---:|
| Existing +0.1 m repeated until ≥0.5 m | 500 | 2 | 0.0167671 | 0.180952 |
| Existing coarse Water+ tap | 70 | 2 | 0.0103096 | 0.262646 |
| New explicit target exactly 0.5 m | 148 | 2 | 0.0141036 | 0.384883 |

Carbon-density sums are kg C/m² summed over occupied patches, not a single patch
or global total. These are not dose-matched interventions: coarse Water+ adds 1 m
to the selected patch only; fine increments can overshoot 0.5 m; the target sets
exactly 0.5 m. Habitat persistence changes climate and ecological trajectories,
including mutation opportunities. Results do not guarantee the same outcome for
other seeds or management choices, and do not prove a universal optimal dose.

Unwatered expanded/seeded neighbors lose living support by day 40. Traces show
neighbor habitats drying below the biological threshold and center cohorts
competing with actual grazers. Managed runs retain genuine inherited structure.
Coarse management includes a generation-7 support-bearing descendant at day 100;
target management includes a generation-3 descendant. These organisms also graze;
they are organized microbial producers/consumers, not taxonomically true plants.

## Guard and persistence gates

Planet target setter rejects nonfinite values, negative targets, values above
5 m, invalid indices and non-Origin mode without changing water. Targets 0 and
5 are accepted; actual signed depth change is returned. Shared PlayState callback
rejects a stale selected point and invalid input in the native game harness.
Both 100-day runs pass malformed-save rejection and exact v6 restoration, including
real support tissue. Existing native shutdown allocation warning remains.

This tests the real shared native game handler, not browser initialization or
physical Android interaction. Joint WASM/export and UI checks remain integration
gates. Screenshots show actual day-100 state, but the small producer schematic
still warrants a separate readability improvement. Raw worlds/screenshots/logs
are retained as test artifacts; publish only through the coordinator's artifact
and privacy workflow.

## Recommendation

Use existing coarse Water+ for routine replenishment; use the explicit 0–5 m
target for deliberate precision. Both require a fresh player action and add or
remove external water. Neither persists a target, silently refills a pond, adds
organisms or guarantees survival. The target is a convenience, not a prerequisite
for genuine long-lived organization.

### Reproducible endpoint details

Fine increments: lineage 13 (generation 2) has 0.1570513 living carbon and
0.0141500 support; its daughter 56 (generation 3) has 0.0239003 living carbon and
0.0026171 support. Coarse Water+: lineage 8 (generation 1) and lineage 115
(generation 7, parent 101) retain actual support. Exact target: lineage 7
(generation 1) and lineage 178 (generation 3, parent 133) retain actual support.
These lineage numbers are run-local identities, not species names.

The source generator `web/tests/egl-producer-diagnostic-prepare.py` wraps the
existing actual-engine harness, instruments daily habitat/cohort conditions,
and optionally invokes real coarse or target callbacks. It does not modify
biological equations or install a recurring game action. Reproduction remains
stochastic and donor-funded.

Frozen SHA-256:
- `src/simulation/microbes.zig`: `f11b13d7a76b102e49abca50b2c00f7b930bd9b067fa0679249345b82c52c5ac`
- `src/simulation/planet.zig`: `b790419bc66b1626bb1853987f8a6834bd2dcee54a9990dded6a5b4dc4647d96`

No further biological edits are part of this acceptance boundary.

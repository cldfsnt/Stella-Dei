# Proposed observations, distinct from current state

Design only. No runtime or save schema implementation is included.

An optional disclosure in Life can preserve genuine events that players miss between inspections. Current conditions and current cohorts remain the primary snapshot. Observations describe past simulation events, not a complete family tree, species unlocks, or proof of causal mechanisms.

## Bounded records

Keep two durable first-event records and at most 16 recent observations. Each stores simulated time, applicable patch and lineage IDs, actual support/collecting masses and height, and measured water, temperature and biological light at the observation. Label the ring as recent observations, not complete history.

- First support tissue observed: hook the actual update crossing zero to positive support, consistent with the glyph predicate. Even tiny positive tissue is an observation, not an established plant class.
- First support-bearing daughter: hook successful reproduction with the actual resulting daughter carrying positive support. Generation alone is insufficient.
- Later presence/absence transitions: record whether living support-bearing cohorts remain, using the existing simulation pass rather than another full scan every rendered frame.
- Optional explicit intervention observations: record player-requested water or climate changes with before/after values. Do not label subsequent decline as caused by that intervention.

“No living support-bearing cohort remains” must not become “the lineage went extinct.” A surviving cohort can shed support during relocation. Event creation must not consume random numbers or alter the simulation.

## Persistence and presentation

Use a versioned save field with bounded validation. Old saves default to empty observations; never fabricate pre-load history. Preserve first-event records when recent entries are overwritten. Repeated reads do not append events. Show historical conditions separately from current conditions, with no inferred environmental cause.

## Acceptance tests

1. An ordinary coupled-climate run creates transient support and later loses it; the observation remains readable after the glyph disappears.
2. Successful reproduction with actual positive daughter support records a daughter event; failed reproduction and a merely positive generation do not.
3. Relocation shedding support does not report lineage extinction.
4. Reads leave arrays, RNG, counters and simulation time unchanged.
5. Save/load preserves exact events; old saves have no invented history; the ring stays bounded.
6. At 320 and 390px, open, scroll, close and reopen the optional disclosure without obstructing play or adding permanent HUD rows.

## Visual follow-up

Real playtests show tiny positive support can be hard to distinguish from a mat and feeding dot. A future schematic may separate the support shape above the mat while keeping the actual-positive-support-and-collecting-tissue gate. Improved framing or legibility must not invent biomass, imply physical scale, or replace the actual habitat with decorative organisms.

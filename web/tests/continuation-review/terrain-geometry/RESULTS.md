# Terrain-tool same-frame geometry candidate

Isolated from rooted-founder and deployed files. Source base is the live Wetlands tree; only Planet and Play change. Raise/Lower retain their exact elevation limits, rates, neighborhood order and pentagon duplicate behavior. Each assignment calls setTerrainElevation: unchanged values return immediately; changed values update that one transformed point with the same terrainPoint/axial-tilt calculation as full rendering/save restore.

## Why
Normal web frames apply held terrain tools, then simulate, then render. Previously only rendering refreshed transformedPoints, so same-frame physics could use old terrain geometry. Direct tool→Advance could similarly precede a render. Immediate action-local refresh closes that boundary without a persistent dirty flag or a new per-frame/per-tick scan. Normals remain on their existing rendering-only job schedule; simulation does not consume those mesh normals.

## Actual native gate: PASS
Eight actual typed tool cases: Raise/Lower × ordinary cell6/pentagon cell0 × axial tilt0/23.4. Every action's transformed points matched a full refresh bit-for-bit before rendering. Elevations exactly matched the old update sequence; all other saved material state remained unchanged.

Each case ran an actual Play.update frame (30ms raw frame demand at72000×, one1440s physics tick). Instrumented actual Planet.simulate entry asserted all transformed points current. Full saved state/RNG matched a restored/refreshed control with the same tick, excluding exactly camera, camera_target, camera_distance and target_distance (legitimate update interpolation). No biology, schema, time-step or resource formula changed.

Counters recorded7 local transform refreshes per changed action; repeated clamped edits and no-tool actions recorded0. No render was needed for tool freshness. Runtime candidate adds no per-frame/per-tick checks, arrays, allocation, jobs or global geometry traversal. It performs at most center+6 small transforms per brush call, only for represented elevation changes; existing render upload remains unchanged. This is bounded-work/source proof, not a measured speedup, frame-rate or device-performance claim.

## Retained QA failures
1. Old native adapter lacked the preview startup field; corrected only in QA Game.
2. Native startup used163842 cells while the immutable input has40962; startup topology corrected only in QA.
3. Unlabeled assertion abort with20ms×72000 frame demand; f32 conversion can fall below the1440s threshold. Named errors and30ms unambiguous demand were used for the final passing gate. Candidate source did not change through these corrections.

No rooted-source changes, promotion, full web build or deployment. Other terrain-writing tools are outside this narrow Raise/Lower fix and are not newly certified. No additional run is needed before coordinator review.

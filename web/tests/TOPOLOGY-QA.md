# Browser grid compatibility QA

New browser worlds use subdivision 6 (40,962 points). Native defaults are unchanged.
Version-1 browser saves with subdivision 6 or 7 are accepted without conversion.
Subdivision 7 saves keep all 163,842 point IDs, data, plant traits and animal state.

`save_game.replaceWorld` validates first and refuses an unfinished normal-computation
job. A different topology is generated in a separate arena, fully populated, and
only then committed. The prior world is destroyed after successful commit. This
briefly requires memory for both worlds plus the parsed save. No resampling occurs.
The one-ring brush at level 6 approximates the physical footprint of three rings
at level 7; existing saved worlds retain their original brush behavior.

## Actual production-engine test

`egl-topology-prepare.py` makes an isolated source copy for the existing native EGL
harness. Input fixture `/tmp/stella-day5-topology7-save.json` is a validated actual
five-day subdivision-7 ecosystem save, not a mocked world. The fixture stays out
of published assets. Run with `STELLA_EGL_INTERACT=1` and a unique capture prefix.

Verified 2026-11-13:
- Real new level-6 planet generated 40,962 points.
- Dry-land focus succeeded; zoom lowered target distance; placement added two rabbits.
- An unfinished queued normal job rejected load without replacing the world.
- Invalid saved array shape preserved the entire level-6 save byte-for-byte.
- Loading the old level-7 save generated the proper 163,842-point topology and
  recaptured exactly the same 34,880,319 JSON bytes.
- Forced animal-capacity growth after commit preserved plant-trait storage,
  checking arena-copy ownership against the earlier overlap regression.
- Loading back the level-6 save restored exactly its 4,996,057 JSON bytes.

See `evidence/topology/roundtrip.log`. Native EGL verifies actual engine code and
serialization, not Android WebGL performance, browser lifecycle or touch gestures.

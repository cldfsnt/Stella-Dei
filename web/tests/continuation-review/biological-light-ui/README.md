# Biological light summary mock UI

Current production shell from 59e127c, with explicitly mocked native replies only. Supported managed preview and CUA checked the 358px-wide panels in a desktop browser viewport, not a physical mobile device or actual WebGL game.

- Origin Plant summary shows zero as `Biological light: none now (not screen brightness)`.
- Selected Life panel shows positive .123456 as `0.12× reference (not screen brightness)`.
- Missing/null light shows `Biological light: unavailable`, not zero/night.
- Screenshots visually inspected: labels wrap within each narrow panel, no horizontal overflow; vertical scrolling remains available.
- Fixture and source hashes are retained. No production physics or native export changed by this QA. No browser simulation/device performance claim.

Preview was stopped after verification. Fixture is excluded from release runtime files.

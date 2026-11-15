# Proposed selected-patch balance, not yet implemented
Scope: Sandbox only, one explicitly inspected patch, session-only observer. Bind world/storage/cell/mode. Begin a fresh interval when the player selects/inspects a patch; unavailable until an actual coupled tick completes. Display actual observed simulated duration, never call it a whole-world census or a guaranteed rolling day. Reset on selection/world/load and invalidate on direct plant/water/terrain actions at that patch rather than silently mixing godtool input into autonomous growth. Paused time does not accumulate. No biology, RNG, save schema, full-world scan or per-patch array.

Actual source seams:
1. `Planet.simulateVegetation`: snapshot input -> result of `Ecology.growTough` before neighbor loop = signed local physiology change. Label growth/maintenance/environment, not pure photosynthesis or exact carbon.
2. Same function neighbor loop: actual represented before/after cover increment = incoming spread. Count accepted placement separately; it can replace genotype, so no individual ancestry claim.
3. Final clamp actual adjustment separate if nonzero. If vegetation is affected outside these seams, explicitly mark unexplained delta rather than assigning a cause.
4. `Life.aiStep`: after `Foraging.takeTough` and actual assignment at watched `idx`, sum represented oldcover-newcover only for successful bites. No estimate from number of rabbits, desired hunger or net decline.
5. Tick-start/end actual selected cover and net difference. Check (physiology + incoming spread + clamp − actual bites) against endpoint difference with explicit floating arithmetic residual. Observational sum is diagnostic, not a material authority.

Suggested details: `Observed 2.4h: growth/maintenance +0.012 · spread +0.003 · grazed −0.008; net +0.007 cover`. When no tick or an intervention breaks continuity, show warming/reset, not zeros implying no grazing. Keep current trait and temperature/water facts beside the receipt. Do not promise defense benefit, infer cause from toughness, call patch replacement a species extinction, or add another permanent overlay.

Acceptance before any promotion: observer on/off exact full saves/RNG; actual warm-world selected Tender and Tough trajectories; zero-bite positive-growth, actual bite, flooded negative physiology, incoming placement, selection/load/action reset, paused interval, no disabled-mode overhead beyond constant guard. This follows stats v70 freeze; no changes in current experiment.

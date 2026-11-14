# Origin UI implementation and evidence boundaries

The new-world menu offers **Origin: simple life** and **Sandbox: plants & rabbits**.
Origin sets `Game.startOriginNext` and consumes it in `PlayState.init`; loading via
`initWithTopology` does not consume this new-world choice. Existing worlds remain
Sandbox according to the versioned save migration, owned by the persistence work.

Origin starts empty and paused. **Seed** deliberately introduces an existing
photosynthetic colony, not abiogenesis. **Nutr. +** explicitly adds an external
nutrient input. No plant or rabbit tool is presented in Origin; input routing is
also mode-checked by gameplay code. Water/terrain/climate remain interventions.

**Habitat** first locates existing living colonies, including declining ones for
rescue. Empty candidates prefer actual low-latitude (|z|<.35),1–5m suitable water
above neighbor count, then other suitable shallow-water fallback. It does not manufacture water, biomass or births.
If none exist, the visible feedback says so. The initial generated transformed
point bug (raw water mass added as kilometres) was reproduced with a136374km
camera and fixed by the gameplay worker to match terrain-upload geometry.

Turquoise mat symbols use `Microbes.biomass(cell)`, never the modern vegetation
array. Radius increases with biomass; max512 projected candidates/max64 glyphs,
normal close view only. Symbols denote cell-scale carbon biomass, not gigantic
individual organisms. Surface Inspect displays real biomass, depth, temperature,
nutrients and dominant living lineage/generation/traits. No inferred speciation,
adaptation, modern plant/animal emergence or long-term survival is claimed.

HTML mode labels poll only a constant-time mode export once per second. Full
biomass/goal scanning happens on Guide Open/Check only. Origin goal codes100–102
mean no live biomass, living biomass, or recorded microbial reproduction. Guide
and manual explicitly state the limits of this first microbial mode.

## Executed here
- Production shell VM tests: Origin/Sandbox labels, first steps, guide reopen,
  blocked localStorage, pre-runtime/export absence and existing storage paths pass.
- First Origin native engine compile passed and startup reproduced the geometry
  bug above; this is not post-fix visual acceptance.
- Independent rendering worker is assigned corrected320/390 actual control,
  seeding, mat/state and menu acceptance. Integration owns browser preview and
  publication. Follow their actual execution report before calling this complete.

## Corrected startup / actual menu acceptance
After the generator fix, the real MainMenu Origin button was clicked through
actual native GLFW callbacks at320x640 and390x700. Both reached Origin with zero
vegetation/rabbits, paused, Seed selected. Camera distances were5285km and5279km
on naturally generated suitable shallow-water cells, rather than136374km.
Visually reviewed320 mode menu and390 focused habitat; buttons/caption/toolbars
fit. Evidence: `evidence/origin-menu`. Repro uses
`egl-origin-menu-prepare.py`, `egl-origin-menu-build.zig`, and environment
`QA_WIDTH=320 QA_HEIGHT=640` (or390/700). These tests do not seed or fake growth.

Final focus helper `habitat_focus.zig`:2/2 tests pass for live rescue priority,
low-latitude1–5m tier, fallback and polar exclusion. Final coupled production
Habitat+Seed gate is assigned to gameplay worker, not replaced by helper tests.

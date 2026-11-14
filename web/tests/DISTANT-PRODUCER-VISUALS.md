# Distant producer morphology

Production NanoVG map markers now remain visible out to 4.5 planet radii,
including globe view. Screen-size LOD is clamped to 0.32–1.15; a contrasting
plinth and dark vector outlines preserve separation against water/land/ice.
Close views retain 512-neighbour search. Wide views inspect actual cells rather
than sampling a stride that could miss a small occupied patch. Rendering is
allocation-free and capped at 64 de-cluttered glyphs. Climate overlays omit them.

Origin chooses the living cohort with greatest real support mass, falling back
to dominant biomass. The glyph uses `Microbes.producerForm`: mat, cushion,
rosette, ribbon, branching or canopy. It is a population-morphology symbol,
not an individual count, taxonomic species or a decorative timer unlock.
Color encodes inherited thermal optimum (cool cyan, temperate green, warm gold).
Sandbox uses a branching population symbol with its actual inherited optimum.

Five visual-helper unit tests pass. Full browser static-library compile is an
integration gate. Physical-device rendering/performance remains unverified.
Actual engine captures must be reviewed before claiming visual acceptance.

The newly used vector path/stroke operations exposed dormant NanoVG Zig 0.13
compatibility errors. `appendCommands` now copies const input into the existing
reserved command buffer before transforming it, rather than mutating temporary
literal arrays. `atan2` uses Zig 0.13's two-argument signature.

Living cells now draw biomass-scaled organic green ground footprints even when
their morphology glyph is decluttered. Adjacent occupied populations blend into
a patch; no footprint is added to empty cells. Dense (>0.3) populations at close
LOD have two smaller shoots of their actual form to read as colonies. These are
population symbols, not a claim of individual organism counts. The controlled
six-form fixture spaces actual occupied cells across a 0.12-radian habitat ring
so de-cluttering does not hide most of the comparison. It is not evolution proof.

Origin Seed mode now marks actual seedable visible cell centers with green +
target rings, checked through the same `Planet.seedEligibility` used by the
seed action. Targets include current water, temperature, empty cohort slots,
nutrients and carbon checks. They are capped at64 and separated by38 screen
pixels to avoid an unreadable blanket. The selected patch has a larger green
ring when valid or a salmon ring/X when invalid; the generic white selection
is suppressed in Seed mode. No model values or eligibility are changed here.
The bottom reason text and Find-seedable behavior are integrated separately.

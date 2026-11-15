# Source-audited integration boundaries, before prototype promotion

This is a source audit, not a test result or shipped functionality. Production remains v57; isolated soil/root work must not be imported simply because a local transfer kernel conserves water.

## Current coupled ordering

`src/simulation/planet.zig` runs thermal work, liquid/wind transport, swaps current water/vapor arrays, and runs atmosphere-water exchange before biological work. New uptake must use those current arrays, not `newWaterMass` scratch or diagnostic rainfall history. Existing hydrology is skipped for dt>=15000s; a new soil model needs an explicit compatible time contract rather than silently advancing one water subsystem while another is suspended.

`simulateMicrobes` currently skips every cell with no biomass and no detritus. Finite soil evaporation/drainage therefore cannot be inserted only inside that biological body. Empty substrate must still exchange water. Soil-only patches must NOT be marked reproductive-active: that would change legacy RNG consumption and add biology work to abiotic water bookkeeping.

## Physiology is more than a successful transfer

The isolated hydration core currently combines its signal with external habitat through a maximum. Its `effectiveHydration` still fades to zero at the old20cm aquatic threshold and excludes temperature<=273.15K or>=355K. New actual throughflow must not silently replace that habitat law or add a second reserve signal. All canopy-dependent support uses must consistently exclude both paid root and storage fractions; no double tissue use.

A represented water receipt proves neither photosynthetic growth nor survival. Compare actual carbon, nitrogen, oxygen, mortality, cutoff, support and inherited allocation in the coupled scheduler before asserting any advantage. Preserve failed small-reserve and coarse-timestep cases rather than selecting only successful phenotypes.

## Establishment, motion, and offspring

The real exploration/propagule path admits finite dry destinations; fallback reproduction and relocation still use the aquatic `habitable` gate. A root-enabled resident growing on damp substrate would not by itself demonstrate a complete land-life cycle or dry-land motion. Do not change these gates incidentally. Record destination soil ownership, offspring paid tissue, post-birth available reserves, next-tick fate and boundary behavior independently.

Patch soil never travels with a colony. Manual moves, autonomous support shedding, death, grazing, terrain edits, water tools, save restoration and return-only cells require explicit ownership tests. Old defaults must remain disabled/zero with exact legacy state and RNG; enabled soil hydrology necessarily changes water motion even with zero roots, which must be labeled separately.

## Performance and persistence gate

A dense f64 soil pool at40,962patches adds327,696bytes before allocator/container overhead. This is a size calculation, not a runtime benchmark. Measure empty-world and occupied-world full ticks and saves; do not claim constant-time global simulation. Legacy loads must not prefill moisture or infer it from rainfall history. No schema change until the finite local mechanism and actual benefit survive independent review.

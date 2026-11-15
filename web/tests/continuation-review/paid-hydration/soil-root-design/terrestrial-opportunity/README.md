# Actual world has film habitat, but no exposed living canopy

Fixed all-cell census at production days30/60/90; no simulation or model change. There are18/64/41 living colonies on10/37/37 patches. ZERO living cohorts have their paid canopy above standing water. Minimum living depths are1.219m/.1653m/.1734m; maximum paid heights only.00764m/.03465m/.03770m. This is an aquatic community, not established terrestrial producers.

Warm exactlydry cells number4/3/2, with NONE immediately adjacent to occupied patches. Warm positive water shallower than20cm numbers735/692/677;668 indices occur in all three snapshots, but only0/1/1 are adjacent to occupied patches. This is potential moist-film landscape, not proof of sustained moisture, reachable land or survival. Legacy worlds have NO soil state. Nonzero filtered rainfall at these patches is historical condensation, not a stored reservoir or continuous rain promise. Only2 warm dry indices persist across all snapshots; continuity between snapshots is unknown.

## Why the chosen drained patch refills

Patch12352's terrain is5005.269km. Four actual neighbors have higher surface heads, roughly251m,353m,1479m and2673m above it; two are lower. Removing0.705m standing water does not reshape these terrain gradients or isolate the patch. The previous actual drain trace independently resolves the first refill: at tick1 BEFORE atmospheric phase it already contains58.0000458 native water (7.5624mm), with zero condensation; evaporation/infiltration reduce that to7.5306mm. Tick2 also adds34.01794 native condensation (~4.4355mm), so later refill is both lateral transport and atmospheric input. No claim that all refill is one process.

## Distinct numerical scale warning

Actual liquid transport forms f32 totalHeight=elevation+waterDepth for both endpoints. At radius-scale elevation~5005km, adjacent representable values are.00048828125km=.48828125m apart. That is much coarser than observed centimeter canopy heights. This is a SOURCE-derived precision hypothesis, not yet a proved flux bug or a reason to alter biological survival rates. A fixed-input expression comparison is the appropriate next diagnostic.

## Actionable mechanics implications

Water− is water removal, not drainage infrastructure; expecting one click to create persistent land in a connected basin is unsupported. Increasing root conductance already did nothing beyond k1 because opportunity vanished under returning water. A defensible progression path needs (a) material conservation fixed, (b) coherent shallow water/head representation, and (c) actual accessible exposed moist habitat with paid autonomous propagation and inherited root variation. The current world has some potential film habitat but sampled living phenotypes and local dispersal remain aquatic. Do not force a plant unlock, suppress rain, repeatedly refill/drain, or select a favorable patch after outcomes to imply success.

summary.json preserves every living phenotype, all depth bins, fixed patch neighbors and repeated-snapshot index sets. Quantities are read-only reconstructions from hashed originals and the exact saved native topology dump; this is not a new full-engine experiment.

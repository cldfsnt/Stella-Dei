# Fixed Wetlands day7→21: real progression, not land establishment

**Completed unchanged**, all840ticks plus independent day14→21 restart. No care, reseeding, assigned root allocation, rate edits or extension. Complete endpoint/RNG byte-exact. Prior day7 evidence/input is preserved.

## What ordinary play produced

-267→**1,140 living colonies**,239→**391 occupied patches**.
-**2,115 paid births**,1,242 disappearing living identities,11actual movements. Per-tick newborn counts match the engine's paid birth counter; identity balance closes. No individual loss cause is inferred.
- All six actual growth forms:228mats,431cushions,214rosettes,87ribbons,27branching,153canopies. Maximum generation6. Morphologies are not species or invented animals.
- Summed biomass density across patches2.76855→18.55486kgC/m². This is a sum across same-area cells, not one local density or a claim of mass without resources. Actual full scheduler photosynthesis/upkeep/feeding supplies the result.
- Positive actual grazing over the interval:56,120,857,666.09683kgC removed globally and14,030,214,416.524208kgC grazing respiration in the model counters (planet radius5000km; large patch area explains the scale).537living endpoint cohorts have nonzero recorded lifetime grazing. These are real grazing counters, not decorative fauna or inferred feeding from a shape.

## Root progression and retained negative

39positive-root identities observed;29developed paid support during this continuation. Day21 has20living root-allocation cohorts,17with paid support. First supported root record is tick693/day11.55. All living allocation values are1/32; no values assigned by QA.

Original mutant421 survives: day7 biomass0.00517727→day21 0.01523034, but its support remains0. It produced five actual children1213/1407/1840/2051/2391.1213 and1407 survive;1407 has support0.0000351503 and actual root tissue≈0.00000109845kgC/m². Thus inheritance and tissue maturation are genuine, not merely a prescribed trait fixture.

**No allocated root-water credits or positive hydration signals anywhere in the fixed interval.** There are zero positive/current-demand hydration records; an empty Fraction oracle is not positive funding proof. All3,664 recorded supported-root post-step states are submerged: minimum depth64.422mm, maximum cohort geometry height12.988mm, smallest paired water-above-height margin62.723mm. This is a read-only f64 calculation from logged post-step states, not a claim that every internal phase was captured. It supports the observed lack of exposed root demand. Soil and roots existing does not mean land establishment or demonstrated root benefit.

## Actual v74 player visit, inspected

The predeclared lowest living supported-root ID is **704**, patch36453, generation2, root1/32, paid support0.000448760, biomass0.0148622, actual lifetime grazing0.00410402kgC/m². Released `stella_visit_growth_form` selects exactly704's actual rosette form; no fallback phenotype or artificial organism. Screenshot `day-21-visit.png` visibly shows the rosette with several distinct real neighbors and23%patch-biomass share. Actual Details click shows ID704/gen2 and its own≈0.015kgC/m², water≈0.15m. Both390×700 portraits were visually inspected: terrain/life visible, controls and panel legible. All saved ecology/resources/RNG remain exact after only camera fields are normalized.

This is native software rendering, not Android/browser WebGL, device FPS or a survival benchmark. Host QA main18.597s (840ticks plus logging/save/render), restart9.000s (420ticks). No runtime ceiling or integrity failure occurred; no hidden extension.

## Concrete next gameplay opportunity, not implemented

Visit now genuinely reveals evolved diversity rather than returning only the old mat. At a mixed patch, the next interpretability gap is following the **chosen lineage's** actual growth/feeding instead of only patch totals:704 is23%ofpatch biomass, so patch-wide change can mask it. A narrowly scoped selected-lineage Watch using existing biomass/support/lifetime-grazed values could show honest per-interval change and explicitly report disappearance without inventing a cause. This needs no forced root advantage, new physiology or prolonged survival trial. Root uptake should continue to say unavailable/zero as supported, not be inferred from allocation.

## Archive

Prereg57b99dd, harness63a8d8f. Every copied simulation file matched prior verified preview physics before applying the identical existing observer hooks. Root credits are counted once before consumption; mortality/growth evaluations are not summed as new physical doses. Day14/day21 and logs are losslessly gzipped; identical restarted endpoint is hash-only. No artifact exceeds8MiB. Original day7 save is referenced by hash rather than duplicated. No release/source/deployment changes.

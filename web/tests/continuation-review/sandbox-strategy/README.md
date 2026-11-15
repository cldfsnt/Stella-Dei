# Existing Sandbox strategies: thermal inheritance, not grazing forms

Read-only audit of exact shipped mechanics and immutable warm day14/day30 saves. Nine pure/imported tests pass; no production changes or new world runs. Source hashes, raw test log and complete living-plant inventory retained.

## What is real today
Sandbox Plant stores ONLY optimum temperature and generation. Offspring optimum varies locally; growth and neighbor replacement use thermal fitness. This is a real inherited environmental tradeoff. At identical cover/satiety/time, Foraging.take has no optimum/form/defense input and produces exactly the same debit. Every Sandbox sprout is rendered with the hardcoded `branching` glyph; blue/green/yellow are thermal-optimum bands, not three defended plant strategies. Origin's separate paid support/morphology/feeding system must not be conflated with this.

Day14:117positive patches,102sprout-eligible, thermal optima290.678–298.969K, maxgeneration4. Blue115patches/60.325cover, green2/1.376cover.
Day30:89positive patches, only12sprout-eligible, optima289.371–301.706K, maxgeneration8. Blue78/2.281cover, green11/2.115cover; no yellow in either input. Cross-time color shares are confounded by location, weather, grazing and colonization. Do not call the green increase proof of grazing resistance.

Finite foraging slows sparse consumption, but there is no protected per-cell tissue or trait-specific refuge. Hungry movement chooses richer accessible neighbors using cover+0.05, water and temperature; no defense preference. Exactly zero cover cannot grow on its own; existing neighbor colonization can restore it. Warm30 evidence already shows four actual post-extinction recolonizations and a finite bust/rebound, so adding immortal cover or globally weakening rabbits is not warranted.

## Most substantive small next candidate
One inherited, costly continuous handling-resistance trait (‘toughness’) could make fast tender versus slower defended plants real. It should reduce rabbit acquisition rate, NOT create inaccessible immortal biomass or free satiety. Costs must reduce positive production and propagule investment while leaving respiration/environmental losses intact. The separate proposal fixes a first experiment; nothing is implemented. This is a new hypothesis, not an explanation retrospectively assigned to existing graphics.

## Source seams
- simulation/ecology.zig: Plant, grow, offspring.
- simulation/planet.zig: simulateVegetation local growth, neighbor offspring/replacement and cover addition.
- simulation/life.zig: aiStep actual paid bite; hungry target selection currently raw cover.
- simulation/foraging.zig: finite time/hunger/resource budgets and conservative satiety credit.
- states/play.zig renderSprouts: Sandbox always branching, color from optimum; actual Inspect shows cover/generation/temperature adaptation.
- save_schema.zig aliases Ecology.Plant; save_game captures/copies plantTraits. A new field automatically entering JSON is NOT enough: explicit model identity, defaults/validation/legacy refusal and replay gates are required.

Reproduce inventory with web/tests/analyze-sandbox-strategy.py <warm-day14> <day30>; paths/hashes in inventory. Pure gate src/qa_sandbox_strategy_audit.zig imports actual production functions. This audit reads traits and existing behavior; it makes no future fitness prediction.

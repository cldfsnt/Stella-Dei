# Warm Sandbox through day30: boom, bust, early recovery

Fixed no-care day14→30 continuation completed exit0. Production biology, rates, climate and saved schema are unchanged. Source/fixture preregistration895492d and per-tick peak observationc6c9c45 preceded outcomes. No extension or new intervention was performed.

## What actually happened
The already saved warm16 world begins with82rabbits and61.70total vegetation-cover units onday14. Rabbits rise to a measured per-tick peak192 byday27, remain192 atday28, then fall to164 atday29 and82 atday30. Cumulative births66→176 and deaths0→110; exact population balance is checked every tick. These are model births/deaths, not implied real-world species evolution. No specific death-cause ledger was added, so hunger is suggested by declining satiety/food, not individually proven for all110deaths.

Vegetation peaks62.713 atday16, then declines to3.75566day29 and rebounds to4.39598day30 (+17.05%). Actual cover consumed drops from4.89096 onday29 to2.22994 onday30. At endpoint89patches retain positive plants,79 within the frozen213-cell dry-connected component. Component cover4.39559. This is severe depletion, not total island annihilation or proven stable long-term recovery.

Every-tick observations record66positive→zero transitions and38zero→positive transitions. The latter includes FIRST colonization, not38recoveries from extinction. Four patches explicitly recolonize after an observed earlier local extinction:25/20076 atday29,330/26714 atday30. Example25 reaches0 atday26 and.01931cover atday30. Surviving patches also regrow under reduced grazing; no immortal per-cell floor or replenishment was added. Results and all2,074daily patch records remain available in results.json/run.log.gz.

## Player-facing blocker and minimal recommendation
The original selected center436 ends at exactly0cover. The samecenter native day30 screenshot shows bare ground even though82rabbits and89vegetated patches survive elsewhere. This can look like whole-island failure when the actual ecology has dispersed. No additional feeding/rate patch is justified by this single run. A small Sandbox ‘Find surviving plants/rabbits’ navigation action would let the player follow real survivors and recolonization. This is a proposal only; no UI or production implementation here.

## Integrity and limits
Endpoint complete save reload and true10tick uninterrupted/restored continuation are exact; original input restored. Cover stays finite[0,1]. Read-only feeding instrumentation records actual bite debits and satiety increments, no extra model random calls. Total continuation cover removed277.43305; actual satiety under-credit fraction7.9613e-6 (0.000796%). Sandbox vegetation is phenomenological cover, not a closed elemental carbon/nutrient model; no new whole-material conservation claim.

Input is prior controlled warm scenario:19actual plant-brush taps painted37cells, with16explicit fixture-stocked rabbits (including deterministic genders/RNG), followed by14days of real coupled dynamics. This run adds no plants/rabbits/water or climate care. It does not establish all-island survival, equilibrium, cross-seed robustness or timestep convergence. Fixed island membership uses starting depth<=0.5m, not a coastline classifier. The ending screenshot is paused native software rendering, not browser/device proof.18.742seconds is the instrumented native960tick runtime, not FPS or mobile speed; observer logs add overhead. No measured performance claim.

Reproduction: generator web/tests/egl-sandbox-warm30-prepare.py, same native EGL build seam as production finite-foraging acceptance; QA_PULSE_SAVE is the pinned warm day14 endpoint. Summarize using web/tests/analyze-sandbox-warm30.py. Raw large endpoint remains outside Git with SHA/path in provenance; logs compressed, copied source/public exports pinned. Explicit QA exit skips inherited teardown after original restoration.

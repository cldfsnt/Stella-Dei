# Stable warm shoreline versus recorded harsh weather

## Practical result

Existing paid rooted life CAN grow on exposed moist ground without reducing mortality. The controlled warm shoreline supports real finite-soil uptake and strong growth; hardiness costs growth in that environment. Replacing only the temperature forcing of the harsh thin-margin record also changes rooted decline into growth. This supports Todd's concern that severe climate fluctuations, not universally incapable organisms, are a major gameplay obstacle.

No mortality or exposure coefficients were changed. No new law/schema was created. The naturally evolved small supported cohort remains fragile; these outcomes do not establish that present mutation/demography will readily discover the chosen founder phenotype.

## Fixed experiment

One isolated native ReleaseSafe test executes twelve fixed local arms: three actual phenotypes × four environments, each420×1440seconds (seven days), with no rerun, care, retargeting, or outcome-selected parameters.

Phenotypes:
- Standard paid rooted founder from actual126 receipt: B .01999999955, support .00499999989, rootfraction .5, organization .25, structure0.
- Actual Hardy choice: same paid C/N/support/root/organization, structure .5.
- Actual naturally evolved supported125 day7 endpoint from combined1337 ordinary: complete recorded genotype/tissue, B≈.002681, root1/32. Not enlarged to founder size or assigned extra tissue.

Environments:
0. Stable hospitable shoreline: .5mm surface water, T=298±2K daily sinusoid, biological incident light=max(0,sin(dailyphase)), maximum1. Rooted body starts20mm tall (Hardy17mm), so this is not hidden full submergence.
1. Periodic replay of actual126's60 recorded final-physiology temperature/depth/light values.
2. Periodic replay of actual1845's60 recorded final-physiology temperature/depth/light values.
3. Same1845 depth and light as2, replacing ONLY temperature with the298±2K forcing. This isolates temperature within this local assay; all four scenarios were generated before reading results.

Each arm starts identical finite experimental reservoirs: soil .7101186234866845kg/m², available atmospheric carbon .2kgC/m², mineral N .02kgN/m², oxygen carbon-equivalent capacity .2. The unchanged shared-soil solver debits actual finite soil and credits vapor; unchanged law3 receives that exact receipt with lineage ownership. Gas carbon/oxygen update from actual fixation/recycling; nutrient/dead matter follow existing physiology. Soil and resources are NOT refilled. Carbon and N totals are checked every step within1e-5 float accumulation tolerance. Soil never increases. Existing root, maintenance, photosynthetic, light, cold, establishment and geometry formulas are unchanged.

IMPORTANT: this is a controlled local physiology test, not Planet.simulate. No atmosphere/column, rainfall, lateral flow, bare-soil evaporation, migration, reproduction or competition is simulated. Standing depth is an externally specified boundary, not generated or water-budgeted hydrology. Root phase and physiology see the same imposed environment, unlike actual fullscheduler phase changes. Biological night is retained. The finite carbon reservoir is a lab condition, NOT a player resource grant or exact current-world atmosphere. Results establish conditional capacity and tradeoffs, not a seven-day world forecast or exact reproduction of previous natural trials. Repeating the recorded24h weather seven times is a prospective stress cycle, not observed seven-day weather.

## Results

|Phenotype|Warm shore day1 / day7 B|126 replay day7 B|1845 replay day7|1845 warm-temperature-only day7 B|
|---|---:|---:|---:|---:|
|Rooted|.0307294 / .1428151|.0088871|Dead tick152 (60.8h)|.1652146|
|Hardy|.0249205 / .0864440|.0053479|Dead tick214 (85.6h)|.0635209|
|Natural125|Dead tick32 (12.8h)|Dead tick2|Dead tick17|Dead tick31|

Warm shore standard expands7.14×, Hardy4.32×. Standard pays .0338221kg/m² root water across seven days, leaving soil .6762965; Hardy pays .0171692, leaving .6929494. Both receive positive funded root hydration on every step. Real support maintenance and fewer photosynthetic leaves remain costs. Standard ends with only .00581646 available carbon; the warm-temperature-only1845 arm has .000346955, showing finite resource limitation rather than guaranteed exponential growth.

Hardiness delays death in the cold1845 replay but is inferior in the warm setting. It also loses to standard in this simplified126 replay, unlike the original fullworld24h comparison. That difference is retained, not hidden: the assay deliberately removes climate/root-phase dynamics and does not claim to reproduce natural relative fitness.

Natural125 starts just above the existing .0025 unresolved-establishment cutoff. It gains some carbon in the warm shallow scenario but still crosses the cutoff within12.8h; the warm-temperature-only1845 arm dies before positive growth. Thus a small near-threshold juvenile's failure is not evidence that all supported phenotypes lack warm habitat capacity. Dormancy discussions must distinguish cold stress from night/juvenile reserve and explicit establishment cutoff semantics.

## Design judgment / next practical action

Do not globally weaken mortality on the basis of the earlier negative sites. First make a genuinely stable warm moist margin attainable and discoverable in the actual world, then verify the paid standard/Hardy tradeoff through one real player journey. A prospective fullscheduler climate/thermal-scale review is warranted: .5mm versus27–70mm liquid water and near-freezing final temperatures are materially different regimes, and stable temperature alone changes this assay's result.

Todd's dormancy idea is also relevant specifically to transient stress. A dormant strategy should pay for protection and recovery, stop acquisition/reproduction, retain finite losses, and specify near-threshold survival; it should not be justified merely by lowering maintenance. That separate proposal belongs to the other worker. No dormant behavior or temperature modification has been installed here.

## Reproduce

`python3 web/tests/prepare-shoreline-climate-feasibility.py`, then run lifecycle-build.zig against `site-tmp/shoreline-climate-feasibility/src/climate_qa.zig`. Inputs and complete copied-source SHA256 manifest are retained. Native build/test exit0, initial run only; actual microbe/shared-soil imported source tests also execute. No live/shared simulation edits, schema changes, device-performance claims or deployment.

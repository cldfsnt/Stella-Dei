# Exposure and within-step reserve signal: independent design critique

Read-only review, no implementation or production enablement. Preserve the negative near-quantum result: actual ID2003 charged on3/10 ticks yet endpoint reserve and physiology did not improve. That outcome motivates separating hypotheses, not adjusting coefficients until a winner appears.

## Biological scope and exposure

The old adapter evaporates funded reserves into atmospheric vapor irrespective of whether the cohort is submerged. Suppressing that direct atmospheric loss for submerged tissue is a defensible model hypothesis. However gas/water exchange under water is not simply terrestrial transpiration: a primary experiment on submerged wetland leaves measured gas-film effects on exchange with surrounding water, not a universal storage evaporation coefficient ([Colmer and Pedersen, 2008](https://pubmed.ncbi.nlm.nih.gov/18086222/)). This supports distinguishing interfaces, not any chosen rate or microbial vascular-plant claim.

`hydration_continuous_core.aquaticSubmergence` is the existing smooth15–20cm compatibility fade. It is NOT tissue geometry: a1cm cohort under10cm remains fully exposed by that law, while a50cm canopy in20cm receives no direct atmospheric loss. `producerHeightMeters` already derives height from paid non-retention support, efficiency and toughness. Actual aerial fraction would be the more coherent long-term exposure variable, but vertical leaf-area distribution is absent; even height-based linear exposed fraction is a declared approximation. Zero-height mats and dry surfaces need explicit non-singular behavior, not an epsilon that creates a habitat benefit. Do not silently introduce this additional law into the registered2×2; first label the depthfade comparison honestly.

## Time averaging

Let initial funded reserve be W0, fixed capacity C, and potential linear loss over the interval L. Real emitted water is min(W0,L), and the endpoint stays max(0,W0-L). The exact mean reserve for this frozen-rate path is W0-L/2 when L<=W0; W0²/(2L) when L>W0; and W0 when L=0. Divide by C only for positive valid capacity. Zero capacity or zero reserve gives zero hydration. Using (W0+endpoint)/2 after early exhaustion overstates the mean.

This integral is exact only for the stipulated frozen capacity/loss path, not the full physiology. M.step applies mortality, support change, photosynthetic max/habitat weighting, exponential growth, resource competition and cutoff recycling. Evaluating those nonlinear operations once with mean hydration does not equal integrating the actual hydrated/dry phases. Average hydration must not survive as water or confer immunity after tissue death. Describe it as an approximation and compare identical horizons at1440/720/360-second steps, retaining all discrepancies; do not change the production timestep or parameters to force agreement.

## Required controls before interpretation

- Preserve all four old/new exposure × endpoint/mean signal arms and original coefficients, fixed initial worlds and horizon, no chosen successful target.
- Separate actual funded water ledgers from the dimensionless hydration signal: emission can never exceed available reserve, and no analytic averaging returns water.
- Zero reserve/capacity/allocation, zero frond tissue, exact exhaustion, early exhaustion, no-loss and fully submerged cases.
- Same paid support costs and nutrient/C/O2 budgets in all arms; no free change to capacity or growth coefficients.
- Depth0, tinypositive,15cm,20cm and height-crossing examples; cold/hot/deep exclusions retained. Check changed surface liquid from uptake does not covertly select exposure using stale depth.
- Loss coefficient/light fixed within each analytic interval; if growth changes tissue, document operator ordering. Identical world/save replay and original mutation RNG behavior remain gates.
- Do not infer land establishment from retained water or improved founder biomass. Require actual funded descendant persistence over repeated natural exposure/replenishment cycles.

Source inspected: experimental hydration_exchange.step uptake→evaporation→M.step→settle/deposit ordering; hydration_continuous_core producerHeightMeters/effectiveHydration/aquaticSubmergence and mortality/photosynthetic response. No calibrated biological rates claimed.

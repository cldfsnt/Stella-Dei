# Bounded soil flux review, after the negative gate

Design only. No new outcomes, implementation, rate selection by survival, or production changes.

## What the current rates actually mean

The capillary prototype declares capacity C=1kg/m²=1mm water equivalent and maximum infiltration I=1kg/m²/day=1mm/day. A24-minute conditioning interval can therefore supply at most1/60mm; the actual funded0.0166166mm is correct. These constants were deliberately frozen for numerical comparisons, NOT empirically calibrated or independently justified gameplay rates. Earlier CAPILLARY-BUCKET prereg explicitly calls its head law a surrogate, not hydraulic conductivity/matric suction.

The inherited atmospheric phase has an86400s relaxation time, but it relaxes the WHOLE atmospheric saturation deficit. That is not a one-day lifetime for a tiny soil pool. Here the first exposed request is5.084566mm/24min, versus0.0166166mm available soil. A constant-rate linearization would exhaust soil in~4.7s; this is a diagnostic ratio, not an actual solved depletion time. At720s the atmospheric request is still2.718328mm. Entire available soil goes first to atmosphere; roots are called afterward.

Thus current failure is primarily a mismatch of substrate supply/access and atmospheric demand plus sequential priority. It is not evidence that real roots cannot help land organisms. Nor is arbitrary larger prefilled capacity justified.

## Minimal coherent candidate to preregister

Retain a finite physical soil pool W, capacity C, initially zero. All recharge comes from an actual represented standing-water debit. Keep the existing capillary head factor and explicit cold exclusion. No nominal water, protected escrow, lower reservoir or new rain source.

Treat substrate evaporation as a distinct conductance-limited access route, not an unlimited opening of all pore water to the atmospheric deficit. A minimal uncalibrated law is E_potential = W*(1-exp(-dt/tau_soil)), capped by the remaining SAME atmospheric evaporation budget after standing-water evaporation. This bounds dry-soil depletion smoothly and uses no additional pool. An initial transparent game-scale hypothesis could reuse tau_soil=1 simulated day, with existing C=1mm and I=1mm/day: wet filling and exposed evaporation both operate on day scales. This is a NEW declared phenomenological law, not a calibration or proof of realism. It must be approved before execution. It should be judged on actual paid responses, including failure, not adjusted until pioneers survive.

Compute root requests from the SAME pre-exchange W and actual paid root tissue, exposure, temperature, light and demand. Express conductance units explicitly:
R_i = min(D_i, k_root * rootCarbon_i * (W/C) * dt_days).
k_root has units kg water/(kg root carbon day); W/C is dimensionless. At current C=1 this is numerically the same pre-allocation request as the old helper, but unlike multiplying by dimensional W it remains meaningful if capacity is deliberately changed later. C=0 gives zero flow. Retain k_root=10 and all biological costs for the first candidate; no growth/mortality coefficient changes.

Allocate the finite accessible soil simultaneously to E_potential and all R_i, proportionally if their sum exceeds W, without slot priority. Root physiological credit cannot exceed the actual represented, receiver-funded root share or its own D_i. Evaporation receives no physiological credit. Root plus evaporation actual receipts are one total soil debit and one vapor credit; rounding loss/uncredited flow is explicit, never drinkable. The atmosphere cap applies to evaporation, not a second independent soil evaporation call. This simplified model does NOT establish thermodynamic closure or plant gas-exchange realism.

All these claims must refer to one clearly defined scheduler instant: use current physical pools/environment and current living cohorts, settle the shared soil exchange once, then use its root receipts in that same biological interval. Store only transient per-step credits if ordering requires it; no second withdrawal after advection. Advection may transport the resulting vapor normally. Empty/dead patches still evaporate/recharge; no organism ownership of environmental soil. This requires explicit integration review, not simply inserting a second root call.

## Recharge semantics and gameplay scale

Water+1m adds vastly more standing water than this1mm soil capacity; it does not instantly wet the soil. One24-minute wait stores~0.0166mm because infiltration is rate-limited. Removing surface water then retains only that amount. A player-facing beta must not describe one tap as a full soil recharge. Either explain the wetting wait or deliberately define a different infiltration law in a separate pre-outcome amendment. Do not silently refill to capacity.

The proposed one-day soil-access timescale makes an Advance-one-day action meaningful while preserving a drying cost. It does not guarantee hydration sufficiency: this donor has little paid root tissue, and normalized root conductance at low W may still leave demand mostly unmet. Capacity remains1mm, not an invented deep soil profile. If this remains unplayable, evaluate supply, root efficiency and gameplay goals explicitly rather than pretending numerical failure or selecting a favorable organism.

## First acceptance gate, if approved

Use the SAME conditioned donor/input already archived, root0/.25, no new wetting or transplant. Compare old sequential law versus the newly declared shared law over48minutes; no timestep sweep. Require actual per-route paid receipts and no duplicate/root-over-demand credit, material budget within the already declared practical bounds, zero-demand and empty-cell behavior, cold/deep exclusions, slot permutation, and unchanged legacy disabled branch. Report soil remaining, actual root demand satisfaction and biomass; geometry-only differences remain separate.

Only after that, one preregistered day-scale exposed/recharge test can assess whether the declared timescale yields a meaningful choice. No mutation, lineage establishment or sustained terrestrial ecosystem claim follows from either gate.

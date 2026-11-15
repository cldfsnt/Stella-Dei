# Exposure compatibility and within-step hydration: design checkpoint

Status: proposal only, pending independent review and coordinator approval. No implementation, new assay or production change. Quantum result9b85609 stays frozen, including zero end reserves and no physiology advantage. This is a physiological hypothesis, not another numerical receipt correction.

## Two independent factors, fixed before outcomes

E0: existing evaporation at all depths. E1: same evaporation coefficient multiplied by 1−A(depth), where A is the CURRENT aquaticSubmergence compatibility function (fade15–20cm). This is explicitly NOT a measured air-exposed frond fraction. A1cm submerged organism at10cm can still evaporate under E1; a50cm emergent organism at20cm cannot. Those limitations must be shown, not concealed. Producer-height-aware exposure is a separate unselected hypothesis requiring its own tissue geometry rule, not a substitute chosen after seeing results.

H0: current hydration signal uses end-of-step store. H1: analytical mean reserve during a constant-rate depletion step, divided by fixed start-of-depletion capacity. For valid capacity C>0, initial funded W0 in[0,C], and nonnegative potential evaporative loss L:
- L=0: mean reserve W0.
- 0<L<=W0: mean reserve W0−L/2.
- L>W0: mean reserve W0²/(2L).
Use overflow-safe equivalent forms; clamp only roundoff at valid bounds, reject invalid inputs. Capacity0 implies signal0 and no protected water. Actual evaporation still removes min(W0,L) by represented receipt into vapor return. Mean reserve is an observation of previously funded water, never a new reservoir or material credit. Store signal is combined with the existing compatibility/temperature gates, without changing those gates.

L remains0.1×frondMass(kgC/m²)×dt(seconds)/86400×(0.5+0.5×clamp(light,0,1)), optionally multiplied by E1. Coefficient units are modeled kgWater per kgC per day. Capacity remains10kgWater/kgC×paid support×inherited allocation. No coefficient, mutation, reproduction or uptake-policy tuning. Reserve/capacity fixed for calculating this step's signal; subsequent real core metabolism and settlement retain existing material accounting.

Mean signal into nonlinear growth, max and extinction cutoffs is NOT exact integration of the organism dynamics. Three timestep comparisons below are mandatory and all divergences retained. Global latent heat remains absent from existing hydrology; this does not establish thermodynamic closure.

## Bounded proposed assay

Use two fixed actual saved full cells/whole phenotypes from completed six-arm run: arm3 patch12397 includes ID2003 (naturally positive allocation, paid support); arm5 patch13668 includes ID1828 (positive allocation but zero support). No trait assignment, favorable lineage search or stripping competing resident cohorts. These are shared-world examples, not independent evolutionary replicates.

Before branching law comparisons, attempt one actual finite-source paid charge using the reviewed numerical transaction on the original saved liquid pool. Reuse the exact resulting owned state in every paired law; zero-support remains uncharged. Preserve source debit/escrow ledger. Imposed habitat depths0m,.175m,1m are explicit laboratory initial conditions, not a claim of player reachability or natural colonization. Any setup pool removal/addition is recorded as an external setup sink/source, then fixed equal among the four law conditions; never silently count it as conserved internal transfer.

Each full-cell run has finite shared CO2 budget1kgC/m² and oxygen capacity1kgC-equivalent/m² at start, no replenishment; original nutrient/detritus/cohorts retained. Temperature300K and light1 are declared prescribed common conditions, not real-world climate. Apply each actual core flux once to finite shared budgets, refuse negative resource balances. Water uptake remains actual finite pool-derived, not prescribed h; evaporation returns vapor, no external irrigation/condensation refill. Geometry depth follows remaining physical liquid rather than a continually reset pool.

First gate:4law combinations×2cells×3initial depths×dt1440/720/360s, each over exactly86400s =72 runs. Dry initial-depth cases extend to fixed30days at1440s =8 long runs, without selecting survivors or changing parameters. Entirely dry uncharged and zero-allocation/zero-support controls, h0/h1 boundary arithmetic, zero/infinite/NaN time/capacity invalidity are separate unit gates, not tuned ecological cases. If this scope is too large, narrow BEFORE execution, never based on outcome.

Record starts/ends and fixed daily checkpoints: every lineage's mass/support/allocation/owned water, cumulative real uptake/evaporation, liquid/vapor/escrows, fixed/respired/grazed carbon and nutrient inventory, all extinctions and reproduction. Inspect same-interval convergence differences across dt; do not call one timestep the truth. Retain finite drought exhaustion or negative outcomes. Expected invariants, not expected winners: no protection without paid store/capacity; no water/C/N creation; eventually finite reserve exhausted without recharge under exposed loss; fully submerged E1 loses no water via this evaporation term; H0/H1 identical when loss0; unchanged zero-allocation physiology/RNG.

## Promotion boundaries

Initial cell assay is not full coupled climate, natural selection, land establishment or evolved plants/animals. If supported, next phase requires separately persisted exposure/time model identity, old-save defaults, unsupported-model atomic refusal, actual coupled scheduler and target-WASM tests. A genuine from-zero strategy claim requires later fixed natural inheritance/selection trials, not this imposed-habitat assay. No promotion based solely on a desired survivor.

## Approved pre-outcome amendment (supersedes E1 above)

Before any implementation or outcomes, coordinator and independent review c4c748a replace compatibility-fade evaporation E1 with a paid-height uniform-vertical-frond surrogate: snapshot current existing producerHeightMeters H and actual physical depth D in metres after uptake, before depletion. For finite H>0, fraction=clamp((H−D)/H,0,1); H=0 convention is1 at D=0 and0 at any positive depth. This discontinuous zero-height/tiny-film convention is explicit and tested, not botanical calibration. Compute geometry in f64; no new height/tissue coefficient. Retention allocation reduces aboveground paid height, affecting both exposure and existing light/competition costs. Record height/exposure; no free-benefit claim. Existing15–20cm hydration/growth habitat compatibility remains UNCHANGED as residual phenomenology, not an evaporation proxy. The old proposed fade arm will not be executed.

This first bounded assay calls actual M.step metabolism/competition/grazing but does NOT schedule reproduction/dispersal or mutate genomes. Report births as not simulated, not observedzero natural reproduction. Entire saved cells/IDs are retained, but this is a closed physiology comparison, not the full Planet scheduler or evolutionary selection. Subsequent whole-engine reproduction proof requires a separate preregistration.72+8 scope, fixed parameters, resources and timestep tests otherwise unchanged.

# Independent continuous hydration adapter audit

Source reviewed:8bbdb08 against preregistratione5708e5. This folder initially preserves the independent first run; production and adapter source were not changed by this reviewer.

## First result:72/73 tests pass, one guard defect

`src/qa_hydration_exchange_audit.zig` imports the actual experimental exchange adapter and production reference core.

Passing checks:
- Actual source liquid/owned reserve determine depth/hydration. Paired nominal depth999 versusNaN and nominal hydration0 versusNaN/Inf/1/−1 yield identical material state and flux; those nominal fields are intentionally ignored, not accepted physical sources.
- Zero allocation matches all production cohort fields, nutrient, detritus, RNG and flux across three liquid quantities ×three ordinary timesteps ×48 steps, including alternating day/night. No source water or vapor changes. This is disabled physiology parity, not a complete scheduler/save parity claim.
-100 combinations of conversion/pool/demand test actual represented donor debit, budget ceiling and bounded reverse deposit with explicit scale-relative f64 accounting tolerance. No nominal pool-delta credit.
-11 explicitly invalid area/pool/environment/time cases refuse before mutating cell or pool bit patterns.

Failure retained:
- Finite area1e−250m², finite liquid1billionkg, valid living cell and finite environment pass initial validation, but derived depth cannot fitf32. Adapter still returns a flux and changes cell state. Expected atomic refusal fails: `DERIVED_DEPTH_OVERFLOW accepted=true model_changed=true`.
- This is not a realistic game's mesh area; it is an API fail-closed contract defect. A guard on area finiteness and conversion alone is insufficient to guarantee finite derived arithmetic. Require validated derived quantities before mutation, or a bounded transactional candidate with no commit on invalid results. Do not alter valid realistic areas or physiology to satisfy this witness.

## Read-only semantic review

The two core hydration gates use preregistered `h*(1-aquaticSubmergence(depth))`; the existing15–20cm fade and temperature exclusion remain. Uptake is simultaneous capacity-deficit sharing from represented liquid removal. Evaporation uses owned reserves and credits vapor-return escrow. Escrow settlement and remaining demand do not take nominal hydration arguments; no hidden held-water reservoir exists inside the adapter. QA external wet/dry exposure is a separate experimental intervention. Allocation changes support function, but this does not establish natural evolved adoption or land plants.

Actual area conversion is dimensionally consistent: billionkg/patch ×1e9/area giveskg/m²; division by1e6 giveskm liquid depth. Full scheduler ordering, water phase/latent energy, complete material budgets, all lifecycle destinations, native/WASM parity and performance remain separate gates. Existing ordinary boundary tests are evidence for the preregistered fade, not proof for every valid input.

## Reproduce

```
$ZIG build --build-file web/tests/lifecycle-build.zig --cache-dir "$ABSOLUTE_QA_CACHE" -Dsource=src/qa_hydration_exchange_audit.zig --summary all
```

First source hashes and failure log retained. Owning worker notified; subsequent corrected run must be separately recorded, not overwrite this failure.

## Correction reviewed

Owning worker's293a8c7 adds only a pre-mutation bound:
`maximum_depth=(f64(liquid)*conversion+liquid_return)/1e6` must be finite and representable asf32. This includes all possible initial escrow deposit. `validCell` already requires owned reserves≤capacity, so the initial settlement cannot release additional water beyond this bound; uptake decreases free liquid. No area clipping or physiology coefficient change.

Reviewed corrected source SHA2567733b7912505b9e2ae21c1ab9e05c58c72275d8e8aa91a07cc793fa85ea754a2 and owning worker's rerun of the **unchanged independent test file**:73/73 pass in `../derived-depth-fix.log.gz`. Original source hash matches8bbdb08; first failure remains intact. This resolves the identified extreme-input defect, not all possible numerical or coupled-scheduler issues. Proceed to isolated actual scheduler gate, not production promotion.

# Proposed minimal f64 local gate, pending independent approval

Design only. Inventory found old-world actual aerial demand zero, so this is an explicitly prescribed local-root model test, not naturally emerged rooting. Preserve d1a94eb alternatives and all earlier outcomes. No full Planet migration yet.

## Consistent local receipt policy

Replace all local physical transfers with one staged strictf64 routine, shared by surface→soil infiltration, soil→vapor bare evaporation, soil→surface drainage, root/store→vapor flow, capacity/death return and held→surface recharge. No binade caps, protected escrow or separate special recharge algorithm. Keep same compartments, requests, rates, capacities and ordering. No calls to f128 at runtime; offline Fraction remains oracle.

Clamp request to finite actual source/capacity. Choose represented source after such that actual debit never exceeds request (if nearest subtraction overspends, nextAfter toward oldsource). Derive a conservative f64 debit with strict error-free TwoDiff, rounding downward when needed. Individually funded root/storage receipts cannot exceed this actual source debit or demand. Add transferred amount to physical receiver normally; record actual receiver increment independently, including zero/rounded-up cases. A receiver rounding artifact never increases physiological credit. Never silently correct totalwater by topping up another pool. Simultaneous cohorts share a single source budget using canonical sums/downward grants, no slot-priority leftover; unused allocation remains source rather than biological escrow.

Need precise implementation/review of debit-versus-grant residual: construct final source change from actually allocated grants, recalculate represented debit and bound each credit. If one source quantum cannot be paid without exceeding requests, retain water in source and report unrepresented demand. Do not silently store a grant remainder in an inaccessible compartment. This protocol permits bounded signed endpoint rounding error, NOT nominal source-unfunded hydration.

## Two preregistered acceptance levels proposed

Arithmetic envelope: every physical transfer's exact Fraction source debit minus receiver credit must fall within a conservative envelope derived from the actual endpoint rounding ULPs (two endpoint half-ULPs plus explicitly counted arithmetic/units-conversion error; use a full ULP where directed rounding is used). Derive/prove formula in helper tests, not fit a coefficient to observed errors. Invalid/nonfinite inputs refuse before mutation. Negative source/receiver never accepted. Root/storage physiological credit≤actual source debit and≤demand tested exactly offline; h supplied tof32 core rounded downward, so no signal amplification.

Practical local budget: KEEP existing absolute water budget1e-9kg/m² over seven days and additionally require SUM ABSOLUTE transfer residuals≤1e-9, so cancellation cannot hide drift. Report signed sum, absolute sum, maximum single residual and subresolution request mass/count separately. Also require cumulative credited-signal rounding deficit≤1e-10 times total positive aerial demand for each nonzero-demand cohort; this is a proposed new signal-precision criterion, not survival tuning, and needs reviewer approval before runs. Do not apply a relative-to-tiny-throughput gate to vapor rounding: inventory includes legitimate2.6e-15flows into~250kg/m² vapor where all receiver increment can round away. They must still fit absolute physical budget, source-paid signal constraints and reported relative-error distribution.

These budgets apply ONLY to the fixed local density fixture, not arbitrary oceans or complete Planet. Native-unit conversion/fullworld policies require separate range/accumulation analysis. If proposed bounds fail, retain failure and stop rather than widen them after biological outcomes.

## Fixed test sequence before biological rerun

1. Originalstep27, all recorded actual recharge event operands, zero/full/exhausted/invalid/sourcezero/demandzero, subnormal/extreme error-envelope tests, scalar and fourcohort24permutation tests. Offline Fraction validates actual source receipt, physical signed/absolute residual and no physiological overcredit. Include source-request overshoot witnesses from inventory. No maximum-flow promise on subresolution demand.
2. Actual fixed111value fixture and frozen local-assay operand replay: error-envelope and practical receipt gates only, no phenotype search or numerical coefficient tuning. Confirm partial transfers reflect request/capacity/source, not arbitrary binade boundaries.
3. ONLY after independent review, repeat SAME36seven-day cases, all rates/gases/setup/recharge/root fractions/timesteps unchanged. Both old36resultsets retained. Every actual recharge and infiltration amount logged. Wet/root0 same-environment core parity, finite demand and nonnegative compartments remain required. Report timestep differences and no wet competition cost separately.

Do not add compensation/savefields, tune conductance, simulate extra generations, change depth compatibility or call the result an evolved plant. This gate determines whether a practical consistent water representation can support the already observed paid-root mechanism without numerical flow barriers.

## Approved pre-outcome machine-resolution amendment

The f64 funded-receipt rounding gate and f32 signal conversion are SEPARATE. The proposed1e-10 demand-relative credit deficit applies only to arithmetic loss converting actual funded flow into conservative f64 per-cohort credit, not unmet demand due to resources, and not f32 signal conversion. For h delivered to the f32 core, use downward conversion and bound deficit by the exact adjacent-f32 spacing at that value times demand (a global conservative bound2^-24×sum positive demand for h∈[0,1]). Record both observed deficits independently. This resolves a known precision mismatch before implementation/outcomes, not a post-hoc tolerance relaxation. Physical signed and sum-absolute1e-9 seven-day limits remain fixed.

## Pre-matrix shared-flow rounding clarification

Independent review permits the tiny downward proportional-allocation deficit to remain explicitly UNcredited physical throughflow into vapor, rather than refunding it through a second rounded transfer. This supersedes the earlier wording that every allocation-rounding remainder must remain in source. Actual total source debit stays≤sum desired root flow; per-cohort credit stays≤actual funded share/demand; no biological bonus or protected pool is introduced. The fixed1e-10×aerialdemand f64-credit-loss gate applies to this deficit, reported separately from f32 signal quantization. Large unused requests still remain source; this exception concerns only rounding loss in distributing a paid shared flow. Freeze before any new matrix outcomes.

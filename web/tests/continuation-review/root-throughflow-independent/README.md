# Independent root-only throughflow gate

Three focused new tests plus34 inherited core tests pass in ReleaseSafe (37 total). QA is copied beside the generated isolated simulation modules; production files are untouched.

Preactivation review caught missing `/86400` on the frozen per-day conductance1/10, which would have interpreted it per second. Owner corrected units before outcomes and added invalid environmental guards. This failure is preserved here as source-review evidence, not a failed executed biological arm.

New tests cover both conductances at360/720/1440s with low soil, requiring actual paid flow to match the per-day conductance-limited law rather than the much larger demand cap; positive credits do not exceed represented source debit or demand, and f32 hydration times demand does not exceed credited water. In these deliberately tiny flows, large f32 vapor receives no increment and the negative rounding residual is explicitly observed, NOT repaired or claimed conserved.

NaN/infinite/negative/out-of-range environmental refusals preserve input. Cold, extreme heat, deep water, absent root, zero soil and zero support give no paid flow or signal. Source hashes are recorded. These targeted tests do not prove a practical whole-engine water budget, root0 scheduler parity, persistence or ecological advantage; those remain separate gates.

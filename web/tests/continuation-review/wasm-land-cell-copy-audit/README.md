# Read-only compiled Cell-copy evidence

The exact named WASM from e29c963 (executable sections identical to the frozen uninstrumented beta) contains two explicit368-byte memcpy operations on the column/shared-soil path. First source is the Planet cohort array indexed by the column, destination stack+264. Second source is that stack+264, destination stack+1176, immediately following bare soil demand's toDensity/downProduct/expm1 calculation. Context excerpts and exact calls retained.

Measured candidate Cohort size88bytes; four cohorts plus nutrient/detritus/RNG make Cell368bytes. Two copies per40,962columns imply30,148,032 copied bytes/tick when those call sites are reached. This is a static traffic estimate, not measured instruction counts. It does not assign all310 direct-main memcpy samples to these copies. No Result-copy cost claim is made.

One narrow candidate is justified: readonly borrowed Cell through the capillary→shared-soil call chain. Preserve existing value-taking standalone API wrappers; Planet opts into the borrowed path while owning and not mutating that cell during the call. Keep all validation, phase ordering, allocation, rounding and Result fields unchanged. Do not simultaneously remove diagnostic Result stages or apply the rejected environment/coefficients variants.

Before any promotion: verify these exact memcpy sites disappear in generated WASM, then exact full state/RNG/soil/vapor/ledger results on the frozen empty and actual root-drain fixtures, then one fixed cost screen. Pointer lifetime/alias behavior must be scoped to a synchronous read-only call. No implementation or run performed for this audit.

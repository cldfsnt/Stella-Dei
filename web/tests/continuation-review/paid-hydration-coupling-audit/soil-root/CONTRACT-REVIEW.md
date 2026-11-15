# Independent soil/root kernel contract review

Reviewed design d1f5b70 before implementation. Approved scope for isolated tests: homogeneous-unit parameterized physical exchange kernel, not production hydrology, a calibrated plant model, new mutation law or automatic save-schema promotion.

## Contract to freeze

All local pools, deficits and actual receipts are kgH2O/m²; dt is seconds. Root carbon is already-paid support*u, storage carbon support*r, u+r<=1. Root conductance must explicitly be kgH2O/(kgRootC·second). Define physical infiltration, evaporation and drainage capacities in kgH2O/m²/second (or another fully declared dimensional law), with finite nonnegative inputs; choose no hidden rate. Soil starts empty and fills only from an actual surface-liquid debit. Diagnostic rainfall cannot be credited again.

Stage each transaction and commit only actual represented debits/credits that meet its stated ledger policy, rejecting unrepresentable tiny receiver additions or explicitly accounting residual returns without hydration access. Homogeneous f64 pools simplify the first test but do not prove the later native f32 liquid/vapor bridge. Test large existing vapor plus tiny transpiration, near-full soil, all-zero pools, overflow, subnormal and mixed-magnitude cases. No nominal removal creates a physiological receipt.

Root demands are simultaneous, bounded by paid root mass, finite conductance, soil supply and per-cohort demand. Preserve all slot permutations. Storage covers only residual demand after root receipts, never the same demand twice. Report separate root and storage actual receipts; combined `h_paid=actual_paid_flow/demand`, bounded[0,1], zero demand=>0. Do not label the combined signal h_root. Zero demand means no root/storage spend, not cessation of independent soil evaporation/drainage. Actual transferred water reaches represented vapor; root signal is not material. Soil evolves even when no organisms live there and never follows a colony.

Caller-supplied physiological demand must be explicitly aerial demand if throughflow goes directly to vapor. The kernel does not justify submerged transpiration. Geometry/temperature and habitat combination remain outside this initial test. With no calibrated rates, kernel success proves conservation/fairness only, not useful biological performance.

## Later physiology gate, not silently included

Specify one demand shared by root/storage, then combine paid signal with external habitat once, preserving existing temperature/deep-water exclusions. Do not stack root hydration plus reserve hydration. Choose and preregister the temporal signal policy; averaged reserves and actual throughflow are different observables. Every aboveground support use (height, spread, film protection, light competition) must consistently use support*(1-u-r), while upkeep charges all paid support. Root allocation cannot count simultaneously as canopy/storage. Existing support prerequisite is not a second new trait, but natural inheritance and from-zero establishment remain unproved.

Initial tests should compare root-only/storage-only/neither/both with matched paid tissue and finite equal total resources; any soil partition must have a recorded source debit. Declare parameter sets/horizons before outcomes and retain nulls. Keep later lifecycle, mutation partition boundaries, native-unit receiver precision, legacy save/reset, and natural scheduler tests separate rather than expanding this kernel into an unreviewed ecosystem rewrite.

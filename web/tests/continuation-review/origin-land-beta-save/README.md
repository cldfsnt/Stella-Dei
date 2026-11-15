# Isolated Origin land beta save adapter

Production untouched. Reusable patcher owns only copied save_schema/save_game. Schema8 is an experimental wire identity only, not a reserved production format or exposed migration. Experimental schema8 adds required beta record identity/config/soil/vapor; disabled capture stays schema7 and existing Origin model revision5 remains unchanged. Beta law is separately explicit, not inferred from schema number. Legacy loads reset beta off, never enable existing worlds.

Authoritative f64 vapor (native billion kg) is retained exactly; f32 vapor is a checked derived compatibility projection. Soil density is f64 kg/m² in [0,1], including empty patches. Sparse cohort serialization includes actual root_fraction. Null beta rejects every nonzero root; old versions reject beta config/material. Full validation precedes world changes and allocation; scratch is reconstructed, not saved authority.

Pure actual copied-schema tests exit0: old existing schema tests plus beta sparse-root/empty-soil/sub-f32-vapor/max-u64 roundtrip, version disguises, unknown laws, missing enable, wrong mode, bad shape, NaN/range and inconsistent projection refusal. These are schema tests, not proof of actual apply atomicity or new-process continuation; native scheduler owner must execute those next. Existing canonical file is not rewritten on load; save_io unchanged.

Capture borrows physical arrays, as existing save capture does. Serialize/deep-decode before changing a world. Beta apply does not zero borrowed authority before copying.

## Confirmed old-reader compatibility repair

The first actual candidate off-v7 serialization failed the unchanged production parser with UnknownField. Both beta_origin:null and root_fraction:0 were new wire fields. Retained failed JSON locally and failure log/hash here. The isolated custom off writer now omits both extension fields; off validation/capture requires canonical positive-zero roots (negative zero refused), while beta retains all fields. Final actual old parser accepts natural60 output and all old typed fields exactly match the original, normalizing only input version6 to7. This is wire compatibility, not a claim of byte-identical JSON: optional null/empty fields may be spelled out. The final candidate schema suite also retains positive-root and sub-f32 authority roundtrip tests. No production parser was modified.

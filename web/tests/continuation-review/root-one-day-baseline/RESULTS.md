# Matched production one-day diagnostic result

All three unchanged-production 60×1440 s runs exited 0. Saved/restored 10-tick continuation hashes match exactly in runs.json. These are native actual-engine results, not browser/device verification.

Comparison uses f64 math.fsum of native saved standing water and vapor plus candidate soil density sum × mean area / 1e9. These are stored native inventory units, not kilograms; the physical conversion uses 1e9 kg per native unit. Areas match (7,669,529,600 m²). Soil starts absent/zero. No water interventions.

Production inventory decreases by 2,027,138.573; 2,264,054.085; and 2,341,587.703 native units for day30, day60 and day90. Candidate root0 inventory, including soil, decreases an additional 71,381.219; 76,526.031; and 74,428.799. Candidate stores 27,258.991; 27,234.271; and 27,167.273 native soil units at endpoints.

This is a release blocker, not evidence of conservative integration. It does not identify which phase causes the incremental loss: native f32 phase representation, subsequent advection, changed climate, or interactions require same-state phase replay and scheduler ledgers. Original outcomes remain frozen. No production or model changes in this checkpoint.

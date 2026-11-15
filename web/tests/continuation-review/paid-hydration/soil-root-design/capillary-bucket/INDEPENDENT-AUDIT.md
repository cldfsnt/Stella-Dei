# Independent capillary paired audit

Owner confirmed both logs completed against unchanged source99b181f; each reports eight passing tests. Independently read both source/harness implementations and parsed all9,171 per-step records per representation plus nine seven-day endpoints. No simulation rerun or parameter change.

Offline Python Fraction checks reconstructed hybrid liquid/vapor/rain as f32 before exact rational arithmetic; f64 records use their represented values. In EVERY record:

- Actual soil infiltration gain is nonnegative and no greater than actual surface source debit converted using the recorded area.
- Soil stays within finite capacity.
- Actual standing-water evaporation plus actual soil-water evaporation, in common units, does not exceed the single atmospheric request.
- Cold substrate water is unchanged; positive represented standing water excludes soil evaporation.
- Final no-drain stage equals preceding stage exactly.

All nine paired seven-day initial states match exactly after hybrid f32 promotion, including the small finite source. The head law and phase order are the same; pool representation differs intentionally.

Maximum single-step sum of absolute phase water residuals: hybrid **3.183254224618423e-5 kg/m²**, f64 **5.931633242966307e-14 kg/m²**. Sum of absolute phase residuals across ALL NINE seven-day sequences combined: hybrid **2.2704518106188382e-5**, f64 **6.142108349239315e-14 kg/m²**. The latter pooled audit statistic is not one world's cumulative budget or a chosen acceptance threshold.

Wet hybrid final soil is approximately .9999954403 kg/m² at all three timesteps; f64 approaches1. Dry and small-finite-source endpoints were retained, not discarded. A better numerical ledger does not establish ecological benefit. The original drainage model/evidence remains a separate hypothesis; no prior case or rate was changed to meet a precision limit.

No practical whole-engine precision budget, climate integration, root physiology, or production enablement is approved by this audit. The unchanged compatibility-only drainage parameter is still validated despite being unused; extreme irrelevant values can refuse, a documented API limitation outside the frozen cases.

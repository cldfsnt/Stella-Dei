# Timestep coefficient hoist: correct, no measured benefit

One isolated candidate, no production edits. `PhaseStep.init(dt)` moved outside the beta column loop and passed into `stepPrepared`; standalone `step` remains available. All physical laws/rates, strict receipt arithmetic, root costs, numerical budgets and save fields unchanged. Prepared API refuses mismatched timestep or invalid coefficient bounds.

## Fixed correctness gates

-648 prescribed structural cases (wet/dry/depleted/saturated pools; cold/boundary/warm;dt0/360/720/1440; empty/paid-root cohorts): original, standalone candidate and prepared candidate serialize **every Result field identically**.82 total tests including imported tests passed. These are controlled software fixtures, not ecological outcomes.
-Actual Node-WASM72tick empty-beta complete saved endpoint matches frozen reference exactly: `177388476e42306cadfbe9694bf5cbca003ef8738a2e1765ce667fefa1d1b699`.
-Actual native frozen root-drain ID524 rooted/control replay: both arms' complete saves at0/30/60ticks byte-identical. All1,227/1,220 existing setup, drain, birth, root-water and fate rows byte-identical, including all actual funded doses and subsequent deaths. No trial extension or new ecological condition. Existing restart proof was not independently rerun here.

Initial standalone test syntax error corrected before execution. Offline log comparison initially selected a nonexistent `LAND_` prefix and found zero rows; corrected to actual `SETUP/DRAIN/BIRTH/ROOT_WATER/FATE` tags, without engine rerun. No changed acceptance criteria.

## One fixed ABBA, no trace

Node/V8 WASM ReleaseSafe; same empty beta input,12warmup+60timed full scheduler ticks. Original samples30.769,31.370ms/tick; candidate31.625,30.901ms/tick. Median31.0695→31.2630: **+0.623%**, no demonstrated benefit. Every timed complete endpoint matches reference. No repeated screen or second candidate. Startup, serialization and rendering excluded; no device/browser/mobile claim.

Do not promote as a performance improvement. The source-level repeated initializer hypothesis did not translate into a useful measured gain; whether compiler hoisting or other column costs dominate remains unproven. Original enabled beta cost and prior negative empty-env optimization are retained. No further optimization proposed in this pass.

# Existing-trace depth context, not a changed acceptance gate

All7,373,160 cell-steps from the same completed traces; no engine rerun. Bands classify each cell's actual PRE-transport standing-water depth at that tick. Exact integer classification uses stored area and f32 pool, not the future post-transfer depth. Half-open bounds:0≤d<.02,.02≤d<.2,.2≤d<2,2≤d<100,100≤d. Included zeros in nearest-rank percentiles. Each world's stratified A and outgoing gross transfer exactly re-sum to the prior independent audit.

## Main observation

The approximately1.03mm maximum error occurs only in the≥100m band, which accounts for99.9922–99.9926% of absolute error across the three worlds. At ecological shallow depths the measured errors are much smaller:

| Pre-depth | Maximum depth error across worlds | Approx99th-percentile range | Swallowed positive NET receipts day30/60/90 |
|---|---:|---:|---:|
|0–.02m|.995nanometres|.881–.886nm|0/0/0|
|.02–.2m|7.958nm|7.741–7.772nm|0/0/0|
|.2–2m|122.854nm|57.199–57.619nm|0/1/0|
|2–100m|4.074micrometres|3.803–3.809µm|14/3/2|
|≥100m|1.03029millimetres|.515145mm|10635/14112/16375|

The one shallow(<2m) swallowed NET receipt is not evidence of a biological injury, individual edge rejection, or dead colony. Conversely, these diagnostics cannot prove no gameplay/ecology effect: tiny numerical changes can alter thresholds/lineage paths. There was no visible-harm experiment here.

## Bandwise ratios and limitations

Outputs retain A/incoming and A/outgoing separately, each directed edge counted once at destination or donor respectively. These assign traffic differently and are descriptive, not a new per-band pass rule. A/incident uses incoming+outgoing and therefore double-counts world traffic. Below2m, A/incoming~2.20e−6 to3.38e−6;2–100m~4.72e−5 to6.80e−5;≥100m~.01414 to.01890. A/outgoing and all p50/p90/p99/p99.9/max values are in each JSON. Maximum error relative to a nonzero PRE-pool is also reported, not relative to its much smaller net transfer; zero pools separately counted.

The frozen aggregate A/T=1.34–1.77% still FAILS its0.1% gate. This added context does NOT retrospectively pass it, authorize new solver variants, certify biological safety, or justify another performance run. It explains why the maximum absolute-depth headline should not be described as millimetres of error at shallow soil/film cells.

Saved script `web/tests/stratify-liquid-wasm.py`; hashes link original trace, graph and prior audit. Research stops after this evidence checkpoint.

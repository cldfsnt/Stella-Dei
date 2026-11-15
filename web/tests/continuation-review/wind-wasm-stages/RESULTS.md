# One diagnostic, no repair claim

Fixed four-run window22:10:53.695–22:11:02.930 UTC, explicit sibling CPU holds and release afterward. All four instrumented endpoints exactly match both original legacy/candidate full-state/RNG hashes. No rerun, no code optimization.

Baseline25.9196 versus candidate27.1582ms/tick (+4.78%); both candidate runs exceed both baseline. Median stage milliseconds, baseline→candidate:
- Temperature2.2414→2.2927 (+0.0513)
- Liquid/wind3.7967→3.8862 (+0.0895)
- Atmosphere9.9948→10.5538 (+0.5591)
- Rabbit AI8.1551→8.6372 (+0.4821)
- Vegetation/bookkeeping1.7222→1.7758 (+0.0537)

The penalty is broad, mainly in source-identical atmosphere and rabbit code; no new wind check executes in Sandbox and its microbe array is empty. The +1.25MiB Origin cohort allocation therefore cannot directly explain this case. Planet layout changed24bytes, with compiled offsets/code-layout/JIT behavior plausible but NOT causally established. Timers and host conditions can change compiled/runtime behavior: instrumented baseline/candidate totals are about4.7%/8.1% below their earlier uninstrumented medians, noncontemporaneous comparisons. This diagnostic neither erases the original+8.67% nor demonstrates zero legacy cost.

No physics or timing parameters changed. Parent chose practical same-host optional runtime isolation rather than force promotion into classic or perform more favorable-repeat searches. Classic deployed binary must remain exact. This is Node WASM full-scheduler timing, not device/browser rendering performance.

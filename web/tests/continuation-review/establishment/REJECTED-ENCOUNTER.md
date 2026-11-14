# Rejected isolated grazing candidate

Production microbes.zig and deployed v33 were not changed. An external source copy replaced the existing `min(food, predator_biomass * 3 * feeding * days)` desired ingestion with:

```zig
food * (1 - exp(-predator_biomass * 3 * feeding * days / (food + 0.1)))
```

This tests finite scarce-prey encounters and a bounded depletion fraction, not a taxonomic winner or guaranteed succession. The half-saturation 0.1 is an experimental model parameter, not calibrated biology.

The actual Planet probe completed its conservation and state assertions, but the complete imported regression suite passed only 37/39 tests. The failed tests were `real inherited grazing consumes prey and funds offspring in darkness, unlike controls` and `feeding remains finite and conservative at exposed simulated step sizes`. Stable-world post-day30 daughters still suffered roughly92–97% one-day mortality; maximum generation at180days was5/5/6. More cohort slots became occupied, creating a second bottleneck. This did not reliably improve sustained succession, and was rejected for release.

Do not loosen existing tests to declare this successful. A future candidate needs trophic viability, timestep comparisons, late-generation establishment and heterogeneous habitat tests, alongside conservative ledgers and no forced winner.

`rejected-encounter-candidate.log` retains failed-suite output and actual outcomes. This is rejected research evidence, not deployed gameplay.

# Isolated moist-shore lab

This copy is not the deployed game. Experimental microbes/planet derive from the preserved moist-shore prototype; dependencies are shared read-only from the main checkout. Main release source must not be replaced wholesale: it has newer seed-eligibility/UI changes.

Diagnostic planet logs shelf arrivals and per-step growth/death at world fixture cell 3421. The shelf is one explicit geometry/water intervention on day 20. Simulation remains coupled; no organisms or traits are injected.

The bounded neighbor-first experiment uses the existing persisted PRNG and a 25% placement priority, preserving all donor thresholds, paid mass and mutation rules. Local fallback remains when adjacent destination is blocked. The native diagnostic generation optionally overrides this scheduling through STELLA_NEIGHBOR_FIRST for A/B comparison. This environment flag is diagnostic only.

Before any integration, strip logs and reconcile narrowly with production seed-eligibility changes, run microbe/save/conservation regressions, and demonstrate actual shelf establishment. Controlled fitness alone is insufficient.

## Requested ecological strategies roadmap

First finish inherited desiccation tolerance with real shoreline acceptance. Todd also wants genuinely differentiated post-fire strategies, including rapid recovery and delayed reseeding. A later dormant propagule bank must be funded from parental carbon/nutrients, persist in an explicit compatible save design, incur decay and habitat constraints, and trigger germination from real conditions. Fire should transfer biomass to accounted gases/detritus/seed mortality; it must not spawn organisms after a timer. No fire or seed-bank feature is implemented in this experiment.

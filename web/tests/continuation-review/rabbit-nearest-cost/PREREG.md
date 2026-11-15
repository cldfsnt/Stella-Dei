# Actual rabbit cost attribution, before outcomes

Frozen actual warm16 day14 endpoint `foraging-production/warm-actual-end.json`, SHA256362c943ce1e6869876a4c2767a85f4debd61602ab2ec0e44000674d60a892187:82 rabbits,40,962 terrain points. No synthetic512 case or behavior changes in this initial gate.

Copied actual Planet.simulate and cooperative scheduler: restore same input each arm,12 untimed warmup ticks,60 measured1440s ticks. Fixed instrumentation off/on/on/off. Collect full simulate duration, timed aiStep, nearest query, breeding-habitat function plus density/mate loop counts. Exact complete saved endpoints/RNG must match all four arms; restore original. Timers/counters only in copied source, no physics stubs. No rendering in measured loop. Shared timestamp/branch overhead can distort small subphases; off/on whole-step difference measures instrumentation noise/overhead, not an optimized algorithm. Native only, no device/browser frame-rate claim. Require other workers' explicit release before execution.

Next implementation requires coordinator review of actual contribution. Any acceleration must retain exact existing rounded-sqrt comparison and ascending index tie choice; topology/geometry-index options additionally require elevation/tilt/load lifetime invalidation. No algorithm candidate or performance threshold is retroactively selected here.

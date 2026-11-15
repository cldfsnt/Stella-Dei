# Independent immutable-gather ownership/adversarial review

First pure test run:2passed/1failed. The helper rejected equal pointers but accepted offset-overlapping source/output slices, mutating source authority. Failure log retained. Implementation owner added byte-range overlap rejection (including elevation/topology/scratch intersections); independent tests were rerun against corrected source, now4/4pass.

Tests cover reciprocal/self/duplicate topology, same-lane and final-tail transfer, unchanged zero-dt output, forward/reverse output identity, all-source outgoing budgets, zero/tiny/huge mass scales, finite nonnegative endpoints, nonreciprocal rejection before output, invalid inputs, offset mass/output overlap and elevation/output alias. No solver source was edited by this reviewer.

Read-only scheduler integration review: Origin liquid scatter is bypassed while Sandbox branch remains; all wind jobs join before immutable gather; source waterMass and destination newWaterMass are separate allocated arrays; authority swaps only after helper succeeds. Topology is cached by fixed mesh size in the Planet-owned simulation arena, which survives ticks and is destroyed at Planet teardown. Scratch arrays are not save authority. Actual frozen scheduler buffers were disjoint, so initial API defect is not an observed fullworld corruption.

Outgoing budgets use immutable source; duplicate/self edges contribute no extra flow and nonreciprocal graphs reject. Every cell including remainder cells receives its own budget. Late invalid outputs may leave scratch partially written, but the caller does not commit them. Allocation/helper failures in this experimental caller still abort rather than provide a production recovery path.

Reported helper rounding ledger covers final f32 casts only, not f64 intermediate-gather arithmetic or approximate global summation. This is not exact conservation or source-funded per-recipient rounded-credit proof. Fullworld phase, save/restart, numerical-budget and performance gates remain independently required; no production promotion follows these pure tests.

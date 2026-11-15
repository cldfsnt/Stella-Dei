# Compact liquid gather: independent gate

Experimental, no production approval. `zig test src/qa_liquid_compact_independent.zig -O ReleaseSafe`: **3/3 passed**.

Reference: cached gather. Five mass fixtures including wide scales and signed zero; three dt (0,1440,15000); both traversal orders; reciprocal duplicate/self/tail graph and explicitly re-prepared changed same-count graph. Every output bit, widened f32 outgoing edge bit, and both ledger fields match the reference. Nonreciprocal topology and offset output aliases refuse. New heads workspace overlapping mass or output also refuses without mutating inputs.

Source review: outgoing flow was already f32; storage narrows no computed value. Gather explicitly widens at the original arithmetic positions. Validation computes each head with the same f32 expression, stored once. All new workspace overlaps are guarded. As before, prepared topology is an immutable precondition. Invalid finite-number validation remains present; this small independent gate does not separately exercise every malformed numeric input. No claim of exhaustive proof.

CPU released to owner for fixed paired native timing. Performance results pending. Prior cached version remained held: useful same-output reduction of redundant work did not establish consistent speedup. No water-closure tolerance changed.

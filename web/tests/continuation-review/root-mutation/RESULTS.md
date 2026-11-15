# Root-only mutation gate: 73 tests pass

Law frozen in 45558b9 before outcomes. Isolated source generated from the retained archived root-only core; production untouched. No bridge, whole scheduler, production save schema, long survival or adaptive-benefit claim.

- 4,096 successful resource-funded same-cell, neighbor and exploratory births: every legacy cohort field, stats and donor RNG exactly match archived baseline. Root allocation is the only changed trait; parent allocation remains unchanged. Nine tested children arise from zero with positive root allocation. Disabled law and mutate=false preserve inheritance.
- Fixed 65,536 tuples: 513 positive and 508 negative proposals. At zero, negative proposals clip to no change; symmetry applies to proposals/interior, not realized boundary changes. This is reproducible domain-separated event-keyed variation, not proof of independent random streams/worlds.
- Insufficient donor mass/credit, full target, invalid law and invalid root allocation refuse with both cells/stats/RNG unchanged. The mutation runs after all paid birth checks.
- Actual relocation preserves lineage and root trait; support is discarded under the existing movement law, so inherited roots without paid support do not become free root tissue. Actual mortality produces no phantom descendants.
- Aboveground support remains support_mass*(1-root_fraction), retaining the opportunity cost. No new tissue or water is granted. Existing f32 birth subtraction roundoff remains baseline behavior, not exact real-number closure.
- Independent Python hashlib SHA256/endian vector passes. Disabled law1 max-u64 seed JSON roundtrip passes. This is configuration-value roundtrip only, NOT integrated game checkpoint/loader support. New wrappers require explicit config; existing scheduler calls remain disabled wrappers.

73 includes 68 inherited core tests plus five focused tests. QA syntax/const-vector compile failures retained; these were test harness issues, not model outcomes. Source, baseline, logs and hashes are compressed losslessly. Reproduce: `python3 web/tests/prepare-root-mutation.py <isolated-dir>` then Zig 0.13 `test <isolated-dir>/qa_root_mutation.zig -O ReleaseSafe`.

Next integration obligation: persist validated mutation law/seed and thread it through actual scheduler births in an isolated model only. Movement/death never consume the new mutation stream. No production enablement or schema change is authorized by this gate.

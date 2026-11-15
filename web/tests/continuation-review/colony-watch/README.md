# Bounded per-colony observation endpoints (unapplied prototype)

Candidate engine.patch adds fixed-capacity start/end members to the existing Population snapshot. Capture occurs only for the selected watched patch at start and existing actual post-growth/reproduction/movement tick endpoint. Four entries each, no world scan, biology change, RNG, retained lineage history or save fields. Snapshot ID and biomass are matched by exact identifier, not array slot. IDs are emitted as decimal JSON strings with custom serialization, including9007199254740993 and18446744073709551615. Watch JSON buffer grows1024→4096bytes; endpoint storage is bounded. Invalid/missing identities yield null detail instead of fabricated IDs while aggregate observation remains valid.

The standalone formatter proposal unions at most8 endpoint IDs. It distinguishes net gain/loss, unchanged, present only at end and no longer present at end. It explicitly does NOT infer death, births, movement or a cause, and misses colonies which appear/disappear between endpoints. Empty endpoints do not prove inactivity. Numeric IDs, leading zeros, out-of-range IDs, duplicate IDs, >4entries and invalid biomass are rejected; no string→Number conversion. No I/O/timers/persistence.

Suggested UI: collapsed optional retained Individual colony changes section after watching stops/completes, not an expanding live HUD. controller.patch adds the snapshot as optional third render argument; it does not add timers or lifecycle behavior. Main owns integration with shell and presentation.

## Executed verification

-2 snapshot module unit tests passed: exact maxu64 string JSON and bounded valid/tiny/invalid/duplicate identities.
-Formatter tests pass exact IDs, endpoint wording, invalid-data rejection and immutable input. Controller test verifies optional snapshot argument on active and stopped state.
-Actual two-patch scheduler funded-birth fixture: observed initially empty target records the actual newly assigned ID after reproduction; donor pays tissue/credit. Observer-on/off cohorts/RNG/stats/feedback/gases identical.
-64 controlled movement cases (32 RNG seeds × watching source/destination):18 cases relocate. End member snapshot equals actual final cell and source disappearance/destination presence is recorded without death inference. Complete relevant engine state matches observer-off. This uses explicitly assigned finite grazer/prey fixture, not naturally evolved behavior.
-Actual natural30day QA world, cell3421,60ticks/one simulated day: start and end member arrays exactly match independent actual cell snapshots. Biomass0.009361055446788669→0.006635898724198341, colonies2→1. Exact growth/recycle/grazing flux oracles pass, grazing0.0014814876212767558. Full observer-on/off saved worlds identical; pause/selection/load cancellation passes. This does not establish why a particular endpoint member vanished.

QA world SHA256 ce23ae3cdd81b5186dcda3ab8f87c362b8322daf255b76db0b7d158d28904e35. Loaded preserved generated world into current engine; not a new30day regeneration. Native EGL/mobile-policy proof, not Android/browser testing. Existing teardown GPA warning remains. Native source hashes and lossless compressed logs preserved. Initial serializer compilation surfaced too-broad NoSpaceLeft error from bounded u64 formatting; fixed by guaranteed20-byte formatting before unit/native acceptance.

No production patch, shell change, push or deployment by this worker. Engine/controller patch application checks pass against reviewed source; main must recheck concurrent changes, build WASM and integrate optional UI.

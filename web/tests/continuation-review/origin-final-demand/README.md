# Law3 final-demand receipt prototype: focused and native gates PASS

Dedicated source `site-tmp/origin-final-demand/src`; native fixture in separate `origin-final-demand-native`. Production, historical beta law1 and basal law2 copies remain unchanged. No longer ecological trial performed here. Density100 and hydrology ordering unchanged.

## Contract

Experimental schema10 / format origin_land_beta_v3 requires physiology_law3. Law1 remains schema8/v1; law2 remains schema9/v2; legacy remains unchanged. No automatic upgrade or public enabling action. Native fixture explicitly changes only the day30 snapshot identity/config to law3, asserting every other field unchanged.

The existing root signal scratch is widened to f64. Historical laws store their exact f32 ratios widened losslessly and recover the original f32 values; their lifecycle remains unchanged. Law3 stores actual credited kg water/m², alongside explicit u64 recipient lineages. These are receipts for water already transferred to vapor, NOT a new water pool, escrow or later refund. Scratch is excluded from saves.

At physiology entry, compute interval demand from final environment and current cohort. Each mortality/growth use derives a downward-rounded fraction from actual credit / max(entry demand,current demand). A smaller later tissue demand cannot inflate the signal; increased demand lowers it. Zero CURRENT demand, invalid credit/demand, zero/mismatched recipient lineage or domain-ineligible tissue gets zero signal. The same allowance bounds both biological responses for one interval; neither is a second physical spend. Existing effectiveHydration attenuation can further reduce it.

All tick-start/reset/load boundaries clear amount+owner. Law3 clears a processed cell immediately after its physiology call, before relocation/birth. Existing scheduler has no cohort replacement between column receipt creation and physiology; explicit ID matching additionally prevents wrong-lineage consumption. Old-law ratios are not cleared at this new consumption point. No physical arrays are repaired or renormalized.

Memory: old16bytes/patch becomes32bytes amounts +32bytes lineage IDs. Increment48*40962=1,966,176bytes (~1.87509MiB); total scratch2,621,568bytes. Allocation currently applies to beta storage including old beta laws, even though only law3 uses IDs. A whole-WASM memory/performance gate remains necessary before promotion.

## Gates executed

ReleaseSafe helper/core tests passed: drying increases final demand and lowers h; unchanged demand matches paid ratio; wetting to zero demand gives zero root signal; replacement/zero IDs refuse; empty/invalid credits refuse; exact f128-product checks bound h*demand by credit across mixed scales; larger demand floor cannot inflate benefit. Full serialized cells/RNG match frozen law2 core with immersion off/on across48 depth/temperature cases, supplemented by imported core tests. Schema tests preserve old identities and roundtrip/reject new law3/disguises.

Actual cooperative native scheduler and real save_game tests passed:
- explicit migration changes only identity;
- owned capture/decode/apply exact;
- artificial pending receipt+owner cleared by actual load;
- post-step receipt/owner arrays all zero;
- invalid version/hydrology/physiology and disguised old identity refuse atomically;
- beginOrigin idempotent and legacy load resets authority/traits;
- fresh-process2+2ticks equals independent4ticks byte-for-byte, SHA0289d001b988e0e104e6c4a5da45d483c7275cb513ed8fd2325aece601791f6a;
- law1 four-tick, law2 four-tick and both legacy natural/Sandbox ten-tick complete saved states/RNG equal their frozen historical outputs exactly, no normalization.

Initial native compile exposed a preparer semicolon syntax error, retained in build-first-syntax-failure.log; corrected before any native outcomes. Successful build66337 and run63392 exit0. All logs and exact final source/output hashes retained. No survival claim, performance claim or production exposure. Fixed law2 ecological outcomes retain their historical interpretation; upcoming law3 comparison requires actual consumption-site logging, not provisional root-phase h.

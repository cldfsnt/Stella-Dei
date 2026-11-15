# Independent experimental mutation-config acceptance

Design f100c4e/36bb511, copied candidate prepared by owning worker, independent additional QA in a SEPARATE frozen tree. No production/schema promotion. Native EGL ReleaseSafe config-only run exits0.

Verified actual native save.capture / schema parse / save.apply:
- Law1 enabled AND disabled with stream_seed18446744073709551615 preserves the exactu64 and complete serialized state across reset+reload. No JS Number conversion exists in this native/file path.
- Law0+enabled, law0+nonzero seed, unknownlaw255 and unknownlaw2+enabled all reject with InvalidValue and leave the complete previously configured save unchanged.
- Disguised future config under eachv2–v7 rejects with IncompatibleSave before any reset. v6 andv7 valid default imports reset a previously enabled config to law0/false/0.
- Existing owner's runtime gate checks explicit enabledseed42 restart, unsupportedlaw2 atomicity, v7 disguise and Sandbox reset.
- Independent Sandbox→beginOrigin transition resets a deliberately stale enabled/maxseed config. This tests entry to new Origin mode; full Planet generation default initialization is supported by source inspection, not an extra generated-world test.
- Existing native originSaveCheck invalid-load/exact-restore gate passes. No biological trial ticks or six-arm replay were run here. Actual mutation-enabled evolutionary continuation remains the owning worker's endpoint gate.

Read-only source review: config is Planet-owned, captured in Origin and restored after validation/allocations. Law0 is legal onlydisabled/seed0, law1 preserves expliciton/off and anyu64seed. Unknownlaws fail closed; pre-v8 nondefault configs reject. Sandbox apply clears config; supported explicit wrappers receive the saved streamseed, not a recalculated worldseed. Stateless domain-tagged SHA generation introduces no mutable cursor or extra legacy random draw. Process-global QA birth counters are instrumentation only, not generator state. No fitness conditioning or automatic enablement found.

Initial inherited fixture compile failed because an intermediate diagnostic-only outer support variable rename was inconsistent. After the owner corrected its source, the independent copy was regenerated; no model/schema patch or relaxed assertion was needed. Both provenance snapshots and failure retained. Current run includes the inherited unrelated GPA teardown diagnostic; no memory-leak fix claim.

Reproduce: `python3 web/tests/egl-retention-config-audit-prepare.py <frozen-owner-src> <isolated-src>`; build with egl-propagule-visual-build.zig; run QA_MUTATION_CONFIG_ONLY=1, QA_PULSE_SAVE=natural60-day60.json, STELLA_ORIGIN_COUPLED=1, STELLA_ORIGIN_FAST=1, STELLA_ORIGIN_WIDTH=390, LIBGL_ALWAYS_SOFTWARE=1. Native source hashes pin the reviewed fields and calls. No actual browser/Android execution or natural selection outcome is claimed.

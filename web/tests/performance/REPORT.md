# Atmospheric wind cache performance probe

Isolated native EGL full engine from v21, single-thread browser-mode simulation,
390x700 rendering. Renderer explicitly queried: llvmpipe LLVM19.1.7 software GL,
Mesa25.0.7. These are not WebGL/Android hardware results. No main-source edits.

## Baseline bottleneck

Fast 5.008s/123frames/121physics ticks. Actual9.66 simulatedhours/second.
Per tick: atmosphere phase+advection18.11ms, temperature1.79ms, liquid1.93ms,
microbes1.42ms. Atmosphere dominates~78% physics. Render submission1.898s plus
explicit gl.finish295.8ms perwindow. GPU upload52ms ofthatwindow, not dominant.

Code does18 edgeRate evaluations percell; every evaluation repeats the same
localwind tangentbasis construction. Cache only the windvector once percell
perstep, leaving phase, edge formulas, edgeorder, donorcoefficient rounding and
gather summation unchanged.

## Initial test-only cache

Global-f64 scratch probe: Fast5.013s/116frames/224ticks;17.87simh/s. Atmosphere
7.71ms/tick. Fullsix-tick serializedworld hash d523353839672a4 identical to
baseline and allthree requested speeds. This globalarray is not the production
proposal. Lower per-tickwork also lets secondtick fit existing16ms startbudget.
Do not infer guaranteed17.87h/s or smoothAndroidfps; maxframe106ms thisrun.

## Owned candidate

owned-wind-cache.patch is the narrow production candidate. Lazy allocator-owned
[3]f32 cache adds491544bytes for40962cells or1966104bytes for163842cells. Original
wind components were alreadyf32 widenedtof64, so cachingf32 thenwidening retains
exact values. Fresh velocities are cached after jobsjoin, everyphysicalstep.
Nothing is serialized; no save-schema change. Allocationfailure fallsback to
original uncachedcalculations. Oldscratch freedonlyafter successfulreplacement;
Planet.deinit freesit. Lazycache introduces no new failurepoint in worldinit.

Long-run equivalence and lifecycle checks pending; not approved for integration
until recorded below. Existing native shutdownGPA diagnostic remains separate.

## Owned candidate acceptance

PASS: 1800 fixed1440s ticks/30days from same parsed seededworld. Forced-OOM
uncached path and ownedcache fullserialized-world hash3138eaaced1f785 exactly.
Both validate. Cache poisoned withNaNs afterload was entirely refreshed nexttick.
Elapsed35.60s vs26.59s here had concurrentcompilerwork; not a controlledspeedclaim.

PASS: separate fullPlanet allocationtracker aftergeneration+simulation+deinit:
30,265,400 bytes allocated and30,265,400 freed. No cacheleak. Two actual
save.replaceWorld6→7→6 cycles created correctlysized freshcaches and validated.
No scratchsaved and no newgenerationfailurepoint. Existing enginegeneration
allocationcleanup flaws are outside thispatch; lazycache avoids adding to them.

Patch appliescleanly to current main; no main modifications bythisworker.
qa/prepare.py packages actual fixture with currentrepo engine and narrowpatch;
qa/README.md contains invocation. The baseline/profile logs and exacthash/lifecycle
logs are retained inresults. WASM build and finalmergedtests remain integrator work.

Owned[3]f32 cache renderedwall repeat (same llvmpipe machine, not Android):
- target1h/s:0.960h/s achieved,242frames/5.002s,maxframe207ms.
- target6h/s:5.810h/s achieved,169frames/5.026s,maxframe172ms.
- target24h/s:16.530h/s achieved,109frames/5.009s,maxframe78ms.
These fluctuate with machine load. The firstglobal-f64probe17.87 and owned16.53
are differentruns, not two promised speeds. Old nativebaseline9.66 inthisprobe
shows usefulheadroom but do not call it a measuredAndroidgain. Peakspersist;
this is not evidence thatallgamefunctionsaresmooth. Full6tickphysics hash and
saveinvalid/restore tests also passed theownedrepeat.

## Final integrated atlas + Fit-reason + owned cache smoke

Current main nativeEGL QA_CLOCK passed exit0. Actual exported speed callbacks
preservedpause, rejectedinvalidtarget, cleareddebt onlonggap/menu/load, and did
notadvance visualtime withoutphysicalticks. Allthree requestedrates again
produced exactfullsave hashd523353839672a4 after6ticks. Invalidsave rejected
withoutworldmutation; exactrestore passed. Seven core-source hashes unchanged
throughprepare/build/run. Renderingran with integratedatlas code/actualasset.

Initial integratedbuild correctlycaught missingfitLivingClusterResult after
an atlaspatch inadvertently reversed thereasonmethod. Parent restored that
method; regenerated current-source build andthisfinalsmoke pass. No production
release was made from that mismatch. Initialfailurelog retained inresults.

Integrated CLOCK_WALL lines are correctnesssmoke only: concurrentbuilds were
running. Do not use those numbersas a benchmark or as Android/WebGL evidence.
The existing native shutdownGPA diagnostic persists despiteexit0 and is not
explainedaway by thiscache's independentlybalancedallocationtracker.

Set STELLA_SOURCE_ROOT to the actual repository checkout. Then:

python3 prepare.py /tmp/wind-qa

Build with existing repo web/tests/egl-origin-build.zig, -Dsource=/tmp/wind-qa/main.zig,
using writable Zig local/global caches and a unique --prefix. Run the resulting
stella-egl from repository cwd (assets there):

QA_WIND_LONG=1 STELLA_PRODUCER_SEED=42 STELLA_FORMS_SINGLE=1 <binary>
QA_WIND_LIFECYCLE=1 STELLA_PRODUCER_SEED=42 STELLA_FORMS_SINGLE=1 <binary>
QA_CLOCK=1 STELLA_PRODUCER_SEED=42 STELLA_FORMS_SINGLE=1 <binary>
QA_CLOCK=1 QA_WIND_UNCACHED=1 STELLA_PRODUCER_SEED=42 STELLA_FORMS_SINGLE=1 <binary>

Long test compares same parsed seeded world under forced scratch OOM/original
uncached computation versus successful owned cache for1800 physical ticks/30days.
Compares complete serializedworld hash, validates both and poisons transient
scratch across load to verify refresh. No biological edits or grants.
Lifecycle uses a tracked allocator for an entire generated/simulated/deinitialized
Planet, then two actual replaceWorld6→7→6 cycles, simulating/validating each.
Clock fixture is existing requestedrate/actualrenderedwall/fullstatehash QA.
Native EGL forces browserstyle singlethread, but it is NOT Android/WebGL runtime.
No shader/device performance guarantee. Run profiles sequentially to limit noise.

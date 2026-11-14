Set STELLA_SOURCE_ROOT to repository checkout. Run:
python3 prepare.py /tmp/empty-bloom-qa
Build with repo web/tests/egl-origin-build.zig -Dsource=/tmp/empty-bloom-qa/main.zig,
writable Zig caches and unique --prefix. Run resulting stella-egl from repo cwd:

QA_EMPTY_BLOOM=1 STELLA_PRODUCER_SEED=42 STELLA_FORMS_SINGLE=1 <binary>
QA_CLOCK=1 QA_FORCE_BLOOM=1 STELLA_PRODUCER_SEED=42 STELLA_FORMS_SINGLE=1 <binary>
QA_CLOCK=1 STELLA_PRODUCER_SEED=42 STELLA_FORMS_SINGLE=1 <binary>

First test compares actual full framebuffer bytes/hashes, not visual impressions.
Nursery/globe/side, all four other modes, real HDRsun/freecam, stale bright→empty
transition, Sandbox rabbit render fixture, and model save check. Only explicit
view fields normalized in modelhash; no restore hides simulated-world changes.
Rabbit is a render fixture, not an evolved Origin animal.

Clock compares unchanged physical hashes, pause/background/load/save callbacks,
and synthetic native pointerdown-frame-pointerup-frame pause with no extra tick.
Wall timing is native llvmpipe, not Android/WebGL; p50/p95/p99/max from <=2048
actual frames in each5secondwindow. Force/full runs and auto runs use samebinary.
Run sequentially, and don't present noisy max/tail values as device promises.

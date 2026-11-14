# Inline water transfer: paired real-engine acceptance

Isolated candidate based on public 7cd26361b9c343220a6999a8af33b0cb639b3e0a.
Production change is only `fn sendWater` → `inline fn sendWater` in planet.zig.
No equations, iteration order, timestep, random generation, save schema or
simulation scheduling changes.

Actual original engine, fixed seed1337, topology6 (40,962 cells), Sandbox with
fixed angular vegetation patch, 65 full updates × dt1/60 × timeScale3600.
Native Zig0.13 ReleaseSafe CPUbaseline (consistent SIMD width), cooperative
single-thread jobs, offscreen Mesa EGL rendering at390×700. Offline audio and
direct Playing entry are test-only. First5 updates excluded; 60 timed updates
per process. Sequential order baseline/inline/inline/baseline, no concurrent
compilation. Final simulated time3900.0002479553223 retains existing float
arithmetic, not rounded/rewritten by harness.

Full update median baseline9.777–10.256ms versus inline8.284–8.308ms:
about15–19% lower for this scenario on this native host. This is not Android,
WASM or browser FPS evidence, nor all-world correctness proof. Render cost
is separate and no promised60fps result follows.

All four complete serialized world states equal byte-for-byte:8,593,365bytes,
SHA256 `3a3b7d2e5866dd7f803ae9d67ad4efc9c9482c6f6bbed35cc9757ff223c3c74a`.
Logs/results in evidence/inline-water. Existing GPA shutdown leak observed
in both variants, not repaired or hidden. No Origin organism trajectory or
long-running lifecycle coverage is claimed by this short Sandbox benchmark.

Reproduce from candidate root (official Zig0.13 at ../stella-toolchains):

```sh
python3 web/tests/inline-water-prepare.py /tmp/stella-profile-base
python3 web/tests/inline-water-prepare.py /tmp/stella-profile-inline --inline
# For baseline when production already inline: change only the generated copy's
# `inline fn sendWater` back to `fn sendWater`; preparation does this automatically.
for v in base inline; do
 ../stella-toolchains/zig-linux-x86_64-0.13.0/zig build \
 --build-file web/tests/egl-bench-build.zig -Dsource=/tmp/stella-profile-$v/main.zig \
 -Dcpu=baseline --prefix /tmp/stella-profile-$v-out \
 --global-cache-dir ../stella-toolchains/zig-cache --cache-dir /tmp/stella-profile-cache
done
for spec in 'base base2' 'inline inline1' 'inline inline2' 'base base3'; do
 set -- $spec
 MESA_SHADER_CACHE_DIR=/tmp/stella-mesa-cache STELLA_PROFILE_SAVE=/tmp/stella-$2.json \
 /tmp/stella-profile-$1-out/bin/stella-egl > /tmp/stella-$2.log 2>&1
done
python3 web/tests/inline-water-results.py /tmp/stella-base2 /tmp/stella-inline1 /tmp/stella-inline2 /tmp/stella-base3
```

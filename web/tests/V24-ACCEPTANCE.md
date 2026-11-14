# v24 · Lighter views and world choices

## Avoid work with no visual contribution
The browser Origin Normal map, stable radial daylight, orbit camera and no
animals have a provably black bloom input. A bounded guard skips only that
empty bright-extraction/blur contribution. Other maps, free camera, nonstable
daylight, animals, unusual camera distances and Sandbox retain the original
HDR path. The final composite explicitly disables old bloom so a previous
bright sun frame cannot leak a stale glow. A new HDR-producing scene feature
must update the guard contract rather than silently losing its bloom.

Three native views produce byte-identical pixels with full and skipped bloom.
Unsupported maps, actual HDR sun, bright→eligible transition and a rabbit scene
preserve their output. Physics and saved-world state are unchanged.

Native normal/Grow median frames improved about 15–16 ms → 7 ms, and a synthetic
two-frame pointer pause test about 30 ms → 17 ms. Fast throughput improved 17.33 → 19.27
simulated hours/sec in the paired test, but p95/max frame tails did NOT improve
consistently. This is not an Android benchmark, a guarantee of smooth Fast, or
an O(1) whole-world simulation. The guard is constant-time; model work remains
proportional to world size.

## Measure the actual device locally
Speed → Performance details opts into bounded frame/physics/render-call
aggregates. It is local only, with no network telemetry. Closing details or the
dialog, Escape or hiding the tab disables/reset measurement. Render-call time
can include driver waits; it is not a GPU timer. Achieved simulation rate remains
separate. Native enable/read/disable checks preserve full save and clock exactly.

## Explicit new-world Continents
Random stays the default. Choosing Continents before Origin or Sandbox creation
sets initial sea level from a terrain quantile, targeting about 70% ocean. It does
not flatten terrain or drain an existing world. Selection alone never creates or
resets a planet. Existing and newly created saves restore byte-exactly while
Continents remains selected; schema 6 is unchanged.

A separate 30-day one-seed experiment produced 10 occupied patches, 13 cohorts and
five aquatic forms. Dry terrain exposure increased, but no drought-reserve
advantage or completed terrestrial evolution is claimed. See continents QA for
controlled versus descriptive comparison limitations.

Native/EGL tests and WASM compilation are not a real Android WebGL acceptance
run. Existing native shutdown allocation diagnostic remains disclosed. Editable
source, test fixtures/generators and evidence are retained with this release.

Final combined checks passed: current-main paired pixels, HDR transitions, rabbit scene and model equality; all three clock targets retain identical physical save hash d523353839672a4. Actual pointer pause stops extra ticks. Current-menu Origin/Sandbox creation and existing/new save restoration remain byte-exact. Full WASM package and six JavaScript suites pass. Integrated timings are correctness smoke, not fresh benchmarks.

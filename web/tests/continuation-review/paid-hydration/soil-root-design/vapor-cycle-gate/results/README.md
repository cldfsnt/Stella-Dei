# Minimal executed phase→edge probe

8 ReleaseSafe tests pass (2 new,6 imported atmosphere tests). Offline exact Fraction checks pass108 legs across36 cases:6 fixed columns×dt360/720/1440×pulse off/on. Source files are `src/experimental/vapor_cycle_probe.zig`, `src/qa_vapor_cycle_probe.zig`; audit `web/tests/audit-vapor-cycle.py run.log`.

The first two cases combine the actual root25k10 action1 ticks1/2 standing-column inputs, temperature/saturation and actual post-advection vapor/soil/pulse operands. This is a **conditioned local replay**, not an actual next-tick trajectory: those measurements occur at different operator stages. Remaining four cases deliberately test deep liquid, cold condensation, dry atmosphere evaporation and huge receiver/tiny pulse. The directed edge is synthetic100km with.01km/s wind using the real edgeRate/coefficient functions; no claim actual world topology/velocity. Initial soil and pulse densities are converted once to authoritative f64 native mass. This explicitly does NOT prove the live f64-density/native bridge, multi-neighbor gather or full scheduler.

Mixed phase exchange floors toward unchanged f32 liquid, then accepts only exact represented equal source/receiver deltas (strict TwoDiff). Otherwise that leg remains unchanged, with no receipt or hidden store. Evaporation and condensation use the existing request/temperature laws; rain-rate persistence is not implemented in this minimal probe. Root and edge receipts use the existing isolated f64 equal-or-refuse helper. No new biology.

At dt1440, actual first pulse pays.000417676046708948 native mass; phase evaporates.4528045654296875 against.4528064891600378 requested. Second pulse pays.000010396687684988137; condensation pays19.400222778320312 against19.400236576163866 requested. Their phase and subsequent directed-edge transfers preserve exact represented material. Unspent requests remain in ordinary source pools. These are native mass units, NOT kg/m².

Important failures retained: deep liquid1e12 cannot represent the requested224.1823712242554 condensation at all, so it stays vapor; huge vapor1e30 refuses tiny root pulse and even the edge receipt. Thus this demonstrates favorable actual shallow-column feasibility, NOT general authority adequacy or unchanged climate kinetics. f64 vapor does not remove the f32-liquid boundary. All legacy f32 phase endpoints are logged for comparison, without claiming their separate roundoff is new root loss.

Audit setup failure retained in interpretation: initial Python parsing treated Zig shortest f32 decimals as f64, spuriously reporting phase imbalance. Correct audit reconstructs declared f32 liquid outputs before exact Fraction comparison. No model change or tolerance was used. Native exact-difference checks already passed.

Run: `zig test src/qa_vapor_cycle_probe.zig -O ReleaseSafe`; then `python3 web/tests/audit-vapor-cycle.py <log>`. No CPU-heavy world trial, production/schema edit, live deployment or browser performance claim.

## Frozen failed production-style receiver reference

Area7,669,529,600m². Pulse1 soil density before.9999999167069676, vapor before1680.0450439453125native, requested/paid soil density.00005445914790658257; original f32 vapor receives.00004774881336920585kg/m², losing.000006710334537376725. Pulse2 soil density before.9999991749741014, vapor before1635.706298828125native, requested/paid.0000013555834952327928kg/m²; original f32 vapor receivesZERO and loses the entire pulse. Total loss.000008065918032609518kg/m² (~14.45% of soil spend). These exact original operands remain literal in qa_root_vapor_receipt.zig and the current cycle fixture. Nothing is topped up or redistributed to compensate.

# Receipt-backed intervention feedback

`renderGodEffects` reads the last successful bounded action receipt. It never
changes simulation state. Wave ripples are projected onto the actual changed
cells (up to seven), excluding zero deltas. Lightning draws one fixed bolt and
small local halo only where temperature actually increased. There is no fire
animation or invented casualty counter. These are action feedback symbols, not
a claim of physical fluid-wave or plasma simulation.

The 1.2-second lifetime uses frame elapsed real time, independent of accelerated
simulation time. Alpha fades monotonically: no geometry jitter, strobing or
full-screen flashes. Hidden hemisphere and toolbar areas are excluded.

`zig test src/god_visuals.zig` passes 28 visual/action/ecology tests, including
failure, empty receipt, unchanged deltas, invalid count, expired/non-finite time,
and actual positive heat requirements. Native action screenshots are a separate
visual gate; these tests alone do not demonstrate browser/device appearance.

Native EGL visual gate completed via `egl-god-visual-prepare.py` and dedicated
build/shim: frame55 shows cyan rings at changed water cells after an actual Wave;
frame95 shows the fixed local bolt and halo after actual heat action, with HUD
20→60°C. Wave receipt recorded seven cells and 7669.546875 engine mass units
moved; heat recorded one cell and 1.8088399765e19 J input. No synthetic receipt
was injected. Exit0 included a GPA shutdown leak diagnostic; physical Android
and WebGL visual conformance are not established by these desktop EGL captures.

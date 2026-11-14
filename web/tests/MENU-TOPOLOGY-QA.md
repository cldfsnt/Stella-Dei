# Browser decorative menu topology reduction

Production change: only browser MainMenu decorative globe uses subdivision6
(40,962 cells) instead of Release subdivision8(655,362). Native remains7 in
Debug and8 otherwise. Playable worlds, save topology and simulation are unchanged.

Actual native EGL adapters exercised the browser menu at320×700 and390×700.
Reviewed before/after menu PNGs in `evidence/menu-topology`: logo, both mode
buttons and caption fit; the lower-resolution decorative globe remains coherent.
Actual Origin button callbacks enter modeorigin, zero vegetation/rabbits, paused.
Actual Sandbox button callbacks reach the existing GameIntroState at both widths.

One paired native smoke per width, warm shared shader-cache path:

| Width | Menu8 peak RSS KiB | Menu6 peak RSS KiB | Menu8 wall s | Menu6 wall s |
|---|---:|---:|---:|---:|
|320|456964|233568|3.420|2.490|
|390|532912|243356|3.502|2.073|

Measured using Python `resource.getrusage(RUSAGE_CHILDREN).ru_maxrss` and
`time.perf_counter`, executing preserved menu8 and current menu6 binaries.
These are whole native menu→Origin smoke processes, including fixed frame waits,
initialization and GL rendering; not isolated website startup or physical-phone
performance, and not statistical benchmarks. Seeds are generated normally.

Reproduce current menu via `egl-origin-menu-prepare.py` / `egl-origin-menu-build.zig`;
`QA_WIDTH=320 QA_HEIGHT=700` or390/700. `QA_SANDBOX=1` chooses Sandbox.
No renderer/model quality or lifecycle semantics were changed for this reduction.

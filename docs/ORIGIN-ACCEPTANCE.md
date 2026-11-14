# Origin integration acceptance

Goal: real simple-life population gameplay, preserving the modern plant/rabbit Sandbox. This first model seeds already-living phototrophs; it does not simulate abiogenesis, multicellular plants or animals yet. Thermal/light trait inheritance and competition are adaptation within the implemented group, not new species/class emergence.

Passed before environmental corrections:
- WASM build, JavaScript shell/storage/touch tests, five microbe tests and thirteen schema/ecology tests.
- Controlled rendered growth, real drying/recovery, no-carbon-fixation in darkness, visible mats and Inspector at 320/390 widths.
- Actual mode entry starts empty with no hidden plants/rabbits.
- Exact ~21.6 MB Origin save/restore and malformed-shape rejection; legacy Sandbox v1 payload migration unchanged.

Initially FAILED ordinary generated-world gate: seed1337 shallow habitat at normal60-second simulation steps loses most biomass and has no reproduction over5days. Original terrain/water climate has unit-inconsistent water thermal capacity and water transfer. Controlled success is not a substitute for ordinary gameplay.

Validated and integrated Origin-only correction: real water thermal capacity (explicit50m mixed layer cap), dimensionally correct conservative transfer and selection of actual low-latitude shallow habitat. No increased biological tolerance or forced survival. Legacy Sandbox solver preserved. Final production Habitat→Seed checks passed at normal60-second and accelerated1440-second steps over5days. Normal biomass0.02→0.035354 with one daughter/gen1; accelerated0.102620 with one daughter/gen1. Both stayed one occupied cell: this is bounded starter viability, not widespread growth. Exact21.46/21.59MB restore and corrupt-shape rejection passed. Total water+vapor drift was0.00367%/0.000142%, not exact conservation; closed helper conservation is separately tested. Sandbox37day results stayed unchanged. Final rendering and menu-memory checks accompany the release.

Known boundaries: native EGL graphics are not Android WebGL; physical-device performance remains unverified. Native shutdown allocation leak remains. Microbial maps show cell-scale populations, not individual microbes. Original game assets remain GPL and included source accompanies releases.

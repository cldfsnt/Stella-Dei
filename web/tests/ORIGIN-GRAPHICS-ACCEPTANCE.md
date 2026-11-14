# Origin native graphics acceptance plan

Owner: isolated EGL graphics worker. Pending actual model/UI interfaces; this document is a plan, not a passing report.

## Environment and isolation
- Snapshot production source only after model/UI freeze to a separate temporary copy.
- Actual Stella Dei engine, simulation, shaders and assets; native Mesa/EGL with mobile branches selected. No alternate game implementation.
- Separate build output, cache, capture prefix, save path. Preserve Sandbox test artifacts.
- 320×700 and390×700; same deterministic seed and initial scenario.
- Do not interpret native software-GL performance as Android/WebGL FPS or pointer callbacks as browser touch-event proof.

## Scenario gates
1. Enter Origin through actual mode initialization. Record mode, seed, fieldcount, all vegetation sum, rabbitcount, microbe biomass, live cohort count, resources and initial lineage information. Plants/rabbits must be absent, rather than merely hidden.
2. Capture initial globe and inspected seed. Mat positions/intensity must correspond to actual populated cells.
3. Advance real simulation in suitable conditions; record births/spread and parent/child lineage from actual model, biomass, resource changes. Capture same viewpoint and inspect descendants. No direct success-counter edits.
4. Intervene through actual supported temperature/light/water setting or genuine field-condition change in test-only code if UI lacks control. Explicitly label test-only interventions. Record decline and surviving biomass/cohorts; restore conditions and show real recovery where possible. Never repopulate silently to manufacture recovery.
5. UI: all tools/labels/Inspector fit320/390; menus retain clicks while modal camera/picking/zoom remain blocked.
6. Run independent Sandbox placement/Play/modal regression; legacy functionality must not disappear.

## Performance/consistency
- Warmup then bounded fullsimulation-step and render timings, with glFinish for render cost; record samplecount, median/p95, fieldcount and population.
- Startup and process peakRSS; compare same build's Sandbox where feasible.
- Assert finite/nonnegative biomass and resource fields using actual model bounds.
- Save/restore exactness belongs to save worker; do not duplicate or claim it without their evidence.
- Adaptation/distribution/control experiment belongs to model worker; variation or generation count alone is not adaptation evidence.

## Evidence
Keep source revision/hash, raw logs, screenshots and concise interpretation under a new evidence directory. Record failures as failures and coverage gaps explicitly. No publish action from graphics worker.

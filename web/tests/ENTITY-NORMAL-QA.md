# Entity normal correction

Confirmed mismatch: rabbit OBJ normals are model-local, groundedRabbit rotates
mobile rabbits' localY into the world radial direction, but entity.vs forwarded
local normals unchanged while entity.fs compared them with world-space lightDir.
At world+X a local+Y top face had diffuse0 instead of1 under stable daylight.

Narrow fix: normalize(mat3(modelMatrix)*aNormal) in vertex shader; normalize
interpolated normal before the fragment dot product. This is correct for all
existing entity matrices, which use rotation and positive uniform scale. It is
not a general nonuniform/skinning solution; future assets must supply a proper
inverse-transpose normal matrix. No geometry, daylight direction, ecology, asset,
material or UI changes. Avoids per-vertex matrix inverse and extra uniforms.

Seven matrix/biology helper tests pass. Native four-site paired screenshots use
same actual rabbit mesh, model transform, fixed world, camera and stable daylight.
Only entity shaders differ via test-only runtime path selection. Deliberately
placed rabbits are a rendering fixture, not a claim of Origin evolution.
Integrated into v21 after isolated checks. Native shader evidence is not phone GPU profiling.

## Final verification

WASM ReleaseSafe compilation passed. Native EGL compiled/linked both shader
variants and rendered four positions successfully. Cropped visual comparison
shows incorrect half-dark radial-facing rabbit before, coherent front lighting
after, without changing daylight. Native runs finish exit0 with the existing
shutdown GPA leak. No phone-GPU timing or WebGL runtime claim.

Integration scope: entity-normal.patch only (entity.vs and entity.fs).
Proof to checkpoint: src/entity_normal_test.zig; web/tests/egl-normal-prepare.py;
results/entity-normal/stella-normal-unit.log; results/entity-normal/stella-normal-before.log;
results/entity-normal/stella-normal-after.log; results/entity-normal/stella-normal-web.log;
results/entity-normal/stella-normal-pair-25.png; results/entity-normal/stella-normal-crop-25.png.
The before shaders are fixture-only and not production assets.

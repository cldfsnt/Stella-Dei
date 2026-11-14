# Full-resolution depthless bloom/blur targets

Candidate only, based on v27 bd5bada. No main edits, push or deployment by this worker.

## Exact change
- Framebuffer.create remains depth-attached for scene and other existing users.
- New createColorOnly uses identical full-size HDR color texture, extension requirement, sampling and completeness check, but omits depth allocation/attachment.
- Only bloom/blur constructor and resize calls use createColorOnly. Every bright/blur pass already disables depth testing. Only scene depth is sampled anywhere in production; it remains attached and preserved.
- Optional depth ID0 is never deleted. Error unwind deletes created depth/color/FBO resources. The same unwind also fixes existing incomplete-FBO cleanup for regular depth targets.
- No changes to bloom pass count, shader/kernel, scene resolution, simulation, native renderWater or saved data.

## Memory evidence and limits
Two fewer depth texture objects at live target size. WebGL requests DEPTH_COMPONENT32F: logical removal 2*4*width*height bytes =2,184,000 at390x700,5,152,000 at920x700. This is not measured physical VRAM; tiling/alignment/driver allocations unknown. Native default uses unsized depth and may choose a different format. A second desktop GL test explicitly uses browser RGBA16F/HALF_FLOAT and DEPTH_COMPONENT32F; actual depth-size query returns32bits before removal. This is not WebGL extension negotiation or phone-driver testing.

## Tests
Native default-format initial run exit0: four target sizes (32x64,390x700,920x700,64x32), depth-on/off attachment completeness, object liveness and actual deletion; injected incomplete-FBO unwind leaves all generated objects dead. This is injected incompleteness, not real GPU OOM. Exact framebuffer hashes in10map/atmosphere combinations; visible rabbit, HDRsun9.96875, bright return/daylight toggles and unchanged serialized model.

Final browser-format desktop tests include production constructor+resize calls. Logs and final results recorded below after execution. Native browser-style harness is not actual WebGL runtime.

QA naming retains unused-upload ancestor labels: UNUSED_PIXELS means depth-attached vs depthless; candidate toggle only recreates bloom/blur targets. UNUSED_UPLOAD counters are irrelevant inherited diagnostics and are not an optimization claim. Timings include final glFinish wait; no GPU timestamp or phone-speed claim. First QA build failed because helper named Play rather than PlayState, then corrected; failure log retained. Existing native shutdown GPA warning remains.

Production patch/hash in HASHES.txt; reproducible qa/prepare.py and README.md. Parent must run full WASM/integrated/live gate before deployment.

## Final executed results
- web-formats-390.log and web-formats-920.log both exit0. All eight lifecycle cases each pass, with32-bit depth queried before deletion; ten map/atmosphere exact framebuffer pairs each, visible rabbit, HDRsun9.96875, bright return/day-night and unchanged model pass. Production initial800x600→actual viewport resize calls included. Scene depth remains nonzero during every paired target replacement.
- clock.log exit0. Three clock targets yield full-state hash d523353839672a4. Actual pause/rate/background/menu/load checks pass; save8,734,640bytes rejects invalid payload unchanged and restores exactly.
- Native default-format run exit0 too. Existing shutdown allocator warning unchanged.
- Timing does not establish a reliable speed gain. At390, original medians16.69/16.78ms vs depthless17.08/16.34ms, tails mixed. At920, original36.56/32.43 vs depthless31.96/32.03ms, but shared-machine timing and order effects prevent a firm claim. This checkpoint reduces proven-unused objects/storage without a phone-speed guarantee.
- Reproducer regenerates final instrumented main/renderer/play byte-for-byte. Actual WebGL runtime/full WASM/integrated release gate remain parent's next steps.

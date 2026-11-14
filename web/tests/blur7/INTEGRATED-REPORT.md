# Isolated current-v28 plus final blur candidate gate

Source snapshot manifests identify actual v28 code copied before panel-closed diagnostics changed main/play. Shader final candidate f4707f7304725199e22cb7ef3fa825029b4e2b191e50821afb3bbf6104d57bc6. No production edits by this worker.

Native build exit0, paired390pixel process exit0: all maps/atmosphere,rabbit,HDRsun9.96875,bright/daylight transition display bytes exact,model unchanged. Candidate explicitly selected for clock process, exit0: all rate hashes d523353839672a4,pause/rate/background/menu/load pass,save8,734,640bytes invalid-reject/no-mutation/exactrestore pass.

Full isolated WASM compile/link/package exit0; output hash in wasm-output-sha256.txt. It uses copied production source, only candidate shader replaced, symlinked read-only deps/assets. No live-browser validation. Static glslangValidator unavailable; shaders.log records that. Actual native GL and separate actual ES3 synthetic shader compilation passed.

Post-test live-main readback differs in main/play due independently integrated diagnostic hooks, and shader due parent's accepted candidate. Renderer/planet unchanged. Therefore gate covers capturedv28+shader, NOT newest combined diagnostics. Parent/sibling finalcombined gate is separate.

ESSL actual-game supplemental build first failed due test-only globalplatform override pulling emscripten symbols into native. Corrected to preserve native platform flag while overriding shader adaptation and browsertextureformats; result pending below. Not actual WebGL/ES-context gameplay.

## Supplemental actual-game ESSL result: completed
Corrected native build exit0; ESSL390 and ESSL920 processes both exit0. Actual game renderer uses browser shader_source.prepare(...,true) andRGBA16F/DEPTH_COMPONENT32F texture formats, while retaining desktop GL context/native platform APIs. This tests ESSL precision on actual game images, NOT actual GLES-context/WebGL gameplay.
All ten map/atmosphere comparisons complete, visible-rabbit fixture, bright sunpeak9.984375,day/night transitions,unchanged model pass. Display is NOT exact:390 maps1–4components differ, sun48components, bright return2;920 sun46components,bright return4. All differences max1/255; night0. Original/candidate390sun PNGs viewed: no discernible halo/edge artifact. Native ESSL medians favor7tap in both windows, with mixed max/tails; no phone claim.

Recommendation: accept narrow shader candidate with these measured rounding caveats. No known compile/runtime/model failure remains. Final latest-main diagnostic hooks were tested separately by parent/sibling; this shader proof's source manifests remain frozenv28. Compact supplemental evidence in package/results and viewed PNGs.

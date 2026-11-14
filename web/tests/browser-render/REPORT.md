# Sandbox final-composite shader candidate

## Scope
A narrow shader-only change places depth sampling, inverse-matrix ray reconstruction and atmosphere intersection inside the existing enableAtmosphere branch. Browser rendering disables atmosphere. Bloom extraction, all four blur passes, animal drawing, full framebuffer resolution and HDR mapping remain unchanged. The no-bloom eligibility guard is NOT broadened. No simulation or save change.

Baseline v25 repository commit and exact relevant shader/source hashes are retained. Baseline postprocess SHA256 f0a4c663c26f85548b90406187f8bae3a7d37ba525c18d092205d91ae21e5e39. The final clean shader differs from measured candidate only by indentation/comments.

## Pixel/model checks
Same binary switches between original/candidate shader programs, so fixtures do not depend on separate world initialization. All tests exit 0 at 390×700 and 920×700 on native llvmpipe:
- Rabbit is visibly rendered: adding it changes framebuffer pixels.
- All five map modes are byte-identical with atmosphere disabled, and with atmosphere forcibly enabled for the unsupported/native path.
- Actual free-camera HDR sun remains identical, with bloom peak9.96875.
- Bright→normal return and stable-daylight/day-night changes remain identical.
- Full serialized model remains unchanged, apart from intentionally normalized view fields.
Existing unrelated allocator shutdown warning remains.

## Measured effect and limits
Native driver evidence supports a modest gain, not an explanation for an observed 68ms mobile render call. Two-second render-only ABBA windows at390×700 showed original medians15.61/15.02ms vs candidate15.05/14.34ms; at920×700 original30.75/30.33 vs candidate28.24/29.72ms. Maxima and submission-stage timing overlap and vary substantially. No consistent tail improvement claim.

To test whether the compiler eliminated disabled atmosphere work already, a separate QA-only experiment drained prior GPU work with glFinish, timed final composite submission, and waited for completion. Six-second ABBA means:
-390×700 original1.827/1.550ms vs candidate1.043/0.961ms.
-920×700 original3.377/3.244ms vs candidate1.879/1.972ms.
This driver did not eliminate all cost. The synchronized bracket changes pipeline scheduling, is NOT a hardware GPU timer, and cannot be equated with normal game frame duration. Other mobile drivers may optimize differently. These results justify a low-risk tested cleanup, not a promise of mobile FPS improvement or solving render stalls.

Scene/post/UI/flora wall-time aggregates are retained in profile.log and wide.log. They include submission and possible driver waits, not GPU time. Framebuffer width920 here is a stress test with height700, not the phone's aspect ratio.

## Recommendation and next evidence
Candidate is suitable for integration/WASM verification at a measured checkpoint, without a rushed deployment or quality reduction. The large phone render spike still needs actual guard/pass/resolution context and stage timing. Screenshot labels suggest different world modes but do not expose the obscured camera/map/guard. No controlled before/after phone claim is made.

See qa/ for preparer, paired fixtures and optional profile/bracket instrumentation; results/ contains all raw logs. postprocess.patch is production-only. No main source was edited.

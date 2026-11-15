# Save continuation: independent source audit

## Correction to the premise

The hydration worker confirmed that its initial restored-vs-restored continuation test was precautionary, **not a response to an observed uninterrupted-versus-restored mismatch**. Prior receipt-engine research also labels uninterrupted equivalence untested; it does not establish a failed cache oracle. Do not cite a “known derived-cache confound” as fact.

The worker is adding true uninterrupted10 coupled ticks versus independently restored10 ticks to both production baseline and hydration candidate, retaining raw complete snapshots and reporting exact equality. Any normalization is prohibited for that comparison. Earlier restored-repeatability and capture/load byte equality remain useful but weaker properties.

## Derived state source findings

- `save_game.apply` restores saved biological, material, gas, wind and clock fields; it resets frame-clock accumulator and transient observations/tools. Scratch temperature/liquid/vapor arrays are copied too, and the coupled solver refreshes these before their normal per-step use.
- The cooperative native fixture follows browser partition count1. The native multithreaded temperature code computes heat capacities per partition and reads neighboring capacities/scatters temperatures; potential cross-partition concurrency is a separate concern, not an explanation for a one-partition continuation mismatch.
- Meteorite timing is unsaved, but its production branch is explicitly disabled (`and false`); it is not an active cause.
- Camera interpolation/normalization can change camera fields on render. This must be compared under matched render histories; it cannot excuse differing temperature/water/cohorts/RNG.

## Specific production-shared load risk, not yet runtime-proven

`save_game.apply` copies saved elevation and axial tilt and resets `uploadNo`, but does not rebuild `Planet.transformedPoints`. Those positions are rebuilt by `Planet.upload` during rendering. Both temperature/atmospheric transport and biological illumination consume transformed positions. `web_frame` invokes update/simulation before rendering. Therefore a load with different previously rendered terrain/tilt can expose stale geometry to a physics step before the first post-load render, **if a simulation tick is due then**. Clock-reset timing may postpone the first tick until after a render; it does not synchronously establish geometry correctness.

This source-level risk is distinct from same-geometry endpoint restore tests, which may pass. It is shared by existing production, not introduced by hydration. No current evidence establishes its magnitude or first divergent field.

A bounded future witness should use legitimate different rendered terrain/tilt states, apply the same deep-frozen target save, then execute one identical tick before versus after a geometry-refresh-only operation. Preserve complete outputs and identify the first raw material/biological divergence. No poisoning arbitrary memory, no physiology normalization, no change to saved resources. If verified, prefer separating deterministic derived-geometry preparation from GPU rendering rather than serializing renderer buffers or adding hidden compensating resources.

No production edits or claim of full continuation equivalence accompany this source audit.

## Actual results now preserved

Six same-geometry continuation pairs independently byte-compared: production baseline and five hydration candidate endpoints all equal (actual-pairs.json). There is no divergent field in these tests.

Separate production geometry witness confirms the source risk: both arms render legitimate45° tilt plus one actual RaiseTerrain tap, then load exactly the same frozen natural60 save. Control refreshes geometry with existing upload before one1440s tick; test arm does not. Saved starting bytes are identical, and upload alone changes no saved values. Raw outputs differ in40,983 values:15temperature,5liquid,40,961vapor,2rainfall. Firsttemperature1597:162.61973571777344 versus162.6197509765625K. Firstvapor0:491.3895263671875 versus507.8249206542969billionkg/patch; maximum vapor difference287.7760009765625. No cohort, RNG, clock or camera difference after this one tick. Single cooperative partition; original full save restored. Native EGL, not browser/device pacing proof.

Raw ~10MB endpoints remain local with exact hashes in witness-diff-summary.json; no normalization was performed. Existing unrelated GPA teardown diagnostic retained. This is not a hydration-specific bug.

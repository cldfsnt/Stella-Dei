# Make a successful planting visible

Read-only proposal, no implementation or ecology runs. Inspected actual native390×700 screenshots:
- mobile-native/living-shell.png: compact shell-owned rendering leaves room, but only one small green colony near center; exact framing makes it identifiable.
- unified-land-starter/day0.png and day3.png: paid starter success is reported, but both views look like nearly identical empty terrain. These are pre-redesign native chrome captures, not proof of the current HTML dock.
- protective-natural-journey/day0.png,day7.png,day21.png: close fixed view visibly changes from simple mats to multiple forms and arrival markers. These are biological forms, not evidence of species or natural land establishment.

Largest remaining visible blocker: after a real paid action the player can fail to see the actual organism or know where to look next. A cleaner dock alone does not solve this.

## One bounded fix

After a successful single-colony paid seed/founder action, retain its exact world/cell/lineage receipt and show a short actionable confirmation: `Colony planted · View colony`. The explicit View action invokes existing safe one-shot surface framing for that cell and focuses the exact live lineage in Peek/Details. Do not auto-pan, auto-follow, add a permanent toolbar, change the camera on a failed planting, or search for a substitute organism. If the organism no longer lives or world changed, say `That colony is no longer available`; no invented survival or replacement.

Rooted action already pins `receipt.lineage` and its actual form in main.zig, but does not call camera framing there. Reuse those identity semantics, not a new global scan/history tracker. Ordinary seed can use its actual newly paid identity if the existing action exposes it safely. Keep first implementation scoped to verified single-founder receipts; bulk seeding must not pretend one arbitrary colony represents its entire outcome.

A single optional View action is preferable to automatic cinematic movement because planting is often part of an intentional terrain/water workflow. The user keeps control of camera and pause. Current baseline lineage mutations, roots, thermal behavior and finite water are untouched.

## Actual acceptance

Use an existing immutable suitable world and actual public paid action once. Verify receipt ID equals the newly funded cohort, and that View shows this exact living lineage at readable scale in390×700 and700×390 native renders with shell margins. Invoke Details and compare displayed ID/traits to actual cell. Capture before/after images, not just assertions.

Compare full save/RNG before/after View, allowing only documented camera/selection fields. No simulation time, resources, birth count or phenotype changes. Pause and speed remain exact. Test stale world, dead/removed identity, mixed-cell minority identity, unsafe viewport and repeated calls. A failed or expired receipt cannot focus another colony or silently seed again. Test actual DOM receipt button routing separately; native software images do not establish browserGPU/phone performance.

No new model, schema, runtime or long survival experiment required. Existing screenshots are referenced rather than duplicated.

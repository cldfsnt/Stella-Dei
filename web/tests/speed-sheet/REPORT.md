# Mobile Speed dialog accessibility follow-up

Reviewed both actual Todd screenshots (1000419335.png and1000419336.png). Their Speed title/Close had scrolled out of view while diagnostics remained open. Source cause is specific: Life and God dialogs already have sticky headings, but Speed was omitted from that selector.

## Narrow change
- Include Speed in the existing opaque sticky-heading pattern; explicit heading stacking order keeps it above scrolling diagnostic text.
- Close remains a nonshrinking ≥64×44 CSS-pixel control.
- Existing responsive dialog width (viewport minus16px, max450px),80dvh height limit and internal scrolling retained. Scroll overscroll stays contained.
- Reopen starts at scrollTop0, collapses diagnostics and stops stale measurement. Repeated open is guarded, not a second modal call.
- Shorter explanations preserve local-only/no-upload wording, bounded physics/background behavior, frame-tail interpretation, and the distinction between render call, GPU time and touch latency.
- Every actual metric, stage and render-context formatter is byte-identical. No measurements hidden, removed or reinterpreted. No engine/simulation/source changes outside shell and its test.

## Verification
Production shell handler suite passes, including repeated open, Close, the close-event path used by native Escape, hidden-page reset, collapsed diagnostics and scroll reset. Structural CSS asserts verify sticky Speed selector, opaque background, heading stacking order,44px control target, bounded responsive sheet/internal scroll, and unchanged diagnostic formatting.

Actual browser visual/bounding-box check is BLOCKED, not passed: local Chromium failed before opening the fixture because OS socket creation is denied. One ordinary run and one approved escalation retry failed identically; no repeated setup attempts. No actual mobile screenshot, sticky-position geometry or native keyboard Escape event is claimed verified. The browser fixture qa/browser.py is provided for a permitted browser environment and covers320×700,390×700 and640×360 bounds, hit testing, close/reopen and native Escape. Its API is mocked, not gameplay QA.

Main untouched. Apply speed-sheet.patch (two files). Patch SHA25668b0d27c2cb6885d8666338694b50829cd62e9529265f97bee58f993a3a131e1. Review resulting dialog in an available browser before publication if possible.

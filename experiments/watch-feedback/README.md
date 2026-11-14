# Watch readability candidate, not production

Apply watch-feedback.patch to src/states/play.zig and copy watch_feedback.zig
into src/watch_feedback.zig. Narrow UI-only change; no save schema/data mutation.

Watch shows actual current session paid-arrival and tracked-lineage-loss counts
with 'Since load' wording. Display caps at999+; exact u64 counters are unchanged.
Text measurement scales overflow to fit, including320px. Full Tools retains
persistent lifetime microbial births. Colored vector diamond/X legend explains
paid arrival / tracked loss (not all deaths). Existing temporary action feedback
can temporarily occupy the legend row; counters stay visible.

Standalone formatting tests cover0,999,1000,u64max. Native320x400 callback harness
uses real starter+Seed, then separate explicitly synthetic maxcounter layout
fixture. It serializes/parses a real save, verifies sessioncounter reset and
persistent lifetimebirth preservation. No synthetic values are evidence of
biological success. Browser WASM ReleaseSafe compile passes.

No deployment or production source changes. Native screenshot is not Android
browser conformance evidence. QA source in lab/web/tests/egl-watch-view-*.

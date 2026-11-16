# One mobile navigation system: proposal, not implementation

Source inspected: staged unified-ui/web/shell.html and unified-game/src/states/play.zig. No model, saved-world or product changes in this checkpoint.

## Observed conflict

Native `renderMobileUI` draws Pause/Climate/Menu plus Inspect/Water+/Water−/Seed/Land+/Land−/Nutrients and Speed. On a narrow canvas its reserved top is166px, footer84px. HTML independently renders Navigate, zoom buttons, Globe, World stats and Tools. Tools opens a second five-group navigation row, often followed by another actual dialog. The hidden HTML keyboard buttons are not the visible duplication; the visible native chrome plus HTML dock are. God tools are unnecessarily Tools → God tools → Open God tools.

The native function also renders living glyphs, seed targets, Peek and real effect cues. Hiding the entire function would remove gameplay, not just clutter. Its pointer exclusion, safe framing and focus/picking margins must match whichever chrome is actually visible.

## Primary architecture

One persistent bottom HTML dock: **Play/Pause | Speed | Seed | God | Stats | World**. Six equal icon+label buttons, minimum44px touch height, roughly53px width at320px; no horizontal scrolling or second row. Full safe-area padding. Selected section highlighted. Pause uses actual native state, not a local guessed toggle. No native top toolbar in shell-owned mode; native standalone retains current functional fallback.

The world occupies remaining space. Small passive day/time status only, not a second action bar. Touch defaults to orbit; pinch zoom. A selected patch shows one compact Peek card (form, amount, temperature/depth) with **Details** and **Watch**. No automatic full-screen modal on ordinary selection. Choosing a brush creates a compact contextual `Water + · tap/drag · Done` chip, never a second general menu. Done returns to navigation. Dangerous tools remain deliberate taps where required by current semantics.

## Exact destinations

- **Play/Pause:** one tap toggles run state. Remains available on world view; sheets do not silently change pause. Paused-required action presents an explicit Pause & review choice rather than telling the user to navigate elsewhere.
- **Speed:** direct compact sheet: Slow / Normal / Fast; separate Advance day. Achieved speed and rendering quality under Details, diagnostics under Advanced. Preserve cancellation/recovery safeguards.
- **Seed:** direct sheet: Seed here, Find habitat, Seed all. Current selection eligibility in one short line. Default ordinary paid founder unchanged. Seed-all retains explicit plan/review/apply and count/resource warnings. Special chosen founder genetics belong under God, not disguised as evolution.
- **God:** direct actual action sheet, not intermediary group. First view has Water +, Water −, Set depth, Raise, Lower, Fire/Heat/Wave. Land starter and Pioneer assistance clearly named below. Climate is a collapsible subsection here. Selecting a tool is two taps from world; consequential paid/terrain plans retain their review action. Do not promise every mutation can complete in two taps.
- **Stats:** direct current community summary and Find life. Six real growth-form rows with Visit; root/aerial/protective traits retain evidence labels. Effects/seed-marker visibility and View controls (Globe, Map, Zoom ±) in a compact secondary section. No requirement to know the term Observe.
- **World:** first screen Save, Continue saved world, Open saved worlds, New planet. Recovery and Download in Saved worlds; classic/sandbox choices under New → Advanced. Show existing canonical save first; importing other stores stays explicit and preserves source bytes. New-world replacement still requires existing safeguards.

One sheet open at a time. Opening another destination replaces sheet content rather than stacking dialogs. Back/Escape closes the current review/subview first, then sheet; it never creates/resumes a world or applies a tool. Opening/closing menus preserves pause, selection, speed and pending transaction semantics. Explicit cancellation discards tokens; closing a review must not accidentally apply.

## Copy and visual hierarchy

Short headings and one actionable status line. Routine explanation moves into `How it works` disclosure. Keep material warnings (world replacement, resource cost, non-reversible terrain change, scope of selected genetics) visible at the final confirmation, not buried. Remove repeated goal banners, permanent guide paragraphs, technical performance output and overlapping native/HTML status messages. Help is optional in World. Use one typography/color system,44px targets, constrained sheet width and sticky title/close only. Do not remove essential evidence qualifiers just to reduce word count.

## Acceptance before release

1. 320×568,390×700 and700×390: one dock, no clipped labels, no horizontal page scrolling; useful terrain visible; safe areas respected.
2. World→God→Water/terrain is two taps to choose; Seed→Seed here and Stats→Visit are two taps where eligible. Final confirmation adds a deliberate tap when required.
3. Native fallback still has navigation. Shell-owned scene retains colonies, seed targets, actual effects and Peek. Former166px top/84px bottom native reservations cannot intercept world taps or bias Find framing when chrome hidden.
4. Pause/Speed state agrees with engine before and after sheet changes, Watch, Advance, load and new world. Back/close never implicitly resumes.
5. One selected minority lineage stays exact in Peek/Details; touching dock/sheet never paints behind it; drag/pinch and accessibility zoom work; brush Done reliably exits.
6. Seed-all and paid founder review/cancel/stale token tests unchanged; repeat clicks cannot double apply. God previews remain current and no automatic resource grants occur.
7. Save/import/recovery lock and failed-save durability tests remain passing. New/Load/Import during busy operation refuse; original sources and canonical protection remain intact.
8. Actual native render and public-export checks plus DOM/CUA interaction tests. Cloud browser GPU unavailable: do not claim browser WebGL/phone performance from mock UI or software-native images.

Implementation ownership recommendation: frontend owns single dock/sheets; native owner exposes an explicit transient shell-ownership switch and separates chrome from overlays/hit bounds. QA independently tests both modes and complete state/RNG purity of navigation. No persisted setting or schema required.

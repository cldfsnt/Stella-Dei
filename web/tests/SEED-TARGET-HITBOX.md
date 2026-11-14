# Seed target touch contract

Seed markers and input share the exact last-rendered target list (cell ID plus
screen center). The 24px hit radius covers both the13px + marker and20px selected
ring. Touch selection chooses the nearest visible target, but rejects a boundary
where two centers are within1px of equally near. It never seeds a de-cluttered,
hidden or arbitrary ray-picked cell. Outside/ambiguous taps only select terrain.

Both mouse move and press use this list, so release/move events cannot undo a
snapped selection. Current eligibility is rechecked by the action: a target that
filled since rendering is rejected, never redirected to a second target. Cache
checks reject mismatched viewport/world and non-Seed/non-Origin/non-Surface modes.
The direct Seed colony button remains explicit selected-patch seeding.

CSS audit: shell resize passes rounded stage.getBoundingClientRect dimensions to
stella_resize, with no devicePixelRatio multiplier. Thus the target radius is
approximately24 CSS pixels on mobile, not24 device pixels on a high-DPR screen.

Native actual pointer-callback test `egl-seed-hitbox-prepare.py` passed:
center, +22x, -22x, +22y, -22y, +16x/+16y each seeded exactly one intended cell;
outside every target and a stale full target seeded nothing. No biology assigned
by the fixture: generated planet, actual Make Pond, then real pointer callbacks.
Two target-selection unit tests pass, and24 eligibility/model tests pass including
miss-hint priority. Invalid actual reasons override transient guidance; eligible
misses say to tap closer or use Seed colony. Native exit0 retained the pre-existing
GPA shutdown leak diagnostic. Physical Android taps remain a separate check.

Repeated the actual callback suite at 320×700 and 430×800: all six positions
seed exactly one intended cell; outside/stale targets reject; wrong-cell seeds 0.
Loads explicitly clear rendered target caches and transient god effects.

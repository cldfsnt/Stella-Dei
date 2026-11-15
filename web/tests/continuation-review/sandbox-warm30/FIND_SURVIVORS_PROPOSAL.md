# Minimal Sandbox survivor navigation proposal (not implemented)

## Verified existing path
- `stella_find_life` calls `Play.findLivingClusterResult`; `frameLivingCluster` explicitly refuses Sandbox(-2). The current Observe handler tells Sandbox users to use Find land.
- `focusLand` selects dry/high terrain, not vegetation or animals, and can take the player away from survivors.
- v66 Origin Find already selects its framed living anchor and uses reviewed life_camera fitting. Leave that path untouched.
- Sandbox sprouts are rendered only for cover>=.08 and water depth<=.5m, subject to projection/LOD. Rabbits use actual positions. Positive sub-.08 cover is still ecological vegetation, not visually rendered as a sprout. No-life wording must distinguish these.
- Native patch Inspect currently exposes altitude/temperature/humidity, not individual rabbit identity. Rabbits have no stable user-facing ID; array indexes change on orderedRemove. Do not invent identity or persistent tracking.

## Proposed UI and native scope
Reuse Observe's existing Find area. In Origin retain Find existing life/Fit unchanged. In Sandbox show two explicit actions: **Find plants** and **Find rabbits**. No new always-visible toolbar and no auto action on world load. Ordinary Find land remains world navigation, not survivor search.

Add a Sandbox-only finder helper and one mode-specific API with kind plants/rabbits and restart/step/cancel convention. Plants scan512patches per call; rabbits<=512scan once. Read-only requests; cancel/failure changes no view, selection, time, biology or RNG. Capture owner/storage/world/mode/time and view direction; invalidate on load/world/advancement, with explicit retry rather than silently returning stale life. No automatic pause or recurring tracking. Latest candidate must be revalidated before camera commit.

Plants: nearest to the current view among finite currently sprout-visible patches (cover>=.08, depth<=.5m), stable index tie. If none, nearest finite positive cover is a truthful sparse/submerged fallback with feedback ‘Very sparse plants here; no visible sprout yet’ or ‘Remaining submerged cover’, not ‘no plants’. Return no plants only when no finite positive cover exists anywhere; malformed data yields unavailable. This avoids falsely equating numerical survivors with a visible forest.

Rabbits: nearest current actual finite rabbit position, stable current-array tie. No long-lived array-index handle, no promised individual tracking. Focus the live position and select its nearest terrain patch for ordinary Inspect. Feedback says ‘Living rabbit found; it may move’. A pure failure leaves selection/camera unchanged.

Both: Normal display, toolNone, close blocking menu, one-shot close view using existing orbit setter and validated nonpolar geometry. Do not reuse Origin colony-fitting assumptions or mutate its reviewed helper. Stage camera/selection locally, project target into unobscured viewport before commit; report too-small/polar/unsafe geometry honestly rather than wrong focus. A found plant selects exactly the same terrain patch; rabbit uses its true position plus nearest ground patch, clearly distinguished. Do not auto-open a detail dialog that hides the found organism. A concise native selected-cover feedback can show actual cover without another global census.

## Bounded acceptance before release
Use pinned day30 endpoint, untouched input and existing v66 Origin fixture. Prove full saved simulation/RNG unchanged excluding deliberate camera/selection view fields. Find plant must select a current sprout-visible survivor where available, screenshot actually shows it; Find rabbit must frame a current living rabbit, not center436's barren terrain. Verify zero plants, sparse-only plants, zero rabbits, hidden/submerged plants, distant island, stale time/world/load, invalid viewport/polar positions, cancel, unchanged failure and no auto-follow. Repeat existing Origin Find regression so v66 behavior is not duplicated or broken. Saved worlds/schema unchanged. No ecology changes justified by this bounded evidence.

Performance work has priority. This is a design checkpoint only; no native/UI implementation or new timing run has begun.

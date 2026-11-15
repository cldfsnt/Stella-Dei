# Temporary Wetlands frontend scaffold (not deployed)

Owned files only: `web/wetlands*`. Production shell/storage are unchanged. The release owner may copy the reviewed runtime to a `wetlands/` directory, run `python3 web/wetlands-prepare.py <absolute-copied-wetlands-dir>`, and stage the `wetlands-main-link.html` fragment in the main game's World menu only after native/public-flow acceptance. This is a temporary safety boundary within the same private host, not a separate Site/account or permanent parallel game.

Native requirements before packaging:
- Fresh experimental Origin factory with explicit law identity; ordinary root-page Origin unchanged. No existing-world activation or automatic conversion.
- Native save/read/temp paths all `/wetlands-saves`; the patcher changes IDBFS mount and backup paths to that namespace. Merely a URL prefix is not storage isolation.
- Separate `stella_wetlands_snapshot()` contract: `{status:"wetlands",enabled:true,world_serial,cell,physiology_law,soil_kg_m2,root_allocations:[{id:string,living:bool,fraction,root_tissue_kg_c_m2}],receipt_available:false}`. The frontend checks world/cell against the current life snapshot before displaying it. IDs must align with current living identities. Native owner has agreed to these fields; implementation still needs acceptance. absence is explicitly unavailable, never uptake inferred from allocation. No actual uptake receipt currently displayed.
- No bundled demo/import action in this scaffold. A future explicit migrated demo must preserve original/source hash and disclose prior paid Auto-seeding, elapsed days and exact law transition; never silently mutate a law1 save into law3.
- Full save/reload/invalid-import namespace and default legacy gates, actual public Seed/100mm target/Watch journey required. Existing seed20cm eligibility remains distinct from shallower existing-colony physiology.

The banner and readout make no land-establishment/root-benefit claim. Graphics failure wording reports the required graphics-context failure without diagnosing hardware or blaming the user's device. Cloud-browser WebGL creation is currently unavailable; formatter, copied-shell and mocked IDBFS tests are not rendered-game proof.

Test: prepare disposable copies of `web/shell.html` as `../site-tmp/wetlands-frontend-test/wetlands/index.html` and `web/stella-storage.js` beside it; run patcher then `node web/wetlands-preview.test.cjs`. This includes exact large string IDs, malformed numeric/ownership rejection, copied shell seams and distinct mount/backups.

## Final packaging checks
- `node web/wetlands-module-check.cjs <dist>` loads the actual linked Module with the unchanged split asset package and no initial main; it verifies real exports and uninitialized refusal/snapshot. This is not rendered gameplay.
- First copied-suite failures (missing optional preview global in legacy UI harness, old storage-fixture namespace) are retained. Preview hooks now degrade without poisoning ordinary life; only copied storage fixture paths change, not assertions. All111 pass.
- Compiled IDBFS opens its database by `mount.mountpoint`; `/wetlands-saves` separates it from `/saves` on the same host. No authored local/session storage save fallback, cache or service-worker exists. The only other authored persistent key, welcome-dismissal, is now `stella-wetlands-guide-dismissed-v1`.
- Staged discovery URL is `/wetlands/index.html`; nested-directory default routing is not assumed.

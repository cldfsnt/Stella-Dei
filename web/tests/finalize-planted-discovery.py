from pathlib import Path
import json,hashlib,tarfile,io,shutil
r=Path(__file__).resolve().parents[2]; p=r.parent/'site-tmp/planted-discovery'; d=p/'web/dist'; e=r/'web/tests/continuation-review/planted-discovery-release/build'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
m=json.loads((e/'source-manifest.json').read_text()); blob=b''.join((e/x['file']).read_bytes()for x in m['parts']);assert hashlib.sha256(blob).hexdigest()==m['archive_sha256']
t=tarfile.open(fileobj=io.BytesIO(blob),mode='r:gz');count=0
for x in t.getmembers():
 if x.isfile() and (p/x.name).is_file():assert t.extractfile(x).read()==(p/x.name).read_bytes(),x.name;count+=1
for x in m['parts']:shutil.copy2(e/x['file'],d/x['file'])
shutil.copy2(e/'source-manifest.json',d/'source-manifest.json')
base=r.parent/'site-tmp/mobile-ux'
changes={str(x.relative_to(p)):sha(x) for x in (p/'src').rglob('*.zig') if not (base/x.relative_to(p)).exists() or sha(x)!=sha(base/x.relative_to(p))}
assert set(changes)=={'src/main.zig','src/states/play.zig','src/planted_view.zig'},changes
(d/'source.html').write_text('<!doctype html><meta charset="utf-8"><title>Stella Dei exact source</title><h1>Stella Dei source</h1><p>This exact source includes single-dock navigation and optional View colony after a verified paid rooted founder. View targets that exact living colony, never substitutes or seeds again. Ecology and save laws are unchanged. Download all source parts, concatenate and extract the gzip archive. Follow README-COMBINED-WETLANDS-SOURCE.md to recover the25original assets from the same release preload files.</p>'+''.join(f'<p><a href="{x["file"]}">{x["file"]}</a></p>' for x in m['parts'])+'<p><a href="source-manifest.json">SHA256 source and asset manifest</a></p><p>GPL source and dependency licenses included. Historical worlds retain their original laws.</p>')
(d/'qa.html').write_text('<!doctype html><meta charset="utf-8"><title>Verified game checks</title><h1>Planted colony discovery checks</h1><p>Actual native engine tests validate a resource-paid rooted founder, exact living identity, read-only view (camera/selection only), stale/dead/load refusal, repeated view and portrait/landscape framing. Frontend controller tests cover optional explicit View and failures.</p><p>Native software-rendered screenshots and controller tests are not real Android/browserGPU gameplay. Pinch/pan and saved-world interaction with the dock on a real graphics-capable device remain pending. This feature does not change ecological laws or prove natural land establishment.</p><p><a href="index.html">Return to game</a></p>')
(e/'source-freeze.json').write_text(json.dumps({'source_files_compared':count,'native_changes':changes,'archive_sha256':m['archive_sha256'],'assets_verified':len(m['asset_recovery']['assets']),'wasm':sha(d/'index.wasm')},indent=2)+'\n')
assert sha(d/'index.wasm')=='c399ea4bea64d3a455e2e9d8a3e9fde1aad995a8a2ed1542e6f0622cbe8b54e4'
art=[{'file':x.name,'bytes':x.stat().st_size,'sha256':sha(x)}for x in sorted(d.iterdir())if x.is_file()];(e/'artifacts.json').write_text(json.dumps(art,indent=2)+'\n');print(json.dumps({'files':len(art),'source_files':count,'native_changes':list(changes),'wasm':sha(d/'index.wasm')}))

"""Archive exact isolated source and recover immutable assets from shipped preloads."""
from pathlib import Path
import sys,json,hashlib,re,tarfile,io,shutil
root=Path(sys.argv[1]).resolve();out=Path(sys.argv[2]).resolve();dist=root/'web/dist';out.mkdir(parents=True,exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
js=(dist/'index.js').read_text();start=js.index('loadPackage({files:');end=js.index('remote_package_size:',start)
rows=[]
for name,a,b in re.findall(r'filename:("[^"]+"),start:(\d+),end:(\d+)',js[start:end]):
 name=json.loads(name);p=root/name.lstrip('/');assert p.is_file();rows.append(dict(path=name.lstrip('/'),start=int(a),end=int(b),sha256=sha(p)))
parts=sorted(dist.glob('assets-*.bin'));data=b''.join(p.read_bytes() for p in parts)
for r in rows:assert hashlib.sha256(data[r['start']:r['end']]).hexdigest()==r['sha256']
assert len(rows)==len(list((root/'assets').rglob('*')))-sum(p.is_dir() for p in (root/'assets').rglob('*'))
manifest={'preloads':[{'file':p.name,'sha256':sha(p),'bytes':p.stat().st_size} for p in parts],'assets':rows}
recover='''from pathlib import Path
import json,hashlib,sys
m=json.loads(Path('asset-recovery.json').read_text());base=Path(sys.argv[1]);chunks=[]
for p in m['preloads']:
 b=(base/p['file']).read_bytes();assert hashlib.sha256(b).hexdigest()==p['sha256'];chunks.append(b)
data=b''.join(chunks)
for p in m['assets']:
 b=data[p['start']:p['end']];assert hashlib.sha256(b).hexdigest()==p['sha256'];target=Path(p['path']);assert target.parts[0]=='assets' and '..' not in target.parts;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(b)
print('Verified and recovered',len(m['assets']),'original asset files')
'''
readme='''# Exact isolated combined Wetlands source

This is the generated combined Wetlands physiology3/wind1 candidate, wire13 for historical combined or wire14 for explicitly chosen calmer ground response, and historical7–10 when off; not standalone Wind or classic source. No live deployment is implied.

Download all four assets-N.bin files from the same /wetlands/ artifact. From this extracted directory run `python3 recover-assets.py /directory/containing/preloads`. Every preload and original asset is SHA256-verified. Assets are not duplicated in this archive.

Build with Zig0.13.0 and Emscripten from the accompanying build provenance, using `STELLA_TOOLCHAINS=/absolute/toolchains STELLA_SYSROOT=/absolute/emscripten/cache/sysroot bash web/build.sh`. Exact build scripts, source and dependency source are included; no external application source checkout is required. Toolchains must be installed separately. The source uses GPL licensing and dependency/asset licenses retained here or recovered with assets.
'''
archive=out/'combined-wetlands-source.tar.gz'
with tarfile.open(archive,'w:gz') as t:
 for name in ['src','deps','web','build.zig','build.zig.zon','web-build.zig','LICENSE']:
  p=root/name
  def filt(i):
   if i.name.startswith('web/dist') or any(x in Path(i.name).parts for x in ['__pycache__','.git','.zig-cache','zig-out']):return None
   i.uid=i.gid=0;i.uname=i.gname='';return i
  t.dereference=True;t.add(p,arcname=name,filter=filt)
 for name,b in [('asset-recovery.json',json.dumps(manifest,indent=2).encode()),('recover-assets.py',recover.encode()),('README-COMBINED-WETLANDS-SOURCE.md',readme.encode())]:
  i=tarfile.TarInfo(name);i.size=len(b);t.addfile(i,io.BytesIO(b))
blob=archive.read_bytes();chunks=[]
for i,a in enumerate(range(0,len(blob),7*1024*1024)):
 p=out/f'combined-wetlands-source.tar.gz.part{i:02}';p.write_bytes(blob[a:a+7*1024*1024]);chunks.append({'file':p.name,'bytes':p.stat().st_size,'sha256':sha(p)})
archive.unlink();result={'archive_sha256':hashlib.sha256(blob).hexdigest(),'archive_bytes':len(blob),'parts':chunks,'asset_recovery':manifest};(out/'source-manifest.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'bytes':len(blob),'parts':len(chunks),'assets':len(rows)}))

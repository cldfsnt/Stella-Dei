from pathlib import Path
import json,gzip,hashlib,shutil
from PIL import Image
r=Path(__file__).resolve().parents[2];b=r.parent/'site-tmp/natural-shoreline';o=r/'web/tests/continuation-review/calmer-natural-shoreline';o.mkdir(exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert (b/'final.json').read_bytes()==(b/'resumed.json').read_bytes()
assert (b/'parity-on.json').read_bytes()==(b/'parity-off.json').read_bytes()
rows={}
for line in(b/'main.log').read_text().splitlines():
 tag,_,body=line.partition(' ')
 try:value=json.loads(body)
 except:continue
 rows.setdefault(tag,[]).append(value)
assert len(rows['FOUNDER'])==7 and all(x['planted']for x in rows['FOUNDER'])
assert len(rows['DAILY'])==22 and rows['DAILY'][-1]['tick']==1260
assert rows['DAILY'][-1]['living']==7+rows['DAILY'][-1]['stats']['births']-len(rows['DEATH'])
summary={k:rows[k]for k in ['DAILY','FOUNDER','WATER_PLUS','POND_TARGET','DRAWDOWN','ROOT_DAILY','COMPLETE','VISIT']}
summary['root_births']=[x for x in rows['BIRTH_OR_INITIAL']if x['cohort']['root_fraction']>0]
ids={x['cohort']['lineage']for x in summary['root_births']};summary['root_deaths']=[x for x in rows['DEATH']if x['id']in ids]
summary['restart_exact']=True;summary['observer_parity_exact']=True
(o/'results.json').write_text(json.dumps(summary,indent=2))
(o/'state-hashes.json').write_text(json.dumps({p.name:{'sha256':sha(p),'bytes':p.stat().st_size}for p in b.glob('*.json')if p.name not in ['owner-hashes.json','source-hashes.json']},indent=2))
for n in ['main.log','resume.log','parity-on.log','parity-off.log','final.json']:
 data=(b/n).read_bytes();z=gzip.compress(data,mtime=0);assert gzip.decompress(z)==data;assert len(z)<8*1024*1024;(o/(n+'.gz')).write_bytes(z)
for n in ['build-first.log','build-second.log','build-third.log','owner-hashes.json']:shutil.copy2(b/n,o/n)
(o/'source-hashes-final.json').write_text(json.dumps({str(p.relative_to(b/'src')):sha(p)for p in(b/'src').rglob('*.zig')},indent=2))
for n in ['day0','day7','day21']:Image.open(b/(n+'.ppm')).save(o/(n+'.png'))
print('PASS',sha(b/'final.json'),'ARCHIVE_BYTES',sum(p.stat().st_size for p in o.iterdir()if p.is_file()))

from pathlib import Path
import json,hashlib,re,sys
b=Path(sys.argv[1]);root=Path(__file__).resolve().parents[2]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def exports(s):
 out={}
 for m in re.finditer(r'export fn (\w+)\(',s):
  start=m.start();i=s.index('{',start)+1;depth=1
  while depth:
   if s[i]=='{':depth+=1
   elif s[i]=='}':depth-=1
   i+=1
  out[m[1]]=s[start:i]
 return out
proof=json.loads((b/'drain-provenance.json').read_text());files={f:sha(b/'src'/f)==h for f,h in proof['files'].items()};assert all(files.values())
inputs={Path(p).name:sha(Path(p))==h for p,h in proof['inputs'].items()};assert all(inputs.values())
a=exports((root/'src/main.zig').read_text());c=exports((b/'src/main.zig').read_text());assert len(a)==55 and all(c.get(k)==v for k,v in a.items());assert set(c)-set(a)=={"egl_trace"}
rows=[]
for run in json.loads((b/'runs.json').read_text()):
 assert run['exit']==0;log=(b/(run['label']+'.log')).read_text();assert 'ORIGIN_SAVE' in log and 'exact_restore=true' in log
 for action in range(2):
  name=f"{run['label']}-action-{action}.json";p=b/name;u=Path(str(p)+'.uninterrupted.json');r=Path(str(p)+'.restored.json');assert u.read_bytes()==r.read_bytes()
  d=json.loads(p.read_bytes());ud=json.loads(u.read_bytes());assert ud['game_time']-d['game_time']==14400
  assert d['version']==10 and d['origin']['model_revision']==9 and d['origin']['root_config']['enabled']
  marker=f"ROOT_DRAIN_ENDPOINT label={run['label']} action={action} exact_roundtrip=true exact_continuation=true";assert marker in log
  rows.append(dict(endpoint=name,endpoint_sha256=sha(p),continuation_sha256=sha(u),restored_sha256=sha(r),exact=True,continuation_seconds=14400,endpoint_time=d['game_time'],config=d['origin']['root_config']))
print(json.dumps(dict(source_hashes_match=files,input_hashes_match=inputs,exports_exact=55,extra_native_fixture_exports=["egl_trace"],endpoints=rows,limits=['Continuation is in-process decoded apply plus actual ticks, not process relaunch.','Roundtrip and original restoration are native assertion/log evidence, not independently retained recapture bytes.','No browser click or UI/device interaction proof.']),indent=2))

from pathlib import Path
import shutil,json,hashlib
r=Path(__file__).resolve().parents[2];t=r.parent/'site-tmp';base=t/'wasm-cutoff-cost';base.mkdir(exist_ok=True);reference=t/'wasm-root-wind-screen/candidate'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
manifest={}
for mode,threshold in [('legacy','.0025'),('small','.001')]:
 b=base/mode;o=b/'src';b.mkdir(exist_ok=True);shutil.copytree(reference/'src',o,dirs_exist_ok=True)
 if mode=='small':
  p=o/'simulation/microbes.zig';s=p.read_text();assert s.count('if(c.biomass<0.0025){')==1;p.write_text(s.replace('if(c.biomass<0.0025){','if(c.biomass<0.001){'))
 for seed in(42,1337):
  p=t/'cutoff-trial'/mode/f'{seed}-pioneer-day14.json';e=json.loads(p.read_text());assert e['format']=='cutoff_qa_v1'and abs(e['threshold']-float(threshold))<1e-9
  out=base/f'{seed}-{mode}.json';out.write_text(json.dumps(e['state'],separators=(',',':')));manifest[out.name]={'sha256':sha(out),'envelope_sha256':sha(p),'threshold':e['threshold']}
 (b/'source-hashes.json').write_text(json.dumps({str(p.relative_to(o)):sha(p)for p in o.rglob('*')if p.is_file()},indent=2))
for p in(base/'legacy/src/simulation').rglob('*.zig'):
 q=base/'small/src/simulation'/p.relative_to(base/'legacy/src/simulation');a=p.read_text();b=q.read_text();assert (a.replace('if(c.biomass<0.0025){','if(c.biomass<0.001){')if p.name=='microbes.zig'else a)==b
shutil.copy2(t/'wasm-root-wind-screen/graph.json',base/'graph.json');manifest['graph.json']={'sha256':sha(base/'graph.json')};(base/'inputs.json').write_text(json.dumps(manifest,indent=2));print('MODEL_SINGLE_LITERAL_DIFF_PASS')

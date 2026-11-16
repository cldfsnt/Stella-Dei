from pathlib import Path
import json,re,hashlib,gzip
r=Path(__file__).resolve().parents[2];b=r.parent/'site-tmp/unified-land-starter';e=r/'web/tests/continuation-review/unified-land-starter';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert(b/'final.json').read_bytes()==(b/'resumed.json').read_bytes()
lines=(b/'main.log').read_text().splitlines();again=(b/'resume.log').read_text().splitlines()
rows=lambda tag:[json.loads(x[len(tag)+1:])for x in lines if x.startswith(tag+' ')]
patch=rows('PATCH');assert len(patch)==180
assert [x for x in patch if x['tick']>90]==[json.loads(x[6:])for x in again if x.startswith('PATCH ')]
for tag in ['ROOT_CREDIT','ROOT_USED']:
 assert [x for x in lines if x.startswith(tag+' ')and int(re.search(r'tick=(\d+)',x)[1])>90]==[x for x in again if x.startswith(tag+' ')]
receipt=rows('PAID')[0];sid=int(receipt['founder_id']);seed=json.loads((b/'seeded.json').read_text());before=json.loads((b/'preseed.json').read_text());end=json.loads((b/'final.json').read_text())
normalized=json.loads(json.dumps(seed));normalized['carbon_dioxide']=before['carbon_dioxide'];normalized['oxygen']=before['oxygen'];normalized['origin']['cells'][334]=before['origin']['cells'][334]
for k in ['next_lineage','fixed_carbon']:normalized['origin']['stats'][k]=before['origin']['stats'][k]
assert normalized==before,'paid action altered unrelated saved state'
family=[]
for i,cell in enumerate(end['origin']['cells']):
 for slot in cell.get('sparse',[]):
  c=slot['value']
  if c['biomass']>0:family.append({'point':i,'cohort':c})
credit=[dict(tick=int(m[1]),id=int(m[2]),kg_m2=float(m[3]))for x in lines if(m:=re.match(r'ROOT_CREDIT tick=(\d+) id=(\d+) kg_m2=(.*)',x))]
used=[dict(tick=int(m[1]),id=int(m[2]),h=float(m[3]))for x in lines if(m:=re.match(r'ROOT_USED tick=(\d+) id=(\d+) h=(.*)',x))]
result={'scope':'one fixed assisted Standard founder, current integrated15; no coefficient/trait edits or rescue','receipt':receipt,'preview':rows('PREVIEW')[0],'water_plus':rows('WATER_PLUS'),'target':rows('TARGET'),'endpoint_sha256':sha(b/'final.json'),'restart_exact':True,'final_living':family,'stats_initial':seed['origin']['stats'],'stats_final':end['origin']['stats'],'root_credit':credit,'used_h':used,'temperature_range':[min(x['temperature']for x in patch),max(x['temperature']for x in patch)],'depth_range_m':[min(x['depth_m']for x in patch),max(x['depth_m']for x in patch)],'soil_range_kg_m2':[min(x['soil']for x in patch),max(x['soil']for x in patch)],'dry_surface_ticks':sum(x['depth_m']==0 for x in patch),'daily':[x for x in patch if x['tick']%60==0]}
(e/'results.json').write_text(json.dumps(result,indent=2)+'\n')
manifest={n:sha(b/n)for n in ['spin.json','preseed.json','seeded.json','midpoint.json','final.json','resumed.json','day0.ppm','day3.ppm']};manifest['source_fresh15']=sha(r.parent/'site-tmp/protective-journey/fresh.json');(e/'hashes.json').write_text(json.dumps(manifest,indent=2)+'\n')
for n in ['main.log','resume.log','final.json','first-build-failure.log','second-build-failure.log','build.log']:(e/(n+'.gz')).write_bytes(gzip.compress((b/n).read_bytes(),mtime=0))
(e/'source-hashes.json').write_text(json.dumps({str(p.relative_to(b/'src')):sha(p)for p in(b/'src').rglob('*.zig')},indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items()if k not in ['root_credit','used_h','daily']},indent=2))

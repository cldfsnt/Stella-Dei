"""Read existing fixed endpoints only; hypothetical handling, no simulation."""
import json,hashlib,pathlib
root=pathlib.Path(__file__).resolve().parents[3]/'site-tmp'
paths=['wind-bulk/ordinary-day7.json','wind-bulk/pioneer-day7.json','wetlands-day21/day-21.json','origin-land-day30/day-30.json']
out=[]
for name in paths:
 p=root/name;x=json.loads(p.read_bytes());rows=[]
 for i,cell in enumerate(x['origin']['cells']):
  cs=[s['value'] for s in cell['sparse']] if 'sparse' in cell else cell['cohorts']
  for c in cs:
   b=c['biomass']
   if b<=0:continue
   d=c['structure']*c['support_mass']/b
   exposed=any(q['biomass']>0 and q['feeding']>0 and q['lineage']!=c['lineage'] for q in cs)
   rows.append(dict(cell=i,id=c['lineage'],biomass=b,structure=c['structure'],support_fraction=c['support_mass']/b,d=d,request_reduction=d/(1+d),co_located_grazer=exposed))
 positive=[r for r in rows if r['d']>0];ex=[r for r in positive if r['co_located_grazer']]
 out.append(dict(path=name,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),version=x['version'],living=len(rows),positive=len(positive),positive_with_other_feeder=len(ex),max=max(rows,key=lambda r:r['d']),biomass_weighted_reduction=sum(r['biomass']*r['request_reduction'] for r in rows)/sum(r['biomass']for r in rows),over_one_percent=sum(r['request_reduction']>=.01 for r in rows),positive_rows=positive))
print(json.dumps(out,indent=2))

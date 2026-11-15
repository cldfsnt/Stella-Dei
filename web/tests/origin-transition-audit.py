#!/usr/bin/env python3
"""Read-only saved-phenotype census. Height computed from the production formula."""
import json,collections,hashlib
from pathlib import Path
root=Path(__file__).resolve().parents[2];base=root.parent/'site-tmp';rows=[]
for day,p in [(30,base/'natural60-day30.json'),(60,base/'natural60-day60.json'),(90,base/'grazing-coupled/arm-0-day90.json')]:
 d=json.loads(p.read_text());co=[x['value'] for c in d['origin']['cells'] for x in c['sparse'] if x['value']['biomass']>0]
 def form(c):
  if c['support_mass']<=0 or c['biomass']-c['support_mass']<=0:return 'mat'
  if c['organization']<.025:return 'cushion'
  if c['structure']>=.12:return 'branching'
  if c['efficiency']>=1.04:return 'canopy'
  if c['efficiency']<.97:return 'ribbon'
  return 'rosette'
 heights=[min(.5,.2*c['support_mass']/(max(0,c['biomass']-c['support_mass'])+.01)*(1+.6*(1-c['efficiency'])-.3*c['structure'])) for c in co]
 dominant=[]
 for cell in d['origin']['cells']:
  live=[x['value'] for x in cell['sparse'] if x['value']['biomass']>0]
  if live:dominant.append(max(live,key=lambda x:(x['support_mass'],x['biomass'])))
 rows.append({'day':day,'input_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'cohorts':len(co),'occupied':len(dominant),'cohort_forms':dict(collections.Counter(map(form,co))),'dominant_patch_forms':dict(collections.Counter(map(form,dominant))),'max_height_m_formula_f64':max(heights),'median_height_m_formula_f64':sorted(heights)[len(heights)//2],'trait_ranges':{k:[min(c[k] for c in co),max(c[k] for c in co)] for k in ['organization','structure','feeding','mobility','efficiency']},'rabbits':len(d['rabbits']),'nonzero_vegetation':sum(x>0 for x in d['vegetation']),'dormant_plant_trait_entries':len(d['plants'])})
print(json.dumps(rows,indent=2))

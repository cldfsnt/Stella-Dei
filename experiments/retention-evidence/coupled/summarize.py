"""Read local serialized fixtures; emit compact exact-result metadata, never edits worlds."""
from pathlib import Path
import sys,json,math,struct,hashlib,re
root=Path(sys.argv[1]);out={}
for name in ['matched-initial100','on100-final','off100-final']:
 pth=root/(name+'.json')
 if not pth.exists():continue
 p=json.loads(pth.read_text());n=len(p['water']);area=struct.unpack('f',struct.pack('f',4*math.pi*(p['radius']*1000)**2/n))[0];bio=det=nt=stored=carry=0;live=occupied=0;shore=[]
 for i,c in enumerate(p['origin']['cells']):
  cs=[x['value']for x in c['sparse']];b=sum(x['biomass']for x in cs);bio+=b;det+=c['detritus'];nt+=c['nutrient']+.1*b;stored+=sum(x['water_reserve']for x in cs);carry+=c['surface_water_carry']+c['vapor_water_carry'];live+=len(cs);occupied+=b>0;depth=p['water'][i]*1e6/area
  if b and depth<.2:shore.append({'cell':i,'depth_m':depth,'temperature':p['temperature'][i],'biomass':b,'cohorts':cs})
 carbon=p['carbon_dioxide']*1e9*n*12/44+(bio+det)*area;water=(sum(p['water'])+sum(p['vapor']))*1e9+(stored+carry)*area
 out[name]={'fixture_sha256':hashlib.sha256(pth.read_bytes()).hexdigest(),'fixture_bytes':pth.stat().st_size,'biomass_density_sum':bio,'living':live,'occupied':occupied,'body_water_kg_m2_sum':stored,'water_kg':water,'carbon_kg':carbon,'nutrient_kg':nt*area,'shallow_residents':shore}
initial=out.get('matched-initial100')
if initial:
 for name,x in out.items():
  if name== 'matched-initial100':continue
  for k in ['water_kg','carbon_kg','nutrient_kg']:x[k+'_change']=x[k]-initial[k]
  x['water_change_global_equivalent_m']=x['water_kg_change']/(4*math.pi*5000000**2)/1000
for arm in ['on','off']:
 p=root/(arm+'100.log')
 if p.exists():
  s=p.read_text();out[arm+'_events']={'shallow_local_births':re.findall(r'^SHORE_LOCAL_BIRTH.*$',s,re.M),'target_arrivals':re.findall(r'^RIM_ARRIVAL.*$',s,re.M),'last_shore_flux':re.findall(r'^SHORE_FLUX.*$',s,re.M)[-1:], 'outgoing_shallow_propagules':sum(float(re.search(r'source_depth_m=([^ ]+)',l)[1])<.2 for l in s.splitlines() if l.startswith('SHORE_PROPAGULE'))}
print(json.dumps(out,indent=2))

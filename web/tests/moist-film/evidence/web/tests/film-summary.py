from pathlib import Path
import json,math,struct,hashlib,re,sys
root=Path(sys.argv[1]);suffix=sys.argv[2] if len(sys.argv)>2 else '';names=['initial'+('100' if suffix else ''),'on'+suffix+'-final','off'+suffix+'-final'];out={}
for name in names:
 path=root/(name+'.json')
 if not path.exists():continue
 p=json.loads(path.read_text());n=len(p['water']);area=struct.unpack('f',struct.pack('f',4*math.pi*(p['radius']*1000)**2/n))[0];bio=det=nt=0;live=occupied=0;shore=[]
 for i,c in enumerate(p['origin']['cells']):
  cs=[x['value']for x in c['sparse']];b=sum(x['biomass']for x in cs);bio+=b;det+=c['detritus'];nt+=c['nutrient']+.1*b;live+=len(cs);occupied+=b>0;depth=p['water'][i]*1e6/area
  if b and depth<.2:shore.append({'cell':i,'depth_m':depth,'temperature':p['temperature'][i],'biomass':b,'cohorts':cs})
 out[name]={'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'schema':p['version'],'biomass':bio,'living':live,'occupied':occupied,'shallow':shore,'carbon_kg':p['carbon_dioxide']*1e9*n*12/44+(bio+det)*area,'nutrient_kg':nt*area,'water_kg':(sum(p['water'])+sum(p['vapor']))*1e9}
initial=out[names[0]]
for name in names[1:]:
 if name not in out:continue
 for k in ['carbon_kg','nutrient_kg','water_kg']:out[name][k+'_change']=out[name][k]-initial[k]
for arm in ['on','off']:
 p=root/(arm+suffix+'.log')
 if p.exists():
  s=p.read_text();out[arm+'_observations']={'last_flux':re.findall(r'^FILM_DAY.*$',s,re.M)[-1:],'paid_births':re.findall(r'^FILM_PAID_BIRTH.*$',s,re.M),'thin_film_credit_funded_births':re.findall(r'^FILM_FUNDED_BIRTH.*$',s,re.M),'save_check':re.findall(r'^ORIGIN_SAVE.*$',s,re.M)}
print(json.dumps(out,indent=2))

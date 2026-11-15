"""Retrospective saved-world water/temperature census, not current engine eligibility."""
import json,math,pathlib,hashlib,sys
root=pathlib.Path(sys.argv[1]);out=pathlib.Path(sys.argv[2]);rows=[]
for day in [30,40,50,60]:
 f=root/f'natural60-day{day}.json';raw=f.read_bytes();p=json.loads(raw);n=len(p['water']);area=4*math.pi*(p['radius']*1000)**2/n;depth=[w*1e6/area for w in p['water']]
 hab={i for i,d in enumerate(depth) if .2<=d<=50 and 260<p['temperature'][i]<355};growth={i for i in hab if p['temperature'][i]>273.15};occupied={i for i,c in enumerate(p['origin']['cells']) if any(x['value']['biomass']>0 for x in c['sparse'])}
 rows.append({'day':day,'input_sha256':hashlib.sha256(raw).hexdigest(),'cells':n,'depth_temperature_habitable':len(hab),'growth_temperature_subset':len(growth),'occupied':len(occupied),'habitable_occupied':len(hab&occupied),'film_0_to_0_2m':sum(0<d<.2 for d in depth),'dry':sum(d<=0 for d in depth),'deep_over_50m':sum(d>50 for d in depth),'sqrt_mean_area_km':math.sqrt(area)/1000})
out.write_text(json.dumps({'scope':'One preserved historical native world, saved checkpoints; Python double arithmetic, not authoritative f32 live eligibility, connectivity, sunlight or resource guarantee','rows':rows},indent=2)+'\n')

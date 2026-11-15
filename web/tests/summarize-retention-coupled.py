from pathlib import Path
import json,sys,copy
root=Path(sys.argv[1]);records=[];fates={};absent=[];births=[];arm=None;open_trial=False
for line in (root/'run.log').read_text().splitlines():
 if line.startswith('MUTATION_COUPLED '):
  r=json.loads(line.split(' ',1)[1]);records.append(r);arm=r['arm'];open_trial=r['tick']<600
 elif line.startswith('MUTATION_FATE '):
  d=dict(x.split('=',1) for x in line.split()[1:]);key=(int(d['arm']),int(d['id']));fates.setdefault(key,[]).append(d)
 elif line.startswith('MUTATION_ABSENT '):absent.append(dict(x.split('=',1) for x in line.split()[1:]))
 elif line.startswith('MUTATION_PAID_BIRTH ') and open_trial:births.append({'arm':arm,**dict(x.split('=',1) for x in line.split()[1:])})
off=[]
for a in [0,2,4]:
 s=json.loads((root/f'arm-{a}.json').read_text());assert s['version']==8 and s['origin']['model_revision']==7;cfg=s['origin']['retention_mutation'];assert cfg['law']==1 and not cfg['enabled'];cfg['stream_seed']=0;off.append(s)
assert off[0]==off[1]==off[2],'Off worlds differ beyond explicit stream key'
summary=[]
for key,rows in sorted(fates.items()):
 summary.append({'arm':key[0],'id':key[1],'parent':int(rows[0]['parent']),'first_tick':int(rows[0]['tick']),'last_tick':int(rows[-1]['tick']),'observations':len(rows),'max_allocation':max(float(r['allocation']) for r in rows),'max_owned_water':max(float(r['water']) for r in rows),'min_depth_m':min(float(r['depth_m']) for r in rows),'max_mass':max(float(r['mass']) for r in rows),'last_mass':float(rows[-1]['mass']),'patches':sorted({int(r['patch']) for r in rows})})
print(json.dumps({'same_world_not_independent_planets':True,'off_exact_except_saved_stream_seed':True,'daily':records,'all_positive_lineage_fates':summary,'disappearances_unattributed':absent,'paid_births_during_trial':births},indent=2))

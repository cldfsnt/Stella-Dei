#!/usr/bin/env python3
import pathlib,os,subprocess,json,gzip,hashlib
r=pathlib.Path(__file__).resolve().parents[2];base=r.parent/'site-tmp/thermal-nurture';e=r/'web/tests/continuation-review/thermal-nurture'
def run(kind,stage,point=0,resume=False):
 b=base/kind;env=dict(os.environ,EGL_PLATFORM='surfaceless',LIBGL_ALWAYS_SOFTWARE='1',QA_STAGE=stage,QA_POINT=str(point));env.pop('QA_RESUME',None)
 if resume:env['QA_RESUME']='1'
 p=b/(('resume'if resume else stage)+'.log')
 with p.open('wb')as f:subprocess.run([str(b/'build/bin/stella-egl')],cwd=r,env=env,stdout=f,stderr=subprocess.STDOUT,check=True,timeout=900)
 return p
manifest={}
point=334;result=[]
for kind in ['control','candidate']:
 b=base/kind;run(kind,'plant',point);run(kind,'plant',point,True)
 assert(b/'final.json').read_bytes()==(b/'resumed.json').read_bytes()
 lines=(b/'plant.log').read_text().splitlines();again=(b/'resume.log').read_text().splitlines();rows=lambda t:[json.loads(l[len(t)+1:])for l in lines if l.startswith(t+' ')]
 for tag in ['PATCH','ROOT_WATER','USED_H']:
  assert[x for x in rows(tag)if x['tick']>60]==[json.loads(l[len(tag)+1:])for l in again if l.startswith(tag+' ')],(kind,tag)
 before=json.loads((b/'preseed.json').read_text());seeded=json.loads((b/'seeded.json').read_text());receipt=rows('FOUNDER')[0];sid=int(receipt['founder_id'])
 # Actual paid action changes only local colony/resources and global gas/lineage allocator.
 normalized=json.loads(json.dumps(seeded));normalized['carbon_dioxide']=before['carbon_dioxide'];normalized['oxygen']=before['oxygen'];normalized['origin']['cells'][point]=before['origin']['cells'][point];normalized['origin']['stats']['next_lineage']=before['origin']['stats']['next_lineage'];normalized['origin']['stats']['fixed_carbon']=before['origin']['stats']['fixed_carbon'];assert normalized==before
 assert seeded['origin']['stats']['next_lineage']==before['origin']['stats']['next_lineage']+1
 assert seeded['origin']['stats']['fixed_carbon']>before['origin']['stats']['fixed_carbon']
 end=json.loads((b/'final.json').read_text());family=[]
 for i,cell in enumerate(end['origin']['cells']):
  for slot in cell.get('sparse',[]):
   c=slot['value']
   if c['biomass']>0 and(c['lineage']==sid or c['parent']==sid):family.append({'point':i,'cohort':c})
 patch=rows('PATCH');used=rows('USED_H');water=[x for x in rows('ROOT_WATER')if x['lineage']==sid]
 result.append({'kind':kind,'seed':before['seed'],'point':point,'receipt':receipt,'water_input':rows('WATER_INPUT'),'conditioning':rows('NURTURE'),'drawdown':rows('WATER_DRAWDOWN'),'family':family,'family_density_sum':sum(x['cohort']['biomass']for x in family),'temperature':[min(x['temperature']for x in patch),max(x['temperature']for x in patch)],'cold_ticks':sum(x['temperature']<=273.15 for x in patch),'depth_m':[min(x['depth_m']for x in patch),max(x['depth_m']for x in patch)],'soil':[min(x['soil']for x in patch),max(x['soil']for x in patch)],'root_credit':sum(x['credit']for x in water),'used_ticks':len({x['tick']for x in used if x['effective_h']>0}),'endpoint_sha256':hashlib.sha256((b/'final.json').read_bytes()).hexdigest()})
 for name in ['spin.json','preseed.json','seeded.json','midpoint.json','final.json','resumed.json']:
  manifest[kind+'/'+name]=hashlib.sha256((b/name).read_bytes()).hexdigest()
 for name in ['plant.log','resume.log','final.json']:(e/(kind+'-'+name+'.gz')).write_bytes(gzip.compress((b/name).read_bytes(),mtime=0))
(e/'results.json').write_text(json.dumps(result,indent=2)+'\n');(e/'input-hashes.json').write_text(json.dumps(manifest,indent=2)+'\n');print(json.dumps(result,indent=2))

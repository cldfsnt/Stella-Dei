from pathlib import Path
import os,subprocess,json,hashlib
r=Path(__file__).resolve().parents[2];tmp=r.parent/'site-tmp';b=tmp/'origin-final-demand-native';exe=b/'install/bin/stella-egl';old=tmp/'origin-land-gate/candidate/install/bin/stella-egl';day=tmp/'origin-land-day30/day-30.json'
def run(name,path,ticks,migrate=False,binary=exe,reset=False):
 out=b/(name+'.json');env=dict(os.environ,EGL_PLATFORM='surfaceless',LIBGL_ALWAYS_SOFTWARE='1',QA_LAND_INPUT=str(path),QA_LAND_OUTPUT=str(out),QA_LAND_TICKS=str(ticks));
 if migrate:env['QA_FINAL_DEMAND_MIGRATE']='1'
 if reset:env['QA_LAND_RESET']=str(tmp/'natural60-day60.json')
 with (b/(name+'.log')).open('w') as log:subprocess.run([str(binary)],cwd=r,env=env,stdout=log,stderr=subprocess.STDOUT,check=True,timeout=180)
 return out
results={}
# Explicit migration only here, no new traits/resources/climate edits.
initial=run('law3-initial',day,0,True)
a=json.loads(day.read_bytes());c=json.loads(initial.read_bytes());expected=json.loads(day.read_bytes());expected['version']=10;expected['beta_origin']['format']='origin_land_beta_v3';expected['beta_origin']['config']['physiology_law']=3
assert c==expected,'migration changed more than law identity'
p2=run('law3-2',initial,2);p22=run('law3-2plus2',p2,2,reset=True);p4=run('law3-4',initial,4)
assert p22.read_bytes()==p4.read_bytes();results['law3_fresh_process_2plus2_equals4']=True
l1=run('law1-4',day,4);ref=run('law1-reference-4',day,4,binary=old);assert l1.read_bytes()==ref.read_bytes();results['law1_exact_original_beta']=True
for name,path in [('natural',tmp/'natural60-day60.json'),('warm',tmp/'foraging-production/warm-actual-end.json')]:
 p=run('legacy-'+name,path,10);reference=tmp/('origin-land-gate/candidate-'+name+'.json');assert p.read_bytes()==reference.read_bytes();results['legacy_'+name+'_exact']=True
law2=run('law2-historical-4',tmp/'origin-basal-native/law2-initial.json',4);assert law2.read_bytes()==(tmp/'origin-basal-native/law2-4.json').read_bytes();results['law2_exact_historical']=True
results['explicit_migration_identity_only']=True;results['hashes']={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in b.glob('*.json') if p.name!='source-sha256.json'}
(b/'results.json').write_text(json.dumps(results,indent=2)+'\n');print(json.dumps(results,indent=2))

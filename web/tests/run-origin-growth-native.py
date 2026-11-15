from pathlib import Path
import os,subprocess,json,hashlib
r=Path(__file__).resolve().parents[2];t=r.parent/'site-tmp';b=t/'root-growth-normalization';exe=b/'install/bin/stella-egl'
def run(name,path,ticks,migrate=False):
 out=b/(name+'.json');env=dict(os.environ,EGL_PLATFORM='surfaceless',LIBGL_ALWAYS_SOFTWARE='1',QA_LAND_INPUT=str(path),QA_LAND_OUTPUT=str(out),QA_LAND_TICKS=str(ticks))
 if migrate:env['QA_GROWTH_MIGRATE']='1'
 with (b/(name+'.log')).open('w')as log:subprocess.run([str(exe)],cwd=r,env=env,stdout=log,stderr=subprocess.STDOUT,check=True,timeout=180)
 return out
results={};old=t/'origin-final-demand-native'
for law,input,reference in [('law3',old/'law3-initial.json',old/'law3-4.json'),('law2',t/'origin-basal-native/law2-initial.json',t/'origin-basal-native/law2-4.json'),('law1',t/'origin-land-day30/day-30.json',old/'law1-4.json')]:
 actual=run(law+'-4',input,4);assert actual.read_bytes()==reference.read_bytes(),law;results[law+'_full_saved_state_rng_exact']=True
for name,input,reference in [('natural',t/'natural60-day60.json',old/'legacy-natural.json'),('warm',t/'foraging-production/warm-actual-end.json',old/'legacy-warm.json')]:
 actual=run(name+'-10',input,10);assert actual.read_bytes()==reference.read_bytes(),name;results[name+'_full_saved_state_rng_exact']=True
initial=run('law4-initial',old/'law3-initial.json',0,True);expected=json.loads((old/'law3-initial.json').read_bytes());expected['version']=12;expected['beta_origin']['format']='origin_land_beta_v4';expected['beta_origin']['config']['physiology_law']=4;assert json.loads(initial.read_bytes())==expected;results['migration_identity_only']=True
p2=run('law4-2',initial,2);p22=run('law4-2plus2',p2,2);p4=run('law4-4',initial,4);assert p22.read_bytes()==p4.read_bytes();results['law4_fresh_process_restart_exact']=True
results['hashes']={p.name:hashlib.sha256(p.read_bytes()).hexdigest()for p in b.glob('*.json')};(b/'native-results.json').write_text(json.dumps(results,indent=2)+'\n');print(json.dumps(results,indent=2))

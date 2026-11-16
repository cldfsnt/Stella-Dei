from pathlib import Path
import os,subprocess,json,hashlib
r=Path(__file__).resolve().parents[2];t=r.parent/'site-tmp';out=t/'protective-world';e=r/'web/tests/continuation-review/protective-world';results={}
for mode in ['off','on']:
 b=out/mode
 for arm in range(2):
  for resumed in [False,True]:
   env=dict(os.environ,QA_ARM=str(arm),EGL_PLATFORM='surfaceless',LIBGL_ALWAYS_SOFTWARE='1');env.pop('QA_RESUME',None)
   if resumed:env['QA_RESUME']='1'
   with (e/f'{mode}-{arm}-{"resume" if resumed else "main"}.log').open('w') as log:subprocess.run([str(b/'install/bin/stella-egl')],cwd=r,env=env,stdout=log,stderr=subprocess.STDOUT,check=True,timeout=180)
  final=b/f'arm-{arm}-60.json';resume=b/f'resume-arm-{arm}-60.json'
  assert final.read_bytes()==resume.read_bytes(),(mode,arm,'world restart')
  assert Path(str(final)+'.activity.json').read_bytes()==Path(str(resume)+'.activity.json').read_bytes(),(mode,arm,'activity restart')
  if mode=='off':assert final.read_bytes()==(t/f'rooted-natural/arm-{arm}-60.json').read_bytes(),(arm,'legacy exact')
  results[f'{mode}-{arm}']={'sha256':hashlib.sha256(final.read_bytes()).hexdigest(),'activity':json.loads(Path(str(final)+'.activity.json').read_text()),'restart_exact':True,'old_exact':mode=='off'}
  (e/'results.json').write_text(json.dumps(results,indent=2)+'\n')
print('ALL_FIXED_GATES_PASS')

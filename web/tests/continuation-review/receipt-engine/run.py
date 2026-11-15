from pathlib import Path
import subprocess,os,json,hashlib,time
root=Path(os.environ['STELLA_WORKSPACE']);out=root/'site-tmp/receipt-engine';repo=root/'stella-independent-review';records=[]
for day in (30,60):
 save=root/f'site-tmp/natural60-day{day}.json';data=save.read_bytes()
 for dt in (1440,720):
  env=os.environ.copy();env.update(STELLA_ORIGIN_COUPLED='1',STELLA_ORIGIN_FAST='1',QA_PULSE_SAVE=str(save),LIBGL_ALWAYS_SOFTWARE='1',EGL_PLATFORM='surfaceless',STELLA_EGL_CAPTURE_PREFIX=str(out/f'd{day}-dt{dt}'))
  if dt==720:env['QA_RECEIPT_HALF']='1'
  log=out/f'd{day}-dt{dt}.log';t=time.monotonic()
  with log.open('w') as f:p=subprocess.run([str(out/'build/bin/stella-egl')],cwd=repo,env=env,stdout=f,stderr=subprocess.STDOUT)
  records.append(dict(day=day,dt=dt,save_sha256=hashlib.sha256(data).hexdigest(),save_bytes=len(data),game_time=json.loads(data)["game_time"],save_top_level_keys=list(json.loads(data)),exit=p.returncode,wall_seconds=time.monotonic()-t,log=log.name))
  (out/'runs.json').write_text(json.dumps(records,indent=2)+'\n')
  if p.returncode:raise SystemExit(p.returncode)

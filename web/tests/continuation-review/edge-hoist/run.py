from pathlib import Path
import os,subprocess,json,time,hashlib
root=Path(os.environ['STELLA_WORKSPACE']);out=root/'site-tmp/edge-hoist/engine';records=[]
for name,save in [('early',root/'site-tmp/cpu-v44/cold-base-early.json'),('day30',root/'site-tmp/natural60-day30.json'),('day60',root/'site-tmp/natural60-day60.json')]:
 env=os.environ.copy();env.update(STELLA_ORIGIN_COUPLED='1',STELLA_ORIGIN_FAST='1',QA_PULSE_SAVE=str(save),LIBGL_ALWAYS_SOFTWARE='1',EGL_PLATFORM='surfaceless',STELLA_EGL_CAPTURE_PREFIX=str(out/name))
 t=time.monotonic()
 with (out/(name+'.log')).open('w') as f:p=subprocess.run([str(out/'build/bin/stella-egl')],cwd=root/'stella-independent-review',env=env,stdout=f,stderr=subprocess.STDOUT)
 records.append(dict(world=name,sha256=hashlib.sha256(save.read_bytes()).hexdigest(),game_time=json.loads(save.read_text())['game_time'],exit=p.returncode,wall_seconds=time.monotonic()-t));(out/'runs.json').write_text(json.dumps(records,indent=2)+'\n')
 if p.returncode:raise SystemExit(p.returncode)

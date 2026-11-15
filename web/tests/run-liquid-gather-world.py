from pathlib import Path
import subprocess,os,json,hashlib,shutil,time
r=Path(__file__).resolve().parents[2];base=r.parent/'site-tmp';p=base/'liquid-gather-world';results=[]
for label,inp in [('day30','natural60-day30.json'),('day60','natural60-day60.json'),('day90','grazing-coupled/arm-0-day90.json')]:
 d=p/label;d.mkdir(exist_ok=True);env=os.environ|{'LIBGL_ALWAYS_SOFTWARE':'1','EGL_PLATFORM':'surfaceless','STELLA_ORIGIN_COUPLED':'1','STELLA_ORIGIN_FAST':'1','STELLA_ORIGIN_WIDTH':'390','QA_PULSE_SAVE':str(base/inp),'STELLA_EGL_CAPTURE_PREFIX':str(d/'capture')}
 with (d/'run.log').open('w')as f:
  start=time.monotonic();proc=subprocess.run([str(p/'build/bin/stella-egl')],cwd=r,env=env,stdout=f,stderr=subprocess.STDOUT);duration=time.monotonic()-start
 assert proc.returncode==0,(label,proc.returncode)
 for suffix in ['', '.uninterrupted.json','.restored.json']:shutil.copy2(p/('arm-0.json'+suffix),d/('endpoint.json'+suffix))
 assert (d/'endpoint.json.uninterrupted.json').read_bytes()==(d/'endpoint.json.restored.json').read_bytes()
 lines=(d/'run.log').read_text().splitlines();stages=[json.loads(l.split(' ',1)[1])for l in lines if l.startswith('WATER_STAGE ')];gathers=[json.loads(l.split(' ',1)[1])for l in lines if l.startswith('LIQUID_GATHER ')];assert len(stages)>=60 and len(gathers)>=60
 rows=dict(label=label,exit=proc.returncode,process_seconds_including_startup_save=duration,continuation_exact=True,endpoint_sha256=hashlib.sha256((d/'endpoint.json').read_bytes()).hexdigest(),stages={k:sum(x[k]for x in stages[:60])for k in stages[0]},gather={k:sum(x[k]for x in gathers[:60])for k in ['signed','sumabs','ns']},scratch_bytes=gathers[0]['scratch_bytes']);results.append(rows);print(rows,flush=True)
 (d/'stages.json').write_text(json.dumps(stages,indent=2));(d/'gathers.json').write_text(json.dumps(gathers,indent=2))
(p/'results.json').write_text(json.dumps(results,indent=2))

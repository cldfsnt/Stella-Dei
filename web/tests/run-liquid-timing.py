from pathlib import Path
import os,json,re,subprocess,hashlib,statistics
r=Path(__file__).resolve().parents[2];base=r.parent/'site-tmp';results=[]
for label,inp in [('day30','natural60-day30.json'),('day60','natural60-day60.json'),('day90','grazing-coupled/arm-0-day90.json')]:
 for repeat in range(3):
  for mode in (['baseline','candidate'] if repeat%2==0 else ['candidate','baseline']):
   p=base/('liquid-timing-'+mode);d=p/f'{label}-{repeat}';d.mkdir(exist_ok=True);env=os.environ|{'LIBGL_ALWAYS_SOFTWARE':'1','EGL_PLATFORM':'surfaceless','STELLA_ORIGIN_COUPLED':'1','STELLA_ORIGIN_FAST':'1','STELLA_ORIGIN_WIDTH':'390','QA_PULSE_SAVE':str(base/inp),'STELLA_EGL_CAPTURE_PREFIX':str(d/'capture')}
   with (d/'run.log').open('w')as f:proc=subprocess.run([str(p/'build/bin/stella-egl')],cwd=r,env=env,stdout=f,stderr=subprocess.STDOUT)
   assert proc.returncode==0,(label,repeat,mode,proc.returncode)
   log=(d/'run.log').read_text();ns=int(re.search(r'FULLSTEP ns=(\d+) ticks=60',log)[1]);endpoint=p/'arm-0.json';expected=base/('water-stage-production'if mode=='baseline'else'liquid-gather-world')/label/'endpoint.json';assert endpoint.read_bytes()==expected.read_bytes(),(label,mode,'instrumentation/guard changed model')
   assert (p/'arm-0.json.uninterrupted.json').read_bytes()==(p/'arm-0.json.restored.json').read_bytes()
   row=dict(label=label,repeat=repeat,mode=mode,ns=ns,ms_per_tick=ns/60e6,endpoint_same_prior=True,continuation_exact=True);results.append(row);print(row,flush=True)
(base/'liquid-timing-results.json').write_text(json.dumps(results,indent=2))
for label in ['day30','day60','day90']:
 a=[x['ms_per_tick']for x in results if x['label']==label and x['mode']=='baseline'];b=[x['ms_per_tick']for x in results if x['label']==label and x['mode']=='candidate'];print(label,'median',statistics.median(a),statistics.median(b),'paired_percent',[(y/x-1)*100 for x,y in zip(a,b)],flush=True)

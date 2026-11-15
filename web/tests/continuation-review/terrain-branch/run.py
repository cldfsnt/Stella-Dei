from pathlib import Path
import os,subprocess,hashlib,json
r=Path(__file__).resolve().parent;results=[]
worlds={'early':r.parent/'cpu-v44/cold-base-early.json','established30d':r.parent/'cpu-v44/save.json'}
for width,height in [(390,700),(1366,768)]:
 for world,save in worlds.items():
  for repeat in range(3):
   pairs={}
   for kind in (['base','branch'] if repeat%2==0 else ['branch','base']):
    stem=f'{width}-{world}-{repeat+1}-{kind}';e=os.environ.copy();e.update(STELLA_CPU_LOAD=str(save),STELLA_CPU_RESULT_PREFIX=str(r/stem),STELLA_ORIGIN_COUPLED='1',STELLA_ORIGIN_FAST='1',STELLA_PRODUCER_LONG='1',STELLA_DIAGNOSTIC_DAYS='30',STELLA_FORMS_SINGLE='1',STELLA_ORIGIN_WIDTH=str(width),STELLA_ORIGIN_HEIGHT=str(height),STELLA_CPU_LEVEL='6')
    if kind=='branch':e['STELLA_TERRAIN_BRANCH']='1'
    if repeat==0:e['STELLA_SHADER_PROOF']=str(r/stem)
    with (r/(stem+'.log')).open('w') as f:
     p=subprocess.Popen([str(r/'build/bin/stella-egl')],env=e,stdout=f,stderr=subprocess.STDOUT);_,status,u=os.wait4(p.pid,0);code=os.waitstatus_to_exitcode(status)
    row={'width':width,'height':height,'world':world,'repeat':repeat+1,'kind':kind,'exit':code,'rss_kib':u.ru_maxrss};results.append(row);print(row,flush=True)
    if code:raise SystemExit(code)
    pairs[kind]=[hashlib.sha256((r/f'{stem}-loaded-{speed}.json').read_bytes()).hexdigest() for speed in [0,21600,86400]]
   assert pairs['base']==pairs['branch'],(width,world,repeat,pairs)
   print('STATE_PARITY',width,world,repeat+1,True,flush=True)
   if repeat==0:
    for mode in range(5):
     images=[hashlib.sha256((r/f'{width}-{world}-1-{kind}-mode{mode}.ppm').read_bytes()).hexdigest() for kind in ['base','branch']]
     print('IMAGE_PARITY',width,world,mode,images[0]==images[1],flush=True)
     assert images[0]==images[1],(width,world,mode,images)
(r/'results.json').write_text(json.dumps(results,indent=2))

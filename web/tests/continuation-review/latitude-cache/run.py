from pathlib import Path
import os,subprocess,hashlib,json
r=Path(__file__).resolve().parent
worlds={'early':r.parent/'cpu-v44/cold-base-early.json','established30d':r.parent/'cpu-v44/save.json'}
results=[]
for world,save in worlds.items():
 for repeat in range(3):
  pair=[]
  for kind in (['base','candidate'] if repeat%2==0 else ['candidate','base']):
   stem=f'{world}-{repeat+1}-{kind}';e=os.environ.copy();e.update(STELLA_CPU_LOAD=str(save),STELLA_CPU_RESULT_PREFIX=str(r/stem),STELLA_ORIGIN_COUPLED='1',STELLA_ORIGIN_FAST='1',STELLA_PRODUCER_LONG='1',STELLA_DIAGNOSTIC_DAYS='30',STELLA_FORMS_SINGLE='1',STELLA_ORIGIN_WIDTH='390',STELLA_CPU_LEVEL='6')
   if repeat==0:e['STELLA_CPU_COLD']='1'
   else:e.pop('STELLA_CPU_COLD',None)
   with (r/(stem+'.log')).open('w') as f:
    p=subprocess.Popen([str(r/(kind+'-build/bin/stella-egl'))],env=e,stdout=f,stderr=subprocess.STDOUT);_,status,u=os.wait4(p.pid,0);code=os.waitstatus_to_exitcode(status)
   row={'world':world,'repeat':repeat+1,'kind':kind,'exit':code,'max_rss_kib':u.ru_maxrss,'cold':repeat==0};results.append(row);print(row,flush=True)
   if code:raise SystemExit(code)
   pair.append(hashlib.sha256((r/(stem+'-loaded.json')).read_bytes()).hexdigest())
  assert pair[0]==pair[1],(world,repeat,pair)
  print('FULL_WORLD_PARITY',world,repeat+1,pair[0],flush=True)
(r/'results.json').write_text(json.dumps(results,indent=2))

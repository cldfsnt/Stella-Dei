from pathlib import Path
import subprocess,json,re,hashlib,statistics,datetime,sys
r=Path(__file__).resolve().parents[2];o=r.parent/'site-tmp/wasm-land-phases';previous=r.parent/'site-tmp/wasm-land-screen';inputs={'off':previous/'empty-off.json','on':previous/'empty-beta.json'};names=['thermal','liquid_wind','atmosphere_prepare','column','coefficient','gather','ecology']
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def run(label,arm,mode):
 p=o/(label+'.json');l=o/(label+'.log')
 with l.open('w')as f:subprocess.run(['node',str(o/arm/'profile.js'),str(inputs[mode]),str(o/'graph.json'),str(p),'72','0'],stdout=f,stderr=subprocess.STDOUT,check=True)
 return p,l.read_text()
if sys.argv[1]=='gates':
 old=json.loads((previous/'gates.json').read_text());out={}
 for arm in ['plain','traced']:
  for mode in ['off','on']:
   p,l=run('gate-'+arm+'-'+mode,arm,mode);expected=old[('empty'if mode=='off'else'beta')+'-candidate']['sha256'];assert sha(p)==expected,(arm,mode,'endpoint');out[arm+'-'+mode]=expected
 (o/'gates.json').write_text(json.dumps(out,indent=2));print(out)
else:
 gates=json.loads((o/'gates.json').read_text());rows=[];start=datetime.datetime.now(datetime.timezone.utc).isoformat()
 sequence=[('plain','off'),('plain','on'),('traced','on'),('traced','off'),('traced','off'),('traced','on'),('plain','on'),('plain','off')]
 for i,(arm,mode)in enumerate(sequence):
  p,l=run('time-'+str(i),arm,mode);assert sha(p)==gates[arm+'-'+mode];ms=float(re.search(r'WASM_PLANET .*?total_ms=([\d.e+-]+)',l)[1]);vals=[float(x.strip()) for x in re.search(r'LAND_PHASES \{([^}]+)',l)[1].split(',')];row={'arm':arm,'mode':mode,'index':i,'ms_per_tick':ms/60,'stages_ms_per_tick':dict(zip(names,[v/60 for v in vals]))};rows.append(row);print(row,flush=True)
 summary={}
 for mode in ['off','on']:
  a=statistics.median(x['ms_per_tick']for x in rows if x['arm']=='plain'and x['mode']==mode);b=statistics.median(x['ms_per_tick']for x in rows if x['arm']=='traced'and x['mode']==mode);summary[mode]={'plain':a,'traced':b,'overhead_percent':100*(b/a-1),'stage_medians':{name:statistics.median(x['stages_ms_per_tick'][name]for x in rows if x['arm']=='traced'and x['mode']==mode)for name in names}}
 result={'start':start,'end':datetime.datetime.now(datetime.timezone.utc).isoformat(),'rows':rows,'summary':summary};(o/'timing.json').write_text(json.dumps(result,indent=2));print(summary)

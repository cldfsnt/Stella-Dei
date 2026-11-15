from pathlib import Path
import json,subprocess,hashlib,re,statistics,sys,datetime
r=Path(__file__).resolve().parents[3];o=r/'site-tmp/wasm-receipt-screen';inp=r/'site-tmp/foraging-production/warm-actual-end.json'
def run(label,arm,mode,ticks,source=inp):
 out=o/(label+'.json');log=o/(label+'.log')
 with log.open('w') as f: subprocess.run(['node',str(o/arm/'profile.js'),str(source),str(o/'graph.json'),str(out),str(ticks),str(mode)],stdout=f,stderr=subprocess.STDOUT,check=True)
 return out,json.loads(out.read_text()),log.read_text()
def norm(j):
 j=json.loads(json.dumps(j));j.pop('sandbox_defense',None);j.pop('version',None)
 for p in j['plants']:
  assert p.get('toughness',0)==0;p.pop('toughness',None)
 return j
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
if sys.argv[1]=='gates':
 results={};ends={}
 for name,arm,mode in [('baseline','baseline',0),('no_selection','candidate',0),('selected','candidate',1)]:
  z,j,l=run(name+'-zero',arm,mode,0);assert norm(j)==norm(json.loads(inp.read_text()))
  end,j,l=run(name+'-72',arm,mode,72);ends[name]=j
  resumed,jr,_=run(name+'-resume',arm,mode,10,end);full,jf,_=run(name+'-82',arm,mode,82);assert jr==jf
  results[name]={'endpoint_sha256':sha(end),'bytes':end.stat().st_size,'layout':next(x for x in l.splitlines()if x.startswith('LAYOUT')),'positive_toughness_patches':sum(p.get('toughness',0)>0 for p in j['plants']),'max_toughness':max(p.get('toughness',0)for p in j['plants']),'continuation_exact':True}
 assert ends['baseline']==ends['no_selection']==ends['selected']
 (o/'gates.json').write_text(json.dumps(results,indent=2));print(results)
else:
 gates=json.loads((o/'gates.json').read_text());rows=[];start=datetime.datetime.now(datetime.timezone.utc).isoformat()
 for group,b in [('no_selection',0),('selected',1)]:
  for i,(arm,mode,key) in enumerate([('baseline',0,'baseline'),('candidate',b,group),('candidate',b,group),('baseline',0,'baseline')]):
   path,j,log=run(f'time-{group}-{i}',arm,mode,72);assert sha(path)==gates[key]['endpoint_sha256']
   ms=float(re.search(r'WASM_PLANET .*?total_ms=([\d.e+-]+)',log)[1]);rows.append(dict(group=group,index=i,arm=arm,ms_per_tick=ms/60));print(rows[-1],flush=True)
 summary={}
 for group in ['no_selection','selected']:
  a=statistics.median(x['ms_per_tick']for x in rows if x['group']==group and x['arm']=='baseline');b=statistics.median(x['ms_per_tick']for x in rows if x['group']==group and x['arm']=='candidate');summary[group]={'baseline':a,'candidate':b,'percent':100*(b/a-1)}
 (o/'timing.json').write_text(json.dumps(dict(start=start,end=datetime.datetime.now(datetime.timezone.utc).isoformat(),rows=rows,summary=summary),indent=2));print(summary)

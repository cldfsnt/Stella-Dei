from pathlib import Path
import subprocess,json,hashlib
r=Path(__file__).resolve().parents[2];b=r.parent/'site-tmp/wasm-protective-cost';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def run(label,mode,inp,ticks):
 out=b/(label+'.json')
 with(b/(label+'.log')).open('wb')as f:subprocess.run(['node',str(b/mode/'profile.js'),str(inp),str(b/'graph.json'),str(out),str(ticks),'0'],stdout=f,stderr=subprocess.STDOUT,check=True,timeout=180)
 return out
norm=lambda v:({k:norm(x)for k,x in v.items()if not(k=='cohorts'and x==[])}if isinstance(v,dict)else[norm(x)for x in v]if isinstance(v,list)else v)
gates={}
for case in ['off','enabled']:
 gates[case]={}
 for arm,mode in [('A','legacy'),('B','small')]:
  inp=b/f'{case}-{mode}.json';prefix=f'{case}-{mode}';zero=run(prefix+'-zero',mode,inp,0)
  # schema15 canonical includes default protective fields omitted from identity-only QA input.
  def clean(v):
   if isinstance(v,dict):return {k:clean(x)for k,x in v.items()if not(k=='protective_investment'and x==0)and not(k=='protective_clock'and x==-1)}
   return [clean(x)for x in v]if isinstance(v,list)else v
  assert clean(norm(json.load(open(zero))))==clean(norm(json.load(open(inp))))
  # Feed canonical zero to balanced harness to keep exact default-field domain.
  inp.write_bytes(zero.read_bytes())
  end=run(prefix+'-72',mode,inp,72);res=run(prefix+'-resume',mode,end,10);full=run(prefix+'-82',mode,inp,82);assert res.read_bytes()==full.read_bytes()
  if case=='off'and mode=='small':assert (b/'off-legacy-72.json').read_bytes()==end.read_bytes()
  gates[case][arm]={'input':inp.name,'endpoint_sha256':sha(end),'zero_material_exact':True,'restart_exact':True,'cross_build_exact_required':case=='off'}
  print(case,mode,'PASS',flush=True)
(b/'gates.json').write_text(json.dumps(gates,indent=2))

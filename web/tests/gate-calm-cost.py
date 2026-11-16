from pathlib import Path
import subprocess,json,hashlib
r=Path(__file__).resolve().parents[2];b=r.parent/'site-tmp/wasm-calm-cost';reference=r.parent/'site-tmp/wasm-root-wind-screen/candidate';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def run(label,bin,inp,ticks):
 out=b/(label+'.json')
 with(b/(label+'.log')).open('wb')as f:subprocess.run(['node',str(bin/'profile.js'),str(inp),str(b/'graph.json'),str(out),str(ticks),'0'],stdout=f,stderr=subprocess.STDOUT,check=True,timeout=180)
 return out
norm=lambda v:({k:norm(x)for k,x in v.items()if not(k=='cohorts'and x==[])}if isinstance(v,dict)else [norm(x)for x in v]if isinstance(v,list)else v)
gates={}
for seed in(42,):
 gates[str(seed)]={}
 for arm,mode in [('A','legacy'),('B','small')]:
  inp=b/f'{seed}-{mode}.json';prefix=f'{seed}-{mode}';binary=b/mode
  zero=run(prefix+'-zero',binary,inp,0);assert norm(json.load(open(zero)))==norm(json.load(open(inp)))
  end=run(prefix+'-72',binary,inp,72);res=run(prefix+'-resume',binary,end,10);full=run(prefix+'-82',binary,inp,82);assert res.read_bytes()==full.read_bytes()
  if mode=='small':
   assert (b/'42-legacy-72.json').read_bytes()==end.read_bytes()
  gates[str(seed)][arm]={'mode':mode,'input':inp.name,'endpoint_sha256':sha(end),'zero_exact':True,'restart_exact':True,'cross_build_exact':True}
  print(seed,mode,'CORRECTNESS_PASS',flush=True)
(b/'gates.json').write_text(json.dumps(gates,indent=2))

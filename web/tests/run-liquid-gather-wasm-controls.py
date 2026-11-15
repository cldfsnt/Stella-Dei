from pathlib import Path
import subprocess,json,hashlib,datetime
r=Path(__file__).resolve().parents[2];b=r.parent/'site-tmp';o=b/'liquid-gather-wasm';base=b/'wasm-planet-profile';reference=json.loads((base/'results.json').read_text());h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
inputs={int(d):r.parent/v['path']for d,v in reference['inputs'].items()}
def execute(mode,input,ticks,label,trace=False):
 dest=o/(label+'.json');cmd=['node',str(o/mode/'profile.js'),str(input),str(base/'graph.json'),str(dest),str(ticks)]
 if trace:cmd.append(str(o/(label+'.bin')))
 with (o/(label+'.log')).open('w')as f:p=subprocess.run(cmd,cwd=r,stdout=f,stderr=subprocess.STDOUT)
 assert p.returncode==0,(label,p.returncode)
 return dest
proof={'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'worlds':{}}
for day,input in inputs.items():
 zero=execute('candidate',input,0,f'zero-day{day}');assert json.loads(zero.read_text())==json.loads(input.read_text())
 cand=execute('candidate',input,60,f'candidate-plain-day{day}');trace=execute('candidate-trace',input,60,f'candidate-day{day}',True);assert cand.read_bytes()==trace.read_bytes(),(day,'trace neutrality')
 baseline=execute('baseline-trace',input,60,f'baseline-day{day}',True);assert h(baseline)==reference['integrity'][f'wasm-{day}-60'],(day,'legacy trace neutrality')
 full=execute('candidate',input,70,f'uninterrupted-day{day}');restart=execute('candidate',cand,10,f'restarted-day{day}');assert full.read_bytes()==restart.read_bytes(),(day,'process restart')
 proof['worlds'][day]={'zero_input_equal':True,'diagnostic_exact':True,'legacy_diagnostic_exact':True,'new_process_restart_exact':True,'input_sha256':h(input),'candidate60_sha256':h(cand),'baseline60_sha256':h(baseline),'candidate70_restart_sha256':h(full),'candidate_trace_sha256':h(o/f'candidate-day{day}.bin'),'baseline_trace_sha256':h(o/f'baseline-day{day}.bin')};(o/'controls.json').write_text(json.dumps(proof,indent=2)+'\n');print('CONTROLS_PASS',day,flush=True)
proof['ended_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();(o/'controls.json').write_text(json.dumps(proof,indent=2)+'\n')

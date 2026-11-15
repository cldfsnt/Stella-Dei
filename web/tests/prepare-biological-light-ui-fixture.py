from pathlib import Path
import re,shutil,json,hashlib
r=Path(__file__).resolve().parents[2];out=Path('/workspace/scratch/f67c3ac60ca3/stella-competition-preview/dist');out.mkdir(parents=True,exist_ok=True)
s=(r/'web/shell.html').read_text().replace('{{{ SCRIPT }}}','').replace('{{{SCRIPT}}}','')
s=s.replace('</head>','<style>#more-menu,#life-sheet{width:358px;max-width:calc(100vw - 16px)}</style></head>')
s=s.replace('<body>','<body><aside style="padding:12px;background:#6d3c00">UI MOCK ONLY · 358px panels · no simulation<div id="mock-light-controls"></div></aside>')
for name in re.findall(r'<script src="([^"]+)"',s):
 if (r/'web'/name).is_file():shutil.copy2(r/'web'/name,out/name)
mock='''(()=>{let light=0;Module.started=true;Module.failed=false;Module._stella_world_mode=()=>1;Module._stella_life_snapshot=()=>0;Module._stella_goal_stage=()=>0;Module.ccall=(name)=>JSON.stringify(name==='stella_life_snapshot'?{status:'origin',world_serial:3,cell:12397,paused:true,time:86400,day:1,water_m:5,temperature_c:28,seed_reason:'eligible',simulation_light:light,cohorts:[]}:{status:'unavailable'});document.getElementById('cover').hidden=true;for(const [label,v] of [['Zero light',0],['Positive light',.123456],['Unavailable light',null]]){let b=document.createElement('button');b.textContent=label;b.onclick=()=>{light=v;refreshStarter();refreshLife();};document.getElementById('mock-light-controls').append(b);}let b=document.createElement('button');b.textContent='Open selected life';b.onclick=()=>{document.getElementById('more-menu').close();refreshLife();document.getElementById('life-sheet').showModal();};document.getElementById('mock-light-controls').append(b);syncWorldMode();openToolGroup('plant');refreshStarter();})();'''
s=s.replace('</body>','<script>'+mock+'</script></body>');(out/'index.html').write_text(s)
e=r/'web/tests/continuation-review/biological-light-ui';(e/'fixture-hashes.json').write_text(json.dumps({'shell':hashlib.sha256((r/'web/shell.html').read_bytes()).hexdigest(),'fixture':hashlib.sha256(s.encode()).hexdigest(),'mock':mock},indent=2)+'\n')

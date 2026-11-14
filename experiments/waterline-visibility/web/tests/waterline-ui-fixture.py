"""Render the unchanged Life-sheet handlers using actual native snapshot JSON.
This is UI-only screenshot QA, explicitly not a live simulation assertion.
"""
from pathlib import Path
import sys,json,shutil
root=Path(__file__).resolve().parents[2];output=Path(sys.argv[1]);output.mkdir(parents=True,exist_ok=True)
for name in ['touch-controls.js','stella-storage.js','life-trend.js','waterline-feedback.js']:shutil.copy2(root/'web'/name,output/name)
for case in ['wet','exposed']:
 data=json.loads((root/'tmp'/f'{case}.json').read_text());script='''<script>const recordedSnapshot=%s;
Module.ccall=(name)=>{if(name!=='stella_life_snapshot')throw Error('Unexpected UI call');return JSON.stringify(recordedSnapshot);};
Module.started=true;Module._stella_world_mode=()=>1;
document.getElementById('life-toggle').click();
const proof=document.createElement('p');proof.textContent='UI test: recorded native snapshot, not live simulation';proof.className='life-note';document.getElementById('life-sheet').appendChild(proof);
document.body.dataset.uiTest=document.getElementById('life-waterline').textContent;
</script>'''%json.dumps(data)
 html=(root/'web/shell.html').read_text().replace('{{{ SCRIPT }}}',script)
 (output/f'{case}.html').write_text(html)

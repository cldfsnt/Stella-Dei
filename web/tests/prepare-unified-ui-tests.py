"""Adapt only intentionally replaced preview UI expectations; preserve other assertions."""
from pathlib import Path
import shutil
r=Path(__file__).resolve().parents[2];base=r.parent/'site-tmp/protective-ui/web/tests';out=r.parent/'site-tmp/unified-ui/web/tests'
for name in ['combined-recovery-shell','combined-shell','combined-world','protective-ui','root-water-combined','shell']:
 s=(base/(name+'.test.cjs')).read_text()
 if name=='combined-recovery-shell':s=s.replace('Wetlands · optional roots + wind','Stella Dei · evolving worlds')
 if name=='combined-shell':s=s.replace('stella_wetlands_combined_new','stella_combined_protective_new')
 if name=='combined-world':s=s.replace('/off/','/original rules/')
 if name=='root-water-combined':s=s.replace('replaces the existing Wetlands browser save slot','replaces the existing game browser save slot')
 if name=='protective-ui':
  lines=s.splitlines();s='\n'.join("test('unified New has no climate/protection toggle maze',()=>{const fs=require('node:fs'),path=require('node:path'),s=fs.readFileSync(path.join(__dirname,'../shell.html'),'utf8');assert.doesNotMatch(s,/id=\"combined-climate\"|id=\"combined-protective\"/);assert.match(s,/Save \\+ new living planet/);});" if line.startswith("test('creation checkbox") else "test('world details retains non-numeric protection cost disclosure',()=>{const fs=require('node:fs'),path=require('node:path'),s=fs.readFileSync(path.join(__dirname,'../shell.html'),'utf8');assert.match(s,/adds simulation work and may run slower/);assert.doesNotMatch(s,/5\\.71%/);});" if line.startswith("test('optional new-world cost") else line for line in lines)+'\n'
 if name=='shell':s=s.replace('StellaCombined:', 'StellaWorldLibrary:{mount:()=>({cancel(){}})},StellaCombined:')
 (out/(name+'.test.cjs')).write_text(s)
shutil.copy2(r/'web/tests/world-library.test.cjs',out/'world-library.test.cjs')

(out/'fixtures').mkdir(exist_ok=True)
shutil.copy2(r/'web/tests/continuation-review/unified-transition/wind11-snapshot.json',out/'fixtures/wind11-snapshot.json')
s=(r/'web/tests/unified-ui.test.cjs').read_text().replace("path.resolve(__dirname,'../../../site-tmp/unified-ui/web')","path.resolve(__dirname,'..')").replace("continuation-review/unified-transition/wind11-snapshot.json","fixtures/wind11-snapshot.json")
(out/'unified-ui.test.cjs').write_text(s)

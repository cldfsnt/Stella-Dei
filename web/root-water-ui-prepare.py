from pathlib import Path
import shutil
r=Path(__file__).resolve().parents[1];t=r.parent/'site-tmp';o=t/'root-water-ui'
if not (o/'web').exists():shutil.copytree(t/'combined-playtest/web',o/'web',ignore=shutil.ignore_patterns('dist','node_modules','.cache'))
if not (o/'src').exists():shutil.copytree(t/'root-calm/src',o/'src')
for name in ['deps','assets']:
 if not (o/name).exists():(o/name).symlink_to((t/'root-wind-recovery'/name).resolve(),target_is_directory=True)
for name in ['build.zig','build.zig.zon','web-build.zig','LICENSE']:
 if (t/'root-wind-recovery'/name).exists():shutil.copy2(t/'root-wind-recovery'/name,o/name)
shutil.copy2(r/'web/root-water-founder.js',o/'web/rooted-founder.js')
shutil.copy2(r/'web/tests/root-water-founder.test.cjs',o/'web/tests/root-water-founder.test.cjs')

shutil.copy2(r/'web/root-water-combined.js',o/'web/combined-world.js')
shutil.copy2(r/'web/root-water-traits.js',o/'web/combined-traits.js')
shutil.copy2(r/'web/tests/root-water-combined.test.cjs',o/'web/tests/root-water-combined.test.cjs')
p=o/'web/shell.html';s=p.read_text()
if 'id="combined-climate"' not in s:
 s=s.replace('<button id="combined-new">','<label for="combined-climate">New combined world climate</label><select id="combined-climate" style="min-height:44px;font:inherit;width:100%;max-width:100%;box-sizing:border-box;background:#102c30;color:#f4fff8"><option value="historical" selected>Historical temperature response (default)</option><option value="calmer">Calmer ground-temperature response</option></select><p>New worlds only. Calmer temperature does not add water or guarantee survival. Imported worlds retain their saved settings.</p><button id="combined-new">')
 s=s.replace("fresh:world=>Module.ccall('stella_wetlands_combined_new','number',['number'],[world])", "fresh:(world,choice)=>Module.ccall(choice==='calmer'?'stella_combined_calm_new':'stella_wetlands_combined_new','number',['number'],[world])")
 p.write_text(s)

s=p.read_text()
if "canCreate:choice=>" not in s:
 s=s.replace("fresh:(world,choice)=>Module.ccall", "canCreate:choice=>choice!=='calmer'||typeof Module._stella_combined_calm_new==='function',fresh:(world,choice)=>Module.ccall")
 p.write_text(s)

p=o/'web/build.sh';s=p.read_text()
if '_stella_combined_calm_new,' not in s:s=s.replace('-sEXPORTED_FUNCTIONS=','-sEXPORTED_FUNCTIONS=_stella_combined_calm_new,')
p.write_text(s)

(o/'web/tests/fixtures').mkdir(exist_ok=True)
for n in [0,1]:shutil.copy2(r/f'web/tests/continuation-review/rooted-water-support/actual-receipt-{n}.json',o/f'web/tests/fixtures/root-water-actual-{n}.json')

from pathlib import Path
import shutil,difflib
r=Path(__file__).resolve().parents[2];base=r.parent/'site-tmp/wasm-planet-profile';out=r.parent/'site-tmp/wasm-edge-validation'
for mode in ['plain','stages']:
 d=out/mode;shutil.copytree(base/mode/'src',d/'src',dirs_exist_ok=True)
 p=d/'src/simulation/atmosphere_water.zig';s=p.read_text()
 s=s.replace(' pub fn rate(s:EdgeSource,to:[3]f64)f64{',' pub fn rate(s:EdgeSource,to:[3]f64)f64{return s.rateChecked(to,false);}\n // Caller must validate every target coordinate before choosing this path.\n pub fn rateFiniteTarget(s:EdgeSource,to:[3]f64)f64{return s.rateChecked(to,true);}\n fn rateChecked(s:EdgeSource,to:[3]f64,comptime target_validated:bool)f64{')
 s=s.replace('if(!std.math.isFinite(to[i]))return 0;const d=','if(!target_validated and !std.math.isFinite(to[i]))return 0;const d=')
 p.write_text(s)
 p=d/'src/simulation/planet.zig';s=p.read_text();start=s.index('        if(self.ensureAtmosphericEdgeScratch())for(');end=s.index('        const divider=self.getSubstanceDivider()',start)
 # The stage marker immediately before divider belongs after either branch.
 block=s[start:end];marker=''
 if 'qa_substages[1]' in block:
  at=block.index('        qa_substages[1]');marker=block[at:];block=block[:at]
 replacement='''        var qa_targets_finite=true;
        for(self.transformedPoints)|point|{
            if(!std.math.isFinite(point.x()) or !std.math.isFinite(point.y()) or !std.math.isFinite(point.z())){qa_targets_finite=false;break;}
        }
        if(qa_targets_finite){
'''+block.replace('source.rate(', 'source.rateFiniteTarget(')+'''        }else{
'''+block+'''        }
'''+marker
 s=s[:start]+replacement+s[end:];p.write_text(s)
 (d/'qa-edge.diff').write_text(''.join(difflib.unified_diff((base/mode/'src/simulation/planet.zig').read_text().splitlines(True),s.splitlines(True))))
print(out)

from pathlib import Path
import shutil,hashlib,json
r=Path(__file__).resolve().parents[2];t=r.parent/'site-tmp';old=t/'origin-final-demand-shoreline';b=t/'root-allocation-diagnostic';o=b/'src';assert not o.exists();shutil.copytree(old/'src',o)
p=o/'main.zig';s=p.read_text().replace(str(old),str(b));s=s.replace('if(depth_index!=0 and depth_index!=1 and depth_index!=3)','if(depth_index!=0)');s=s.replace('    if(ablated)return error.UnrequestedAblation;\n','');s=s.replace('if(ablated)state.planet.microbeCells[18327].cohorts[2].root_fraction=0;', 'std.debug.assert(state.planet.microbeCells[18327].cohorts[2].root_fraction==1.0/32.0);\n      if(ablated)state.planet.microbeCells[18327].cohorts[2].root_fraction=0.25;');p.write_text(s)
changed=[str(p.relative_to(o)) for p in o.rglob('*.zig') if p.read_bytes()!=(old/'src'/p.relative_to(o)).read_bytes()];assert changed==['main.zig'],changed
(b/'source-hashes.json').write_text(json.dumps({str(p.relative_to(o)):hashlib.sha256(p.read_bytes()).hexdigest() for p in o.rglob('*.zig')},indent=2))
(b/'input-sha256.txt').write_text(hashlib.sha256((t/'origin-final-demand-native/law3-initial.json').read_bytes()).hexdigest()+'\n')

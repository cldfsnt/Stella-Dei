from pathlib import Path
import shutil,json,hashlib
r=Path(__file__).resolve().parents[2];o=r.parent/'site-tmp/wasm-wind-screen';o.mkdir(exist_ok=True)
base=(r.parent/'site-tmp/wasm-land-screen/baseline/src/qa_wasm_land.zig').read_text()
for arm in ['baseline','candidate']:
 d=o/arm/'src';assert not d.exists();shutil.copytree(r/'src' if arm=='baseline' else r.parent/'site-tmp/wind-dispersal/src',d)
 s=base.replace('std.debug.print("LAYOUT plant={d} planet={d} cells={d}\\n",.{@sizeOf(S.Plant),@sizeOf(P),n});','std.debug.print("LAYOUT plant={d} planet={d} cells={d} cohort={d} cell={d} microbe_bytes={d}\\n",.{@sizeOf(S.Plant),@sizeOf(P),n,@sizeOf(S.Microbes.Cohort),@sizeOf(S.Microbes.Cell),p.microbeCells.len*@sizeOf(S.Microbes.Cell)});')
 if arm=='candidate':
  s=s.replace(' p.sandboxDefense=saved.sandbox_defense orelse .{};',' p.sandboxDefense=saved.sandbox_defense orelse .{};\n if(saved.wind_dispersal)|w|p.windDispersal=.{.enabled=w.enabled,.law=w.law,.stream_seed=w.stream_seed,.serial=w.serial};')
  s=s.replace(' saved.version=S.VERSION;', ' saved.version=if(p.windDispersal.enabled) S.WIND_VERSION else S.VERSION; saved.wind_dispersal=if(p.windDispersal.enabled).{.enabled=true,.law=p.windDispersal.law,.stream_seed=p.windDispersal.stream_seed,.serial=p.windDispersal.serial} else null;')
  s=s.replace(' try saved.validate();output=', ' std.debug.print("WIND_FINAL enabled={} serial={}\\n",.{p.windDispersal.enabled,p.windDispersal.serial});\n try saved.validate();output=')
 (d/'qa_wasm_wind.zig').write_text(s)
 p=d/'simulation/planet.zig';p.write_text('pub var qa_stages:[4]f64=.{0,0,0,0};\npub var qa_substages:[5]f64=.{0,0,0,0,0};\n'+p.read_text())
 (o/arm/'source-hashes.json').write_text(json.dumps({str(p.relative_to(d)):hashlib.sha256(p.read_bytes()).hexdigest()for p in d.rglob('*.zig')},indent=2))
shutil.copyfile(r.parent/'site-tmp/wasm-planet-profile/graph.json',o/'graph.json')
source=r.parent/'site-tmp/wind-bulk/pioneer-day3.json';shutil.copyfile(source,o/'pioneer-day3.json')
x=json.loads(source.read_text());x.pop('wind_dispersal');x['version']=7
for c in x['origin']['cells']:
 for co in c.get('cohorts',[])or []:co.pop('aerial_allocation',None)
 for e in c.get('sparse',[])or []:e['value'].pop('aerial_allocation',None)
(o/'pioneer-day3-projected-legacy.json').write_text(json.dumps(x,separators=(',',':')))

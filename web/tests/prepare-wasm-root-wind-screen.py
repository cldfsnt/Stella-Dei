from pathlib import Path
import shutil,json,hashlib
r=Path(__file__).resolve().parents[2];tmp=r.parent/'site-tmp';o=tmp/'wasm-root-wind-screen';assert not o.exists();o.mkdir()
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
base=(tmp/'law3-canonical/candidate/src/qa_wasm_land.zig').read_text()
for arm,source in [('baseline',tmp/'rooted-hardy-ui/src'),('candidate',tmp/'root-wind-combined/src')]:
 d=o/arm/'src';shutil.copytree(source,d)
 s=base
 if arm=='candidate':
  needle=' p.sandboxDefense=saved.sandbox_defense orelse .{};';assert s.count(needle)==1
  s=s.replace(needle,needle+'\n if(saved.wind_dispersal)|w|p.windDispersal=.{.enabled=w.enabled,.law=w.law,.stream_seed=w.stream_seed,.serial=w.serial};')
  needle=' try saved.validate();output=';assert s.count(needle)==1
  s=s.replace(needle,' if(p.windDispersal.enabled){saved.version=S.COMBINED_VERSION;saved.wind_dispersal=.{.enabled=true,.law=p.windDispersal.law,.stream_seed=p.windDispersal.stream_seed,.serial=p.windDispersal.serial};}else saved.wind_dispersal=null;\n std.debug.print("WIND_FINAL enabled={} serial={}\\n",.{p.windDispersal.enabled,p.windDispersal.serial});\n'+needle)
 s=s.replace('const elapsed=emscripten_get_now()-begin;','const elapsed=emscripten_get_now()-begin;\n std.debug.print("CELL_LAYOUT cohort={} cell={} cell_array={}\\n",.{@sizeOf(S.Microbes.Cohort),@sizeOf(S.Microbes.Cell),p.microbeCells.len*@sizeOf(S.Microbes.Cell)});')
 (d/'qa_wasm_land.zig').write_text(s)
 p=d/'simulation/planet.zig';p.write_text('pub var qa_stages:[4]f64=.{0,0,0,0};\npub var qa_substages:[5]f64=.{0,0,0,0,0};\n'+p.read_text())
 (o/arm/'source-hashes.json').write_text(json.dumps({str(p.relative_to(d)):sha(p)for p in d.rglob('*')if p.is_file()},indent=2)+'\n')
shutil.copy2(tmp/'wasm-planet-profile/graph.json',o/'graph.json')
shutil.copy2(tmp/'wetlands-day21/day-21.json',o/'historical.json')
shutil.copy2(tmp/'root-wind-native/fresh.json',o/'fresh.json');assert sha(o/'fresh.json')=='3b2a508b4e1c37ab6165dd1917ea54ebca4d502643e598964dd843942af451bd'
x=json.loads((o/'fresh.json').read_text());x['version']=10;x.pop('wind_dispersal')
for c in x['origin']['cells']:
 for co in c.get('cohorts',[])or []:co.pop('aerial_allocation',None)
 for entry in c.get('sparse',[])or []:entry['value'].pop('aerial_allocation',None)
(o/'fresh-projected-off.json').write_text(json.dumps(x,separators=(',',':')))
def census(p):
 x=json.loads(p.read_text());cs=[];occupied=0
 for c in x['origin']['cells']:
  live=[v for v in (c.get('cohorts') or [v['value'] for v in c.get('sparse',[])])if v['biomass']>0]
  occupied+=bool(live);cs+=live
 return {'sha256':sha(p),'bytes':p.stat().st_size,'cells':len(x['water']),'occupied':occupied,'living':len(cs),'root_positive':sum(c.get('root_fraction',0)>0 for c in cs),'aerial_positive':sum(c.get('aerial_allocation',0)>0 for c in cs),'game_time':x['game_time']}
(o/'inputs.json').write_text(json.dumps({n:census(o/n)for n in ['historical.json','fresh.json','fresh-projected-off.json']},indent=2)+'\n')
print((o/'inputs.json').read_text())

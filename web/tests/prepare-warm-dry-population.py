from pathlib import Path
import shutil,json,hashlib
r=Path(__file__).resolve().parents[2];t=r.parent/'site-tmp';src=t/'protective-journey/src';b=t/'warm-dry-population';o=b/'src'
assert not o.exists()
expected=json.loads((r/'web/tests/continuation-review/protective-natural-journey/source-hashes.json').read_text())
for n,h in expected.items():assert hashlib.sha256((src/n).read_bytes()).hexdigest()==h,n
shutil.copytree(src,o)
(o/'simulation/population_audit.zig').write_text('''const std=@import("std");pub var candidate=false;pub var enabled=true;
pub fn emit(comptime tag:[]const u8,c:anytype,v:anytype)void{if(!enabled or c.root_fraction<=0 or c.support_mass<=0)return;var b:[8192]u8=undefined;var s=std.io.fixedBufferStream(&b);std.json.stringify(.{.tick=@import("shore_audit.zig").tick,.id=c.lineage,.data=v},.{},s.writer()) catch unreachable;std.debug.print("POP_"++tag++" {s}\\n",.{b[0..s.pos]});}
''')
p=o/'simulation/microbes.zig';s=p.read_text()
def replace(a,b):
 global s
 assert s.count(a)==1,(a,s.count(a));s=s.replace(a,b)
replace('const dry_mortality=4*(1-0.85*c.structure)+0.10*c.structure;','const dry_rate:f32=if(@import("population_audit.zig").candidate and env.temperature>273.15 and env.temperature<355) 1 else 4;const dry_mortality=dry_rate*(1-0.85*c.structure)+0.10*c.structure;')
replace('        const wanted_upkeep=@min(c.biomass,supportMaintenancePerDay(c.*)*days*support_scale);','        @import("population_audit.zig").emit("ENTRY",c.*,.{.cohort=c.*,.temperature=env.temperature,.depth=env.depth_km,.light=light,.available=available,.nutrient=cell.nutrient});\n        const wanted_upkeep=@min(c.biomass,supportMaintenancePerDay(c.*)*days*support_scale);')
replace('        const fitness=thermalFitness(env.temperature,c.optimum);\n        const dry=', '        @import("population_audit.zig").emit("UPKEEP",c.*,.{.paid=upkeep,.remaining=c.biomass});\n        const fitness=thermalFitness(env.temperature,c.optimum);\n        const dry=')
replace('        // Below 25% of one propagule','        @import("population_audit.zig").emit("MORTALITY",c.*,.{.dead=dead,.remaining=c.biomass,.hazard=hazard,.h=hydrated,.immersion=immersion,.fitness=fitness,.exposed=exposed,.cleanup=c.biomass<0.0025});\n        // Below 25% of one propagule')
replace('        c.support_mass=@min(c.biomass,boundedAdd(c.support_mass,@as(f64,share)*c.organization));','        @import("population_audit.zig").emit("GROWTH",c.*,.{.growth=share,.remaining=c.biomass,.potential=potentials[i]});\n        c.support_mass=@min(c.biomass,boundedAdd(c.support_mass,@as(f64,share)*c.organization));')
p.write_text(s)
p=o/'main.zig';s=p.read_text().replace(str(t/'protective-journey'),str(b))
a='A.enabled=std.posix.getenv("QA_OFF")==null;';assert s.count(a)==1;s=s.replace(a,a+'@import("simulation/population_audit.zig").enabled=A.enabled;@import("simulation/population_audit.zig").candidate=std.posix.getenv("QA_CANDIDATE")!=null;')
a='qaEmit("BIRTH_OR_INITIAL",.{.tick=tick,.point=p,.cohort=c});';assert s.count(a)==1;s=s.replace(a,'qaEmit("BIRTH_OR_INITIAL",.{.tick=tick,.point=p,.cohort=c,.temperature=s.planet.temperature[p],.depth_m=s.planet.waterMass[p]*s.planet.getKmPerWaterMass()*1000});')
a='    const point = state.selectedPoint;'
# Read-only endpoint census, separate from actual per-interval root traces.
a='fn qaCensus(a:std.mem.Allocator,s:*PlayState,seen:*std.AutoHashMap(u64,QaSeen),tick:usize,points:[]const usize)!void{'
assert s.count(a)==1
s=s.replace(a,a+'qaHabitat(s,tick);')
s+='\nfn qaHabitat(s:*PlayState,tick:usize)void{var counts:[3]usize=.{0,0,0};var mass:[3]f64=.{0,0,0};var occupied:[3]usize=.{0,0,0};var roots:[3]usize=.{0,0,0};for(s.planet.microbeCells,0..)|cell,p|{const depth=s.planet.waterMass[p]*s.planet.getKmPerWaterMass();const h:usize=if(depth==0)0 else if(depth<0.0002)1 else 2;var any=false;for(cell.cohorts)|c|{if(c.biomass<=0)continue;any=true;counts[h]+=1;mass[h]+=c.biomass;if(c.root_fraction>0 and c.support_mass>0)roots[h]+=1;}if(any)occupied[h]+=1;}qaEmit("HABITAT",.{.tick=tick,.counts=counts,.biomass_density_sum=mass,.occupied=occupied,.supported_roots=roots});}\n'
p.write_text(s)
for path in o.rglob('*.zig'):
 text=path.read_text();path.write_text(text.replace(str(t/'protective-journey'),str(b)))
(b/'source-hashes.json').write_text(json.dumps({str(p.relative_to(o)):hashlib.sha256(p.read_bytes()).hexdigest()for p in o.rglob('*.zig')},indent=2)+'\n')
(b/'source-changes.json').write_text(json.dumps({n:{'before':h,'after':hashlib.sha256((o/n).read_bytes()).hexdigest()}for n,h in expected.items()if hashlib.sha256((o/n).read_bytes()).hexdigest()!=h},indent=2)+'\n')
print(b)

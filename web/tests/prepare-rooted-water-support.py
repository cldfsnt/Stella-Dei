from pathlib import Path
import shutil,hashlib,json
r=Path(__file__).resolve().parents[2];t=r.parent/'site-tmp';o=t/'root-water-preview/src';assert not o.exists();shutil.copytree(t/'root-wind-recovery/src',o);shutil.copy2(r/'web/tests/rooted-water-support.zig',o/'rooted_water_support.zig')
p=o/'rooted_founder.zig';s=p.read_text();s=s.replace('pub const Receipt=struct{','pub const Receipt=struct{water_support:?@import("rooted_water_support.zig").Estimate=null,',1)
s=s.replace('pub const Snapshot=struct{','pub const Snapshot=struct{vapor:f64,rain:f32,wind_config:@import("simulation/wind_genetics.zig").Config,',1)
s=s.replace('return .{.epoch=epoch,','return .{.vapor=p.landVapor[index],.rain=p.rainfall[index],.wind_config=p.windDispersal,.epoch=epoch,',1)
s+='''
/// Current local 24min reference; no world update or future climate prediction.
pub fn waterSupport(p:anytype,index:usize,r:Receipt,surface:f32)?@import("rooted_water_support.zig").Estimate{
 if(!std.math.isFinite(surface) or surface<0 or surface>2 or index>=p.landVapor.len or index>=p.rainfall.len)return null;
 var cell: M.Cell=undefined;
 if(r.status==.eligible){const staged=forPlanet(p,index) orelse return null;if(staged.receipt.status!=.eligible or staged.receipt.lineage!=r.lineage)return null;cell=staged.cell;}else if(r.status==.planted){if(index>=p.microbeCells.len)return null;cell=p.microbeCells[index];}else return null;
 var slot:?usize=null;for(&cell.cohorts,0..)|*c,i|if(c.lineage==r.lineage and c.biomass>0){slot=i;if(r.status==.eligible)c.structure=r.structure;break;};const which=slot orelse return null;
 const temp=p.temperature[index];if(!std.math.isFinite(temp) or temp<=0)return null;
 const saturation=@as(f64,@TypeOf(p.*).getEquilibriumVaporPressure(temp))*p.getSubstanceDivider()/(@as(f64,temp)*1.380649e-23);
 return @import("rooted_water_support.zig").evaluate(cell,which,.{.liquid=p.waterMass[index],.vapor=p.landVapor[index],.soil=p.landSoil[index],.rain=p.rainfall[index]},p.getMeanPointArea(),p.getKmPerWaterMass(),saturation,.{.temperature=temp,.depth_km=p.waterMass[index]*p.getKmPerWaterMass(),.light=surface,.carbon_available=0,.oxygen_carbon_capacity=0});
}
''';p.write_text(s)
p=o/'main.zig';s=p.read_text();needle='receipt.conditions=R.currentConditions(receipt,state.planet.temperature[point],@import("simulation/microbes.zig").availableLight(surface,depth));';assert needle in s;s=s.replace(needle,needle+'\n   receipt.water_support=R.waterSupport(&state.planet,point,receipt,surface);',1)
# Both receipt construction and success use the same explicit field.
needle='.conditions=receipt.conditions';assert needle in s;s=s.replace(needle,'.water_support=receipt.water_support,'+needle,1);p.write_text(s)
e=r/'web/tests/continuation-review/rooted-water-support';e.mkdir(exist_ok=True);(e/'source-hashes.json').write_text(json.dumps({str(p.relative_to(o)):hashlib.sha256(p.read_bytes()).hexdigest()for p in o.rglob('*.zig')},indent=2)+'\n')

p=o/"rooted_founder.zig";p.write_text(p.read_text().replace("index>=p.landSoil.len)return null;","index>=p.landSoil.len or index>=p.landVapor.len or index>=p.rainfall.len)return null;"))

(e/"source-hashes.json").write_text(json.dumps({str(p.relative_to(o)):hashlib.sha256(p.read_bytes()).hexdigest()for p in o.rglob("*.zig")},indent=2)+"\n")

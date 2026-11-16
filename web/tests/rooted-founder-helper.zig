//! Explicit chosen founder genetics, not evolved ancestry or new physiology.
const std=@import("std");const M=@import("simulation/microbes.zig");
pub const Status=enum{eligible,planted,disabled,invalid,stale,busy,too_cold,too_hot,too_deep,no_soil,no_space,no_nutrients,no_carbon,unrepresentable};
pub const Receipt=struct{status:Status,conditions:?Conditions=null,carbon_kg_m2:f32=0,nitrogen_kg_m2:f64=0,carbon_source_kg:f64=0,carbon_rounding_kg:f64=0,support_kg_c_m2:f32=0,root_kg_c_m2:f32=0,root_fraction:f32=0.5,organization:f32=0.25,soil_kg_m2:f64=0,depth_m:f64=0,lineage:u64=0};
const Plan=struct{receipt:Receipt,cell:M.Cell,stats:M.Stats,co2:f64,oxygen:f64};
pub fn stage(cell:M.Cell,stats:M.Stats,co2:f64,oxygen:f64,area:f64,count:usize,depth:f32,temp:f32,soil:f64)Plan{
 var p=Plan{.receipt=.{.status=.invalid},.cell=cell,.stats=stats,.co2=co2,.oxygen=oxygen};
 if(!std.math.isFinite(soil) or soil<0 or soil>1 or !std.math.isFinite(depth) or depth<0 or !std.math.isFinite(temp) or !std.math.isFinite(co2) or co2<0 or !std.math.isFinite(oxygen) or oxygen<0 or !std.math.isFinite(area) or area<=0 or count==0 or !M.validCell(cell,stats.next_lineage) or stats.next_lineage==0 or stats.next_lineage>=1_000_000_000_000_000)return p;
 p.receipt.soil_kg_m2=soil;p.receipt.depth_m=@as(f64,depth)*1000;
 if(temp<=273.15){p.receipt.status=.too_cold;return p;}if(temp>=355){p.receipt.status=.too_hot;return p;}if(depth>0.05){p.receipt.status=.too_deep;return p;}if(depth<0.0002 and soil<=0){p.receipt.status=.no_soil;return p;}
 var empty:?usize=null;for(cell.cohorts,0..)|c,i|if(c.biomass==0){empty=i;break;};if(empty==null){p.receipt.status=.no_space;return p;}if(cell.nutrient<=0){p.receipt.status=.no_nutrients;return p;}
 const available=co2*1e9/area*(12.0/44.0);if(!std.math.isFinite(available) or available<=0 or available>std.math.floatMax(f32)){p.receipt.status=.no_carbon;return p;}
 const fixed=M.seed(&p.cell,&p.stats,@floatCast(available));if(fixed<=0){p.receipt.status=.unrepresentable;return p;}
 if(@as(f64,M.biomass(cell))+fixed>1){p.receipt.status=.no_space;return p;}
 const required_n=@as(f64,fixed)*@as(f64,M.nutrient_per_carbon);
 if(@as(f64,cell.nutrient)-p.cell.nutrient<required_n and p.cell.nutrient>0)p.cell.nutrient=std.math.nextAfter(f32,p.cell.nutrient,0);
 const n=@as(f64,cell.nutrient)-p.cell.nutrient;if(n<required_n or n<=0 or !std.math.isFinite(n)){p.receipt.status=.unrepresentable;return p;}
 const scale=area/1e9/@as(f64,@floatFromInt(count));p.co2=@max(0,co2-@as(f64,fixed)*scale*(44.0/12.0));p.oxygen=@max(0,oxygen+@as(f64,fixed)*scale*(32.0/12.0));p.stats.fixed_carbon+=@as(f64,fixed)*area;
 const gas_scale=1e9*@as(f64,@floatFromInt(count))*(12.0/44.0);
 if((co2-p.co2)*gas_scale<@as(f64,fixed)*area and p.co2>0)p.co2=std.math.nextAfter(f64,p.co2,0);
 if(!std.math.isFinite(p.co2) or !std.math.isFinite(p.oxygen) or !std.math.isFinite(p.stats.fixed_carbon) or p.co2>=co2 or (co2-p.co2)*gas_scale<@as(f64,fixed)*area){p.receipt.status=.unrepresentable;return p;}
 const c=&p.cell.cohorts[empty.?];c.root_fraction=0.5;c.organization=0.25;c.support_mass=0.25*fixed;
 if(!M.validCell(p.cell,p.stats.next_lineage)){p.receipt.status=.invalid;return p;}
 p.receipt=.{ .status=.eligible,.carbon_kg_m2=fixed,.nitrogen_kg_m2=n,.carbon_source_kg=(co2-p.co2)*gas_scale,.carbon_rounding_kg=(co2-p.co2)*gas_scale-@as(f64,fixed)*area,.support_kg_c_m2=c.support_mass,.root_kg_c_m2=c.support_mass*c.root_fraction,.soil_kg_m2=soil,.depth_m=@as(f64,depth)*1000,.lineage=c.lineage};return p;
}
fn forPlanet(p:anytype,index:usize)?Plan{
 if(p.worldMode!=.origin or !p.landBeta.enabled or p.landBeta.physiology_law!=3 or !p.landBeta.valid())return null;
 if(index>=p.microbeCells.len or index>=p.waterMass.len or index>=p.temperature.len or index>=p.landSoil.len)return null;
 return stage(p.microbeCells[index],p.microbeStats,p.averageCarbonDioxideMass,p.averageOxygenMass,p.getMeanPointArea(),p.vertices.len,p.waterMass[index]*p.getKmPerWaterMass(),p.temperature[index],p.landSoil[index]);
}
pub fn preview(p:anytype,index:usize)Receipt{return if(forPlanet(p,index))|s|s.receipt else .{.status=.disabled};}
pub fn apply(p:anytype,index:usize)Receipt{
 var s=forPlanet(p,index) orelse return .{.status=.disabled};if(s.receipt.status!=.eligible)return s.receipt;
 p.microbeCells[index]=s.cell;p.microbeStats=s.stats;p.averageCarbonDioxideMass=s.co2;p.averageOxygenMass=s.oxygen;s.receipt.status=.planted;return s.receipt;
}
test "chosen tissue is paid subset and seed counters RNG preserve ordinary semantics"{
 const c=M.initialized(42);const stats=M.Stats{};const p=stage(c,stats,1,1,1000,12,0,303,0.5);try std.testing.expectEqual(Status.eligible,p.receipt.status);const child=p.cell.cohorts[0];try std.testing.expectEqual(@as(f32,0.02),child.biomass);try std.testing.expectEqual(child.biomass*0.25,child.support_mass);try std.testing.expectEqual(child.support_mass*0.5,p.receipt.root_kg_c_m2);try std.testing.expectEqual(@as(u64,0),p.stats.births);try std.testing.expectEqual(@as(u64,2),p.stats.next_lineage);try std.testing.expectEqual(c.rng,p.cell.rng);try std.testing.expect(p.co2<1 and p.oxygen>1);try std.testing.expectEqual(@as(f32,0),child.reproduction_credit);try std.testing.expectEqual(@as(u32,0),child.generation);try std.testing.expectEqual(@as(u64,0),child.parent);
 var ordinary=c;var os=stats;_=M.seed(&ordinary,&os,1);var compare=p.cell;compare.cohorts[0].root_fraction=0;compare.cohorts[0].organization=0;compare.cohorts[0].support_mass=0;try std.testing.expectEqualDeep(ordinary.cohorts,compare.cohorts);try std.testing.expect(compare.nutrient<=ordinary.nutrient);
 var limited=c;limited.nutrient=0.0001;const partial=stage(limited,stats,1,1,1000,12,0,303,0.5);try std.testing.expectEqual(Status.eligible,partial.receipt.status);try std.testing.expect(partial.receipt.carbon_kg_m2<0.02 and partial.receipt.carbon_kg_m2>0);
}
test "dry soil temperature slots and nonfinite refuse before any commit"{
 const c=M.initialized(42);const s=M.Stats{};try std.testing.expectEqual(Status.no_soil,stage(c,s,1,1,1000,12,0,303,0).receipt.status);try std.testing.expectEqual(Status.too_cold,stage(c,s,1,1,1000,12,0,273.15,1).receipt.status);try std.testing.expectEqual(Status.too_hot,stage(c,s,1,1,1000,12,0,355,1).receipt.status);try std.testing.expectEqual(Status.invalid,stage(c,s,1,1,1000,12,0,303,std.math.nan(f64)).receipt.status);try std.testing.expectEqual(Status.eligible,stage(c,s,1,1,1000,12,0.0002,303,0).receipt.status);
 var full=c;for(&full.cohorts,0..)|*co,i|{co.*=.{.biomass=0.1,.lineage=i+1};}try std.testing.expectEqual(Status.no_space,stage(full,.{.next_lineage=5},1,1,1000,12,0,303,1).receipt.status);
}

pub var epoch:u64=0;
pub fn invalidate()void{epoch+|=1;}
pub const Snapshot=struct{epoch:u64,cell:M.Cell,stats:M.Stats,co2:f64,oxygen:f64,area:f64,count:usize,water:f32,conversion:f32,temperature:f32,soil:f64,config:@import("simulation/land_beta.zig").Config};
pub fn snapshot(p:anytype,index:usize)?Snapshot{
 if(p.worldMode!=.origin or !p.landBeta.enabled or p.landBeta.physiology_law!=3 or index>=p.microbeCells.len or index>=p.waterMass.len or index>=p.temperature.len or index>=p.landSoil.len)return null;
 return .{.epoch=epoch,.cell=p.microbeCells[index],.stats=p.microbeStats,.co2=p.averageCarbonDioxideMass,.oxygen=p.averageOxygenMass,.area=p.getMeanPointArea(),.count=p.vertices.len,.water=p.waterMass[index],.conversion=p.getKmPerWaterMass(),.temperature=p.temperature[index],.soil=p.landSoil[index],.config=p.landBeta};
}

/// Current prospective founder environment, not a forecast or uptake receipt.
pub const Conditions=struct{temperature_k:f32,optimum_k:f32=303,biological_light:f32,body_height_m:f64,submerged:bool};
pub fn currentConditions(r:Receipt,temp:f32,light:f32)?Conditions{
 if((r.status!=.eligible and r.status!=.planted) or !std.math.isFinite(temp) or !std.math.isFinite(light) or light<0 or light>2 or !std.math.isFinite(r.depth_m) or r.depth_m<0)return null;
 const c=M.Cohort{.biomass=r.carbon_kg_m2,.support_mass=r.support_kg_c_m2,.root_fraction=r.root_fraction,.organization=r.organization};
 const height=@import("simulation/basal_geometry.zig").height(c.biomass,M.producerHeightMeters(c),100) orelse return null;
 return .{.temperature_k=temp,.biological_light=light,.body_height_m=height,.submerged=r.depth_m>=height};
}
test "current conditions use paid founder geometry and reject unavailable light"{
 const r=stage(M.initialized(42),.{},1,1,1000,12,0,303,1).receipt;
 const c=currentConditions(r,290,0).?;try std.testing.expect(!c.submerged);try std.testing.expectEqual(@as(f32,0),c.biological_light);try std.testing.expect(c.body_height_m>0);
 var wet=r;wet.depth_m=c.body_height_m;try std.testing.expect(currentConditions(wet,290,1).?.submerged);
 try std.testing.expect(currentConditions(r,290,std.math.nan(f32))==null);try std.testing.expect(currentConditions(r,std.math.inf(f32),1)==null);try std.testing.expect(currentConditions(r,290,3)==null);try std.testing.expect(currentConditions(.{.status=.disabled},290,1)==null);
}

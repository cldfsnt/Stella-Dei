const std=@import("std");const M=@import("experimental/soil_physiology_core.zig");
const Fixture=struct{cell:M.Cell,surface:f64,vapor:f64};
fn carbon(c:M.Cell)f64{var t:f64=c.detritus;for(c.cohorts)|x|t+=x.biomass;return t;}
fn nitrogen(c:M.Cell)f64{var t:f64=c.nutrient;for(c.cohorts)|x|t+=@as(f64,x.biomass)*M.nutrient_per_carbon;return t;}
fn run(pair:usize,swap:bool,idswap:bool,dt:f32)!void{
 const a=std.testing.allocator;const f=try std.json.parseFromSlice(Fixture,a,@embedFile("experimental/soil_physiology_fixture.json"),.{});defer f.deinit();
 const original=f.value.cell;const donor=original.cohorts[1];try std.testing.expect(donor.lineage==478);
 var cell=original;cell.cohorts=.{.{},.{},.{},.{}};var half=donor;half.biomass/=2;half.support_mass/=2;half.reproduction_credit/=2;half.lifetime_grazed/=2;
 const sa:usize=if(swap)3 else 0;const sb:usize=if(swap)0 else 3;cell.cohorts[sa]=half;cell.cohorts[sb]=half;cell.cohorts[sa].lineage=if(idswap)9002 else 9001;cell.cohorts[sb].lineage=if(idswap)9001 else 9002;
 cell.cohorts[sa].root_fraction=if(pair==2)0.25 else 0;cell.cohorts[sb].root_fraction=if(pair==1)0 else 0.25;
 try std.testing.expectEqual(carbon(original),carbon(cell));try std.testing.expectEqual(nitrogen(original),nitrogen(cell));try std.testing.expectEqual(@as(f64,donor.support_mass),@as(f64,half.support_mass)*2);try std.testing.expectEqual(@as(f64,donor.reproduction_credit),@as(f64,half.reproduction_credit)*2);try std.testing.expectEqual(@as(f64,donor.lifetime_grazed),@as(f64,half.lifetime_grazed)*2);try std.testing.expectEqual(original.rng,cell.rng);
 const depth:f32=@floatCast(f.value.surface/1e6);try std.testing.expect(depth>=0.0002);const initial_light=M.producerLightShares(cell,1,depth);if(pair!=0)try std.testing.expectEqual(initial_light[sa],initial_light[sb]);
 var co2:f64=1;var oxygen:f64=1;const c0=carbon(cell)+co2;const n0=nitrogen(cell);const w0=f.value.surface+f.value.vapor+M.waterTotal(cell);var maxc:f64=0;var maxn:f64=0;var maxw:f64=0;var light=[_]f64{0,0};var fixed:f64=0;var recycled:f64=0;var grazed:f64=0;var death=[_]i64{-1,-1};const perday:usize=@intFromFloat(86400/dt);
 for(0..7*perday)|tick|{
  const shares=M.producerLightShares(cell,1,depth);light[0]+=shares[sa]*@as(f64,dt);light[1]+=shares[sb]*@as(f64,dt);
  const flux=M.step(&cell,.{.temperature=300,.depth_km=depth,.light=1,.carbon_available=@floatCast(co2),.oxygen_carbon_capacity=@floatCast(oxygen)},dt);
  co2+=@as(f64,flux.recycled)-flux.fixed;oxygen+=@as(f64,flux.fixed)-flux.recycled;fixed+=flux.fixed;recycled+=flux.recycled;grazed+=flux.grazed;
  try std.testing.expect(std.math.isFinite(co2) and co2>=0 and std.math.isFinite(oxygen) and oxygen>=0);try std.testing.expect(M.validCell(cell,10000));try std.testing.expectEqual(original.rng,cell.rng);
  maxc=@max(maxc,@abs(carbon(cell)+co2-c0));maxn=@max(maxn,@abs(nitrogen(cell)-n0));maxw=@max(maxw,@abs(f.value.surface+f.value.vapor+M.waterTotal(cell)-w0));try std.testing.expect(maxc<=1e-4 and maxn<=1e-4 and maxw<=1e-9);
  for([_]usize{sa,sb},0..)|slot,i|if(death[i]<0 and cell.cohorts[slot].biomass==0){death[i]=@intCast(tick+1);};
  if((tick+1)%perday==0){const ca=cell.cohorts[sa];const cb=cell.cohorts[sb];const total=@as(f64,ca.biomass)+cb.biomass;const line=try std.json.stringifyAlloc(a,.{.pair=pair,.slot_swap=swap,.id_swap=idswap,.dt=dt,.day=(tick+1)/perday,.a=ca,.b=cb,.a_share=if(total>0)@as(f64,ca.biomass)/total else 0,.initial_light=.{initial_light[sa],initial_light[sb]},.light_integral=light,.canopy=.{M.abovegroundSupport(ca),M.abovegroundSupport(cb)},.fronds=.{M.frondMass(ca),M.frondMass(cb)},.death_tick=death,.fixed=fixed,.recycled=recycled,.grazed=grazed,.co2=co2,.oxygen=oxygen,.nutrient=cell.nutrient,.detritus=cell.detritus,.max_carbon_residual=maxc,.max_nitrogen_residual=maxn,.max_water_residual=maxw},.{});defer a.free(line);std.debug.print("WET_COMPETITION {s}\n",.{line});}
 }
}
test "fixed wet paired competition matrix no required winner"{for(0..3)|pair|for([_]bool{false,true})|swap|for([_]bool{false,true})|idswap|for([_]f32{1440,720,360})|dt|try run(pair,swap,idswap,dt);}

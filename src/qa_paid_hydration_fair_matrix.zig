const std=@import("std");
const H=@import("experimental/paid_hydration_fair.zig");const P=@import("simulation/microbes.zig");
fn donor() H.M.Cohort{return .{.biomass=0.12940502166748047,.organization=0.13426367938518524,.support_mass=0.017374489456415176,.optimum=296.1463928222656,.efficiency=1.0451198816299438,.structure=0.13595879077911377,.feeding=0.20643378794193268,.mobility=0.0,.relocations=0,.last_from=0,.last_to=0,.last_move_time=0.0,.lifetime_grazed=0.047025907784700394,.generation=6,.lineage=478,.parent=232,.reproduction_credit=0.005128047429025173};}
fn wetAt(mode:usize,day:f64)bool{return switch(mode){0=>true,1=>day<1,2=>day<1 or day>=4,else=>false};}
fn budget(s:*const H.State,w0:f64,c0:f64,n0:f64)!void{
 const w=s.totalWater();try std.testing.expect(@abs(w-w0)<=@max(1e-9,64*std.math.floatEps(f64)*@max(w,w0)));
 try std.testing.expect(@abs(s.totalCarbon()-c0)<=1e-4);try std.testing.expect(@abs(s.totalN()-n0)<=1e-4);
 try std.testing.expect(H.M.validCell(s.cell,100000));for(s.retained,0..)|v,i|try std.testing.expect(std.math.isFinite(v) and v>=0 and v<=H.capacity(s.cell.cohorts[i]));
}
test "fixed eight hydration conditions and timestep controls"{
 for([_]f32{3600,1800})|dt|{for(0..4)|mode|{for([_]f32{0,0.25})|r|{
  var s:H.State=.{};s.cell.cohorts[0]=donor();s.cell.cohorts[0].qa_retention=r;s.liquid=@floatCast(1000*H.area/1e9);
  const w0=s.totalWater();const c0=s.totalCarbon();const n0=s.totalN();var maxw:f64=0;var maxc:f64=0;var maxn:f64=0;
  const ticks:usize=@intFromFloat(7*86400/dt);
  for(0..ticks)|tick|{const time=@as(f64,@floatFromInt(tick))*dt;const light:f32=if(@mod(time,86400)<43200)1 else 0;_=s.step(dt,light,wetAt(mode,time/86400));try budget(&s,w0,c0,n0);maxw=@max(maxw,@abs(s.totalWater()-w0));maxc=@max(maxc,@abs(s.totalCarbon()-c0));maxn=@max(maxn,@abs(s.totalN()-n0));
   if((tick+1)%@as(usize,@intFromFloat(86400/dt))==0)std.debug.print("HYDRATION {s}\n",.{try std.json.stringifyAlloc(std.heap.page_allocator,.{.dt=dt,.mode=mode,.r=r,.day=@as(f64,@floatFromInt(tick+1))*dt/86400,.mass=s.cell.cohorts[0].biomass,.support=s.cell.cohorts[0].support_mass,.retained=s.retained[0],.capacity=H.capacity(s.cell.cohorts[0]),.uptake=s.uptake,.evaporated=s.evaporated,.returned=s.returned,.water_residual=s.totalWater()-w0,.max_water_residual=maxw,.max_carbon_residual=maxc,.max_nutrient_residual=maxn},.{})});
  }
 }}}
}
test "zero allocation follows unchanged production physiology"{
 var s:H.State=.{};s.cell.cohorts[0]=donor();s.liquid=@floatCast(1000*H.area/1e9);var p=P.initialized(7);inline for(std.meta.fields(P.Cohort))|field|@field(p.cohorts[0],field.name)=@field(s.cell.cohorts[0],field.name);
 var co2:f64=10;var oxygen:f64=10;
 for(0..168)|tick|{const light:f32=if(tick%24<12)1 else 0;const wet=wetAt(2,@as(f64,@floatFromInt(tick))/24);s.exposure(wet);const depth:f32=if(wet)@floatCast(@as(f64,s.liquid)*(1e9/H.area)/1e6) else 0;
  const f=P.step(&p,.{.temperature=300,.depth_km=depth,.light=light,.carbon_available=@floatCast(co2),.oxygen_carbon_capacity=@floatCast(oxygen)},3600);co2-=f.fixed;co2+=f.recycled;oxygen+=f.fixed;oxygen-=f.recycled;
  _=s.step(3600,light,wet);inline for(std.meta.fields(P.Cohort))|field|try std.testing.expectEqual(@field(p.cohorts[0],field.name),@field(s.cell.cohorts[0],field.name));try std.testing.expectEqual(p.nutrient,s.cell.nutrient);try std.testing.expectEqual(p.detritus,s.cell.detritus);try std.testing.expectEqual(co2,s.co2);try std.testing.expectEqual(@as(f64,0),s.retained[0]);
 }
}
test "zero support or zero water gives no free hydration"{for([_]bool{false,true})|support|{var s:H.State=.{};s.cell.cohorts[0]=donor();s.cell.cohorts[0].qa_retention=0.25;if(!support)s.cell.cohorts[0].support_mass=0;for(0..168)|_|{_=s.step(3600,1,false);try std.testing.expectEqual(@as(f64,0),s.retained[0]);}try std.testing.expectEqual(@as(f32,0),s.cell.cohorts[0].biomass);try std.testing.expectEqual(@as(f64,0),s.totalWater());}}
test "shared wet competition paid allocation slot reversal"{for(0..2)|swap|{var s:H.State=.{};s.liquid=@floatCast(1000*H.area/1e9);s.cell.cohorts[0]=donor();s.cell.cohorts[1]=donor();s.cell.cohorts[1].lineage=479;s.cell.cohorts[swap].qa_retention=0.25;const w0=s.totalWater();const c0=s.totalCarbon();const n0=s.totalN();for(0..168)|tick|{_=s.step(3600,if(tick%24<12)1 else 0,true);try budget(&s,w0,c0,n0);}std.debug.print("HYDRATION_SHARED swap={d} retention={d} no_retention={d}\n",.{swap,s.cell.cohorts[swap].biomass,s.cell.cohorts[1-swap].biomass});}}
test "fixed prolonged drought limit without replenishment"{for([_]f32{3600,1800})|dt|{var s:H.State=.{};s.cell.cohorts[0]=donor();s.cell.cohorts[0].qa_retention=0.25;s.liquid=@floatCast(1000*H.area/1e9);const w0=s.totalWater();const c0=s.totalCarbon();const n0=s.totalN();var first_absent:?f64=null;const ticks:usize=@intFromFloat(30*86400/dt);for(0..ticks)|tick|{const t=@as(f64,@floatFromInt(tick))*dt;try std.testing.expect(s.step(dt,if(@mod(t,86400)<43200)1 else 0,t<86400)!=null);try budget(&s,w0,c0,n0);if(first_absent==null and s.cell.cohorts[0].biomass==0)first_absent=(t+dt)/86400;}std.debug.print("HYDRATION_DROUGHT dt={d} first_absent={any} retained={d} liquid_return={d} vapor_escrow={d} water_residual={d}\n",.{dt,first_absent,s.retained[0],s.liquid_escrow,s.vapor_escrow,s.totalWater()-w0});try std.testing.expect(first_absent!=null and s.retained[0]==0);}}
test "capacity loss and death return actual retained water"{var s:H.State=.{};s.cell.cohorts[0]=donor();s.cell.cohorts[0].qa_retention=0.25;s.retained[0]=H.capacity(s.cell.cohorts[0]);const w=s.totalWater();s.cell.cohorts[0].support_mass*=0.5;s.settle();try std.testing.expect(s.retained[0]<=H.capacity(s.cell.cohorts[0]));try std.testing.expect(@abs(s.totalWater()-w)<1e-12);s.cell.cohorts[0]=.{};s.settle();try std.testing.expectEqual(@as(f64,0),s.retained[0]);try std.testing.expect(@abs(s.totalWater()-w)<1e-12);}
test "invalid wrapper parameters refuse before material changes"{var s:H.State=.{};s.cell.cohorts[0]=donor();const before=s;try std.testing.expect(s.step(0,1,true)==null);try std.testing.expect(s.step(3600,std.math.nan(f32),true)==null);try std.testing.expectEqualDeep(before,s);s.cell.cohorts[0].qa_retention=2;const invalid=s;try std.testing.expect(s.step(3600,1,true)==null);try std.testing.expectEqualDeep(invalid,s);}
test "scarce water allocates to both demands without creating water"{
 for(0..2)|swap|{var s:H.State=.{};s.cell.cohorts[0]=donor();s.cell.cohorts[1]=donor();s.cell.cohorts[1].lineage=479;s.cell.cohorts[swap].qa_retention=0.25;s.cell.cohorts[1-swap].qa_retention=0.125;
 s.liquid=@floatCast(H.capacity(s.cell.cohorts[swap])*0.5*H.area/1e9);const w=s.totalWater();const c=s.totalCarbon();const n=s.totalN();try std.testing.expect(s.step(1800,0,true)!=null);try budget(&s,w,c,n);
 std.debug.print("HYDRATION_SCARCE swap={d} initial_water={d} high_retained={d} low_retained={d} uptake={d} water_residual={d}\n",.{swap,w,s.retained[swap],s.retained[1-swap],s.uptake,s.totalWater()-w});
 try std.testing.expect(s.uptake<=w);try std.testing.expect(s.retained[swap]>s.retained[1-swap] and s.retained[1-swap]>0);
 }
}

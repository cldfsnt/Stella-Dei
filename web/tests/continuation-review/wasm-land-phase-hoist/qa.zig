const std=@import("std");const B=@import("baseline/src/simulation/capillary_bucket.zig");const C=@import("candidate/src/simulation/capillary_bucket.zig");const A=@import("candidate/src/simulation/atmosphere_water.zig");
fn check(s:B.State,p:B.Params)!void{
 const a=std.testing.allocator;const sj=try std.json.stringifyAlloc(a,s,.{});defer a.free(sj);const pj=try std.json.stringifyAlloc(a,p,.{});defer a.free(pj);
 const cs=try std.json.parseFromSlice(C.State,a,sj,.{});defer cs.deinit();const cp=try std.json.parseFromSlice(C.Params,a,pj,.{});defer cp.deinit();
 const b=B.step(s,p);const c=C.step(cs.value,cp.value);const h=C.stepPrepared(cs.value,cp.value,A.PhaseStep.init(p.dt));
 const bj=try std.json.stringifyAlloc(a,b,.{});defer a.free(bj);const cj=try std.json.stringifyAlloc(a,c,.{});defer a.free(cj);const hj=try std.json.stringifyAlloc(a,h,.{});defer a.free(hj);try std.testing.expectEqualStrings(bj,cj);try std.testing.expectEqualStrings(bj,hj);
}
test "fixed bucket structural corpus standalone and prepared exact"{
 var count:usize=0;
 for([_]f32{0,0.0001,100})|liquid|for([_]f64{0,0.25,1})|soil|for([_]f64{0,1,4})|vapor|for([_]f64{270,273.15,300})|temp|for([_]f64{0,360,720,1440})|dt|for([_]f32{0,0.25})|root|{
 const s=B.State{.liquid=liquid,.soil=soil,.vapor=vapor};var cell=@import("baseline/src/simulation/microbes.zig").Cell{};
 if(root>0)cell.cohorts[0]=.{.biomass=0.01,.support_mass=0.005,.root_fraction=root,.lineage=1};
 try check(s,.{.dt=dt,.area=7669529600,.temperature=temp,.saturation=2,.cell=cell,.environment=.{.temperature=@floatCast(temp),.depth_km=if(liquid>0)0.001 else 0,.light=1,.carbon_available=1,.oxygen_carbon_capacity=1}});count+=1;
 };
 std.debug.print("HOIST_CORPUS cases={} exact_all_result_fields=true\n",.{count});
}
test "invalid area and prepared mismatched timestep refuse"{
 try check(.{.liquid=1,.soil=0.25,.vapor=1},.{.dt=1440,.area=0,.temperature=300,.saturation=2});
 try std.testing.expect(C.stepPrepared(.{.liquid=1,.vapor=1},.{.dt=1440,.area=1,.temperature=300,.saturation=2},A.PhaseStep.init(720))==null);
}

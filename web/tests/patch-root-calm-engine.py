from pathlib import Path
import sys
p=Path(sys.argv[1])
f=p/'simulation/planet.zig';s=f.read_text();s=s.replace('windDispersal:@import("wind_genetics.zig").Config=.{},','windDispersal:@import("wind_genetics.zig").Config=.{},\n    groundThermalLaw:u8=0,');s=s.replace('combined_wind:bool=false,','combined_wind:bool=false,\n        ground_thermal_law:u8=0,');s=s.replace('if(options.combined_wind and', 'if(options.ground_thermal_law>1 or (options.ground_thermal_law==1 and !options.combined_wind))return error.InvalidGroundThermalLaw;\n        if(options.combined_wind and',1);s=s.replace('if(options.combined_wind)planet.windDispersal=', 'planet.groundThermalLaw=options.ground_thermal_law;\n        if(options.combined_wind)planet.windDispersal=',1);s=s.replace('self.windDispersal=.{};self.landBeta=.{};', 'self.groundThermalLaw=0;self.windDispersal=.{};self.landBeta=.{};');s=s.replace('SurfacePhysics.originHeatCapacity(pointArea, self.waterMass[pointIndex], self.temperature[pointIndex])','SurfacePhysics.originHeatCapacityLaw(pointArea, self.waterMass[pointIndex], self.temperature[pointIndex],self.groundThermalLaw)');f.write_text(s)
f=p/'simulation/surface_physics.zig';s=f.read_text();s+='''
/// Explicit new-world illustrative thermal reservoir; historical branch exact.
pub fn originHeatCapacityLaw(area:f32,water_mass:f32,temperature:f32,law:u8)f32{
 if(law==0)return originHeatCapacity(area,water_mass,temperature);
 std.debug.assert(law==1);
 const depth_m=@max(0,water_mass)*1e9/area/1000;
 const mixed_depth=@min(depth_m,50);
 const water_cp:f32=if(temperature>273.15)4184 else 2093;
 return area*(0.5*5513*700+mixed_depth*1000*water_cp);
}
test "calmer thermal identity preserves old capacity and adds only declared ground reservoir"{
 for([_]f32{1e9,7.6695296e9})|area|for([_]f32{0,1,1000})|water|for([_]f32{270,300})|temp|{
  try std.testing.expectEqual(originHeatCapacity(area,water,temp),originHeatCapacityLaw(area,water,temp,0));
  try std.testing.expectApproxEqRel(originHeatCapacity(area,water,temp)+area*0.4*5513*700,originHeatCapacityLaw(area,water,temp,1),1e-6);
 };
}
''';f.write_text(s)
f=p/'main.zig';s=f.read_text().replace('startCombinedNext:bool=false,','startCombinedNext:bool=false,\n    startCalmNext:bool=false,');s=s.replace('g.startCombinedNext=false;g.startWetlandsNext=true;', 'g.startCalmNext=false;g.startCombinedNext=false;g.startWetlandsNext=true;');s=s.replace('pub fn combinedNewForGame(g:*Game,expected:u32)i32 {','pub fn combinedNewForGame(g:*Game,expected:u32)i32{return combinedVariantNewForGame(g,expected,false);}\npub fn combinedVariantNewForGame(g:*Game,expected:u32,calmer:bool)i32 {');s=s.replace('g.startCombinedNext=true;g.startWetlandsNext=true;', 'g.startCalmNext=calmer;g.startCombinedNext=true;g.startWetlandsNext=true;');s+='''
export fn stella_combined_calm_new(expected:u32)i32{
 if(!is_web or !web_initialized)return -1;
 web_loop.pump(1024);return combinedVariantNewForGame(&game,expected,true);
}
''';f.write_text(s)
f=p/'states/play.zig';s=f.read_text().replace('const wetlands=game.startWetlandsNext;', 'const calmer=game.startCalmNext;game.startCalmNext=false;const wetlands=game.startWetlandsNext;');s=s.replace('preset, wetlands,combined);','preset, wetlands,combined,calmer);').replace('.random, false,false);','.random, false,false,false);').replace('wetlands:bool,combined:bool) PlayState','wetlands:bool,combined:bool,calmer:bool) PlayState');s=s.replace('.combined_wind=combined,','.combined_wind=combined,.ground_thermal_law=if(calmer)1 else 0,');f.write_text(s)
f=p/'combined_view.zig';s=f.read_text().replace('const p=&s.planet;if(!p.windDispersal.valid())','const p=&s.planet;if(p.groundThermalLaw>1 or (p.groundThermalLaw==1 and !p.windDispersal.enabled))return 0;if(!p.windDispersal.valid())').replace('physiology_law==3)13 else 0','physiology_law==3)(if(p.groundThermalLaw==1)14 else 13) else 0').replace('writer==13','(writer==13 or writer==14)').replace('.root_physiology=', '.ground_thermal_law=if(state)|s|s.planet.groundThermalLaw else @as(u8,0),.root_physiology=');f.write_text(s)

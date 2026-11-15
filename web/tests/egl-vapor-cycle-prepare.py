#!/usr/bin/env python3
"""Isolated actual-scheduler vapor authority probe. NO supported save migration."""
from pathlib import Path
import shutil,sys,json,hashlib
r=Path(__file__).resolve().parents[2]; source=r.parent/'site-tmp/root-only/src';out=Path(sys.argv[1]).resolve();shutil.copytree(source,out,dirs_exist_ok=True)
def patch(file,a,b):
 p=out/file;s=p.read_text();assert a in s,(file,a);p.write_text(s.replace(a,b))
# Private import adapter only: JSON f32 vapor values round back to f32 before exact widening.
patch('save_schema.zig','vapor: []const f32','vapor: []const f64')
patch('save_game.zig','@memcpy(p.waterVaporMass, saved.vapor);','for(p.waterVaporMass,saved.vapor)|*d,v|d.*=@as(f32,@floatCast(v));')
patch('save_game.zig','@memcpy(p.newWaterVaporMass, saved.vapor);','@memcpy(p.newWaterVaporMass,p.waterVaporMass);')
# Widen true current/next authority; retain native mass unit.
p=out/'simulation/planet.zig';s=p.read_text().replace('waterVaporMass: []f32','waterVaporMass: []f64').replace('newWaterVaporMass: []f32','newWaterVaporMass: []f64')
s=s.replace('const waterVaporMass = try simAlloc.alignedAlloc(f32','const waterVaporMass = try simAlloc.alignedAlloc(f64').replace('const newVaporMass = try simAlloc.alignedAlloc(f32','const newVaporMass = try simAlloc.alignedAlloc(f64')
s=s.replace('rootSoil:[]f64=&.{},','rootSoil:[]f64=&.{},\n    vaporCoefficients:[]f64,')
s=s.replace('.waterVaporMass = waterVaporMass,','.waterVaporMass = waterVaporMass,\n            .vaporCoefficients=try simAlloc.alloc(f64,numPoints),')
s=s.replace('std.mem.swap([]f32,&self.waterVaporMass','std.mem.swap([]f64,&self.waterVaporMass').replace('std.mem.swap([]f32, &self.waterVaporMass','std.mem.swap([]f64, &self.waterVaporMass')
s=s.replace('AtmosphereWater.coefficient32(vapor,total_rate,dt)','AtmosphereWater.coefficient(vapor,total_rate,dt)').replace('self.newWaterMass[i]=coefficient','self.vaporCoefficients[i]=coefficient').replace('@as(f64,self.newWaterMass[i])*total_rate','self.vaporCoefficients[i]*total_rate').replace('@as(f64,self.newWaterMass[n])*self.cachedAtmosphericEdgeRate','self.vaporCoefficients[n]*self.cachedAtmosphericEdgeRate')
s=s.replace('return self.waterVaporMass[idx] + self.averageNitrogenMass + self.averageOxygenMass + self.averageCarbonDioxideMass + 1;','return @floatCast(self.waterVaporMass[idx] + self.averageNitrogenMass + self.averageOxygenMass + self.averageCarbonDioxideMass + 1);')
s=s.replace('.WaterVapor => self.waterVaporMass,','.WaterVapor => blk:{for(self.waterVaporMass,0..)|v,i|bufData[i]=@floatCast(v);break :blk bufData[0..self.waterVaporMass.len];},')
# Record actual full-field advection endpoint stage separately.
s=s.replace('        // Immutable post-phase vapor + fixed velocities drive both passes.','        // Immutable post-phase vapor + fixed velocities drive both passes.')
s=s.replace('        for(self.waterVaporMass,0..)|vapor,i|{\n            var total_rate', '        for(self.waterVaporMass,0..)|vapor,i|{\n            var total_rate',1)
s=s.replace('        std.mem.swap([]f64,&self.waterVaporMass,&self.newWaterVaporMass);','''        var before_adv:f64=0;var after_adv:f64=0;for(self.waterVaporMass,self.newWaterVaporMass)|a,b|{before_adv+=a;after_adv+=b;}std.debug.print("VAPOR_ADVECTION before={d} after={d} delta={d}\\n",.{before_adv,after_adv,after_adv-before_adv});
        std.mem.swap([]f64,&self.waterVaporMass,&self.newWaterVaporMass);''')
s=s.replace('        const phase_step=AtmosphereWater.PhaseStep.init(dt);','''        const phase_step=AtmosphereWater.PhaseStep.init(dt);
        const qa=@import("vapor_bridge.zig");if(qa.dumps){qa.serial+=1;qa.dump("prephase-liquid",std.mem.sliceAsBytes(self.waterMass));qa.dump("prephase-vapor",std.mem.sliceAsBytes(self.waterVaporMass));qa.dump("prephase-soil",std.mem.sliceAsBytes(self.rootSoil));}
''')
s=s.replace('        for(self.waterVaporMass,0..)|vapor,i|{\n            var total_rate','''        if(qa.dumps){qa.dump("postphase-liquid",std.mem.sliceAsBytes(self.waterMass));qa.dump("postphase-vapor",std.mem.sliceAsBytes(self.waterVaporMass));qa.dump("postphase-soil",std.mem.sliceAsBytes(self.rootSoil));}
        for(self.waterVaporMass,0..)|vapor,i|{
            var total_rate''',1)
s=s.replace('        std.mem.swap([]f64,&self.waterVaporMass,&self.newWaterVaporMass);','        qa.dump("postadvection-vapor",std.mem.sliceAsBytes(self.newWaterVaporMass));\n        std.mem.swap([]f64,&self.waterVaporMass,&self.newWaterVaporMass);')
p.write_text(s)
# Private unused legacy writer adapts type; no outputs from it are requested/supported.
patch('states/play.zig','try writer.writeInt(u32, @as(u32, @bitCast(waterVaporMass)), .little);','try writer.writeInt(u64, @as(u64,@bitCast(waterVaporMass)), .little); // QA only, unsupported legacy output')
# Same phase requests, exact represented mixed-liquid legs; unchanged infiltration.
s=(r/'src/experimental/vapor_cycle_probe.zig').read_text().replace('../simulation/atmosphere_water.zig','atmosphere_water.zig').replace('fn exchange(','pub fn exchange(')
(out/'simulation/vapor_cycle_probe.zig').write_text(s)
(out/'simulation/vapor_bridge.zig').write_text(r'''const std=@import("std");const P=@import("physical_water_f64.zig");
pub var strict_closure:bool=false;
pub var dumps:bool=false;pub var serial:usize=0;
pub fn dump(label:[]const u8,bytes:[]const u8)void{
 if(!dumps)return;var buf:[1024]u8=undefined;const path=std.fmt.bufPrint(&buf,"/workspace/scratch/f67c3ac60ca3/site-tmp/vapor-cycle-engine/{s}-{d}-{s}.bin",.{if(strict_closure)"strict"else"diagnostic",serial,label}) catch unreachable;
 std.fs.cwd().writeFile(.{.sub_path=path,.data=bytes}) catch unreachable;
}
pub const Result=struct{soil:f64,vapor:f64,paid:f64=0,funded:f64=0,native_received:f64=0,residual_density:f64=0};
pub fn step(soil:f64,vapor:f64,area:f64,wanted:f64)?Result{
 @setFloatMode(.strict);if(!std.math.isFinite(area) or area<=0 or !std.math.isFinite(vapor) or vapor<0)return null;
 const keep=Result{.soil=soil,.vapor=vapor};const removed=P.remove(soil,wanted) orelse return null;if(removed.paid==0)return keep;
 const budget=P.downRatio(P.downProduct(removed.paid,area),1e9);if(!std.math.isFinite(budget))return null;
 var after=vapor+budget;if(!std.math.isFinite(after))return null;const delta=P.difference(after,vapor);if(delta.hi>budget or (delta.hi==budget and delta.lo>0))after=std.math.nextAfter(f64,after,vapor);
 const received=P.downDifference(after,vapor);if(received<=0)return keep;
 const sd=P.difference(soil,removed.after);const vd=P.difference(after,vapor);
 if(strict_closure and (sd.lo!=0 or vd.lo!=0 or @as(f128,sd.hi)*@as(f128,area)!=@as(f128,vd.hi)*1e9))return keep;
 const funded=@min(removed.paid,P.downRatio(P.downProduct(received,1e9),area));
 return .{.soil=removed.after,.vapor=after,.paid=removed.paid,.funded=funded,.native_received=received,.residual_density=(after-vapor)*1e9/area-(soil-removed.after)};
}
''')
p=out/'simulation/capillary_bucket.zig';s=p.read_text().replace('vapor: f32','vapor: f64');s=s.replace('    r.standing_evap_native = take32(&r.state.liquid, r.request_native) orelse return null;\n    add32(&r.state.vapor, r.standing_evap_native) orelse return null;','''    const standing=@import("vapor_cycle_probe.zig").exchange(.{.liquid=r.state.liquid,.vapor=r.state.vapor},r.request_native,true);
    r.standing_evap_native=@as(f64,r.state.liquid)-standing.liquid;r.state.liquid=standing.liquid;r.state.vapor=standing.vapor;''')
a=s.index('        const removed = P.remove(r.state.soil, wanted)');b=s.index('\n    }\n    r.stages[1]',a)
s=s[:a]+'''        const transfer=@import("vapor_bridge.zig").step(r.state.soil,r.state.vapor,p.area,wanted) orelse return null;
        r.state.soil=transfer.soil;r.state.vapor=transfer.vapor;r.soil_evap_density=transfer.paid;'''+s[b:]
s=s.replace('    r.condensed_native = take32(&r.state.vapor, rain_request) orelse return null;\n    add32(&r.state.liquid, r.condensed_native) orelse return null;','''    const condensed=@import("vapor_cycle_probe.zig").exchange(.{.liquid=r.state.liquid,.vapor=r.state.vapor},rain_request,false);
    r.condensed_native=@as(f64,condensed.liquid)-r.state.liquid;r.state.liquid=condensed.liquid;r.state.vapor=condensed.vapor;''');p.write_text(s)
p=out/'simulation/root_throughflow.zig';s=p.read_text().replace('vapor:f32','vapor:f64');a=s.index(' const removal=P.remove(soil,request)');b=s.index('\n return out;',a)
s=s[:a]+''' const receipt=@import("vapor_bridge.zig").step(soil,vapor,area,request) orelse return null;

 out.soil=receipt.soil;out.vapor=receipt.vapor;out.paid=receipt.paid;out.vapor_rounding_density=receipt.residual_density;
 if(denominator>0)for(0..4)|i|{out.credits[i]=@min(wants[i],P.downProduct(receipt.funded,P.downRatio(wants[i],denominator)));out.h[i]=P.signal32(out.credits[i],out.demand[i]);};
 if(request>0)std.debug.print("VAPOR_ROOT {{\\"soil_before\\":{d},\\"soil_after\\":{d},\\"vapor_before\\":{d},\\"vapor_after\\":{d},\\"area_m2\\":{d},\\"wanted\\":{d},\\"paid\\":{d},\\"funded\\":{d},\\"demands\\":[{d},{d},{d},{d}],\\"credits\\":[{d},{d},{d},{d}],\\"h_bits\\":[{},{},{},{}]}}\\n",.{soil,out.soil,vapor,out.vapor,area,request,receipt.paid,receipt.funded,out.demand[0],out.demand[1],out.demand[2],out.demand[3],out.credits[0],out.credits[1],out.credits[2],out.credits[3],@as(u32,@bitCast(out.h[0])),@as(u32,@bitCast(out.h[1])),@as(u32,@bitCast(out.h[2])),@as(u32,@bitCast(out.h[3]))});'''+s[b:];p.write_text(s)
patch('simulation/root_scheduler_audit.zig','old_vapor:f32','old_vapor:f64')
# Main: actual loaded endpoint, paired no-action/action,3ticks. No capture of widened state.
p=out/'main.zig';s=p.read_text();needle='          std.debug.print("ROOT_ONLY_COPY_READY no_model_activation=true\\n",.{});';assert s.count(needle)==1
block=r'''
          @import("simulation/vapor_bridge.zig").strict_closure=std.posix.getenv("QA_VAPOR_STRICT")!=null;
          const bridge=@import("simulation/vapor_bridge.zig");
          for([_][3]f64{.{0.9999999167069676,1680.0450439453125,5.445914790658257e-5},.{0.9999991749741014,1635.706298828125,1.3555834952327928e-6}},0..)|w,wi|{
            const receipt=bridge.step(w[0],w[1],7669529600,w[2]).?;
            std.debug.print("VAPOR_FIXED_PULSE {s}\n",.{try std.json.stringifyAlloc(a,.{.index=wi,.strict=bridge.strict_closure,.soil_before=w[0],.vapor_before=w[1],.requested_density=w[2],.area_m2=@as(f64,7669529600),.receipt=receipt},.{})});
          }
          const original_liquid=try a.dupe(f32,state.planet.waterMass);const original_vapor=try a.dupe(f64,state.planet.waterVaporMass);const original_soil=try a.dupe(f64,state.planet.rootSoil);
          const input_path=try std.process.getEnvVarOwned(a,"QA_PULSE_SAVE");const bytes=try std.fs.cwd().readFileAlloc(a,input_path,128*1024*1024);const frozen_input=try std.json.parseFromSlice(saves.schema.Save,a,bytes,.{.allocate=.alloc_always});
          @import("simulation/vapor_bridge.zig").dumps=true;
          for(0..2)|action|{
            try saves.apply(state,frozen_input.value);std.debug.assert(std.mem.eql(f32,original_liquid,state.planet.waterMass) and std.mem.eql(f64,original_vapor,state.planet.waterVaporMass) and std.mem.eql(f64,original_soil,state.planet.rootSoil));
            state.paused=true;state.selectedPoint=12352;state.pointerOnPlanet=true;const old=state.planet.waterMass[12352];if(action==1)std.debug.assert(state.testAction(2));
            std.debug.print("VAPOR_ACTION action={} removed={d}\n",.{action,@as(f64,old)-state.planet.waterMass[12352]});
            for(0..3)|tick|{
              @import("simulation/root_scheduler_audit.zig").current=.{};
              state.planet.simulate(game.loop,.{.dt=1440,.timeScale=1,.solarConstant=state.solarConstant,.gameTime=state.gameTime,.planetRotationTime=state.planetRotationTime,.solarVector=state.simulationSolarVector()});state.gameTime+=1440;
              @import("simulation/vapor_bridge.zig").dump("postroot-vapor",std.mem.sliceAsBytes(state.planet.waterVaporMass));@import("simulation/vapor_bridge.zig").dump("postroot-soil",std.mem.sliceAsBytes(state.planet.rootSoil));
              std.debug.print("VAPOR_TICK {s}\n",.{try std.json.stringifyAlloc(a,.{.action=action,.tick=tick+1,.liquid=state.planet.waterMass[12352],.vapor=state.planet.waterVaporMass[12352],.soil=state.planet.rootSoil[12352],.cohorts=state.planet.microbeCells[12352],.audit=@import("simulation/root_scheduler_audit.zig").current},.{})});
            }
          }
          std.process.exit(0);
'''
s=s.replace(needle,block);p.write_text(s)
(out.parent/'provenance.json').write_text(json.dumps({'source':str(source),'generator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'files':{str(p.relative_to(out)):hashlib.sha256(p.read_bytes()).hexdigest()for p in out.rglob('*.zig')}},indent=2)+'\n');print(out)

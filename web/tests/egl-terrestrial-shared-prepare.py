#!/usr/bin/env python3
"""Separate predeclared shared soil-demand law; old conditioned input unchanged."""
from pathlib import Path
import sys,subprocess,hashlib,json
r=Path(__file__).resolve().parents[2];o=Path(sys.argv[1]).resolve()
subprocess.run([sys.executable,str(r/'web/tests/egl-terrestrial-two-tick-prepare.py'),str(o)],check=True)
p=o/'simulation/root_throughflow.zig';s=p.read_text()
s=s.replace('pub const Result=','pub var enabled:bool=false;\npub const Result=')
s=s.replace('paid:f64=0,','paid:f64=0,bare_credit:f64=0,')
s=s.replace('conductance:u8)?Result','conductance:u8,bare:f64)?Result')
s=s.replace('var out=Result{.soil=soil,.vapor=vapor};','if(!std.math.isFinite(bare) or bare<0)return null;var out=Result{.soil=soil,.vapor=vapor};')
s=s.replace('if(env.temperature<=273.15 or env.temperature>=355 or env.depth_km>=0.0002)return out;','const root_eligible=env.temperature>273.15 and env.temperature<355 and env.depth_km<0.0002;')
s=s.replace('if(c.biomass<=0 or c.root_fraction==0 or c.support_mass<=0)continue;','if(!root_eligible or c.biomass<=0 or c.root_fraction==0 or c.support_mass<=0)continue;')
s=s.replace('const request=P.lowerSum(wants);const denominator=P.upperSum(wants);','const root_request=P.lowerSum(wants);var all=[_]f64{wants[0],wants[1],wants[2],wants[3],bare};std.mem.sort(f64,&all,{},std.sort.asc(f64));var request:f64=0;var denominator:f64=0;for(all)|x|if(x>0){request=std.math.nextAfter(f64,request+x,0);denominator=std.math.nextAfter(f64,denominator+x,std.math.inf(f64));};if(!std.math.isFinite(denominator))return null;')
s=s.replace('if(request>0)std.debug.print(', 'if(denominator>0)out.bare_credit=@min(bare,P.downProduct(receipt.funded,P.downRatio(bare,denominator)));\n if(root_request>0)std.debug.print(')
s=s.replace('VAPOR_ROOT','SHARED_ROOT')
(o/'simulation/shared_soil.zig').write_text(s)
p=o/'simulation/capillary_bucket.zig';s=p.read_text()
s=s.replace('pub const Params = struct {','pub const Params = struct { cell:?@import("microbes.zig").Cell=null, environment:?@import("microbes.zig").Environment=null, conductance:u8=10,')
s=s.replace('pub const Result = struct {','pub const Result = struct { root_h:[4]f32=.{0,0,0,0}, root_credits:[4]f64=.{0,0,0,0}, bare_credit:f64=0,')
a=s.index('    // A represented residual standing pool');b=s.index('    r.stages[1] = r.state;',a)
old=s[a:b]
new='''    if(@import("shared_soil.zig").enabled){
        var bare:f64=0;
        if(warm and r.state.liquid==0 and r.request_native>0){
            r.exposed_seconds=if(initial.liquid==0)p.dt else if(deficit>initial.liquid)@max(0,p.dt-@min(p.dt,-A.evaporation_seconds*std.math.log1p(-@as(f64,initial.liquid)/deficit))) else 0;
            const atmospheric=toDensity(P.downDifference(r.request_native,r.standing_evap_native),p.area);
            const substrate=P.downProduct(r.state.soil,-std.math.expm1(-r.exposed_seconds/86400));
            bare=@min(atmospheric,substrate);
        }
        const shared=@import("shared_soil.zig").step(p.cell orelse return null,r.state.soil,r.state.vapor,p.area,p.environment orelse return null,@floatCast(p.dt),p.conductance,bare) orelse return null;
        r.state.soil=shared.soil;r.state.vapor=shared.vapor;r.root_h=shared.h;r.root_credits=shared.credits;r.bare_credit=shared.bare_credit;r.soil_evap_density=shared.bare_credit;
    }else{
'''+old+'    }\n'
s=s[:a]+new+s[b:];p.write_text(s)
p=o/'simulation/planet.zig';s=p.read_text()
s=s.replace('rootSoil:[]f64=&.{},','rootSoil:[]f64=&.{},\n    sharedRootH:[][4]f32=&.{},')
s=s.replace('fn simulateAtmosphereWater(self:*Planet,dt:f32) void {','fn simulateAtmosphereWater(self:*Planet,dt:f32,options:SimulationOptions) void {\n        if(@import("shared_soil.zig").enabled){if(self.sharedRootH.len!=self.waterMass.len)self.sharedRootH=self.simulationArena.allocator().alloc([4]f32,self.waterMass.len) catch unreachable;@memset(self.sharedRootH,.{0,0,0,0});}')
s=s.replace('self.simulateAtmosphereWater(dt);','self.simulateAtmosphereWater(dt,options);')
needle='.{.dt=dt,.area=self.getMeanPointArea(),.temperature=temperature,.saturation=saturation})'
assert s.count(needle)==1
s=s.replace(needle,'.{.dt=dt,.area=self.getMeanPointArea(),.temperature=temperature,.saturation=saturation,.cell=self.microbeCells[i],.environment=self.microbeEnvironment(i,@max(0,self.transformedPoints[i].norm().dot(options.solarVector))*std.math.clamp(options.solarConstant/1361,0,2)),.conductance=self.rootConfig.conductance})')
s=s.replace('self.waterMass[i]=column.state.liquid;','if(@import("shared_soil.zig").enabled)self.sharedRootH[i]=column.root_h;\n                self.waterMass[i]=column.state.liquid;',1)
needle='if(self.rootConfig.enabled){\n                const receipt=@import("root_throughflow.zig")'
assert s.count(needle)==1
s=s.replace(needle,'if(self.rootConfig.enabled and @import("shared_soil.zig").enabled){environment.root_hydration=self.sharedRootH[i];}else if(self.rootConfig.enabled){\n                const receipt=@import("root_throughflow.zig")')
p.write_text(s)
p=o/'main.zig';s=p.read_text()
s=s.replace('const trial_dt:f32=if(arm<2)1440 else 720;const trial_ticks:usize=if(arm<2)2 else 4;','@import("simulation/shared_soil.zig").enabled=arm>=2;const trial_dt:f32=1440;const trial_ticks:usize=2;')
p.write_text(s)
(o.parent/'shared-provenance.json').write_text(json.dumps({'files':{str(p.relative_to(o)):hashlib.sha256(p.read_bytes()).hexdigest()for p in o.rglob('*.zig')},'scope':'Separate shared-demand law; old arms and old conditioning unchanged'},indent=2)+'\n')

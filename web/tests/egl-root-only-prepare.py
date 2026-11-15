#!/usr/bin/env python3
"""Isolated root-only production-derived copy. No production source mutation."""
from pathlib import Path
import subprocess,sys,hashlib,json
r=Path(__file__).resolve().parents[2];o=Path(sys.argv[1]).resolve()
subprocess.run([sys.executable,str(r/'web/tests/egl-natural60-prepare.py'),str(o)],check=True)
def change(s,a,b):
 assert s.count(a)==1,(a,s.count(a));return s.replace(a,b,1)
s=(r/'src/simulation/microbes.zig').read_text()
s=change(s,'pub const Cohort=struct {','pub const Cohort=struct {\n    root_fraction:f32=0,')
s=change(s,'oxygen_carbon_capacity:f32};','oxygen_carbon_capacity:f32,root_hydration:[4]f32=.{0,0,0,0}};')
s=change(s,'pub fn frondMass','pub fn abovegroundSupport(c:Cohort)f32{return c.support_mass*(1-c.root_fraction);}\npub fn frondMass')
s=s.replace('c.biomass<=0 or c.support_mass<=0 or frondMass(c)<=0','c.biomass<=0 or abovegroundSupport(c)<=0 or frondMass(c)<=0').replace('c.support_mass/@max(c.biomass,0.000001)','abovegroundSupport(c)/@max(c.biomass,0.000001)').replace('0.2*c.support_mass/(frondMass(c)+0.01)','0.2*abovegroundSupport(c)/(frondMass(c)+0.01)').replace('std.math.clamp(c.support_mass/c.biomass,0,1)','std.math.clamp(abovegroundSupport(c)/c.biomass,0,1)').replace('if(c.support_mass>0)organized=true','if(abovegroundSupport(c)>0)organized=true')
s=change(s,'fn aquaticSubmergence','pub fn effectiveHydration(h:f32,depth:f32,temp:f32)f32 {\n if(!std.math.isFinite(h) or !std.math.isFinite(depth) or !std.math.isFinite(temp) or depth<0 or temp<=273.15 or temp>=355)return 0;\n return std.math.clamp(h,0,1)*(1-aquaticSubmergence(depth));\n}\nfn aquaticSubmergence')
s=change(s,'    for(&cell.cohorts) |*c| {','    for(&cell.cohorts,0..) |*c,i| {')
s=change(s,'        const wanted_dead=c.biomass*(1-@exp(-(mortality+3*exposed)*days));','''        const hydrated=effectiveHydration(env.root_hydration[i],env.depth_km,env.temperature);
        const wet_mortality=0.04+(1-fitness)*0.7+0.10*c.structure+0.10*c.feeding+0.05*c.mobility;
        const effective_mortality=if(hydrated>0) mortality*(1-hydrated)+wet_mortality*hydrated else mortality;
        const wanted_dead=c.biomass*(1-@exp(-(effective_mortality+3*exposed*(1-hydrated))*days));''')
s=change(s,'        if(c.biomass<=0 or photosyntheticHabitat(c,env.depth_km,env.temperature)<=0)continue;','''        const effective_habitat=@max(photosyntheticHabitat(c,env.depth_km,env.temperature),effectiveHydration(env.root_hydration[i],env.depth_km,env.temperature));
        if(c.biomass<=0 or effective_habitat<=0)continue;''')
s=s.replace('3*photosyntheticHabitat(c,env.depth_km,env.temperature)*fitness','3*effective_habitat*fitness')
s=change(s,'    for(cell.cohorts) |c| {\n        if(!std.math.isFinite(c.biomass)','    for(cell.cohorts) |c| {\n        if(!std.math.isFinite(c.root_fraction) or c.root_fraction<0 or c.root_fraction>1)return false;\n        if(!std.math.isFinite(c.biomass)')
(o/'simulation/microbes.zig').write_text(s)
for f in ['capillary_bucket.zig','physical_water_f64.zig','root_scheduler_audit.zig']:
 (o/'simulation'/f).write_text((r/'src/experimental'/f).read_text().replace('../simulation/atmosphere_water.zig','atmosphere_water.zig'))
(o/'simulation/root_throughflow.zig').write_text((r/'src/experimental/root_throughflow.zig').read_text())
p=(r/'src/simulation/planet.zig').read_text()
p=change(p,'    microbeCells: []Microbes.Cell = &.{},','''    microbeCells: []Microbes.Cell = &.{},
    rootConfig:RootConfig=.{},
    rootSoil:[]f64=&.{},
''')
p=change(p,'    pub fn ensureMicrobeStorage','    pub const RootConfig=struct{enabled:bool=false,law:u8=0,conductance:u8=1};\n    pub fn ensureRootSoil(self:*Planet)!void {\n        if(self.rootSoil.len==self.vertices.len)return;\n        const replacement=try self.simulationArena.allocator().alloc(f64,self.vertices.len);\n        @memset(replacement,0);self.rootSoil=replacement;\n    }\n    pub fn resetRootModel(self:*Planet)void{self.rootConfig=.{};@memset(self.rootSoil,0);}\n    pub fn ensureMicrobeStorage')
p=change(p,'        self.worldMode = .origin;','        self.worldMode = .origin;self.resetRootModel();')
p=change(p,'            const result=phase_step.phase(liquid,vapor,saturation,temperature,self.rainfall[i]) orelse continue;','''            if(self.rootConfig.enabled){
                std.debug.assert(self.rootConfig.law==1 and self.rootSoil.len==self.waterMass.len);
                const column=@import("capillary_bucket.zig").step(.{.liquid=liquid,.vapor=vapor,.soil=self.rootSoil[i],.rain=self.rainfall[i]},.{.dt=dt,.area=self.getMeanPointArea(),.temperature=temperature,.saturation=saturation}) orelse unreachable;
                @import("root_scheduler_audit.zig").column(@import("capillary_bucket.zig").State{.liquid=liquid,.vapor=vapor,.soil=self.rootSoil[i],.rain=self.rainfall[i]},column,self.getMeanPointArea(),temperature);
                self.waterMass[i]=column.state.liquid;self.waterVaporMass[i]=column.state.vapor;self.rainfall[i]=column.state.rain;self.rootSoil[i]=column.state.soil;
                continue;
            }
            const result=phase_step.phase(liquid,vapor,saturation,temperature,self.rainfall[i]) orelse continue;''')
p=change(p,'            const flux = Microbes.step(cell, self.microbeEnvironment(i, light), dt);','''            var environment=self.microbeEnvironment(i,light);
            if(self.rootConfig.enabled){
                const receipt=@import("root_throughflow.zig").step(cell.*,self.rootSoil[i],self.waterVaporMass[i],self.getMeanPointArea(),environment,dt,self.rootConfig.conductance) orelse unreachable;
                @import("root_scheduler_audit.zig").root(self.waterVaporMass[i],receipt);
                self.rootSoil[i]=receipt.soil;self.waterVaporMass[i]=receipt.vapor;environment.root_hydration=receipt.h;
            }
            const flux = Microbes.step(cell, environment, dt);''')
(o/'simulation/planet.zig').write_text(p)
# Strip inherited natural60 run; owner/reviewer inject bounded current-model gates.
p=o/'main.zig';s=p.read_text();a=s.index('          const start_time=state.gameTime;');b=s.index('\n        try originSaveCheck',a)
s=s[:a]+'''          std.debug.print("ROOT_ONLY_COPY_READY no_model_activation=true\\n",.{});
        }
'''+s[b:];s=s.replace('_=pw;_=pm;const micro=@import("simulation/microbes.zig");','_=pw;_=pm;');p.write_text(s)
# Restore inherited QA ancestor's unintended public pond substitution.
p=o/'main.zig';s=p.read_text();s=change(s,'export fn stella_make_pond(expected_point:u32) i32 {\n    const state=webEditableState() orelse return -1;\n    return state.makeSelectedNursery(expected_point);\n}','export fn stella_make_pond(expected_point:u32) i32 {\n    const state=webEditableState() orelse return -1;\n    return state.makeSelectedPond(expected_point);\n}');p.write_text(s)
(o.parent/'root-copy-provenance.json').write_text(json.dumps({'production_head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=r,text=True).strip(),'files':{str(f.relative_to(o)):hashlib.sha256(f.read_bytes()).hexdigest() for f in [o/'simulation/microbes.zig',o/'simulation/planet.zig',o/'simulation/root_throughflow.zig',o/'main.zig']}},indent=2)+'\n')
print(o)

#!/usr/bin/env python3
"""Isolated v72 beta integration. Never modifies production src."""
from pathlib import Path
import shutil,subprocess,sys,json,hashlib
r=Path(__file__).resolve().parents[2];o=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else r.parent/'site-tmp/origin-land-beta/src';old=r.parent/'site-tmp/mature-daylight/src/simulation'
assert o.resolve().is_relative_to((r.parent/'site-tmp').resolve()),'isolated site-tmp output only'
assert not o.exists(),'refuse overwrite of sibling save work; use explicit separate tree for regeneration'
shutil.copytree(r/'src',o)
subprocess.run([sys.executable,str(r/'web/tests/root-beta-microbes-patch.py'),str(o/'simulation/microbes.zig')],check=True)
for name in ['physical_water_f64','vapor_cycle_probe','capillary_bucket','shared_soil']:
 s=(old/(name+'.zig')).read_text()
 if name=='shared_soil':
  s=s.replace('pub var enabled:bool=false;','');a=s.index(' if(root_request>0)std.debug.print(');b=s.index(' return out;',a);s=s[:a]+s[b:];s=s.replace(' const root_request=P.lowerSum(wants);',' ')
 if name=='capillary_bucket':
  a=s.index('    if(@import("shared_soil.zig").enabled){');b=s.index('    }else{',a);c=s.index('    r.stages[1]',b)
  s=s[:a]+s[a:b].replace('    if(@import("shared_soil.zig").enabled){','    {')+'    }\n'+s[c:]
 (o/'simulation'/(name+'.zig')).write_text(s)
shutil.copy(r/'src/experimental/vapor_bridge_f64.zig',o/'simulation/vapor_bridge.zig')
(o/'simulation/land_beta.zig').write_text('''const R=@import("microbes.zig").RootMutation;
pub const Config=struct{enabled:bool=false,law:u8=0,root_mutation:R.Config=.{},pub fn valid(c:@This())bool{return if(!c.enabled)c.law==0 and c.root_mutation.law==0 and !c.root_mutation.enabled and c.root_mutation.stream_seed==0 else c.law==1 and c.root_mutation.law==1 and c.root_mutation.enabled;}};
''')
p=o/'simulation/planet.zig';s=p.read_text()
def change(a,b):
 global s
 assert s.count(a)==1,(a,s.count(a));s=s.replace(a,b,1)
change('const AtmosphereWater', 'const LandBeta=@import("land_beta.zig");\nconst AtmosphereWater')
change('    waterVaporMass: []f32,','''    waterVaporMass: []f32,
    landBeta:LandBeta.Config=.{},
    landSoil:[]f64=&.{},
    landVapor:[]f64=&.{},
    landNewVapor:[]f64=&.{},
    landCoefficient:[]f64=&.{},
    landRootH:[][4]f32=&.{},''')
change('        generate_terrain: bool = true,','        generate_terrain: bool = true,\n        land_beta:bool=false,')
change('        if(!options.generate_terrain and options.water_preset!=.random)', '        if(options.land_beta and !options.generate_terrain)return error.BetaRequiresNewWorld;\n        if(!options.generate_terrain and options.water_preset!=.random)')
change('        return planet;','''        if(options.land_beta){
            try planet.beginOrigin();try planet.ensureLandBetaStorage();
            for(planet.waterVaporMass,planet.landVapor)|v,*b|b.*=v;
            @memcpy(planet.landNewVapor,planet.landVapor);
            planet.landBeta=.{.enabled=true,.law=1,.root_mutation=.{.enabled=true,.law=1,.stream_seed=seed}};
        }
        return planet;''')
methods='''    pub fn ensureLandBetaStorage(self:*Planet)!void{
        const n=self.vertices.len;if(self.landSoil.len==n and self.landVapor.len==n and self.landNewVapor.len==n and self.landCoefficient.len==n and self.landRootH.len==n)return;
        const a=self.simulationArena.allocator();
        const soil=try a.alloc(f64,n);const vapor=try a.alloc(f64,n);const next=try a.alloc(f64,n);const coeff=try a.alloc(f64,n);const h=try a.alloc([4]f32,n);
        @memset(soil,0);@memset(vapor,0);@memset(next,0);@memset(coeff,0);@memset(h,.{0,0,0,0});
        self.landSoil=soil;self.landVapor=vapor;self.landNewVapor=next;self.landCoefficient=coeff;self.landRootH=h;
    }
    pub fn resetLandBeta(self:*Planet)void{self.landBeta=.{};@memset(self.landSoil,0);@memset(self.landVapor,0);@memset(self.landNewVapor,0);@memset(self.landCoefficient,0);@memset(self.landRootH,.{0,0,0,0});}
    pub fn vaporMass(self:Planet,i:usize)f64{return if(self.landBeta.enabled)self.landVapor[i]else self.waterVaporMass[i];}
    pub fn vaporMass32(self:Planet,i:usize)f32{return if(self.landBeta.enabled)@floatCast(self.landVapor[i])else self.waterVaporMass[i];}
    pub fn setAllVapor(self:*Planet,value:f32)void{if(self.landBeta.enabled){@memset(self.landVapor,value);@memset(self.landNewVapor,value);}else @memset(self.waterVaporMass,value);}

'''
change('    /// Optional Origin storage; use the live arena, never a copied allocator state.',methods+'    /// Optional Origin storage; use the live arena, never a copied allocator state.')
# Direct scalar climate reads retain f32 operations in legacy mode; beta derives current f32 thermal input from authority.
s=s.replace('const h2o = self.waterVaporMass[i] / meanPointArea;','const h2o = self.vaporMass32(i) / meanPointArea;')
change('return self.waterVaporMass[idx] + self.averageNitrogenMass','return self.vaporMass32(idx) + self.averageNitrogenMass')
change('self.temperature[idx], self.waterVaporMass[idx]);','self.temperature[idx], self.vaporMass(idx));')
change('                    .WaterVapor => self.waterVaporMass,','''                    .WaterVapor => if(self.landBeta.enabled) blk:{for(self.landVapor,0..)|v,i|bufData[i]=@floatCast(v);break :blk bufData[0..self.landVapor.len];}else self.waterVaporMass,''')
change('            const flux = Microbes.step(cell, self.microbeEnvironment(i, light), dt);','''            var env=self.microbeEnvironment(i,light);if(self.landBeta.enabled)env.root_hydration=self.landRootH[i];
            const flux = Microbes.step(cell, env, dt);''')
s=s.replace('Microbes.propagate(cell,cohort,&self.microbeCells[n],&self.microbeStats)','Microbes.propagateWithRoot(cell,cohort,&self.microbeCells[n],&self.microbeStats,self.landBeta.root_mutation)')
s=s.replace('Microbes.reproduce(cell, cohort, cell, &self.microbeStats, true)','Microbes.reproduceWithRoot(cell, cohort, cell, &self.microbeStats, true,self.landBeta.root_mutation)')
s=s.replace('Microbes.reproduce(cell, cohort, &self.microbeCells[n], &self.microbeStats, true)','Microbes.reproduceWithRoot(cell, cohort, &self.microbeCells[n], &self.microbeStats, true,self.landBeta.root_mutation)')
# Leave original atmosphere function body intact; beta has separate authority.
a=s.index('    fn simulateAtmosphereWater(');b=s.index('    /// Compute partial pressure',a);legacy=s[a:b]
beta=legacy.replace('fn simulateAtmosphereWater(self:*Planet,dt:f32)','fn simulateLandAtmosphere(self:*Planet,dt:f32,options:SimulationOptions)')
a=beta.index('        const phase_step=');b=beta.index('        // After the preceding swap',a)
beta=beta[:a]+'''        @memset(self.landRootH,.{0,0,0,0});
        for(self.waterMass,self.landVapor,0..)|liquid,vapor,i|{
            const temperature=self.temperature[i];const saturation=@as(f64,getEquilibriumVaporPressure(temperature))*divider/(@as(f64,temperature)*k);
            const env=self.microbeEnvironment(i,@max(0,self.transformedPoints[i].norm().dot(options.solarVector))*std.math.clamp(options.solarConstant/1361,0,2));
            const column=@import("capillary_bucket.zig").step(.{.liquid=liquid,.vapor=vapor,.soil=self.landSoil[i],.rain=self.rainfall[i]},.{.dt=dt,.area=self.getMeanPointArea(),.temperature=temperature,.saturation=saturation,.cell=self.microbeCells[i],.environment=env,.conductance=10}) orelse continue;
            self.waterMass[i]=column.state.liquid;self.landVapor[i]=column.state.vapor;self.landSoil[i]=column.state.soil;self.rainfall[i]=column.state.rain;self.landRootH[i]=column.root_h;
        }
'''+beta[b:]
beta=beta.replace('self.waterVaporMass','self.landVapor').replace('self.newWaterVaporMass','self.landNewVapor').replace('AtmosphereWater.coefficient32','AtmosphereWater.coefficient').replace('self.newWaterMass[i]','self.landCoefficient[i]').replace('self.newWaterMass[n]','self.landCoefficient[n]').replace('std.mem.swap([]f32','std.mem.swap([]f64')
# Derived f64 coefficient may spend at most donor inventory.
beta=beta.replace('const coefficient=AtmosphereWater.coefficient(vapor,total_rate,dt);','var coefficient=AtmosphereWater.coefficient(vapor,total_rate,dt);if(coefficient*total_rate>vapor)coefficient=std.math.nextAfter(f64,coefficient,0);')
change(legacy,legacy+beta)
change('                self.simulateAtmosphereWater(dt);','                if(self.landBeta.enabled)self.simulateLandAtmosphere(dt,options)else self.simulateAtmosphereWater(dt);')
# Always clear transient hydration, including large dt when atmosphere is not stepped.
change('        const dt = options.dt * options.timeScale;\n        // Disable water','        if(self.landBeta.enabled)@memset(self.landRootH,.{0,0,0,0});\n        const dt = options.dt * options.timeScale;\n        // Disable water')
a=s.index('    pub fn simulateMicrobes(');i=s.index('\n',a)+1;s=s[:i]+'        const root_mutation:Microbes.RootMutation.Config=if(self.landBeta.enabled)self.landBeta.root_mutation else .{};\n'+s[i:]
s=s.replace('&self.microbeStats,self.landBeta.root_mutation)','&self.microbeStats,root_mutation)').replace('true,self.landBeta.root_mutation)','true,root_mutation)')
s=s.replace('                @memcpy(self.newWaterVaporMass, self.waterVaporMass);','                if(!self.landBeta.enabled)@memcpy(self.newWaterVaporMass, self.waterVaporMass);').replace('                std.mem.swap([]f32, &self.waterVaporMass, &self.newWaterVaporMass);','                if(!self.landBeta.enabled)std.mem.swap([]f32, &self.waterVaporMass, &self.newWaterVaporMass);')
s=s.replace('temperature: f32, vaporMass: f64','temperature: f32, vapor_mass: f64').replace('temperature, vaporMass +','temperature, vapor_mass +')
p.write_text(s)
p=o/'states/play.zig';s=p.read_text();s=s.replace('@memset(self.planet.waterVaporMass, 0);','self.planet.setAllVapor(0);').replace('@memset(self.planet.waterVaporMass, 5_000_000);','self.planet.setAllVapor(5_000_000);')
for base,idx in [('self.planet','selectedPoint'),('planet','point')]:s=s.replace(base+'.waterVaporMass['+idx+']',base+'.vaporMass('+idx+')')
s=s.replace('    pub fn saveGame(self: *PlayState) !void {','    pub fn saveGame(self: *PlayState) !void {\n        if(self.planet.landBeta.enabled)return error.BetaRequiresModernSave;')
p.write_text(s)
subprocess.run([sys.executable,str(r/'web/tests/patch-land-beta-legacy-thermal.py'),str(o/'simulation/planet.zig')],check=True)
subprocess.run([sys.executable,str(r/'web/tests/patch-origin-land-borrowed.py'),str(o)],check=True)
subprocess.run([sys.executable,str(r/'web/tests/origin-land-beta-save-patch.py'),str(o)],check=True)
(o.parent/'source-manifest.json').write_text(json.dumps({'borrowed_cell_reference':'d726898; original arithmetic, value wrappers preserved; no coefficient hoist', 'production_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=r,text=True).strip(),'files':{str(p.relative_to(o)):hashlib.sha256(p.read_bytes()).hexdigest()for p in o.rglob('*.zig')}},indent=2)+'\n')
print(o)

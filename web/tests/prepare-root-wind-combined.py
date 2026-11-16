from pathlib import Path
import shutil,json,hashlib
r=Path(__file__).resolve().parents[2];t=r.parent/'site-tmp';base=t/'rooted-hardy-ui/src';wind=t/'wind-dispersal/src';dst=t/'root-wind-combined/src';assert not dst.exists();shutil.copytree(base,dst)
for name in ['wind_genetics.zig','wind_packet.zig','wind_dispersal.zig','wind_audit.zig']:shutil.copyfile(wind/'simulation'/name,dst/'simulation'/name)
p=dst/'simulation/microbes.zig';s=p.read_text().replace('    root_fraction:f32=0,','    aerial_allocation:f32=0,\n    root_fraction:f32=0,',1)
needle=' fn reproduceSized(donor:*Cell,which:usize,destination:*Cell,stats:*Stats,mutate:bool,amount:f32,min_parent:f32,credit:f32,config:RootMutation.Config) bool {'
assert needle in s
s=s.replace(needle,'''pub fn prepareCombinedPacket(d:*Cell,w:usize,t:*Cell,stats:*Stats,mutate:bool,root:RootMutation.Config,wind:@import("wind_genetics.zig").Config)bool{return reproduceCombined(d,w,t,stats,mutate,0.004,0.02,0.01,root,wind);}
pub fn reproduceCombinedLarge(d:*Cell,w:usize,t:*Cell,stats:*Stats,root:RootMutation.Config,wind:@import("wind_genetics.zig").Config)bool{return reproduceCombined(d,w,t,stats,true,0.01,0.03,0.04,root,wind);}
pub fn prepareWindPacket(d:*Cell,w:usize,t:*Cell,stats:*Stats,mutate:bool,wind:@import("wind_genetics.zig").Config)bool{return prepareCombinedPacket(d,w,t,stats,mutate,.{},wind);}
pub fn reproduceWithWind(d:*Cell,w:usize,t:*Cell,stats:*Stats,wind:@import("wind_genetics.zig").Config)bool{return reproduceCombinedLarge(d,w,t,stats,.{},wind);}
fn reproduceSized(donor:*Cell,which:usize,destination:*Cell,stats:*Stats,mutate:bool,amount:f32,min_parent:f32,credit:f32,config:RootMutation.Config)bool{return reproduceCombined(donor,which,destination,stats,mutate,amount,min_parent,credit,config,.{});}
fn reproduceCombined(donor:*Cell,which:usize,destination:*Cell,stats:*Stats,mutate:bool,amount:f32,min_parent:f32,credit:f32,config:RootMutation.Config,wind:@import("wind_genetics.zig").Config)bool{
    if(!wind.valid())return false;''')
needle='        if(config.enabled)child.root_fraction=RootMutation.allocation(parent.root_fraction,config.stream_seed,child.parent,child.lineage,child.generation);';assert needle in s;s=s.replace(needle,needle+'\n        if(wind.enabled)child.aerial_allocation=@import("wind_genetics.zig").mutation(parent.aerial_allocation,wind.stream_seed,parent.lineage,child.lineage,child.generation);')
needle='if(!std.math.isFinite(c.root_fraction)';idx=s.index(needle,s.index('pub fn validCell'));s=s[:idx]+'if(!std.math.isFinite(c.aerial_allocation) or c.aerial_allocation<0 or c.aerial_allocation>1)return false;\n        '+s[idx:];p.write_text(s)
p=dst/'simulation/wind_packet.zig';s=p.read_text();sig='pub fn launch(donor:*M.Cell,slot:usize,target:*M.Cell,stats:*M.Stats,area_source:f64,area_target:f64,viable:bool,config:G.Config)?Receipt{';assert sig in s;s=s.replace(sig,sig+'return launchCombined(donor,slot,target,stats,area_source,area_target,viable,config,.{});}\npub fn launchCombined(donor:*M.Cell,slot:usize,target:*M.Cell,stats:*M.Stats,area_source:f64,area_target:f64,viable:bool,config:G.Config,root:M.RootMutation.Config)?Receipt{\n if(!root.valid())return null;');s=s.replace('M.prepareWindPacket(&paid,slot,&packet,&trial_stats,false,config)','M.prepareCombinedPacket(&paid,slot,&packet,&trial_stats,false,root,config)').replace('M.prepareWindPacket(&paid,slot,&packet,&trial_stats,true,config)','M.prepareCombinedPacket(&paid,slot,&packet,&trial_stats,true,root,config)');p.write_text(s)
p=dst/'simulation/planet.zig';s=p.read_text().replace('    landSoil:[]f64=', '    windDispersal:@import("wind_genetics.zig").Config=.{},\n    landSoil:[]f64=',1)
s=s.replace('land_beta:bool=false,','land_beta:bool=false,\n        combined_wind:bool=false,',1)
# generation guard and explicit enable only in fresh rootlaw3 creation
needle='if(options.land_beta';i=s.index(needle);s=s[:i]+'if(options.combined_wind and (!options.land_beta or !options.generate_terrain or options.land_beta_physiology!=3))return error.InvalidCombinedWorld;\n        '+s[i:]
s=s.replace('        return planet;','        if(options.combined_wind)planet.windDispersal=.{.enabled=true,.law=1,.stream_seed=seed};\n        return planet;',1)
s=s.replace('pub fn resetLandBeta(self:*Planet)void{','pub fn resetLandBeta(self:*Planet)void{self.windDispersal=.{};',1)
w=(wind/'simulation/planet.zig').read_text();a=w.index('    /// Explicit chosen founder genetics;');b=w.index('    /// Explicit player-supplied nutrient input',a);extra=w[a:b].replace('.launch(','.launchCombined(').replace('viable,cfg.*)','viable,cfg.*,self.landBeta.root_mutation)')
s=s.replace('    /// Explicit player-supplied nutrient input',extra+'    /// Explicit player-supplied nutrient input',1)
needle='                if(cell.cohorts[cohort].reproduction_credit>=0.01';s=s.replace(needle,'                if(self.tryWindPacket(i,cohort,options.gameTime))|dest|{if(active)|bits|ActiveCells.mark(bits,dest);continue;}\n'+needle,1)
s=s.replace('Microbes.propagateWithRoot(cell,cohort,&self.microbeCells[n],&self.microbeStats,root_mutation)','Microbes.prepareCombinedPacket(cell,cohort,&self.microbeCells[n],&self.microbeStats,true,root_mutation,self.windDispersal)')
s=s.replace('Microbes.reproduceWithRoot(cell, cohort, cell, &self.microbeStats, true,root_mutation)','Microbes.reproduceCombinedLarge(cell, cohort, cell, &self.microbeStats,root_mutation,self.windDispersal)').replace('Microbes.reproduceWithRoot(cell, cohort, &self.microbeCells[n], &self.microbeStats, true,root_mutation)','Microbes.reproduceCombinedLarge(cell, cohort, &self.microbeCells[n], &self.microbeStats,root_mutation,self.windDispersal)');p.write_text(s)
(dst.parent/'base-source-hashes.json').write_text(json.dumps({str(p.relative_to(base)):hashlib.sha256(p.read_bytes()).hexdigest()for p in base.rglob('*.zig')},indent=2))
print(dst)

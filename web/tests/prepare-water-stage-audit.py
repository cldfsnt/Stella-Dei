#!/usr/bin/env python3
"""Observation-only paired phase and transport attribution; immutable source copies."""
from pathlib import Path
import shutil,json,hashlib
r=Path(__file__).resolve().parents[2]; base=r.parent/'site-tmp'
for mode,old in [('production','root-one-day-baseline'),('candidate','root-world-qa')]:
 out=base/('water-stage-'+mode);src=out/'src';shutil.copytree(base/old/'src',src,dirs_exist_ok=True)
 m=src/'main.zig';s=m.read_text().replace(str(base/old),str(out))
 if mode=='candidate':s=s.replace('for(0..arm_count)|arm|{','for(0..arm_count)|arm|{ if(arm!=1)continue;')
 m.write_text(s)
 p=src/'simulation/planet.zig';s=p.read_text();pos=s.index('    fn simulateAtmosphereWater(')
 soil='if(self.rootConfig.enabled){for(self.rootSoil)|w|sum+=w*self.getMeanPointArea()/1e9;}' if mode=='candidate' else ''
 s=s[:pos]+'''    fn qaWaterTotal(self:*Planet)f64{var sum:f64=0;for(self.waterMass,self.waterVaporMass)|l,v|sum+=@as(f64,l)+v; SOIL return sum;}
'''.replace('SOIL',soil)+s[pos:]
 needle='                std.mem.swap([]f32, &self.waterMass, &self.newWaterMass);';assert s.count(needle)==1
 s=s.replace(needle,'                const qa_before_transport=self.qaWaterTotal();\n'+needle)
 needle='                self.simulateAtmosphereWater(dt);';assert s.count(needle)==1
 s=s.replace(needle,'                @import("water_stage_audit.zig").transport=self.qaWaterTotal()-qa_before_transport;\n'+needle)
 needle='        const divider=self.getSubstanceDivider();';assert s.count(needle)==1
 s=s.replace(needle,'''        const qa=@import("water_stage_audit.zig"); const qa_before_phase=self.qaWaterTotal();
        var qa_legacy:f64=0;var qa_legacy_abs:f64=0;var qa_atmos:f64=0;var qa_soil:f64=0;
'''+needle)
 needle='            const saturation=@as(f64,getEquilibriumVaporPressure(temperature))*divider/(@as(f64,temperature)*k);';assert s.count(needle)==1
 s=s.replace(needle,needle+'''
            const qa_old=phase_step.phase(liquid,vapor,saturation,temperature,self.rainfall[i]) orelse unreachable;
            const qa_l:f32=@floatCast(qa_old.liquid);const qa_v:f32=@floatCast(qa_old.vapor);
            const qa_error=(@as(f64,qa_l)-liquid)+(@as(f64,qa_v)-vapor);
            qa_legacy+=qa_error;qa_legacy_abs+=@abs(qa_error);
''')
 if mode=='candidate':
  needle='                @import("root_scheduler_audit.zig").column('
  pos=s.index(needle)
  s=s[:pos]+'''                const qa_stage=column.stages[2];
                qa_atmos+=(@as(f64,qa_stage.liquid)-liquid)+(@as(f64,qa_stage.vapor)-vapor)+(qa_stage.soil-self.rootSoil[i])*self.getMeanPointArea()/1e9;
                qa_soil+=(@as(f64,column.state.liquid)-qa_stage.liquid)+(@as(f64,column.state.vapor)-qa_stage.vapor)+(column.state.soil-qa_stage.soil)*self.getMeanPointArea()/1e9;
'''+s[pos:]
 else:
  # mutable accumulators count original selected execution exactly
  needle='            self.waterMass[i]=@floatCast(result.liquid);';s=s.replace(needle,'            qa_atmos+=qa_error;qa_soil+=0;\n'+needle)
 needle='        // After the preceding swap, newWaterMass holds stale OLD liquid data.';assert s.count(needle)==1
 s=s.replace(needle,'        const qa_after_phase=self.qaWaterTotal();\n'+needle)
 needle='        std.mem.swap([]f32,&self.waterVaporMass,&self.newWaterVaporMass);';assert s.count(needle)==1
 s=s.replace(needle,needle+'''
        std.debug.print("WATER_STAGE {{\\"transport\\":{e},\\"phase_inventory\\":{e},\\"advection\\":{e},\\"same_input_legacy\\":{e},\\"same_input_legacy_abs\\":{e},\\"executed_atmos\\":{e},\\"soil_boundary\\":{e}}}\\n",.{qa.transport,qa_after_phase-qa_before_phase,self.qaWaterTotal()-qa_after_phase,qa_legacy,qa_legacy_abs,qa_atmos,qa_soil});
''')
 p.write_text(s);(src/'simulation/water_stage_audit.zig').write_text('pub var transport:f64=0;\n')
 (out/'provenance.json').write_text(json.dumps({'original':old,'files':{str(f.relative_to(src)):hashlib.sha256(f.read_bytes()).hexdigest()for f in [m,p,src/'simulation/water_stage_audit.zig']}},indent=2))
 print(out)

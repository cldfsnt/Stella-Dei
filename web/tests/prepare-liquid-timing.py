from pathlib import Path
import shutil,sys,re
r=Path(__file__).resolve().parents[2];base=r.parent/'site-tmp';mode=sys.argv[1];out=base/('liquid-timing-'+mode);source=base/('water-stage-production' if mode=='baseline' else 'liquid-gather-world')/'src';shutil.copytree(source,out/'src',dirs_exist_ok=True)
p=out/'src/simulation/planet.zig';prod=(r/'src/simulation/planet.zig').read_text()
if mode=='baseline':s=prod
else:
 s=p.read_text();start=s.index('    fn simulateAtmosphereWater(');end=s.index('    /// Compute partial pressure',start);ps=prod.index('    fn simulateAtmosphereWater(');pe=prod.index('    /// Compute partial pressure',ps);s=s[:start]+prod[ps:pe]+s[end:]
 s=s.replace('                const qa_before_transport=self.qaWaterTotal();\n','').replace('                @import("water_stage_audit.zig").transport=self.qaWaterTotal()-qa_before_transport;\n','')
 s=s.replace('                    const begin=std.time.nanoTimestamp();const n=self.waterMass.len;','                    const n=self.waterMass.len;').replace('                    const receipt=@import("liquid_gather.zig").step','                    _= @import("liquid_gather.zig").step')
 s=s.replace('                    const elapsed=std.time.nanoTimestamp()-begin;\n','');s=re.sub(r'                    std.debug.print\("LIQUID_GATHER[^\n]*\n','',s)
 (out/'src/simulation/liquid_gather.zig').write_text((r/'src/experimental/liquid_gather.zig').read_text())
p.write_text(s)
p=out/'src/main.zig';s=p.read_text().replace(str(source.parent),str(out));s=s.replace('            const ticks:usize=if(arm==0)60 else 420;','            var measured_ns:i128=0;\n            const ticks:usize=if(arm==0)60 else 420;')
needle='              if(tick>0){state.planet.simulate';assert s.count(needle)==1;s=s.replace(needle,'              if(tick>0){const measure_begin=std.time.nanoTimestamp();state.planet.simulate')
needle='state.gameTime+=1440;}\n              if(arm>0';assert s.count(needle)==1;s=s.replace(needle,'state.gameTime+=1440;measured_ns+=std.time.nanoTimestamp()-measure_begin;}\n              if(arm>0')
needle='            const path=try std.fmt.allocPrint';assert s.count(needle)==1;s=s.replace(needle,'            std.debug.print("FULLSTEP ns={d} ticks=60\\n",.{measured_ns});\n'+needle)
p.write_text(s);print(out)

#!/usr/bin/env python3
"""Copy production sources; alter only research scheduling and transfer telemetry."""
from pathlib import Path
import shutil,sys,hashlib
root=Path(__file__).resolve().parents[2]; dest=Path(sys.argv[1]).resolve()
assert not dest.exists(), 'fresh destination required'
shutil.copytree(root/'src',dest)
p=dest/'simulation/planet.zig';s=p.read_text();needle='                if(cell.cohorts[cohort].reproduction_credit>=0.01 and cell.cohorts[cohort].biomass>=0.02){';assert s.count(needle)==1
s='pub var research_policy:u8=0;\n'+s
prefix='''                if(research_policy>0 and cell.cohorts[cohort].reproduction_credit>=0.04){
                    if(Microbes.reproduce(cell,cohort,cell,&self.microbeStats,true))continue;
                    const large_neighbors=self.getNeighbours(i);
                    const large_start:usize=@intCast(Microbes.random(&cell.rng)%large_neighbors.len);
                    var large_done=false;
                    for(0..large_neighbors.len)|large_offset|{
                        const large_n=large_neighbors[(large_start+large_offset)%large_neighbors.len];
                        const large_env=self.microbeEnvironment(large_n,1);
                        if(!Microbes.habitable(large_env.depth_km,large_env.temperature))continue;
                        if(Microbes.reproduce(cell,cohort,&self.microbeCells[large_n],&self.microbeStats,true)){large_done=true;break;}
                    }
                    if(large_done)continue;
                }
'''
s=s.replace(needle,prefix+needle.replace('if(cell','if((research_policy!=2 or cell.cohorts[cohort].reproduction_credit>=0.04) and cell'))
# Candidate already tried original large route: do not retry it after failed fallback.
s=s.replace('                if (cell.cohorts[cohort].reproduction_credit < 0.04) continue;', '                if(research_policy>0)continue;\n                if (cell.cohorts[cohort].reproduction_credit < 0.04) continue;')
p.write_text(s)
p=dest/'simulation/microbes.zig';s=p.read_text();s=s.replace('const std = @import("std");','const std = @import("std");\npub var research_mass:f64=0;\npub var research_credit:f64=0;\npub var research_small:u64=0;\npub var research_large:u64=0;')
needle='    parent.support_mass-=child.support_mass;parent.biomass-=amount;';assert s.count(needle)==1
s=s.replace(needle,'    research_mass+=amount;research_credit+=credit;if(amount<0.006){research_small+=1;}else{research_large+=1;}\n'+needle);p.write_text(s)
print('Copied source baseline',hashlib.sha256((root/'src/simulation/planet.zig').read_bytes()).hexdigest())
print('Copied unchanged physiology with observational paid-transfer counters; policy0 remains original scheduling.')

#!/usr/bin/env python3
from pathlib import Path
import sys,subprocess
here=Path(__file__).resolve().parent;r=Path(sys.argv[1]).resolve()
subprocess.run([sys.executable,str(here/'prepare.py'),str(r)],check=True)
p=r/'main.zig';s=p.read_text();s=s.replace('0..1800','0..20').replace('tick==300','tick==3').replace('tick==900','tick==9')
a=s.index('                    // Equivalent changes');b=s.index('                    const Vec2=',a)
s=s[:a]+'''                    const cell:usize=42;
                    state.selectedPoint=cell;state.pointerOnPlanet=true;
                    std.debug.assert(state.testAction(if(tick==3)5 else 6));
                    state.planet.upload(game.loop,state.displayMode,state.axialTilt);loop.pump(1024);
'''+s[b:]
s=s.replace('steps=1800 days=30','steps=20 canonical_terrain=true direct_edges=true').replace('full_30day_hash_equal=true','full_20tick_hash_equal=true');p.write_text(s)
p=r/'simulation/planet.zig';s=p.read_text();needle='        const divider=self.getSubstanceDivider();const k:f64=1.380649e-23;';s=s.replace(needle,'''        if(self.atmosphericEdgeScratch.len==self.transformedPoints.len){
            for(self.atmosphericEdgeScratch,0..)|rates,i|for(self.getNeighbours(i),0..)|n,j|{
                std.debug.assert(rates[j]==self.atmosphericEdgeRate(i,n));
                std.debug.assert(self.cachedAtmosphericEdgeRate(n,i)==self.atmosphericEdgeRate(n,i));
            };
        }
'''+needle);p.write_text(s)

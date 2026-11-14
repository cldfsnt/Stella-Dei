from pathlib import Path
import subprocess,sys
here=Path(__file__).resolve().parent;out=Path(sys.argv[1]);subprocess.run([sys.executable,str(here/'egl-producer-world-prepare.py'),str(out)],check=True)
p=out/'main.zig';s=p.read_text()
s=s.replace('            edited+=1;','''            if(std.posix.getenv("STELLA_PRODUCER_SEED_NEIGHBORS") != null){state.pointerOnPlanet=true;const seeded=state.testAction(3);std.debug.print("PLAYER_SEED patch={d} success={} depth={d}\\n",.{neighbor,seeded,depth});}
            edited+=1;''')
s=s.replace('@as(usize,6000)','@as(usize,if(std.posix.getenv("STELLA_DIAGNOSTIC_DAYS")) |d| (std.fmt.parseInt(usize,d,10) catch 40)*60 else 2400)')
mark='            if(i%60==59){std.debug.print("HOURLY'
pos=s.index(mark)
add='''            if(i%60==59){
                const center=state.selectedPoint;
                var patches:[7]usize=undefined;patches[0]=idx;for(state.planet.getNeighbours(idx),0..)|n,k|patches[k+1]=n;
                for(patches)|patch|{
                    var depth=state.planet.waterMass[patch]*state.planet.getKmPerWaterMass()*1000;
                    if(std.posix.getenv("STELLA_PRODUCER_IRRIGATE") != null and depth<0.3){
                        state.selectedPoint=patch;var actions:usize=0;
                        while(depth<0.5 and actions<10):(actions+=1){_=state.adjustSelectedWater(@intCast(patch),0.1);depth=state.planet.waterMass[patch]*state.planet.getKmPerWaterMass()*1000;}
                        std.debug.print("PLAYER_IRRIGATE day={d} patch={d} actions={d} depth={d}\\n",.{(i+1)/60,patch,actions,depth});
                    }
                    const cc=state.planet.microbeCells[patch];
                    std.debug.print("PATCH day={d} index={d} depth={d} temp={d} nutrient={d}\\n",.{(i+1)/60,patch,depth,state.planet.temperature[patch],cc.nutrient});
                    for(cc.cohorts)|co|if(co.biomass>0){std.debug.print("LINEAGE day={d} patch={d} id={d} parent={d} generation={d} mass={d} support={d} organization={d} feeding={d} grazed={d} optimum={d}\\n",.{(i+1)/60,patch,co.lineage,co.parent,co.generation,co.biomass,co.support_mass,co.organization,co.feeding,co.lifetime_grazed,co.optimum});};
                }
                state.selectedPoint=center;
            }
'''
s=s[:pos]+add+s[pos:];s=s.replace('i%300==299','i%1200==1199');p.write_text(s)

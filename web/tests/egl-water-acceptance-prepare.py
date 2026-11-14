from pathlib import Path
import subprocess,sys,os
root=Path(__file__).resolve().parents[2];out=Path(sys.argv[1])
subprocess.run([sys.executable,str(root/'web/tests/egl-propagule-prepare.py'),str(out)],check=True)
p=out/'main.zig';s=p.read_text().replace(' production_15m=true',' water_candidate=true').replace('    std.debug.assert(state.planet.seedEligibility(state.selectedPoint)==.eligible);', '''    if(std.posix.getenv("QA_FIXED13508")!=null){state.selectedPoint=13508;state.pointerOnPlanet=true;}
    std.debug.assert(state.planet.seedEligibility(state.selectedPoint)==.eligible);
    for(state.planet.vertices,0..)|_,index|{
        const ns=state.planet.getNeighbours(index);
        for(ns,0..)|n,slot|{if(n==index)continue;std.debug.assert(n<state.planet.vertices.len);
            for(ns[0..slot])|previous|std.debug.assert(previous!=n);
            var reciprocal=false;for(state.planet.getNeighbours(n))|back|{if(back==index)reciprocal=true;}
            std.debug.assert(reciprocal);
        }
    }
    std.debug.print("WATER_TOPOLOGY reciprocal_unique_nonself=true\\n",.{});''').replace('std.debug.assert(@abs(state.planet.waterMass[patch]*state.planet.getKmPerWaterMass()*1000-depth)<0.001);', '''const expected_depth:f32=if(std.posix.getenv("QA_NURSERY")!=null and patch==center)5 else depth;
        std.debug.assert(@abs(state.planet.waterMass[patch]*state.planet.getKmPerWaterMass()*1000-expected_depth)<0.001);''').replace('        const idx=state.selectedPoint;', '''        const idx=state.selectedPoint;
        if(std.posix.getenv("QA_HYDRO")!=null)state.planet.qaHydroPoint=idx;
        std.debug.print("HYDRO_START cell={d} water={d} elevation={d} conversion={d}\\n",.{idx,state.planet.waterMass[idx],state.planet.elevation[idx],state.planet.getKmPerWaterMass()});''');p.write_text(s)
p=out/'pond_action.zig';s=p.read_text().replace('var base:f32=planet.elevation[selected];','const nursery=std.posix.getenv("QA_NURSERY")!=null;\n    var base:f32=planet.elevation[selected]-(if(nursery)@as(f32,0.010) else 0);').replace('if(slot<floor_count)base=@max(base,planet.elevation[idx]);','if(slot<floor_count)base=@max(base,planet.elevation[idx]-(if(nursery and slot==0)@as(f32,0.010) else 0));').replace('planet.waterMass[idx]=if(i<floor_count)floor_water_mass else 0;', 'planet.waterMass[idx]=if(i<floor_count)floor_water_mass else 0;\n        if(nursery and i==0){planet.elevation[idx]=base+0.010;planet.waterMass[idx]=0.005/conversion;}');p.write_text(s)
p=out/'simulation/planet.zig';s=p.read_text().replace('    microbeStats: Microbes.Stats = .{},','    microbeStats: Microbes.Stats = .{},\n    qaHydroPoint:?usize=null,\n    qaHydroStep:usize=0,');s=s.replace('            self.waterMass[i]=@floatCast(result.liquid);', '''            if(self.qaHydroPoint)|point|{if(point==i)std.debug.print("HYDRO_PHASE step={d} evaporated={d} condensed={d}\\n",.{self.qaHydroStep,result.evaporated,result.condensed});}
            self.waterMass[i]=@floatCast(result.liquid);''').replace('        std.mem.swap([]f32,&self.waterVaporMass,&self.newWaterVaporMass);','        self.qaHydroStep+=1;\n        std.mem.swap([]f32,&self.waterVaporMass,&self.newWaterVaporMass);');s=s.replace('                self.newWaterMass[target[i]] += transmitted[i];', '''                if(self.qaHydroPoint)|point|{if(transmitted[i]>0 and (origin[i]==point or target[i]==point))std.debug.print("HYDRO_FLOW step={d} from={d} to={d} mass={d}\\n",.{self.qaHydroStep,origin[i],target[i],transmitted[i]});}
                self.newWaterMass[target[i]] += transmitted[i];''');p.write_text(s)

# Optional read-only focus implementation from the current production UI.
focus=Path(os.environ.get("QA_FOCUS_SOURCE",str(root/'src/states/play.zig'))).read_text()
a=focus.index('    pub fn focusSeedableHabitat(');b=focus.index('    pub fn focusLand(',a)
p=out/'states/play.zig';s=p.read_text();x=s.index('    pub fn focusSeedableHabitat(');y=s.index('    pub fn focusLand(',x);p.write_text(s[:x]+focus[a:b]+s[y:])

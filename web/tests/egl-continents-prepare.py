#!/usr/bin/env python3
"""Current fixed-step engine: read-only climate survey plus explicit nursery override."""
from pathlib import Path
import subprocess,sys
here=Path(__file__).resolve().parent;out=Path(sys.argv[1])
subprocess.run([sys.executable,str(here/'egl-nursery-prepare.py'),str(out)],check=True)
p=out/'states/play.zig';ps=p.read_text().replace('seed, .{}) catch unreachable','seed, .{.water_preset=if(std.posix.getenv("QA_CONTINENTS")!=null) .continents else .random}) catch unreachable');p.write_text(ps)
p=out/'main.zig';s=p.read_text()
needle='    std.debug.assert(state.planet.seedEligibility(state.selectedPoint)==.eligible);'
s=s.replace(needle,'''    if(std.posix.getenv("QA_NURSERY_CELL"))|value|{
        state.selectedPoint=try std.fmt.parseInt(usize,value,10);
        std.debug.assert(state.selectedPoint<state.planet.microbeCells.len);
        std.debug.print("EXPLICIT_NURSERY_LOCATION cell={d} actual_terrain_water_action=true\\n",.{state.selectedPoint});
    }else std.debug.assert(state.planet.seedEligibility(state.selectedPoint)==.eligible);''')
needle='        var fixed_before=state.planet.microbeStats.fixed_carbon;'
s=s.replace(needle,'''        const scan_n=state.planet.waterMass.len;
        const scan_dry=try allocator.alloc(u32,scan_n);defer allocator.free(scan_dry);@memset(scan_dry,0);
        const scan_tmin=try allocator.alloc(f32,scan_n);defer allocator.free(scan_tmin);@memset(scan_tmin,10000);
        const scan_tmax=try allocator.alloc(f32,scan_n);defer allocator.free(scan_tmax);@memset(scan_tmax,0);
        const scan_tsum=try allocator.alloc(f64,scan_n);defer allocator.free(scan_tsum);@memset(scan_tsum,0);
        var scan_steps:u32=0;var scan_last_time=state.gameTime;
'''+needle)
needle='            state.update(&game,1.0/60.0);'
# Only coupled-loop occurrence, after marker.
pos=s.index('        const scan_n=');a=s[:pos];b=s[pos:]
b=b.replace(needle,needle+'''
            if(state.gameTime>scan_last_time){
                scan_last_time=state.gameTime;scan_steps+=1;
                for(state.planet.waterMass,state.planet.temperature,0..)|water,temp,cell|{
                    if(water==0)scan_dry[cell]+=1;
                    scan_tmin[cell]=@min(scan_tmin[cell],temp);scan_tmax[cell]=@max(scan_tmax[cell],temp);scan_tsum[cell]+=temp;
                }
            }''',1);s=a+b
pos=s.index('        std.debug.print("TOTAL_WATER');end=s.index('\n',pos)
s=s[:end]+'''
        if(std.posix.getenv("QA_CLIMATE_SCAN_PATH"))|scan_path|{
            var scan_file=try std.fs.createFileAbsolute(scan_path,.{});defer scan_file.close();
            const writer=scan_file.writer();
            try writer.writeAll("cell,dry_fraction,temp_min,temp_max,temp_mean,water_m\\n");
            for(0..scan_n)|cell|try writer.print("{d},{d},{d},{d},{d},{d}\\n",.{cell,@as(f64,@floatFromInt(scan_dry[cell]))/@as(f64,@floatFromInt(scan_steps)),scan_tmin[cell],scan_tmax[cell],scan_tsum[cell]/@as(f64,@floatFromInt(scan_steps)),state.planet.waterMass[cell]*state.planet.getKmPerWaterMass()*1000});
        }
        var best_ids:[10]usize=.{0}**10;var best_scores:[10]f64=.{-1}**10;
        if(scan_steps>0)for(0..scan_n)|cell|{
            const mean=scan_tsum[cell]/@as(f64,@floatFromInt(scan_steps));
            const dry_fraction=@as(f64,@floatFromInt(scan_dry[cell]))/@as(f64,@floatFromInt(scan_steps));
            if(scan_tmin[cell]<260 or scan_tmax[cell]>355 or mean<285 or mean>325 or dry_fraction<0.05)continue;
            const score=dry_fraction*1000-@abs(mean-303);
            for(0..10)|rank|if(score>best_scores[rank]){
                var slot:usize=9;while(slot>rank):(slot-=1){best_scores[slot]=best_scores[slot-1];best_ids[slot]=best_ids[slot-1];}
                best_scores[rank]=score;best_ids[rank]=cell;break;
            };
        };
        std.debug.print("CLIMATE_SCAN physical_ticks={d} game_time={d} fixed_quantum=1440 biological_edits=false\\n",.{scan_steps,state.gameTime});
        for(best_ids,best_scores)|cell,score|if(score>=0){
            std.debug.print("CLIMATE_DRY_CANDIDATE cell={d} dry_fraction={d} temp_min={d} temp_max={d} temp_mean={d} latitude_z={d} actual_water_m={d}\\n",.{cell,@as(f64,@floatFromInt(scan_dry[cell]))/@as(f64,@floatFromInt(scan_steps)),scan_tmin[cell],scan_tmax[cell],scan_tsum[cell]/@as(f64,@floatFromInt(scan_steps)),state.planet.vertices[cell].z(),state.planet.waterMass[cell]*state.planet.getKmPerWaterMass()*1000});
        };
'''+s[end:]
p.write_text(s)

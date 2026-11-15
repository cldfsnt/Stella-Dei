#!/usr/bin/env python3
"""Fixed actual Sandbox coupled comparison, QA-only finite-foraging branch."""
from pathlib import Path
import sys,subprocess,json,hashlib
r=Path(__file__).resolve().parents[2];o=Path(sys.argv[1]).resolve();subprocess.run([sys.executable,str(r/'web/tests/egl-playable-ecology-prepare.py'),str(o)],check=True)
p=o/'simulation/life.zig';s=p.read_text();s=s.replace('const std = @import("std");','''const std = @import("std");
pub var qa_finite_foraging:bool=false;
pub var qa_food_removed:f64=0;pub var qa_satiety_credit:f64=0;pub var qa_credit_error_abs:f64=0;pub var qa_fragments:u64=0;
pub fn qaReset()void{qa_food_removed=0;qa_satiety_credit=0;qa_credit_error_abs=0;qa_fragments=0;}
''')
a=s.index('        if (self.satiety < 85 and planet.vegetation[idx] > 0.01) {');b=s.index('        if (self.state == .gestation)',a);old=s[a:b]
s=s[:a]+'''        const qa_cover=planet.vegetation[idx];const qa_satiety=self.satiety;
        if(qa_finite_foraging){
            if(self.satiety<85 and planet.vegetation[idx]>0){
                const F=@import("../experimental/sandbox_foraging.zig");const bite=F.take(planet.vegetation[idx],self.satiety,dt);
                if(bite.eaten>0){planet.vegetation[idx]=bite.after;self.satiety=F.fedSatiety(self.satiety,bite.eaten);planet.rabbitMeals+=1;if(bite.fragment)qa_fragments+=1;}
            }
        }else{
'''+old+'''
        }
        const qa_removed=@as(f64,qa_cover)-planet.vegetation[idx];const qa_credit=@as(f64,self.satiety)-qa_satiety;
        qa_food_removed+=qa_removed;qa_satiety_credit+=qa_credit;qa_credit_error_abs+=@abs(qa_credit-qa_removed*150);
'''+s[b:];p.write_text(s)
p=o/'main.zig';s=p.read_text().replace('game.startOriginNext = true;','game.startOriginNext = false;');a=s.index('    const M=@import("simulation/microbes.zig");var state=');b=s.index('\nfn originReport(',a)
s=s[:a]+r'''
    var state=&game.state.Playing;state.paused=true;state.selectedTool=.None;state.showEscapeMenu=false;
    const saves=@import("save_game.zig");const Life=@import("simulation/life.zig");
    var arena=std.heap.ArenaAllocator.init(allocator);const qa=arena.allocator();
    render(window);gl.finish();window.swapBuffers();std.debug.assert(state.planet.worldMode==.sandbox);
    const seed=try std.fmt.parseInt(u64,std.posix.getenv("QA_FLOW_SEED") orelse "42",10);
    const dt=try std.fmt.parseFloat(f32,std.posix.getenv("QA_RABBIT_DT") orelse "1440");const steps:usize=@intFromFloat(86400/dt);
    const empty_bytes=try std.json.stringifyAlloc(qa,try saves.capture(qa,state),.{});const empty=try std.json.parseFromSlice(saves.schema.Save,qa,empty_bytes,.{.allocate=.alloc_always});
    const conv=state.planet.getKmPerWaterMass();var footprint:[19]usize=undefined;var chosen:?usize=null;
    for(0..state.planet.waterMass.len)|i|{
        var ids:[19]usize=undefined;ids[0]=i;var count:usize=1;
        for(state.planet.getNeighbours(i))|n|{var dup=false;for(ids[0..count])|x|if(x==n){dup=true;};if(!dup and count<7){ids[count]=n;count+=1;}}
        const first=count;var overflow=false;
        for(ids[0..first])|n|for(state.planet.getNeighbours(n))|x|{var dup=false;for(ids[0..count])|v|if(v==x){dup=true;};if(!dup){if(count==19){overflow=true;break;}ids[count]=x;count+=1;}};
        if(overflow or count!=19)continue;var valid=true;
        for(ids)|x|{if(state.planet.waterMass[x]*conv>0.0005 or state.planet.temperature[x]<280 or state.planet.temperature[x]>310)valid=false;}
        if(valid){chosen=i;footprint=ids;break;}
    }
    if(chosen==null){std.debug.print("FORAGING_UNAVAILABLE seed={} no_fixed_dry_19patch=true\n",.{seed});std.process.exit(0);}
    const center=chosen.?;const n=state.planet.waterMass.len;const island=try qa.alloc(bool,n);@memset(island,false);const queue=try qa.alloc(usize,n);queue[0]=center;island[center]=true;var head:usize=0;var count:usize=1;
    while(head<count):(head+=1){for(state.planet.getNeighbours(queue[head]))|x|if(!island[x] and state.planet.waterMass[x]*conv<=0.0005){island[x]=true;queue[count]=x;count+=1;};}
    std.debug.print("FORAGING_SETUP seed={} center={} island_cells={} footprint={any} dt={d}\n",.{seed,center,count,footprint,dt});
    for([_]usize{4,16})|stock|{
        if(dt!=1440 and stock!=4)continue;
        try saves.apply(state,empty.value);state.selectedPoint=center;
        for(footprint)|x|{state.selectedPoint=x;state.pointerOnPlanet=true;std.debug.assert(state.testAction(3));}
        state.selectedPoint=center;const point=state.planet.transformedPoints[center];
        const tangent=point.cross(if(@abs(point.norm().z())<0.9)za.Vec3.new(0,0,1) else za.Vec3.new(0,1,0)).norm();
        for(0..stock)|i|{
            const offset=@as(f32,@floatFromInt(i%4))*15;var rabbit=Life.Lifeform.init(point.add(tangent.scale(offset)).norm().scale(point.length()),.Rabbit,state.gameTime);
            rabbit.prng=std.rand.DefaultPrng.init(seed*%1000+%i);rabbit.genome.gender=if(i%2==0).Female else .Male;
            try state.planet.addLifeform(rabbit);
        }
        const initial_bytes=try std.json.stringifyAlloc(qa,try saves.capture(qa,state),.{});const initial=try std.json.parseFromSlice(saves.schema.Save,qa,initial_bytes,.{.allocate=.alloc_always});
        try std.fs.cwd().writeFile(.{.sub_path=try std.fmt.allocPrint(qa,"OUTPUT/input-{d}-{d}-{d}.json",.{seed,stock,@as(u32,@intFromFloat(dt))}),.data=initial_bytes});
        for(0..2)|arm|{
            try saves.apply(state,initial.value);Life.qa_finite_foraging=arm==1;Life.qaReset();
            const previous=try qa.alloc(f32,n);@memcpy(previous,state.planet.vegetation);var extinctions:usize=0;var recoveries:usize=0;
            for(0..14)|day|{
                for(0..steps)|_|{loop.pump(16);state.planet.simulate(game.loop,.{.dt=dt,.timeScale=1,.solarConstant=state.solarConstant,.gameTime=state.gameTime,.planetRotationTime=state.planetRotationTime,.solarVector=state.simulationSolarVector()});state.gameTime+=dt;loop.pump(16);}
                var cover:f64=0;var island_cover:f64=0;var living:usize=0;var low:usize=0;var island_living:usize=0;var min_sat:f32=100;var mean_sat:f64=0;var distance:f64=0;
                for(state.planet.vegetation,0..)|v,i|{std.debug.assert(std.math.isFinite(v) and v>=0 and v<=1);cover+=v;if(v>0)living+=1;if(v>0 and v<0.01)low+=1;if(island[i]){island_cover+=v;if(v>0)island_living+=1;}if(previous[i]>0 and v==0)extinctions+=1;if(previous[i]==0 and v>0)recoveries+=1;previous[i]=v;}
                for(state.planet.lifeforms.items)|rabbit|{std.debug.assert(std.math.isFinite(rabbit.satiety));min_sat=@min(min_sat,rabbit.satiety);mean_sat+=rabbit.satiety;distance+=rabbit.position.distance(point);}
                std.debug.print("FORAGING_DAY {s}\n",.{try std.json.stringifyAlloc(qa,.{.seed=seed,.stock=stock,.arm=arm,.dt=dt,.day=day+1,.cover=cover,.island_cover=island_cover,.living_patches=living,.low_patches=low,.island_living=island_living,.extinctions=extinctions,.recoveries=recoveries,.rabbits=state.planet.lifeforms.items.len,.births=state.planet.rabbitBirths,.deaths=state.planet.rabbitDeaths,.meals=state.planet.rabbitMeals,.minimum_satiety=min_sat,.sum_satiety=mean_sat,.distance_from_start_sum=distance,.food_removed=Life.qa_food_removed,.satiety_credit=Life.qa_satiety_credit,.credit_error_abs=Life.qa_credit_error_abs,.fragment_meals=Life.qa_fragments,.plant_births=state.planet.plantBirths,.center_cover=state.planet.vegetation[center],.center_depth_m=state.planet.waterMass[center]*conv*1000,.center_temperature=state.planet.temperature[center]},.{})});
            }
            const end_bytes=try std.json.stringifyAlloc(qa,try saves.capture(qa,state),.{});const ending=try std.json.parseFromSlice(saves.schema.Save,qa,end_bytes,.{.allocate=.alloc_always});
            try std.fs.cwd().writeFile(.{.sub_path=try std.fmt.allocPrint(qa,"OUTPUT/end-{d}-{d}-{d}-{d}.json",.{seed,stock,@as(u32,@intFromFloat(dt)),arm}),.data=end_bytes});
            try saves.apply(state,ending.value);std.debug.assert(std.mem.eql(u8,end_bytes,try std.json.stringifyAlloc(qa,try saves.capture(qa,state),.{})));
            std.debug.print("FORAGING_ARM_PASS seed={} stock={} dt={d} arm={} endpoint_reload_exact=true\n",.{seed,stock,dt,arm});
        }
    }
    try saves.apply(state,empty.value);std.debug.assert(std.mem.eql(u8,empty_bytes,try std.json.stringifyAlloc(qa,try saves.capture(qa,state),.{})));
    std.debug.print("FORAGING_PASS original_restored=true explicit_qa_exit=true\n",.{});std.process.exit(0);
}
''' .replace('OUTPUT',str(o.parent))+s[b:];p.write_text(s)
subprocess.run([sys.executable,str(r/'web/tests/audit-zig-exports.py'),str(r/'src/main.zig'),str(p)],check=True,stdout=(o.parent/'export-audit.json').open('w'))
(o.parent/'foraging-provenance.json').write_text(json.dumps({'head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=r,text=True).strip(),'source':{f:{'production':hashlib.sha256((r/'src'/f).read_bytes()).hexdigest(),'copy':hashlib.sha256((o/f).read_bytes()).hexdigest()}for f in ['simulation/life.zig','simulation/planet.zig','simulation/ecology.zig','states/play.zig','main.zig','experimental/sandbox_foraging.zig']}},indent=2)+'\n')

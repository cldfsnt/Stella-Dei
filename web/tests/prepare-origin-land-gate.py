#!/usr/bin/env python3
from pathlib import Path
import shutil,subprocess,json,hashlib
r=Path(__file__).resolve().parents[2];base=r.parent/'site-tmp/origin-land-gate';shared=r.parent/'site-tmp/origin-land-beta/src'
for kind,source in [('baseline',r/'src'),('candidate',shared)]:
 o=base/kind/'src';shutil.copytree(source,o,dirs_exist_ok=True)
 p=o/'states/play.zig';p.write_text(p.read_text().replace('var randomPrng = std.rand.DefaultPrng.init(@as(u64, @bitCast(std.time.milliTimestamp())));','var randomPrng = std.rand.DefaultPrng.init(1337);').replace('const subdivisions: usize = if (@import("builtin").target.cpu.arch == .wasm32 or @import("builtin").mode == .Debug) 6 else 7;','const subdivisions: usize = 6; // QA saved topology, not physics'))
 p=o/'audio.zig';s=p.read_text().replace('if (c.ma_engine_init(null, engine)','var config = c.ma_engine_config_init();config.noDevice=c.MA_TRUE;config.channels=2;config.sampleRate=48000;\n        if (c.ma_engine_init(&config, engine)');p.write_text(s)
 p=o/'loop.zig';s=p.read_text().replace('const is_web = @import("builtin").target.cpu.arch == .wasm32;','const is_web = true;');p.write_text(s)
 p=o/'main.zig';s=p.read_text().replace('nosuspend game.setState(MainMenuState);','game.startOriginNext=true;nosuspend game.setState(PlayState);').replace('nosuspend game.setState(SplashScreenState);','game.startOriginNext=true;nosuspend game.setState(PlayState);')
 a=s.index('    std.log.debug("Creating update loop job.."');b=s.index('\nconst expect =',a)
 gate=r'''    const saves=@import("save_game.zig");const P=@import("simulation/planet.zig").Planet;
    var arena=std.heap.ArenaAllocator.init(allocator);defer arena.deinit();const a=arena.allocator();var state=&game.state.Playing;
NEW_BLOCK
    if(std.posix.getenv("QA_LAND_INPUT"))|path|{const bytes=try std.fs.cwd().readFileAlloc(a,path,128*1024*1024);const parsed=try std.json.parseFromSlice(saves.schema.Save,a,bytes,.{.allocate=.alloc_always});try saves.apply(state,parsed.value);}
    const initial=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});const owned=try std.json.parseFromSlice(saves.schema.Save,a,initial,.{.allocate=.alloc_always});try saves.apply(state,owned.value);std.debug.assert(std.mem.eql(u8,initial,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
    if(@hasField(@TypeOf(state.planet),"landBeta"))if(state.planet.landBeta.enabled){
        try state.planet.beginOrigin();std.debug.assert(std.mem.eql(u8,initial,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
        var invalid=owned.value;invalid.version=999;
        if(saves.apply(state,invalid)) |_| unreachable else |_| {}
        std.debug.assert(std.mem.eql(u8,initial,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
        invalid=owned.value;invalid.beta_origin.?.config.law=2;
        if(saves.apply(state,invalid)) |_| unreachable else |_| {}
        std.debug.assert(std.mem.eql(u8,initial,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
        std.debug.print("LAND_NATIVE beginOrigin_idempotent=true invalid_version_law_atomic=true\n",.{});
    };
    const ticks=try std.fmt.parseInt(usize,std.posix.getenv("QA_LAND_TICKS") orelse "10",10);
    for(0..ticks)|_|{state.planet.simulate(game.loop,.{.dt=1440,.timeScale=1,.solarConstant=state.solarConstant,.gameTime=state.gameTime,.planetRotationTime=state.planetRotationTime,.solarVector=state.simulationSolarVector()});state.gameTime+=1440;}
    const ending=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});try std.fs.cwd().writeFile(.{.sub_path=std.posix.getenv("QA_LAND_OUTPUT").?,.data=ending});
    const parsed=try std.json.parseFromSlice(saves.schema.Save,a,ending,.{.allocate=.alloc_always});try saves.apply(state,parsed.value);std.debug.assert(std.mem.eql(u8,ending,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
    if(std.posix.getenv("QA_LAND_RESET"))|path|{const bytes=try std.fs.cwd().readFileAlloc(a,path,128*1024*1024);const old=try std.json.parseFromSlice(saves.schema.Save,a,bytes,.{.allocate=.alloc_always});try saves.apply(state,old.value);
        if(@hasField(@TypeOf(state.planet),"landBeta")){std.debug.assert(!state.planet.landBeta.enabled);for(state.planet.landSoil)|v|std.debug.assert(v==0);for(state.planet.landVapor)|v|std.debug.assert(v==0);for(state.planet.microbeCells)|cell|for(cell.cohorts)|co|std.debug.assert(co.root_fraction==0);}
        std.debug.print("LAND_NATIVE legacy_reset_off=true\n",.{});
    }
    std.debug.print("LAND_GATE ticks={} full_reload_exact=true bytes={}\n",.{ticks,ending.len});std.process.exit(0);
}
'''
 if kind=='candidate':new=r'''    if(std.posix.getenv("QA_LAND_NEW")!=null){
        state.planet=try P.generate(allocator,6,5000,42,.{.land_beta=true});state.gameTime=0;
        std.debug.assert(state.planet.landBeta.enabled);for(state.planet.landSoil)|x|std.debug.assert(x==0);for(state.planet.landVapor,state.planet.waterVaporMass)|v,f|std.debug.assert(v==f);for(state.planet.microbeCells)|c|for(c.cohorts)|co|std.debug.assert(co.root_fraction==0 and co.biomass==0);
        std.debug.print("LAND_NEW generated=true zero_soil_roots=true exact_generator_vapor=true\n",.{});
    }
'''
 else:new='    _=P;'
 s=s[:a]+gate.replace('NEW_BLOCK',new)+s[b:];p.write_text(s)
 (o.parent/'manifest.json').write_text(json.dumps({str(f.relative_to(o)):hashlib.sha256(f.read_bytes()).hexdigest()for f in o.rglob('*.zig')},indent=2)+'\n')
print(base)

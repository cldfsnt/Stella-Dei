from pathlib import Path
import hashlib,json
r=Path(__file__).resolve().parents[2]
qa='''
    const saves=@import("save_game.zig");var arena=std.heap.ArenaAllocator.init(allocator);defer arena.deinit();const a=arena.allocator();const state=&game.state.Playing;
    const bytes=try std.fs.cwd().readFileAlloc(a,"INPUT",128*1024*1024);const parsed=try saves.schema.parse(a,bytes);try saves.apply(state,parsed.value);loop.pump(4096);
    std.debug.assert(state.planet.landBeta.physiology_law==3);
    const initial=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});std.debug.assert(std.mem.eql(u8,bytes,initial));
    for(0..2)|_|{state.planet.simulate(game.loop,.{.dt=1440,.timeScale=1,.solarConstant=state.solarConstant,.gameTime=state.gameTime,.planetRotationTime=state.planetRotationTime,.solarVector=state.simulationSolarVector()});state.gameTime+=1440;}
    try std.fs.cwd().writeFile(.{.sub_path="OUTPUT/endpoint.json",.data=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})});std.debug.print("HISTORICAL_DAY21_LAW3_TWO_TICKS_PASS\\n",.{});std.process.exit(0);
}
'''
for label,source in [('reference','rooted-natural-owner'),('candidate','root-wind-combined')]:
 s=(r/'web/tests/prepare-rooted-player.py').read_text().split('# Reuse frozen observational hooks')[0]
 s=s.replace("b=t/'rooted-player'",f"b=t/'combined-history-{label}'").replace("src=t/'rooted-founder/src'",f"src=t/'{source}/src'").replace("(r/'web/tests/rooted-player-qa.txt').read_text()",'qa')
 exec(compile(s,str(r/'web/tests/prepare-rooted-player.py'),'exec'))
 (b/'source-hashes.json').write_text(json.dumps({str(p.relative_to(o)):hashlib.sha256(p.read_bytes()).hexdigest()for p in o.rglob('*.zig')},indent=2))

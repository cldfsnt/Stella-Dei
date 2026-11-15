from pathlib import Path
import shutil,json,hashlib
r=Path(__file__).resolve().parents[2];o=r.parent/'site-tmp/wetlands-preview';assert not o.exists();o.mkdir();src=r.parent/'site-tmp/law3-canonical/candidate/src';shutil.copytree(src,o/'src')
for name in ['deps','assets']: (o/name).symlink_to(r/name,target_is_directory=True)
for name in ['web-build.zig','build.zig','build.zig.zon','LICENSE']:shutil.copyfile(r/name,o/name)
shutil.copytree(r/'web',o/'web',ignore=shutil.ignore_patterns('dist','continuation-review','__pycache__'))
p=o/'src/simulation/planet.zig';s=p.read_text();s=s.replace('pub var qa_stages:[4]f64=.{0,0,0,0};\npub var qa_substages:[5]f64=.{0,0,0,0,0};\n','',1)
s=s.replace('land_beta:bool=false,','land_beta:bool=false,\n        land_beta_physiology:u8=1,',1).replace('        if(options.land_beta and !options.generate_terrain)', '        if(options.land_beta_physiology<1 or options.land_beta_physiology>3 or (!options.land_beta and options.land_beta_physiology!=1))return error.InvalidBetaPhysiology;\n        if(options.land_beta and !options.generate_terrain)',1)
s=s.replace('planet.landBeta=.{.enabled=true,.law=1,.root_mutation=', 'planet.landBeta=.{.enabled=true,.law=1,.physiology_law=options.land_beta_physiology,.root_mutation=',1);p.write_text(s)
p=o/'src/states/play.zig';s=p.read_text().replace('var state = initNewWorld(game, subdivisions, game.newWorldChoice.preset);','const wetlands=game.startWetlandsNext;game.startWetlandsNext=false;\n        var state = initNewWorld(game, subdivisions, game.newWorldChoice.preset, wetlands);').replace('if (game.startOriginNext) {','if (game.startOriginNext or wetlands) {',1).replace('return initNewWorld(game, subdivisions, .random);','return initNewWorld(game, subdivisions, .random, false);').replace('preset: @import("../world_setup.zig").Preset) PlayState {','preset: @import("../world_setup.zig").Preset, wetlands:bool) PlayState {',1).replace('.{.water_preset=preset}) catch unreachable;','.{.water_preset=preset,.land_beta=wetlands,.land_beta_physiology=if(wetlands)3 else 1}) catch unreachable;',1)
s=s.replace('            state.mobileFeedbackSeconds = 8;','            if(wetlands)state.mobileFeedback="Wetlands experiment: seed in shallow water; roots may emerge through offspring";\n            state.mobileFeedbackSeconds = 8;',1);p.write_text(s)
p=o/'src/main.zig';s=p.read_text().replace('    startOriginNext: bool = false,','    startOriginNext: bool = false,\n    startWetlandsNext:bool=false,',1)
s+='''
// Preview-only explicit fresh factory. Never converts the current saved world.
pub fn wetlandsNewForGame(g:*Game,expected:u32)i32 {
    if(!g.state_init)return -1;
    if(expected!=PerformanceDetails.world_serial)return -2;
    if(AdvanceDay.blocksInput())return -3;
    switch(g.state){
      .Playing=>|*v|{if(v.planet.normalComputeJob)|job|if(!job.isCompleted())return -3;},
      .MainMenu=>|*v|{if(v.planet.normalComputeJob)|job|if(!job.isCompleted())return -3;},
      else=>return -1,
    }
    g.startWetlandsNext=true;g.startOriginNext=false;g.setState(PlayState);return 1;
}
export fn stella_wetlands_new(expected:u32)i32 {
    if(!is_web or !web_initialized)return -1;
    web_loop.pump(1024);return wetlandsNewForGame(&game,expected);
}
export fn stella_wetlands_snapshot()[*:0]const u8 {return @import("wetlands_view.zig").snapshot(webPlayState(),PerformanceDetails.world_serial);}
''';p.write_text(s)
shutil.copyfile(r/'web/tests/wetlands-view.zig',o/'src/wetlands_view.zig')
p=o/'src/save_game.zig';p.write_text(p.read_text().replace('/saves','/wetlands-saves'))
p=o/'web/build.sh';s=p.read_text().replace('-Dweb-gl-debug="$WEB_GL_DEBUG"', '-Dweb-gl-debug="$WEB_GL_DEBUG" -Dsysroot="$TOOLS/emsdk/upstream/emscripten/cache/sysroot"').replace('-sEXPORTED_FUNCTIONS=', '-sEXPORTED_FUNCTIONS=_stella_wetlands_new,_stella_wetlands_snapshot,',1);p.write_text(s)
(o/'engine-source-sha256.json').write_text(json.dumps({str(p.relative_to(o/'src')):hashlib.sha256(p.read_bytes()).hexdigest()for p in (o/'src').rglob('*.zig')},indent=2)+'\n');print(o)

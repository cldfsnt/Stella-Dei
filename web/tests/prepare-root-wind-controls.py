from pathlib import Path
import shutil
r=Path(__file__).resolve().parents[2];t=r.parent/'site-tmp';base=t/'root-wind-combined/src';dst=t/'root-wind-controls/src';assert not dst.exists();shutil.copytree(base,dst)
p=dst/'main.zig';s=p.read_text().replace('    startWetlandsNext:bool=false,','    startWetlandsNext:bool=false,\n    startCombinedNext:bool=false,',1)
s=s.replace('g.startWetlandsNext=true;g.startOriginNext=false;g.setState(PlayState);return 1;','g.startCombinedNext=false;g.startWetlandsNext=true;g.startOriginNext=false;g.setState(PlayState);return 1;',1)
factory=s[s.index('pub fn wetlandsNewForGame'):s.index('export fn stella_wetlands_snapshot')];factory=factory.replace('wetlandsNewForGame','combinedNewForGame').replace('stella_wetlands_new','stella_wetlands_combined_new').replace('g.startCombinedNext=false','g.startCombinedNext=true')
s+='\n'+factory+'\nexport fn stella_combined_snapshot()[*:0]const u8{return @import("combined_view.zig").snapshot(webPlayState(),PerformanceDetails.world_serial);}\n'
w=(t/'wind-dispersal/src/main.zig').read_text();a=w.index('pub fn pioneerForState');b=w.index('// The user has explicitly opened',a);api=w[a:b].replace('@import("wind_view.zig").writerVersion(state)','@import("combined_view.zig").writerVersion(state)');s+=api
s+='''
export fn stella_auto_seed_pioneer_start(world:u32)[*:0]const u8{return if(webEditableState())|state|AutoSeed.startPioneer(state,PerformanceDetails.world_serial,world).ptr else "{\\"ok\\":false,\\"phase\\":\\"failed\\",\\"reason\\":\\"World unavailable\\"}";}
''';p.write_text(s)
p=dst/'states/play.zig';s=p.read_text().replace('const wetlands=game.startWetlandsNext;game.startWetlandsNext=false;','const wetlands=game.startWetlandsNext;game.startWetlandsNext=false;const combined=game.startCombinedNext;game.startCombinedNext=false;');s=s.replace('initNewWorld(game, subdivisions, game.newWorldChoice.preset, wetlands)','initNewWorld(game, subdivisions, game.newWorldChoice.preset, wetlands,combined)').replace('initNewWorld(game, subdivisions, .random, false)','initNewWorld(game, subdivisions, .random, false,false)').replace('wetlands:bool) PlayState','wetlands:bool,combined:bool) PlayState').replace('.land_beta=wetlands,.land_beta_physiology=', '.land_beta=wetlands,.combined_wind=combined,.land_beta_physiology=');p.write_text(s)
s=(t/'wind-dispersal/src/auto_seed.zig').read_text().replace('return std.meta.eql(state.planet.windDispersal,p.original.windDispersal) and','return std.meta.eql(state.planet.landBeta,p.original.landBeta) and std.meta.eql(state.planet.windDispersal,p.original.windDispersal) and').replace(' if(!std.meta.eql(live.windDispersal',' if(!std.meta.eql(live.landBeta,p.original.landBeta))return false;\n if(!std.meta.eql(live.windDispersal');(dst/'auto_seed.zig').write_text(s)
shutil.copyfile(r/'web/tests/root-wind-controls-view.zig',dst/'combined_view.zig')
print(dst)

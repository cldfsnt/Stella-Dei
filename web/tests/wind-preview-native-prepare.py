from pathlib import Path
import sys
r=Path(sys.argv[1]);s=r/'src'
p=s/'save_game.zig';x=p.read_text();assert '"/saves/world.json"' in x;x=x.replace('Browser shell syncs /saves to IndexedDB explicitly.','Wind preview shell syncs /wind-saves to IndexedDB explicitly.');x=x.replace('"/saves/world.json"','"/wind-saves/world.json"').replace('"/saves/world.tmp"','"/wind-saves/world.tmp"').replace('makePath("/saves")','makePath("/wind-saves")');p.write_text(x)
p=s/'main.zig';x=p.read_text();needle='    game.setState(MainMenuState);\n    web_initialized = true;';assert x.count(needle)==1;x=x.replace(needle,'    startWindPreview(&game);\n    web_initialized = true;')
x+='''
// The user has explicitly opened /wind/ and pressed Play. One fresh Origin only.
pub fn startWindPreview(g:*Game)void {g.startWindNext=true;g.startOriginNext=false;g.setState(PlayState);}
export fn stella_auto_seed_pioneer_start(world:u32)[*:0]const u8 {
    return if(webEditableState())|state| AutoSeed.startPioneer(state,PerformanceDetails.world_serial,world).ptr else "{\\"ok\\":false,\\"phase\\":\\"failed\\",\\"reason\\":\\"World unavailable\\"}";
}
''';p.write_text(x)
p=s/'states/main_menu.zig';x=p.read_text();x=x.replace('"Origin: simple life"','"Wind Origin: simple life"').replace('                game.startOriginNext = true;','                game.startWindNext = true;game.startOriginNext = false;',1)
a=x.index('            if (ui.button(vg, game, "web-new-planet"');b=x.index('            vg.textAlign(',a);x=x[:a]+x[b:];x=x.replace('"New planets only; saved worlds unchanged"','"Classic Sandbox is available through Back to main"');p.write_text(x)
p=s/'auto_seed.zig';x=p.read_text();x=x.replace('pub const batch_size:usize=512;','pub const batch_size:usize=512;\npub const FounderKind=enum{ordinary,pioneer};\nvar founder_kind:FounderKind=.ordinary;')
x=x.replace('const Plan=struct{original:P,','const Plan=struct{kind:FounderKind,original:P,')
x=x.replace('.ok=ok,.phase=', '.ok=ok,.founder_kind=@tagName(founder_kind),.phase=',1)
x=x.replace('return state.paused and ', 'return std.meta.eql(state.planet.windDispersal,p.original.windDispersal) and state.paused and ',1)
x=x.replace(' const live=&state.planet;',' const live=&state.planet;\n if(!std.meta.eql(live.windDispersal,p.original.windDispersal))return false;',1)
needle='pub fn startWithAllocator(state:anytype,world:u32,expected:u32,backing:std.mem.Allocator)[:0]const u8{';assert x.count(needle)==1
x=x.replace(needle,'''pub fn startPioneer(state:anytype,world:u32,expected:u32)[:0]const u8{return startKindWithAllocator(state,world,expected,.pioneer,std.heap.page_allocator);}
pub fn startWithAllocator(state:anytype,world:u32,expected:u32,backing:std.mem.Allocator)[:0]const u8{return startKindWithAllocator(state,world,expected,.ordinary,backing);}
pub fn startKindWithAllocator(state:anytype,world:u32,expected:u32,kind:FounderKind,backing:std.mem.Allocator)[:0]const u8{''')
needle=' if(world!=expected or !state.paused';x=x.replace(needle,' if(!state.planet.windDispersal.valid() or (kind==.pioneer and !state.planet.windDispersal.enabled))return fail("Pioneer founders require an explicitly created wind Origin world");\n'+needle,1)
x=x.replace(' scanned=0;total=n;eligible=0;', ' founder_kind=kind;scanned=0;total=n;eligible=0;',1)
x=x.replace(' plan=.{.original=original,',' plan=.{.kind=kind,.original=original,',1)
x=x.replace('else if(p.staged.seedMicrobes(i))','else if(if(p.kind==.pioneer)p.staged.seedPioneer(i) else p.staged.seedMicrobes(i))',1)
p.write_text(x)
p=r/'web/build.sh';x=p.read_text();x=x.replace('_stella_auto_seed_start,','_stella_auto_seed_pioneer_start,_stella_auto_seed_start,',1);p.write_text(x)

from pathlib import Path
import subprocess,sys
here=Path(__file__).resolve().parent;out=Path(sys.argv[1])
subprocess.run([sys.executable,str(here/'egl-prepare.py'),str(out)],check=True)
p=out/'main.zig';s=p.read_text().replace('nosuspend game.setState(PlayState);','nosuspend game.setState(MainMenuState);')
s=s[:s.index('pub export fn egl_trace')]+r'''
extern fn qa_pointer(x:f64,y:f64,down:c_int) void;
pub export fn egl_trace(frame:c_int) void {
 const size=game.renderer.framebufferSize;
 const l=@import("world_setup.zig").Layout.at(size.x(),size.y());
 const cx=l.left+l.width*0.75;const rx=l.left+l.width*0.25;
 if(frame==1){std.debug.assert(game.newWorldChoice.preset==.random);qa_pointer(cx,l.top+22,1);}
 if(frame==2)qa_pointer(cx,l.top+22,0);
 if(frame==3){std.debug.assert(game.newWorldChoice.preset==.continents);std.debug.assert(game.state==.MainMenu);qa_pointer(rx,l.top+22,1);}
 if(frame==4)qa_pointer(rx,l.top+22,0);
 if(frame==5){std.debug.assert(game.newWorldChoice.preset==.random);std.debug.assert(game.state==.MainMenu);qa_pointer(cx,l.top+22,1);}
 if(frame==6)qa_pointer(cx,l.top+22,0);
 if(frame==7){std.debug.assert(game.newWorldChoice.preset==.continents);qa_pointer(l.left+l.width/2,l.top+(if(std.posix.getenv("QA_SANDBOX")!=null) @as(f32,158) else @as(f32,96)),1);}
 if(frame==8)qa_pointer(l.left+l.width/2,l.top+(if(std.posix.getenv("QA_SANDBOX")!=null) @as(f32,158) else @as(f32,96)),0);

 if(frame==10 and std.posix.getenv("QA_SANDBOX")!=null){std.debug.assert(game.state==.GameIntro);qa_pointer(size.x()/2,size.y()*0.58+28,1);}
 if(frame==11 and std.posix.getenv("QA_SANDBOX")!=null)qa_pointer(size.x()/2,size.y()*0.58+28,0);
 if(frame==13){
 std.debug.assert(game.state==.Playing);
 const expected:@import("simulation/microbes.zig").Mode=if(std.posix.getenv("QA_SANDBOX")!=null) .sandbox else .origin;
 std.debug.assert(game.state.Playing.planet.worldMode==expected);
 std.debug.print("WORLD_MENU actual_press_release=true default_random=true reversible=true no_reset_on_select=true new_mode={s} preset=continents\n",.{@tagName(expected)});
 menuSaveReload() catch |err|{std.debug.panic("menu reload {s}",.{@errorName(err)});};
 game.window.setShouldClose(true);
 }

}
'''
s=s.replace('game.state.Playing.planet.isOrigin()','game.state.Playing.planet.worldMode==.origin')
p.write_text(s)
p=out/'states/game_intro.zig';p.write_text(p.read_text().replace('@import("builtin").target.cpu.arch == .wasm32','true'))
p=out/'states/play.zig';p.write_text(p.read_text().replace('@import("builtin").target.cpu.arch == .wasm32','true'))
p=out/'states/main_menu.zig';s=p.read_text().replace('@import("builtin").target.cpu.arch == .wasm32','true');p.write_text(s)

p=out/'main.zig';p.write_text(p.read_text()+r"""
fn menuSaveReload()!void{
 const saves=@import("save_game.zig");
 var arena=std.heap.ArenaAllocator.init(game.allocator);defer arena.deinit();const a=arena.allocator();
 const state=&game.state.Playing;
 game.loop.pump(1024);
 const created=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});
 var created_parsed=try saves.schema.parse(a,created);defer created_parsed.deinit();
 const path=std.posix.getenv("QA_EXISTING_SAVE") orelse "/tmp/nursery-api-final.json";
 const file=try std.fs.openFileAbsolute(path,.{});defer file.close();
 const bytes=try file.readToEndAlloc(a,64*1024*1024);
 var existing=try saves.schema.parse(a,bytes);defer existing.deinit();
 const expected=try std.json.stringifyAlloc(a,existing.value,.{});
 std.debug.assert(game.newWorldChoice.preset==.continents);
 try saves.replaceWorld(state,existing.value);
 const restored=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});
 if(!std.mem.eql(u8,expected,restored)){
 const ef=try std.fs.createFileAbsolute("/tmp/menu-reload-expected.json",.{});defer ef.close();try ef.writeAll(expected);
 const af=try std.fs.createFileAbsolute("/tmp/menu-reload-actual.json",.{});defer af.close();try af.writeAll(restored);
 return error.ExistingSaveNotExact;
 }
 game.loop.pump(1024);
 try saves.replaceWorld(state,created_parsed.value);
 const restored_created=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});
 if(!std.mem.eql(u8,created,restored_created)){
 const ef=try std.fs.createFileAbsolute("/tmp/menu-created-expected.json",.{});defer ef.close();try ef.writeAll(created);
 const af=try std.fs.createFileAbsolute("/tmp/menu-created-actual.json",.{});defer af.close();try af.writeAll(restored_created);
 return error.CreatedSaveNotExact;
 }
 std.debug.print("MENU_SAVE_RELOAD existing_mode={s} new_mode={s} full_json_exact=true preset_ignored=true schema={d}\n",.{@tagName(existing.value.mode),@tagName(created_parsed.value.mode),created_parsed.value.version});
}
""")
# Match browser cooperative scheduling; desktop's independent update thread
# must not race a save fixture restore performed at a rendered frame boundary.
p=out/'loop.zig';p.write_text(p.read_text().replace('const is_web = @import("builtin").target.cpu.arch == .wasm32;','const is_web = true;'))
p=out/'main.zig';s=p.read_text();a=s.index('    std.log.debug("Creating update loop job.."');b=s.index('    std.log.debug("Done!"',a);s=s[:a]+s[b:];s=s.replace('        render(window);','        loop.pump(1024);\n        render(window);');p.write_text(s)

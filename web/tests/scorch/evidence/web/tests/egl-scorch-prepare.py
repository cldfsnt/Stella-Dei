from pathlib import Path
import subprocess,sys
here=Path(__file__).resolve().parent;out=Path(sys.argv[1]);subprocess.run([sys.executable,str(here/'egl-world-menu-prepare.py'),str(out)],check=True)
p=out/'main.zig';s=p.read_text().replace('if (!is_web or !web_initialized or !game.state_init) return null;','if (!game.state_init) return null;');s=s.replace(' std.debug.print("MENU_SAVE_RELOAD', ' try scorchCheck(state,a);\n std.debug.print("MENU_SAVE_RELOAD',1)
s+=r'''
extern fn qa_scorch_capture(name:[*:0]const u8) void;
fn scorchCheck(state:*PlayState,a:std.mem.Allocator)!void{
 if(state.planet.worldMode!=.sandbox)return;
 const Save=@import("save_game.zig");const Life=@import("simulation/life.zig").Lifeform;
 const snapshot=try Save.capture(a,state);const original=try std.json.stringifyAlloc(a,snapshot,.{});
 var original_parsed=try Save.schema.parse(a,original);defer original_parsed.deinit();
 const i:usize=30114;state.selectedPoint=i;state.paused=true;
 // Controlled environmental contrast exercises actual action and animal code.
 for([_]f32{275,295})|temp|{
  var control_sat:f32=0;var control_alive:usize=0;
  for(0..2)|arm|{
   state.selectedPoint=i;
   state.planet.lifeforms.clearRetainingCapacity();state.planet.temperature[i]=temp;state.planet.waterMass[i]=0;state.planet.vegetation[i]=0.2;
   var rabbit=Life.init(state.planet.transformedPoints[i],.Rabbit,0);rabbit.satiety=60;rabbit.prng=std.rand.DefaultPrng.init(42);
   try state.planet.addLifeform(rabbit);
   if(arm==1){
    const json=std.mem.span(stella_god_action(2,@intCast(i)));var receipt=try std.json.parseFromSlice(std.json.Value,a,json,.{});defer receipt.deinit();
    std.debug.assert(std.mem.eql(u8,receipt.value.object.get("failure").?.string,"none"));
    const r=state.godReceipt.?;std.debug.assert(r.success());std.debug.assert(r.affected[0].cover_removed>0 and r.heat_joules>0);std.debug.assert(state.paused);
    std.debug.print("SCORCH_EXPORT json={s}\n",.{json});
    const captured=try Save.capture(a,state);const bytes=try std.json.stringifyAlloc(a,captured,.{});
    var saved_parsed=try Save.schema.parse(a,bytes);defer saved_parsed.deinit();try Save.replaceWorld(state,saved_parsed.value);const restored=try std.json.stringifyAlloc(a,try Save.capture(a,state),.{});std.debug.assert(std.mem.eql(u8,bytes,restored));
   }
   state.planet.lifeforms.items[0].aiStep(&state.planet,.{.dt=@as(f32,1440),.timeScale=@as(f32,1),.gameTime=@as(f64,1440)});
   const alive=state.planet.lifeforms.items.len;const sat=if(alive>0)state.planet.lifeforms.items[0].satiety else 0;
   if(arm==0){control_sat=sat;control_alive=alive;}else{
    std.debug.assert(control_alive==1);if(temp==295)std.debug.assert(alive==0)else std.debug.assert(alive==1 and sat<control_sat);
    std.debug.print("SCORCH_RABBIT startK={d} control_alive={d} scorch_alive={d} control_satiety={d} scorch_satiety={d} paused_save_exact=true\n",.{temp,control_alive,alive,control_sat,sat});
   }
  }
 }
 // Existing vegetation update, fixed favorable daylight; explicit mechanism test,
 // not a promise that full changing climate guarantees recovery.
 state.selectedPoint=i;state.planet.lifeforms.clearRetainingCapacity();state.planet.temperature[i]=275;state.planet.waterMass[i]=0;state.planet.vegetation[i]=0.8;state.planet.plantTraits[i].optimum=295.15;
 for(state.planet.getNeighbours(i))|n|{if(n!=i)state.planet.vegetation[n]=0;}
 const r=state.applyGodAction(.scorch,i);std.debug.assert(r.success());const post=state.planet.vegetation[i];
 state.planet.simulateVegetation(.{.dt=86400,.solarConstant=1361,.planetRotationTime=86400,.gameTime=86400,.timeScale=1,.solarVector=state.planet.transformedPoints[i].norm()},i,i+1);
 std.debug.assert(state.planet.vegetation[i]>post);
 std.debug.print("SCORCH_RECOVERY actual_vegetation_update=true post={d} after_day={d} no_neighbors=true controlled_daylight=true\n",.{post,state.planet.vegetation[i]});
 // Actual exported callback and renderer, paused; no screenshot from restored state.
 state.planet.temperature[i]=275;state.planet.waterMass[i]=0;state.planet.vegetation[i]=0.8;
 state.cameraDistance=state.planet.radius+800;state.targetCameraDistance=state.cameraDistance;
 state.cameraPos=state.planet.transformedPoints[i].norm().scale(state.cameraDistance);state.targetCameraPos=state.cameraPos;
 _=stella_god_action(2,@intCast(i));std.debug.assert(state.godReceipt!=null and state.godEffectSeconds>0);
 render(game.window);qa_scorch_capture("accepted");
 state.planet.waterMass[i]=1;const blocked_before=try std.json.stringifyAlloc(a,try Save.capture(a,state),.{});
 const blocked=std.mem.span(stella_god_action(2,@intCast(i)));std.debug.assert(std.mem.indexOf(u8,blocked,"wet")!=null);
 const blocked_after=try std.json.stringifyAlloc(a,try Save.capture(a,state),.{});std.debug.assert(std.mem.eql(u8,blocked_before,blocked_after));
 std.debug.assert(state.godReceipt==null and state.godEffectSeconds==0);render(game.window);qa_scorch_capture("rejected");
 state.planet.waterMass[i]=0;state.planet.temperature[i]=275;_ = stella_god_action(2,@intCast(i));std.debug.assert(state.godReceipt!=null);_ = stella_god_action(99,@intCast(i));std.debug.assert(state.godReceipt==null and state.godEffectSeconds==0);
 std.debug.print("SCORCH_EFFECT accepted_then_wet_rejected=true invalid_kind_clears=true rejected_state_exact=true\n",.{});
 game.loop.pump(1024);
 try Save.replaceWorld(state,original_parsed.value);const final=try std.json.stringifyAlloc(a,try Save.capture(a,state),.{});std.debug.assert(std.mem.eql(u8,original,final));
 std.debug.print("SCORCH_GATE original_save_restored_exact=true\n",.{});
}
''';p.write_text(s)

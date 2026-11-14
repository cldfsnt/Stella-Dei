from pathlib import Path
import subprocess,sys
root=Path(__file__).resolve().parents[4]
out=Path(sys.argv[1]).resolve()
subprocess.run([sys.executable,str(root/'web/tests/egl-prepare.py'),str(out),'--mobile','--paused'],check=True)
p=out/'main.zig';s=p.read_text();s=s[:s.index('pub export fn egl_trace(frame: c_int)')]+r'''
extern fn qa_pointer(x:f64,y:f64,down:c_int) void;
pub export fn egl_trace(frame:c_int) void {
 if(!game.state_init)return;
 switch(game.state){.Playing=>|*state|{
  if(frame==1){
   state.paused=true;state.planet.ensureMicrobeStorage() catch @panic("microbe storage");state.planet.worldMode=.origin;
   for(state.planet.microbeCells)|*cell|{cell.cohorts=.{.{},.{},.{},.{}};}
   const id=state.planet.getNearestPointTo(za.Vec3.new(5000,0,0));
   state.planet.microbeCells[id].cohorts[0]=.{.biomass=0.8,.support_mass=0.1,.organization=0.08,.structure=0.14,.lineage=1};
   for(state.planet.getNeighbours(id))|i|state.planet.microbeCells[i].cohorts[0]=.{.biomass=0.6,.support_mass=0.1,.organization=0.08,.efficiency=1.06,.lineage=2};
   state.planet.microbeStats.next_lineage=3;state.displayMode=.Temperature;state.watchLifeView=false;
   state.targetCameraPos=za.Vec3.new(-5000,0,0);state.cameraPos=state.targetCameraPos;
   const time=state.gameTime;const speed=state.timeScale;
   std.debug.assert(state.findLivingClusterResult(390,700)==1);
   std.debug.assert(state.displayMode==.Normal and state.watchLifeView and state.paused and state.gameTime==time and state.timeScale==speed);
   std.debug.assert(state.colonyTargets.count==0);
   std.debug.print("FIND_PASS explicit_fixture=true selected_surface_watch=true pace_preserved=true\n",.{});
  }else if(frame==2){
   std.debug.assert(state.colonyTargets.count>0);
   const targets=state.colonyTargets;
   var checked:usize=0;
   for(targets.items[0..targets.count])|t|{
    inline for(.{@as(f32,0),@as(f32,-15)})|offset|{
     qa_pointer(t.x,t.y+offset*t.scale,0);state.mousePressed(&game,.left);
     std.debug.assert(state.selectedPoint==t.cell and state.colonyPeek.cell.?==t.cell);
     checked+=1;
    }
   }
   const saves=@import("save_game.zig");var arena=std.heap.ArenaAllocator.init(std.heap.page_allocator);defer arena.deinit();const a=arena.allocator();
   const snap=saves.capture(a,state) catch @panic("capture");
   const bytes=std.json.stringifyAlloc(a,snap,.{}) catch @panic("json");
   var parsed=saves.schema.parse(a,bytes) catch @panic("parse");defer parsed.deinit();
   saves.apply(state,parsed.value) catch |err| {std.debug.print("APPLY_ERROR {s}\n",.{@errorName(err)});@panic("apply");};
   std.debug.assert(state.colonyTargets.count==0);
   std.debug.print("GLYPH_PASS visible={d} root_body_checks={d} same_grid_load_clears=true\n",.{targets.count,checked});
   game.window.setShouldClose(true);
  }
 },else=>{}}
}
''';p.write_text(s)

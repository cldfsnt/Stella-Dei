from pathlib import Path
import sys
root=Path(sys.argv[1]); src=root/'src'
p=src/'main.zig';s=p.read_text();assert 'stella_wind_new' not in s
s=s.replace('startOriginNext: bool = false,','startOriginNext: bool = false,\n    startWindNext: bool = false,',1)
s+='''
// Explicit fresh-world opt-in; never edits existing lineage genetics.
pub fn windNewForGame(g:*Game,expected:u32)i32 {
    if(!g.state_init)return -1;
    if(expected!=PerformanceDetails.world_serial)return -2;
    if(AdvanceDay.blocksInput())return -3;
    switch(g.state){
      .Playing=>|*v|{if(v.planet.normalComputeJob)|job|if(!job.isCompleted())return -3;},
      .MainMenu=>|*v|{if(v.planet.normalComputeJob)|job|if(!job.isCompleted())return -3;},
      else=>return -1,
    }
    g.startWindNext=true;g.startOriginNext=false;g.setState(PlayState);return 1;
}
export fn stella_wind_new(expected:u32)i32 {
    if(!is_web or !web_initialized)return -1;
    web_loop.pump(1024);return windNewForGame(&game,expected);
}
export fn stella_wind_snapshot()[*:0]const u8 {return @import("wind_view.zig").snapshot(webPlayState(),PerformanceDetails.world_serial);}
pub fn pioneerForState(state:*PlayState,world:u32,point:u32)i32 {
    if(world!=PerformanceDetails.world_serial or point!=state.selectedPoint)return -2;
    if(AdvanceDay.blocksInput() or state.showEscapeMenu or state.showPlanetControl or state.showPointDetails)return -3;
    if(state.planet.worldMode!=.origin or !state.planet.windDispersal.enabled or !state.planet.windDispersal.valid())return -1;
    if(point>=state.planet.microbeCells.len)return -2;
    const paid=state.planet.seedPioneer(point);
    if(paid){
        @import("plant_receipt.zig").invalidate();
        @import("patch_watch.zig").current.stop("Pioneer seeded");
        state.mobileFeedback="Paid Pioneer seeded: aerial allocation 0.5; arrival is not guaranteed";
    }else state.mobileFeedback="No Pioneer planted: check habitat, free cohort slot and available carbon/nutrients";
    state.mobileFeedbackSeconds=6;
    return @intFromBool(paid);
}
export fn stella_seed_pioneer(world:u32,point:u32)i32 {
    const state=webPlayState() orelse return -1;
    return pioneerForState(state,world,point);
}
// The asynchronous backup is in JS; token/schema are checked after the pump.
export fn stella_save_expected(world:u32,writer:u32)i32 {
    if(!is_web or !web_initialized)return -1;
    if(!AdvanceDay.current.recovery_required)web_loop.pump(1024);
    const state=webPlayState() orelse return -1;
    if(world!=PerformanceDetails.world_serial or writer!=@import("wind_view.zig").writerVersion(state))return -6;
    if(AdvanceDay.current.recovery_required){
      if(!AdvanceDay.current.canRecoverySave(state,PerformanceDetails.world_serial))return -4;
    }else if(AdvanceDay.blocksInput())return -4;
    @import("save_game.zig").write(state,game.allocator) catch |err| return if(err==error.SaveTooLarge) -5 else -2;
    return 0;
}
''';p.write_text(s)
p=src/'states/play.zig';s=p.read_text();s=s.replace('var state = initNewWorld(game, subdivisions, game.newWorldChoice.preset);','const wind=game.startWindNext;game.startWindNext=false;\n        var state = initNewWorld(game, subdivisions, game.newWorldChoice.preset, wind);',1).replace('if (game.startOriginNext) {','if (game.startOriginNext or wind) {',1).replace('return initNewWorld(game, subdivisions, .random);','return initNewWorld(game, subdivisions, .random, false);',1).replace('preset: @import("../world_setup.zig").Preset) PlayState {','preset: @import("../world_setup.zig").Preset, wind:bool) PlayState {',1).replace('.{.water_preset=preset}) catch unreachable;','.{.water_preset=preset,.wind_dispersal=wind}) catch unreachable;',1);p.write_text(s)
(src/'wind_view.zig').write_text('''const std=@import("std");
var buffer:[2048]u8=undefined;
pub fn writerVersion(state:anytype)u32 {
 const p=&state.planet;
 if(!p.windDispersal.valid() or (p.windDispersal.enabled and p.worldMode!=.origin))return 0;
 return if(p.windDispersal.enabled)11 else 7;
}
pub fn snapshot(state:anytype,world:u32)[*:0]const u8 {
 const Allocation=struct{id:[]const u8,living:bool,fraction:f32};
 var ids:[4][24]u8=undefined;var a:[4]Allocation=undefined;var count:usize=0;
 var writer:u32=0;var enabled=false;var cell:?u32=null;var law:u8=0;
 if(state)|v|{
   writer=writerVersion(v);enabled=v.planet.windDispersal.enabled;law=v.planet.windDispersal.law;
   if(v.selectedPoint<v.planet.microbeCells.len){cell=@intCast(v.selectedPoint);for(v.planet.microbeCells[v.selectedPoint].cohorts)|c|{
     if(c.biomass<=0 or c.lineage==0)continue;
     const id=std.fmt.bufPrint(&ids[count],"{d}",.{c.lineage}) catch return "{}";
     a[count]=.{.id=id,.living=true,.fraction=c.aerial_allocation};count+=1;
   }}
 }
 var stream=std.io.fixedBufferStream(&buffer);
 std.json.stringify(.{.status=if(writer==0) "unavailable" else if(enabled) "wind" else "classic",.world_serial=world,.enabled=enabled,.writer_version=writer,.law=law,.cell=cell,.aerial_allocations=a[0..count]},.{},stream.writer()) catch return "{}";
 if(stream.pos>=buffer.len)return "{}";buffer[stream.pos]=0;return @ptrCast(&buffer);
}
''')
p=root/'web/build.sh'
if p.exists():
 s=p.read_text();s=s.replace("_stella_save,_stella_load", "_stella_save_expected,_stella_wind_snapshot,_stella_wind_new,_stella_seed_pioneer,_stella_save,_stella_load");p.write_text(s)

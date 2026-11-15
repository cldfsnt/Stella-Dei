//! Paused, session-only basin confirmation. No biology edits or saved fields.
const std=@import("std");const Basin=@import("pond_action.zig");const M=@import("simulation/microbes.zig");
const Pending=struct{plan:Basin.Plan,cells:[19]M.Cell,time:f64,token:u32};
var pending:?Pending=null;var sequence:u32=0;var buffer:[4096]u8=undefined;
pub fn cancel()void{pending=null;}
fn json(value:anytype)[:0]const u8{var stream=std.io.fixedBufferStream(buffer[0..buffer.len-1]);std.json.stringify(value,.{},stream.writer()) catch return "{\"ok\":false,\"reason\":\"Preview unavailable\"}";buffer[stream.pos]=0;return buffer[0..stream.pos:0];}
fn failure(why:[]const u8)[:0]const u8{return json(.{.ok=false,.reason=why});}
fn reason(state:anytype)?[]const u8{if(state.planet.worldMode!=.origin)return "Origin worlds only";if(!state.paused)return "Pause the game before previewing terrain changes";if(!std.math.isFinite(state.gameTime))return "Invalid simulation time";if(state.selectedPoint>=state.planet.microbeCells.len)return "Select a patch first";return null;}
fn fresh(state:anytype,world:u32,p:*const Pending)bool{
 if(reason(state)!=null or state.gameTime!=p.time or world!=p.plan.world or state.selectedPoint!=p.plan.selected or @intFromPtr(&state.planet)!=p.plan.owner)return false;
 const plan=Basin.previewKind(&state.planet,p.plan.selected,state.selectedPoint,p.plan.nursery,p.plan.sunlit,world) orelse return false;
 if(!std.meta.eql(plan,p.plan))return false;
 for(plan.ids[0..plan.count],0..)|id,i|{if(id>=state.planet.microbeCells.len or !std.meta.eql(state.planet.microbeCells[id],p.cells[i]))return false;}
 return true;
}
pub fn guard(state:anytype,world:u32)void{if(pending)|p|if(!fresh(state,world,&p)){cancel();};}
pub fn status(state:anytype,world:u32)[:0]const u8{guard(state,world);return json(.{.pending=pending!=null,.token=if(pending)|p|p.token else @as(u32,0),.world=world,.cell=state.selectedPoint,.paused=state.paused,.available=reason(state)==null,.reason=reason(state) orelse ""});}
fn receipt(p:*const Pending,manual:bool)[:0]const u8{
 const plan=&p.plan;var living_floor:usize=0;var living_rim:usize=0;
 for(p.cells[0..plan.count],0..)|cell,i|{var living=false;for(cell.cohorts)|c|{if(c.biomass>0)living=true;}if(living){if(i<plan.floor_count)living_floor+=1 else living_rim+=1;}}
 const conversion:@TypeOf(@as(f32,0))=@bitCast(plan.conversion_bits);
 return json(.{.ok=true,.manual=manual,.token=p.token,.world=plan.world,.cell=plan.selected,.kind=if(plan.sunlit) "sunlit_nursery" else if(plan.nursery) "nursery" else "pond",.floor_ids=plan.ids[0..plan.floor_count],.rim_ids=plan.ids[plan.floor_count..plan.count],.floor_count=plan.floor_count,.rim_count=plan.count-plan.floor_count,.living_floor_patches=living_floor,.living_rim_patches=living_rim,.water_added_kg=plan.water_added*1e9,.water_removed_kg=plan.water_removed*1e9,.water_added_depth_sum_m=plan.water_added*@as(f64,conversion)*1000,.water_removed_depth_sum_m=plan.water_removed*@as(f64,conversion)*1000,.center_depth_m=if(plan.nursery)@as(u32,5) else 15,.other_floor_depth_m=if(plan.sunlit)@as(u32,5) else 15,.rim_depth_m=@as(u32,0),.warning="Rim patches are raised and dried, including any living colonies. No organisms are added; survival is not guaranteed."});
}
pub fn prepare(state:anytype,world:u32,expected_world:u32,cell:i32,nursery:i32)[:0]const u8{
 cancel();if(reason(state))|why|return failure(why);
 if(world!=expected_world or cell<0 or @as(usize,@intCast(cell))!=state.selectedPoint or nursery<0 or nursery>2)return failure("Selection or world changed; preview again");
 const plan=Basin.previewKind(&state.planet,state.selectedPoint,state.selectedPoint,nursery!=0,nursery==2,world) orelse return failure("This basin cannot be shaped safely");
 var cells:[19]M.Cell=undefined;
 for(plan.ids[0..plan.count],0..)|id,i|{if(id>=state.planet.microbeCells.len)return failure("Population unavailable");cells[i]=state.planet.microbeCells[id];for(cells[i].cohorts)|c|if(!std.math.isFinite(c.biomass) or c.biomass<0)return failure("Population unavailable");}
 if(sequence==std.math.maxInt(u32))return failure("Preview limit reached; reload before another action");sequence+=1;
 pending=.{.plan=plan,.cells=cells,.time=state.gameTime,.token=sequence};return receipt(&pending.?,false);
}
pub fn execute(state:anytype,world:u32,token:u32)[:0]const u8{
 const p=pending orelse return failure("Preview expired; preview again");cancel();
 if(token==0 or token!=p.token or !fresh(state,world,&p))return failure("World or colonies changed; nothing shaped");
 if(Basin.applyChecked(&state.planet,&p.plan,state.selectedPoint,world)<0)return failure("Terrain changed; nothing shaped");
 state.mobileFeedback="Habitat shaped; rim raised and dried. Watch what survives.";state.mobileFeedbackSeconds=5;
 return receipt(&p,true);
}
const Fixture=struct{
 paused:bool=true,selectedPoint:usize=0,gameTime:f64=123,mobileFeedback:[]const u8="",mobileFeedbackSeconds:f32=0,
 planet:struct{
 worldMode:enum{origin,sandbox}=.origin,waterMass:[6]f32=.{0,0.1,0.2,0.3,0,0.02},elevation:[6]f32=.{5000,5000.1,5000.2,5000.3,5000.4,5000.5},microbeCells:[6]M.Cell=[_]M.Cell{.{}}**6,
 pub fn getKmPerWaterMass(_: *@This())f32{return 1;}
 pub fn getNeighbours(_: *@This(),i:usize)[]const usize{return switch(i){0=>&.{1,2},1=>&.{0,2,3},2=>&.{0,1,4},3=>&.{1,4,5},4=>&.{2,3,5},else=>&.{3,4}};}
 }=.{},
};
test "paused preview and one-use execute preserve biology time pace and match old action"{
 cancel();var s=Fixture{};s.planet.microbeCells[3].cohorts[0]=.{.biomass=0.1,.lineage=1};const before=s;
 _=prepare(&s,5,5,0,1);const p=pending orelse return error.NoPreview;
 try std.testing.expect(std.meta.eql(before,s));try std.testing.expect(std.mem.indexOf(u8,receipt(&p,false),"\"living_rim_patches\":1")!=null);
 var expected=s;_=Basin.makeNursery(&expected.planet,0,0);expected.mobileFeedback="Habitat shaped; rim raised and dried. Watch what survives.";expected.mobileFeedbackSeconds=5;
 const result=execute(&s,5,p.token);try std.testing.expect(std.mem.indexOf(u8,result,"\"ok\":true")!=null);
 try std.testing.expect(std.meta.eql(expected,s));const after=s;
 _=execute(&s,5,p.token);try std.testing.expect(std.meta.eql(after,s));try std.testing.expect(pending==null);
}
test "cancel stale same-count colony world time pause selection and external water refuse without writes"{
 for(0..8)|which|{
  cancel();var s=Fixture{};_=prepare(&s,5,5,0,0);const token=pending.?.token;
  var world:u32=5;
  switch(which){0=>cancel(),1=>world=6,2=>s.gameTime+=1,3=>s.paused=false,4=>s.selectedPoint=1,5=>s.planet.waterMass[5]+=0.01,6=>s.planet.microbeCells[3].cohorts[0].lineage=99,else=>{}}
  const before=s;_=execute(&s,world,if(which==7)token+1 else token);
  try std.testing.expect(std.meta.eql(before,s));try std.testing.expect(pending==null);
 }
 var s=Fixture{.paused=false};_=prepare(&s,5,5,0,0);try std.testing.expect(pending==null);try std.testing.expect(!s.paused);
 s.paused=true;_=prepare(&s,5,5,0,0);s.gameTime+=1;_=status(&s,5);try std.testing.expect(pending==null);
}
test "observed unpause invalidates even when re-paused at same simulation time"{
 cancel();var s=Fixture{};_=prepare(&s,1,1,0,0);const token=pending.?.token;
 s.paused=false;guard(&s,1);s.paused=true;const before=s;
 _=execute(&s,1,token);try std.testing.expect(std.meta.eql(before,s));try std.testing.expect(pending==null);
}

test "Sunlit public preview and execute agree on kind depths and material" {
    cancel();var s=Fixture{};const before=s;
    const reply=prepare(&s,7,7,0,2);
    try std.testing.expect(std.mem.indexOf(u8,reply,"\"kind\":\"sunlit_nursery\"")!=null);
    try std.testing.expect(std.mem.indexOf(u8,reply,"\"other_floor_depth_m\":5")!=null);
    const p=pending.?;try std.testing.expect(std.meta.eql(before,s));
    for(p.plan.waters[0..p.plan.floor_count])|water|try std.testing.expectEqual(@as(f32,0.005),water);
    var expected=s;_=Basin.makeSunlitNursery(&expected.planet,0,0);
    const done=execute(&s,7,p.token);try std.testing.expect(std.mem.indexOf(u8,done,"\"kind\":\"sunlit_nursery\"")!=null);
    try std.testing.expectEqualSlices(f32,&expected.planet.waterMass,&s.planet.waterMass);
    try std.testing.expectEqualSlices(f32,&expected.planet.elevation,&s.planet.elevation);
    const once=s;_=execute(&s,7,p.token);try std.testing.expect(std.meta.eql(once,s));
    _=prepare(&s,7,7,0,2);const token=pending.?.token;s.gameTime+=1;const stale=s;
    _=execute(&s,7,token);try std.testing.expect(std.meta.eql(stale,s));
    _=prepare(&s,7,7,0,1);try std.testing.expect(std.mem.indexOf(u8,receipt(&pending.?,false),"\"other_floor_depth_m\":15")!=null);
    cancel();
}

//! Observational session statistics, never saved or used by biology.
const std=@import("std");const M=@import("simulation/microbes.zig");const Recent=@import("recent_ecology.zig");
pub var enabled=true;
var owner:usize=0;var serial:u32=0;var observed_mode:M.Mode=.origin;var recent:Recent.Observer=.{};
const Form=struct{form:[]const u8,biomass_sum:f64=0,colony_count:usize=0};
const Census=struct{active:bool=false,ready:bool=false,mode:M.Mode=.origin,owner:usize=0,world:u32=0,storage:usize=0,total:usize=0,cursor:usize=0,start:f64=0,end:f64=0,forms:[6]Form=undefined,cover_sum:f64=0,vegetated_patches:usize=0,colonies:usize=0};
var census:Census=.{};var buffer:[4096]u8=undefined;
pub fn reset()void{owner=0;serial=0;observed_mode=.origin;recent.reset();census=.{};}
fn bind(p:anytype,world:u32)void{if(owner!=@intFromPtr(p) or serial!=world){reset();owner=@intFromPtr(p);serial=world;observed_mode=p.worldMode;}}
pub fn record(p:anytype,world:u32,time:f64,births:u64,deaths:u64)void{if(!enabled)return;if(owner==@intFromPtr(p) and serial==world and observed_mode!=p.worldMode)reset();bind(p,world);_=recent.record(world,time,.{.births=births,.deaths=deaths});}
pub fn markSaturated(p:anytype,world:u32)void{if(!enabled)return;bind(p,world);recent.saturated=true;}
/// Called only around one Microbes.step, before any movement or birth scheduler.
pub fn physiologyDeaths(before:[4]M.Cohort,after:[4]M.Cohort)u64{
 var n:u64=0;for(before,after)|old,new|{if(old.lineage!=0 and std.math.isFinite(old.biomass) and old.biomass>0 and new.biomass==0)n+=1;}return n;
}
fn json(v:anytype)[:0]const u8{var stream=std.io.fixedBufferStream(buffer[0..buffer.len-1]);std.json.stringify(v,.{},stream.writer()) catch return "{\"status\":\"unavailable\"}";buffer[stream.pos]=0;return buffer[0..stream.pos:0];}
/// Constant bounded read: histogram only, no census, bind, reset or event mutation.
pub fn recentLine(text:[]u8,p:anytype,world:u32,time:f64)[]const u8{
 const unknown="Recent stats warming up · World stats";
 if(owner!=@intFromPtr(p) or serial!=world or observed_mode!=p.worldMode)return unknown;
 const view=recent.view(world,time) orelse return unknown;
 if(view.observed_seconds<=0)return unknown;
 if(view.saturated)return "Recent event counter saturated · World stats";
 return std.fmt.bufPrint(text,"{d:.1}h: {d} births · {d} {s}",.{view.observed_seconds/3600,view.counts.births,view.counts.deaths,if(p.worldMode==.origin) "colony deaths" else "rabbit deaths"}) catch unknown;
}
pub fn snapshot(p:anytype,world:u32,time:f64,restart:bool)[:0]const u8{
 if(!std.math.isFinite(time) or time<0)return json(.{.status="unavailable"});
 bind(p,world);const origin=p.worldMode==.origin;const n=if(origin)p.microbeCells.len else p.vegetation.len;
 const storage=if(origin)@intFromPtr(p.microbeCells.ptr) else @intFromPtr(p.vegetation.ptr);
 if(restart){census=.{.active=true,.mode=p.worldMode,.owner=@intFromPtr(p),.world=world,.storage=storage,.total=n,.start=time,.end=time};for(&census.forms,0..)|*f,i|f.*=.{.form=M.producerFormName(@enumFromInt(i))};}
 if((census.active or census.ready) and (census.mode!=p.worldMode or census.world!=world or census.owner!=@intFromPtr(p) or census.storage!=storage or census.total!=n or time<census.end)){census=.{};return json(.{.status="stale"});}
 if(census.active){const end=@min(n,census.cursor+@min(@as(usize,512),n-census.cursor));for(census.cursor..end)|i|{
  if(origin){for(p.microbeCells[i].cohorts)|co|{if(!std.math.isFinite(co.biomass) or co.biomass<0){census=.{};return json(.{.status="unavailable"});}if(co.biomass>0){if(co.lineage==0){census=.{};return json(.{.status="unavailable"});}var f=&census.forms[@intFromEnum(M.producerForm(co))];f.biomass_sum+=co.biomass;f.colony_count+=1;census.colonies+=1;}}}
  else {const v=p.vegetation[i];if(!std.math.isFinite(v) or v<0 or v>1){census=.{};return json(.{.status="unavailable"});}census.cover_sum+=v;if(v>0)census.vegetated_patches+=1;}
 }census.cursor=end;census.end=time;if(end==n){census.active=false;census.ready=true;std.mem.sort(Form,&census.forms,{},struct{fn less(_:void,a:Form,b:Form)bool{return a.biomass_sum>b.biomass_sum;}}.less);}}
 const view=if(observed_mode==p.worldMode)recent.view(world,time) else null;
 return json(.{.status=if(census.active) "pending" else if(census.ready) "ready" else "unavailable",.world=world,.mode=if(origin) "origin" else "sandbox",.scanned=census.cursor,.total=n,.census_start_time=census.start,.census_end_time=census.end,.forms=if(origin and census.ready)census.forms[0..] else census.forms[0..0],.colonies=census.colonies,.cover_sum=census.cover_sum,.vegetated_patches=census.vegetated_patches,.rabbits=p.lifeforms.items.len,.recent=view,.recent_scope=if(origin) "paid colony births / physiology colony deaths" else "rabbit births / rabbit deaths",.window_seconds=@as(u32,86400),.bucket_seconds=@as(u32,3600),.biomass_units="sum of patch kg C/m2; not species",.sampled=true});
}
test "physiology deaths count cutoff and grazing zero but not positive cohort or empty"{
 var b=[_]M.Cohort{.{.lineage=1,.biomass=0.1},.{.lineage=2,.biomass=0.01},.{},.{}};var a=b;a[0]=.{};try std.testing.expectEqual(@as(u64,1),physiologyDeaths(b,a));a[1].biomass=0;try std.testing.expectEqual(@as(u64,2),physiologyDeaths(b,a));b[0].lineage=0;try std.testing.expectEqual(@as(u64,1),physiologyDeaths(b,a));
}
const Mock=struct{worldMode:M.Mode=.origin,microbeCells:[]M.Cell,vegetation:[]f32,lifeforms:struct{items:[]u8}=.{.items=&.{}}};
test "incremental actual forms census and session counters are pure and mode honest"{
 const a=std.testing.allocator;const cells=try a.alloc(M.Cell,513);defer a.free(cells);@memset(cells,.{});var vegetation=[_]f32{0,0.35,1};
 cells[0].cohorts[0]=.{.biomass=0.1,.lineage=1};cells[512].cohorts[0]=.{.biomass=0.2,.support_mass=0.1,.organization=0.1,.efficiency=1.1,.lineage=2};
 const original=try a.dupe(M.Cell,cells);defer a.free(original);var p=Mock{.microbeCells=cells,.vegetation=&vegetation};reset();defer reset();
 const first=try std.json.parseFromSlice(std.json.Value,a,snapshot(&p,1,0,true),.{.allocate=.alloc_always});defer first.deinit();try std.testing.expectEqualStrings("pending",first.value.object.get("status").?.string);try std.testing.expectEqual(@as(i64,512),first.value.object.get("scanned").?.integer);
 record(&p,1,0,0,0);record(&p,1,1440,2,1);
 const last=try std.json.parseFromSlice(std.json.Value,a,snapshot(&p,1,1440,false),.{.allocate=.alloc_always});defer last.deinit();try std.testing.expectEqualStrings("ready",last.value.object.get("status").?.string);try std.testing.expectEqualStrings("Canopy",last.value.object.get("forms").?.array.items[0].object.get("form").?.string);try std.testing.expectEqual(@as(i64,2),last.value.object.get("recent").?.object.get("counts").?.object.get("births").?.integer);try std.testing.expectEqualDeep(original,cells);
 reset();p.worldMode=.sandbox;const sandbox=try std.json.parseFromSlice(std.json.Value,a,snapshot(&p,2,1440,true),.{.allocate=.alloc_always});defer sandbox.deinit();try std.testing.expectEqual(@as(usize,0),sandbox.value.object.get("forms").?.array.items.len);try std.testing.expectEqual(@as(i64,2),sandbox.value.object.get("vegetated_patches").?.integer);try std.testing.expect(sandbox.value.object.get("recent").?==.null);
}
test "census rejects changed storage and invalid data without modifying model"{
 var cells=[_]M.Cell{.{}};var other=cells;var vegetation=[_]f32{0};var p=Mock{.microbeCells=&cells,.vegetation=&vegetation};reset();defer reset();_=snapshot(&p,3,0,true);p.microbeCells=&other;
 try std.testing.expect(std.mem.indexOf(u8,snapshot(&p,3,0,false),"stale")!=null);
 other[0].cohorts[0].biomass=std.math.nan(f32);try std.testing.expect(std.mem.indexOf(u8,snapshot(&p,3,0,true),"unavailable")!=null);try std.testing.expect(std.math.isNan(other[0].cohorts[0].biomass));
}
test "legacy saturation remains explicit and same storage mode change invalidates"{
 var cells=[_]M.Cell{.{}};var v=[_]f32{0};var p=Mock{.microbeCells=&cells,.vegetation=&v};reset();defer reset();record(&p,8,0,0,0);markSaturated(&p,8);try std.testing.expect(recent.view(8,0).?.saturated);_=snapshot(&p,8,0,true);p.worldMode=.sandbox;try std.testing.expect(std.mem.indexOf(u8,snapshot(&p,8,0,false),"stale")!=null);
}

test "living cohort without identity refuses census"{var cells=[_]M.Cell{.{}};cells[0].cohorts[0].biomass=0.1;var v=[_]f32{0};var p=Mock{.microbeCells=&cells,.vegetation=&v};reset();defer reset();try std.testing.expect(std.mem.indexOf(u8,snapshot(&p,1,0,true),"unavailable")!=null);}

test "recent footer is scoped bounded read with honest interval reset and pause" {
 var cells=[_]M.Cell{.{}};var vegetation=[_]f32{0};var p=Mock{.microbeCells=&cells,.vegetation=&vegetation};var other=p;var text:[160]u8=undefined;
 reset();defer reset();try std.testing.expectEqualStrings("Recent stats warming up · World stats",recentLine(&text,&p,8,0));
 record(&p,8,0,0,0);record(&p,8,3600,3,2);const before=recent;
 try std.testing.expectEqualStrings("1.0h: 3 births · 2 colony deaths",recentLine(&text,&p,8,3600));
 try std.testing.expectEqualStrings("1.0h: 3 births · 2 colony deaths",recentLine(&text,&p,8,3600));try std.testing.expectEqualDeep(before,recent);
 try std.testing.expectEqualStrings("Recent stats warming up · World stats",recentLine(&text,&other,8,3600));try std.testing.expectEqualStrings("Recent stats warming up · World stats",recentLine(&text,&p,9,3600));try std.testing.expectEqualStrings("Recent stats warming up · World stats",recentLine(&text,&p,8,3601));
 p.worldMode=.sandbox;try std.testing.expectEqualStrings("Recent stats warming up · World stats",recentLine(&text,&p,8,3600));record(&p,8,0,0,0);record(&p,8,3600,4,1);try std.testing.expectEqualStrings("1.0h: 4 births · 1 rabbit deaths",recentLine(&text,&p,8,3600));
 reset();try std.testing.expectEqualStrings("Recent stats warming up · World stats",recentLine(&text,&p,8,3600));
}

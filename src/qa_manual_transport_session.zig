const std=@import("std");const M=@import("simulation/microbes.zig");const T=@import("manual_transport.zig");
const P=struct{propaguleFeedback:@import("propagule_feedback.zig").Tracker=.{},worldMode:M.Mode=.origin,microbeCells:[2]M.Cell=.{.{},.{}},microbeStats:M.Stats=.{.next_lineage=9007199254740995},temperature:[2]f32=.{303,302},waterMass:[2]f32=.{1,2},elevation:[2]f32=.{0,0},pub fn getNeighbours(_: *@This(),from:usize)[]const usize{return if(from==0)&.{1} else &.{0};}pub fn getKmPerWaterMass(_: *@This())f32{return 0.001;}};
const State=struct{planet:P=.{},paused:bool=true,gameTime:f64=123,selectedPoint:usize=0,colonyPeek:@import("colony_peek.zig").Pin=.{},communitySample:@import("community_sample.zig").Sample=.{}};
fn seed()State{var s=State{};s.planet.microbeCells[0].cohorts[0]=.{.lineage=9007199254740993,.biomass=0.2,.support_mass=0.03};return s;}
fn value(text:[]const u8)!std.json.Parsed(std.json.Value){return std.json.parseFromSlice(std.json.Value,std.testing.allocator,text,.{.allocate=.alloc_always});}
fn ticket(s:*State)!u32{const p=try value(T.prepare(s,7,7,0,0,1,"9007199254740993"));defer p.deinit();try std.testing.expect(p.value.object.get("ok").?.bool);try std.testing.expectEqualStrings("9007199254740993",p.value.object.get("id").?.string);return @intCast(p.value.object.get("token").?.integer);}
test "bounded options exact ID and one-use commit with no world mutation except slots"{
 var s=seed();defer T.cancel();const before=s;
 var p=try value(T.options(&s,7));defer p.deinit();try std.testing.expectEqualStrings("9007199254740993",p.value.object.get("sources").?.array.items[0].object.get("id").?.string);try std.testing.expectEqual(@as(usize,1),p.value.object.get("neighbors").?.array.items.len);try std.testing.expectEqualDeep(before,s);
 const token=try ticket(&s);const r=try value(T.execute(&s,7,token));defer r.deinit();try std.testing.expect(r.value.object.get("ok").?.bool);try std.testing.expectEqualStrings("9007199254740993",r.value.object.get("id").?.string);
 var expected=before;expected.planet.microbeCells[1].cohorts[0]=expected.planet.microbeCells[0].cohorts[0];expected.planet.microbeCells[0].cohorts[0]=.{};try std.testing.expectEqualDeep(expected,s);
 const again=try value(T.execute(&s,7,token));defer again.deinit();try std.testing.expect(!again.value.object.get("ok").?.bool);try std.testing.expectEqualDeep(expected,s);
}
test "unpause selection environment cell and world invalidation are atomic"{
 for(0..8)|case|{var s=seed();defer T.cancel();const token=try ticket(&s);switch(case){0=>s.paused=false,1=>s.selectedPoint=1,2=>s.gameTime+=1,3=>s.planet.waterMass[1]+=1,4=>s.planet.temperature[0]+=1,5=>s.planet.elevation[1]+=1,6=>s.planet.microbeCells[1].nutrient+=0.1,else=>{}}const before=s;const r=try value(T.execute(&s,if(case==7)8 else 7,token));defer r.deinit();try std.testing.expect(!r.value.object.get("ok").?.bool);try std.testing.expectEqualDeep(before,s);}
}
test "bad source IDs and explicit cancellation refuse"{
 var s=seed();defer T.cancel();for([_] []const u8{"", "0", "01", "9007199254740992", "18446744073709551616", "-1"})|id|{const p=try value(T.prepare(&s,7,7,0,0,1,id));defer p.deinit();try std.testing.expect(!p.value.object.get("ok").?.bool);}
 const token=try ticket(&s);T.cancel();const p=try value(T.execute(&s,7,token));defer p.deinit();try std.testing.expect(!p.value.object.get("ok").?.bool);
}
test "successful manual move clears observations but preserves selection camera-independent model and pause"{
 var s=seed();defer T.cancel();s.colonyPeek.set(0,s.planet.microbeCells[0],s.gameTime);s.communitySample.capture(.{.valid=true,.colonies=@as(usize,1),.patches=@as(usize,1)},7,@intFromPtr(&s.planet.microbeCells),s.gameTime);
 const tok=try ticket(&s);const r=try value(T.execute(&s,7,tok));defer r.deinit();try std.testing.expect(r.value.object.get("ok").?.bool);try std.testing.expect(s.colonyPeek.cell==null and !s.communitySample.valid and s.selectedPoint==0 and s.paused and s.gameTime==123);
}
test "explicit receipt inspection never selects replacement colony and reset forgets cause"{
 var s=seed();defer T.reset();const tok=try ticket(&s);_=T.execute(&s,7,tok);const before=s;
 const wrong=try value(T.inspect(&s,7,7,1,"9007199254740994"));defer wrong.deinit();try std.testing.expect(!wrong.value.object.get("ok").?.bool);try std.testing.expectEqualDeep(before,s);
 const valid=try value(T.inspect(&s,7,7,1,"9007199254740993"));defer valid.deinit();try std.testing.expect(valid.value.object.get("ok").?.bool);var expected=before;expected.selectedPoint=1;try std.testing.expectEqualDeep(expected,s);
 s.planet.microbeCells[1].cohorts[0].lineage=9007199254740994;const replacement=s;const stale=try value(T.inspect(&s,7,7,1,"9007199254740993"));defer stale.deinit();try std.testing.expect(!stale.value.object.get("ok").?.bool);try std.testing.expectEqualDeep(replacement,s);
 T.reset();const cleared=try value(T.inspect(&s,7,7,1,"9007199254740993"));defer cleared.deinit();try std.testing.expect(!cleared.value.object.get("ok").?.bool);
}

test "manual success forgets only moved pending arrival without emitting events; refusal preserves tracker" {
 var s=seed();defer T.reset();
 s.planet.propaguleFeedback.arrived(1,0,9007199254740993,100);
 s.planet.propaguleFeedback.arrived(0,1,9007199254740994,101);
 const original=s.planet.propaguleFeedback;
 const rejected=try ticket(&s);s.paused=false;
 const refusal=try value(T.execute(&s,7,rejected));defer refusal.deinit();
 try std.testing.expect(!refusal.value.object.get("ok").?.bool);
 try std.testing.expectEqualDeep(original,s.planet.propaguleFeedback);
 s.paused=true;const accepted=try ticket(&s);
 const result=try value(T.execute(&s,7,accepted));defer result.deinit();
 try std.testing.expect(result.value.object.get("ok").?.bool);
 var expected=original;expected.forget(9007199254740993);
 try std.testing.expectEqualDeep(expected,s.planet.propaguleFeedback);
 try std.testing.expect(s.planet.propaguleFeedback.pending[0]==null);
 try std.testing.expect(s.planet.propaguleFeedback.pending[1]!=null);
 try std.testing.expectEqualDeep(original.events,s.planet.propaguleFeedback.events);
 try std.testing.expectEqual(original.next_serial,s.planet.propaguleFeedback.next_serial);
 try std.testing.expect(!s.planet.propaguleFeedback.failed(0,9007199254740993,124));
}

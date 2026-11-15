//! Fixed-capacity endpoint observation, never an ecological rule or event history.
const std=@import("std");
pub const Entry=struct{
 id:u64=0,biomass:f64=0,
 pub fn jsonStringify(self:Entry,writer:anytype)!void{
  var buf:[20]u8=undefined;const id=std.fmt.bufPrint(&buf,"{d}",.{self.id}) catch unreachable;
  try writer.beginObject();try writer.objectField("id");try writer.write(id);try writer.objectField("biomass");try writer.write(self.biomass);try writer.endObject();
 }
};
pub const Snapshot=struct{entries:[4]Entry=.{.{},.{},.{},.{}},len:u8=0,valid:bool=true};
pub fn capture(cohorts:anytype)Snapshot{
 var out=Snapshot{};
 for(cohorts)|c|{
  if(!std.math.isFinite(c.biomass) or c.biomass<0)return .{.valid=false};
  if(c.biomass<=0)continue;
  if(!@hasField(@TypeOf(c),"lineage"))return .{.valid=false};
  if(out.len==4 or c.lineage==0)return .{.valid=false};
  for(out.entries[0..out.len])|prior|if(prior.id==c.lineage)return .{.valid=false};
  out.entries[out.len]=.{.id=c.lineage,.biomass=c.biomass};out.len+=1;
 }
 return out;
}
test "exact string IDs beyond JS integer range and max u64"{
 const entry=Entry{.id=std.math.maxInt(u64),.biomass=0.125};const j=try std.json.stringifyAlloc(std.testing.allocator,entry,.{});defer std.testing.allocator.free(j);
 try std.testing.expectEqualStrings("{\"id\":\"18446744073709551615\",\"biomass\":1.25e-1}",j);
}
test "bounded finite unique living identities with tiny survivors"{
 const C=struct{lineage:u64,biomass:f32};const data=[_]C{.{.lineage=9007199254740993,.biomass=0.1},.{.lineage=17,.biomass=1e-9},.{.lineage=0,.biomass=0}};
 const a=capture(data);try std.testing.expect(a.valid and a.len==2 and a.entries[0].id==9007199254740993);
 try std.testing.expect(!capture([_]C{data[0],data[0]}).valid);
 try std.testing.expect(!capture([_]C{.{.lineage=1,.biomass=std.math.nan(f32)}}).valid);
 try std.testing.expect(!capture([_]C{.{.lineage=0,.biomass=1}}).valid);
 const noid=struct{biomass:f32};try std.testing.expect(!capture([_]noid{.{.biomass=1}}).valid);
}

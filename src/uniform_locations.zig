//! Fixed storage owned by exactly one linked program. Overflow falls back to GL.
const std=@import("std");
pub const Cache=struct {
 const Entry=struct{name:[64]u8=undefined,len:u8=0,location:i32=0};
 entries:[32]Entry=undefined,count:u8=0,
 pub fn clear(self:*Cache)void{self.count=0;}
 pub fn get(self:*const Cache,name:[]const u8)?i32{
  if(name.len>64)return null;
  for(self.entries[0..self.count])|entry|if(std.mem.eql(u8,entry.name[0..entry.len],name))return entry.location;
  return null;
 }
 pub fn put(self:*Cache,name:[]const u8,location:i32)void{
  if(name.len>64 or self.count>=self.entries.len)return;
  const e=&self.entries[self.count];@memcpy(e.name[0..name.len],name);e.len=@intCast(name.len);e.location=location;self.count+=1;
 }
};
test "owned name content, missing uniform -1, exact names and relink reset" {
 var c=Cache{};var name=[_]u8{'f','o','o'};c.put(&name,7);name[0]='b';
 try std.testing.expectEqual(@as(?i32,7),c.get("foo"));try std.testing.expect(c.get("boo")==null);try std.testing.expect(c.get("fo")==null);
 c.put("missing",-1);try std.testing.expectEqual(@as(?i32,-1),c.get("missing"));c.clear();try std.testing.expect(c.get("foo")==null);
}
test "program caches isolated and fixed capacity fallback including long names" {
 var a=Cache{};var b=Cache{};a.put("x",1);b.put("x",9);try std.testing.expect(a.get("x").?!=b.get("x").?);
 var chars:[65]u8=[_]u8{'a'}**65;a.put(&chars,5);try std.testing.expect(a.get(&chars)==null);
 a.clear();for(0..32)|i|{var name:[2]u8=.{@intCast(i),0};a.put(&name,@intCast(i));}
 a.put("overflow",42);try std.testing.expect(a.get("overflow")==null);try std.testing.expectEqual(@as(u8,32),a.count);
}

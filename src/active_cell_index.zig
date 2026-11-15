//! Transient ordered activity index. No world ownership, serialized state or RNG.
//! Caller frees init()'s words with the SAME allocator at the end of the tick.
const std=@import("std");
pub fn init(allocator:std.mem.Allocator,count:usize)![]u64{
 const words=try allocator.alloc(u64,count/64+@as(usize,@intFromBool(count%64!=0)));
 @memset(words,0);return words;
}
pub fn mark(words:[]u64,index:usize)void{
 std.debug.assert(index/64<words.len);
 words[index/64]|=@as(u64,1)<<@as(u6,@intCast(index%64));
}
/// Reload words each call: arrivals at a FUTURE index must be seen this phase,
/// including arrivals into the current word. Lower indices are not revisited.
pub fn next(words:[]const u64,cursor:*usize,count:usize)?usize{
 if(cursor.*>=count)return null;
 var word=cursor.*/64;
 var mask=words[word]&(~@as(u64,0)<<@as(u6,@intCast(cursor.*%64)));
 while(true){
  if(mask!=0){const index=word*64+@ctz(mask);if(index>=count)return null;cursor.*=index+1;return index;}
  word+=1;if(word>=words.len)return null;mask=words[word];
 }
}
/// Allocation refusal retains the original ascending full scan, never drops life.
pub fn nextOrLinear(words:?[]const u64,cursor:*usize,count:usize)?usize{
 if(words)|bits|return next(bits,cursor,count);
 if(cursor.*>=count)return null;
 const index=cursor.*;cursor.*+=1;return index;
}
test "future same-word writes are seen; prior cells never revisited"{
 const bits=try init(std.testing.allocator,130);defer std.testing.allocator.free(bits);
 mark(bits,2);mark(bits,90);var c:usize=0;
 try std.testing.expectEqual(@as(?usize,2),next(bits,&c,130));
 mark(bits,3);mark(bits,1);try std.testing.expectEqual(@as(?usize,3),next(bits,&c,130));
 try std.testing.expectEqual(@as(?usize,90),next(bits,&c,130));mark(bits,129);
 try std.testing.expectEqual(@as(?usize,129),next(bits,&c,130));try std.testing.expectEqual(@as(?usize,null),next(bits,&c,130));
}
test "empty, exact word boundary, padding and dense ascending traversal"{
 for([_]usize{0,1,63,64,65,129,130})|count|{
  const bits=try init(std.testing.allocator,count);defer std.testing.allocator.free(bits);var cursor:usize=0;
  try std.testing.expectEqual(@as(?usize,null),next(bits,&cursor,count));
  for(0..count)|i|mark(bits,i);
  cursor=0;for(0..count)|i|try std.testing.expectEqual(@as(?usize,i),next(bits,&cursor,count));
  try std.testing.expectEqual(@as(?usize,null),next(bits,&cursor,count));
 }
 var words=[_]u64{~@as(u64,0),~@as(u64,0)};var c:usize=64;
 try std.testing.expectEqual(@as(?usize,64),next(&words,&c,65));try std.testing.expectEqual(@as(?usize,null),next(&words,&c,65));
}
test "allocation refusal and fallback preserve complete linear traversal"{
 var memory:[0]u8=.{};var allocator=std.heap.FixedBufferAllocator.init(&memory);
 try std.testing.expectError(error.OutOfMemory,init(allocator.allocator(),65));
 var cursor:usize=0;for(0..130)|i|try std.testing.expectEqual(@as(?usize,i),nextOrLinear(null,&cursor,130));
 try std.testing.expectEqual(@as(?usize,null),nextOrLinear(null,&cursor,130));
}

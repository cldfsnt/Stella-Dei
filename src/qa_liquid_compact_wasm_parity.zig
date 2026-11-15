//! Standalone platform parity only; no browser, full-frame or performance claim.
const std=@import("std");const K=@import("experimental/liquid_gather_compact.zig");const C=@import("experimental/liquid_gather_cached.zig");
const Input=struct{mass:[]f32,elevation:[]f32,neighbors:[][6]usize,area:f64};
var bytes:[]u8=&.{};
export fn qa_width()u32{return std.simd.suggestVectorLength(f32) orelse 4;}
export fn qa_word_bits()u32{return @bitSizeOf(usize);}
export fn qa_output()[*]const u8{return bytes.ptr;}
export fn qa_output_len()usize{return bytes.len;}
export fn qa_run(data:[*]const u8,len:usize)u32{run(data[0..len]) catch return 1;return 0;}
fn run(json:[]const u8)!void{
 @setFloatMode(.strict);
 const a=std.heap.c_allocator;const parsed=try std.json.parseFromSlice(Input,a,json,.{});defer parsed.deinit();const d=parsed.value;const n=d.mass.len;
 if(n!=40962 or d.elevation.len!=n or d.neighbors.len!=n)return error.InvalidShape;
 const slots=try a.alloc([6]u8,n);defer a.free(slots);try C.prepare(d.neighbors,slots);
 const ea=try a.alloc([6]f64,n);defer a.free(ea);const eb=try a.alloc([6]f32,n);defer a.free(eb);const heads=try a.alloc(f32,n);defer a.free(heads);const oa=try a.alloc(f32,n);defer a.free(oa);const ob=try a.alloc(f32,n);defer a.free(ob);
 const km:f32=@floatCast(1.0/1000.0/d.area/1000.0*1e9);var output=std.ArrayList(u8).init(a);errdefer output.deinit();try output.appendSlice("LIQUID01");
 for([_]f32{0,360,1440,15000})|dt|{
  const reference=try C.step(d.mass,d.elevation,d.neighbors,slots,ea,oa,km,dt,false);
  for([_]bool{false,true})|reverse|{
   const got=try K.step(d.mass,d.elevation,d.neighbors,slots,eb,heads,ob,km,dt,reverse);
   for(ea,eb)|reference_edges,compact_edges|for(reference_edges,compact_edges)|r,c|{if(@as(u64,@bitCast(r))!=@as(u64,@bitCast(@as(f64,c))))return error.EdgeParity;};
   if(!std.mem.eql(u8,std.mem.sliceAsBytes(oa),std.mem.sliceAsBytes(ob)) or @as(u64,@bitCast(reference.rounding_signed))!=@as(u64,@bitCast(got.rounding_signed)) or @as(u64,@bitCast(reference.rounding_absolute))!=@as(u64,@bitCast(got.rounding_absolute)))return error.Parity;
  }
  try output.appendSlice(std.mem.asBytes(&dt));try output.appendSlice(std.mem.sliceAsBytes(oa));try output.appendSlice(std.mem.sliceAsBytes(ea));try output.appendSlice(std.mem.asBytes(&reference.rounding_signed));try output.appendSlice(std.mem.asBytes(&reference.rounding_absolute));
 }
 bytes=try output.toOwnedSlice();
}
pub fn main()!void{
 const a=std.heap.c_allocator;const args=try std.process.argsAlloc(a);defer std.process.argsFree(a,args);if(args.len!=3)return error.Usage;
 const input=try std.fs.cwd().readFileAlloc(a,args[1],20*1024*1024);defer a.free(input);try run(input);defer a.free(bytes);try std.fs.cwd().writeFile(.{.sub_path=args[2],.data=bytes});
 std.debug.print("LIQUID_PLATFORM native width={} usize_bits={} bytes={} four_dt=0,360,1440,15000 compact_cached_both_orders_exact=true\n",.{qa_width(),qa_word_bits(),bytes.len});
}

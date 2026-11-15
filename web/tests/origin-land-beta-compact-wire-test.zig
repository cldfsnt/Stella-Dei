const std=@import("std");const S=@import("save_schema_compact_qa.zig");
test "compact off endpoint writer" {
 const a=std.testing.allocator;
 inline for(.{"natural","warm"})|name|{
  const base="/workspace/scratch/f67c3ac60ca3/site-tmp/origin-land-gate/";
  const b=try std.fs.cwd().readFileAlloc(a,base++"candidate-"++name++".json",128*1024*1024);defer a.free(b);var p=try S.parse(a,b);defer p.deinit();const out=try std.json.stringifyAlloc(a,p.value,.{});defer a.free(out);
  const old=try std.fs.cwd().readFileAlloc(a,base++"baseline-"++name++".json",128*1024*1024);defer a.free(old);try std.testing.expectEqualStrings(old,out);
  try std.fs.cwd().writeFile(.{.sub_path=base++"compact-"++name++".json",.data=out});std.debug.print("COMPACT_WIRE {s} exact_baseline_bytes=true bytes={d}\n",.{name,out.len});
 }
}

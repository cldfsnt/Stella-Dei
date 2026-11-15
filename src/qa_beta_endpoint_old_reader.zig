const std=@import("std");const S=@import("save_schema.zig");
test "unchanged v72 reader canonical full scheduler endpoints" {
 const a=std.testing.allocator;
 inline for(.{"natural","warm"})|name|{
  const base="/workspace/scratch/f67c3ac60ca3/site-tmp/origin-land-gate/";
  const b=try std.fs.cwd().readFileAlloc(a,base++"baseline-"++name++".json",128*1024*1024);defer a.free(b);
  const c=try std.fs.cwd().readFileAlloc(a,base++"candidate-"++name++".json",128*1024*1024);defer a.free(c);
  var bp=try S.parse(a,b);defer bp.deinit();var cp=try S.parse(a,c);defer cp.deinit();
  try std.testing.expectEqualDeep(bp.value,cp.value);
  const bc=try std.json.stringifyAlloc(a,bp.value,.{});defer a.free(bc);const cc=try std.json.stringifyAlloc(a,cp.value,.{});defer a.free(cc);
  try std.testing.expectEqualStrings(bc,cc);
  std.debug.print("OLD_ENDPOINT {s} typed_exact=true canonical_bytes_exact=true baseline_bytes={d} candidate_bytes={d}\n",.{name,b.len,c.len});
 }
}

test "law4 persisted identity and older identities unchanged" {
 var saved=fixture();saved.version=12;saved.mode=.origin;
 const cells=[_]Microbes.Cell{Microbes.initialized(42)}**12;const sparse=try captureSparse(std.testing.allocator,&cells);defer sparse.deinit(std.testing.allocator);
 saved.origin=.{.model_revision=5,.cohort_encoding=.sparse_indexed,.cells=sparse.cells,.stats=.{}};const soil=[_]f64{0}**12;const vapor=[_]f64{0.5}**12;
 saved.beta_origin=.{.format=.origin_land_beta_v4,.config=.{.enabled=true,.law=1,.physiology_law=4,.root_mutation=.{.enabled=true,.law=1,.stream_seed=42}},.soil=&soil,.vapor=&vapor};
 try saved.validate();const bytes=try std.json.stringifyAlloc(std.testing.allocator,saved,.{});defer std.testing.allocator.free(bytes);var parsed=try parse(std.testing.allocator,bytes);defer parsed.deinit();try std.testing.expectEqualDeep(saved,parsed.value);
 for([_]u32{7,8,9,10,11})|v|{var bad=saved;bad.version=v;try std.testing.expectError(error.IncompatibleSave,bad.validate());}
 var bad=saved;bad.beta_origin.?.format=.origin_land_beta_v2;try std.testing.expectError(error.IncompatibleSave,bad.validate());
}

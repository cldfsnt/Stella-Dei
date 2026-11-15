test "immersion physiology identity roundtrip and old identity refusal" {
 var saved=fixture();saved.version=9;saved.mode=.origin;
 const cells=[_]Microbes.Cell{Microbes.initialized(42)}**12;
 const sparse=try captureSparse(std.testing.allocator,&cells);defer sparse.deinit(std.testing.allocator);
 saved.origin=.{.model_revision=5,.cohort_encoding=.sparse_indexed,.cells=sparse.cells,.stats=.{}};
 const soil=[_]f64{0}**12;const vapor=[_]f64{0.5}**12;
 saved.beta_origin=.{.format=.origin_land_beta_v2,.config=.{.enabled=true,.law=1,.physiology_law=2,.root_mutation=.{.enabled=true,.law=1,.stream_seed=42}},.soil=&soil,.vapor=&vapor};
 try saved.validate();const bytes=try std.json.stringifyAlloc(std.testing.allocator,saved,.{});defer std.testing.allocator.free(bytes);var decoded=try parse(std.testing.allocator,bytes);defer decoded.deinit();try std.testing.expectEqualDeep(saved,decoded.value);
 var bad=saved;bad.version=8;try std.testing.expectError(error.IncompatibleSave,bad.validate());bad=saved;bad.beta_origin.?.format=.origin_land_beta_v1;try std.testing.expectError(error.IncompatibleSave,bad.validate());bad=saved;bad.beta_origin.?.config.physiology_law=3;try std.testing.expectError(error.InvalidValue,bad.validate());
 saved.version=8;saved.beta_origin.?.format=.origin_land_beta_v1;saved.beta_origin.?.config.physiology_law=1;try saved.validate();const old=try std.json.stringifyAlloc(std.testing.allocator,saved,.{});defer std.testing.allocator.free(old);try std.testing.expect(std.mem.indexOf(u8,old,"physiology_law")==null);var old_decoded=try parse(std.testing.allocator,old);defer old_decoded.deinit();try std.testing.expectEqual(@as(u8,1),old_decoded.value.beta_origin.?.config.physiology_law);
}

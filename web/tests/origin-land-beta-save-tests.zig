test "beta authority sparse roots identity and legacy rejection" {
 var saved=fixture();saved.version=8;saved.mode=.origin;
 var cells=[_]Microbes.Cell{Microbes.initialized(42)}**12;var stats:Microbes.Stats=.{};_=Microbes.seed(&cells[0],&stats,1);cells[0].cohorts[0].root_fraction=0.25;
 const sparse=try captureSparse(std.testing.allocator,&cells);defer sparse.deinit(std.testing.allocator);
 saved.origin=.{.model_revision=5,.cohort_encoding=.sparse_indexed,.cells=sparse.cells,.stats=stats};
 var soil=[_]f64{0}**12;soil[11]=0.125;var vapor=[_]f64{0.5}**12;vapor[0]+=0x1p-40;
 saved.beta_origin=.{.format=.origin_land_beta_v1,.config=.{.enabled=true,.law=1,.root_mutation=.{.enabled=true,.law=1,.stream_seed=std.math.maxInt(u64)}},.soil=&soil,.vapor=&vapor};
 try saved.validate();const bytes=try std.json.stringifyAlloc(std.testing.allocator,saved,.{});defer std.testing.allocator.free(bytes);var parsed=try parse(std.testing.allocator,bytes);defer parsed.deinit();try std.testing.expectEqualDeep(saved,parsed.value);try std.testing.expectEqual(vapor[0],parsed.value.beta_origin.?.vapor[0]);
 for(1..8)|v|{var bad=saved;bad.version=@intCast(v);try std.testing.expectError(error.IncompatibleSave,bad.validate());}
 var bad=saved;bad.beta_origin=null;try std.testing.expectError(error.IncompatibleSave,bad.validate());
 bad=saved;bad.beta_origin.?.config.law=2;try std.testing.expectError(error.InvalidValue,bad.validate());
 bad=saved;bad.beta_origin.?.config.root_mutation.enabled=false;try std.testing.expectError(error.InvalidValue,bad.validate());
 bad=saved;bad.beta_origin.?.soil=soil[0..11];try std.testing.expectError(error.InvalidShape,bad.validate());
 soil[11]=std.math.nan(f64);try std.testing.expectError(error.InvalidValue,saved.validate());soil[11]=1.1;try std.testing.expectError(error.InvalidValue,saved.validate());soil[11]=0.125;
 vapor[0]=0.6;try std.testing.expectError(error.InvalidValue,saved.validate());vapor[0]=std.math.inf(f64);try std.testing.expectError(error.InvalidValue,saved.validate());vapor[0]=0.5;
 bad=saved;bad.mode=.sandbox;try std.testing.expectError(error.InvalidValue,bad.validate());
}

const std=@import("std");const C=@import("land_beta.zig").Config;const M=@import("microbes.zig");
test "beta config rejects disabled nested mutator and unsupported laws"{
 try std.testing.expect((C{}).valid());
 const good=C{.enabled=true,.law=1,.root_mutation=.{.enabled=true,.law=1,.stream_seed=std.math.maxInt(u64)}};
 try std.testing.expect(good.valid());var bad=good;bad.enabled=false;try std.testing.expect(!bad.valid());bad=good;bad.law=2;try std.testing.expect(!bad.valid());bad=good;bad.root_mutation.law=2;try std.testing.expect(!bad.valid());bad=good;bad.root_mutation.enabled=false;try std.testing.expect(!bad.valid());
 try std.testing.expect(!@hasField(M.Cohort,"stored_water") and !@hasField(M.Cohort,"retention_allocation"));
}
test { _=@import("qa_root_beta_core.zig");_=@import("qa_root_mutation.zig"); }

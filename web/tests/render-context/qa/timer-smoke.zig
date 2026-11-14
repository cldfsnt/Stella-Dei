const P=@import("candidate/src/performance_details.zig");const std=@import("std");
pub fn main()void{P.metrics.setEnabled(true);const t=P.beginStage();P.endStage(t,.ui);std.debug.assert(t!=null);std.debug.print("NATIVE_STAGE_CLOCK valid=true ms={d}\n",.{P.metrics.current.stage_sum[3]});}

const P=@import("candidate/src/performance_details.zig");
export fn stageTimerSmoke() f64 {P.metrics.setEnabled(true);const t=P.beginStage();P.endStage(t,.ui);return P.metrics.current.stage_sum[3];}

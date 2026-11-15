#!/usr/bin/env python3
"""Read-only target traces in a SEPARATE copied root-only experiment tree."""
from pathlib import Path
import sys
p=Path(sys.argv[1]);a=p/'simulation/root_scheduler_audit.zig';s=a.read_text();s+='''
const M=@import("microbes.zig");const R=@import("root_throughflow.zig");const C=@import("capillary_bucket.zig");
pub const TargetRoot=struct{seen:bool=false,soil_before:f64=0,vapor_before:f32=0,environment:?M.Environment=null,cohorts:[4]M.Cohort=.{.{},.{},.{},.{}},receipt:?R.Result=null};
pub const TargetColumn=struct{seen:bool=false,before:?C.State=null,after:?C.Result=null,temperature:f64=0,saturation:f64=0};
pub var target_root:TargetRoot=.{};pub var target_column:TargetColumn=.{};
pub fn resetTarget()void{target_root=.{};target_column=.{};}
pub fn traceRoot(i:usize,cell:M.Cell,soil:f64,vapor:f32,env:M.Environment,r:R.Result)void{if(i==12352)target_root=.{.seen=true,.soil_before=soil,.vapor_before=vapor,.environment=env,.cohorts=cell.cohorts,.receipt=r};}
pub fn traceColumn(i:usize,before:C.State,result:C.Result,temp:f64,saturation:f64)void{if(i==12352)target_column=.{.seen=true,.before=before,.after=result,.temperature=temp,.saturation=saturation};}
''';a.write_text(s)
a=p/'simulation/planet.zig';s=a.read_text();needle='                self.waterMass[i]=column.state.liquid;';assert s.count(needle)==1;s=s.replace(needle,'''                @import("root_scheduler_audit.zig").traceColumn(i,.{.liquid=liquid,.vapor=vapor,.soil=self.rootSoil[i],.rain=self.rainfall[i]},column,temperature,saturation);
'''+needle,1);needle='                self.rootSoil[i]=receipt.soil;';assert s.count(needle)==1;s=s.replace(needle,'''                @import("root_scheduler_audit.zig").traceRoot(i,cell.*,self.rootSoil[i],self.waterVaporMass[i],environment,receipt);
'''+needle,1);a.write_text(s)
print('ROOT_DRAIN_TRACE exact target12352 no physics changes',p)

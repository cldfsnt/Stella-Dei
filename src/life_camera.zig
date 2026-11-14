//! Read-only local occupied-cluster framing. No planet mutation or global search.
const std=@import("std");
pub const Fit=struct{direction:[3]f32,distance:f32,anchor:usize,count:usize,ids:[128]usize,truncated:bool};
fn dot(a:[3]f32,b:[3]f32)f32{return a[0]*b[0]+a[1]*b[1]+a[2]*b[2];}
fn normal(a:[3]f32)?[3]f32{const n=@sqrt(dot(a,a));if(!std.math.isFinite(n) or n<=0)return null;return .{a[0]/n,a[1]/n,a[2]/n};}
fn point(p:anytype,i:usize)[3]f32{const v=p.transformedPoints[i];return .{v.x(),v.y(),v.z()};}
fn contains(ids:[]const usize,id:usize)bool{for(ids)|v|if(v==id)return true;return false;}
fn living(p:anytype,i:usize)bool{if(i>=p.microbeCells.len)return false;for(p.microbeCells[i].cohorts)|c|if(std.math.isFinite(c.biomass) and c.biomass>0.000001)return true;return false;}
pub const FitError=error{InvalidGeometry,ViewportTooSmall,NoNearbyLife,PolarView,TooWide};
pub fn fit(p:anytype,start:usize,width:f32,height:f32)?Fit {return fitDetailed(p,start,width,height) catch null;}
pub fn fitDetailed(p:anytype,start:usize,width:f32,height:f32)FitError!Fit {
 if(start>=p.transformedPoints.len or !std.math.isFinite(width) or !std.math.isFinite(height))return error.InvalidGeometry;
 if(width<240 or height<240)return error.ViewportTooSmall;
 // Search only a few local rings around the actual viewing direction, not stale selection.
 var local:[128]usize=undefined;var levels:[128]u8=undefined;local[0]=start;levels[0]=0;var n:usize=1;var cursor:usize=0;var anchor:?usize=null;
 while(cursor<n):(cursor+=1){const id=local[cursor];if(living(p,id)){anchor=id;break;}if(levels[cursor]>=3)continue;
  for(p.getNeighbours(id))|v|{if(v>=p.transformedPoints.len)return error.InvalidGeometry;if(contains(local[0..n],v))continue;if(n==local.len)break;local[n]=v;levels[n]=levels[cursor]+1;n+=1;}
 }
 const root=anchor orelse return error.NoNearbyLife;const root_dir=normal(point(p,root)) orelse return error.InvalidGeometry;
 var ids:[128]usize=undefined;ids[0]=root;n=1;cursor=0;var truncated=false;
 while(cursor<n):(cursor+=1){for(p.getNeighbours(ids[cursor]))|v|{
  if(v>=p.transformedPoints.len)return error.InvalidGeometry;if(contains(ids[0..n],v) or !living(p,v))continue;
  const dir=normal(point(p,v)) orelse return error.InvalidGeometry;if(dot(root_dir,dir)<0.98){truncated=true;continue;}
  if(n==ids.len){truncated=true;continue;}ids[n]=v;n+=1;
 }}
 var sum=[_]f32{0,0,0};for(ids[0..n])|id|{const dir=normal(point(p,id)) orelse return error.InvalidGeometry;for(0..3)|k|sum[k]+=dir[k];}
 const center=normal(sum) orelse return error.InvalidGeometry;
 // Match orbit camera's fixed Z up. Refuse its singular polar region, don't jump elsewhere.
 if(@abs(center[2])>0.95)return error.PolarView;
 const right=normal(.{center[1],-center[0],0}) orelse return error.InvalidGeometry;
 const up=[_]f32{right[1]*center[2],-right[0]*center[2],right[0]*center[1]-right[1]*center[0]};
 const tan_y=@tan(@as(f32,std.math.pi/180.0*35.0));const tan_x=tan_y*width/height;
 const usable_x=std.math.clamp((width-72)/width,0.2,0.9);
 const usable_y=std.math.clamp((height-220)/height,0.2,0.9);
 var distance:f32=0;var max_radius:f32=0;
 for(ids[0..n])|id|{const v=point(p,id);const r=@sqrt(dot(v,v));if(!std.math.isFinite(r))return error.InvalidGeometry;max_radius=@max(max_radius,r);
  const depth=dot(v,center);distance=@max(distance,depth+@max(@abs(dot(v,right))/(tan_x*usable_x),@abs(dot(v,up))/(tan_y*usable_y)));
 }
 distance=@max(distance,max_radius+100);
 if(!std.math.isFinite(distance))return error.InvalidGeometry;
 if(distance>max_radius*2)return error.TooWide;
 return .{.direction=center,.distance=distance,.anchor=root,.count=n,.ids=ids,.truncated=truncated};
}
const V=struct{v:[3]f32,fn x(s:@This())f32{return s.v[0];}fn y(s:@This())f32{return s.v[1];}fn z(s:@This())f32{return s.v[2];}};
const Mock=struct{
 transformedPoints:[5]V=.{.{.v=.{5000,0,0}},.{.v=.{4999,100,0}},.{.v=.{4999,-100,0}},.{.v=.{-5000,0,0}},.{.v=.{0,0,5000}}},
 microbeCells:[5]struct{cohorts:[1]struct{biomass:f32}}=.{.{.cohorts=.{.{.biomass=1}}},.{.cohorts=.{.{.biomass=1}}},.{.cohorts=.{.{.biomass=1}}},.{.cohorts=.{.{.biomass=1}}},.{.cohorts=.{.{.biomass=1}}}},
 fn getNeighbours(_: *@This(),id:usize)[]const usize{return switch(id){0=>&.{1,2},1=>&.{0},2=>&.{0},3=>&.{3},else=>&.{4}};}
};
test "local cluster excludes distant island and frames portrait with safe altitude"{var p=Mock{};const f=fit(&p,0,320,700).?;try std.testing.expectEqual(@as(usize,3),f.count);try std.testing.expect(!contains(f.ids[0..f.count],3));try std.testing.expect(f.distance>=5100);try std.testing.expect(f.distance>fit(&p,0,700,390).?.distance);}
test "empty nearby cluster and polar center refuse without mutation"{var p=Mock{};const old=p;try std.testing.expect(fit(&p,4,390,700)==null);try std.testing.expectEqualDeep(old,p);for(0..3)|i|p.microbeCells[i].cohorts[0].biomass=0;try std.testing.expect(fit(&p,0,390,700)==null);}
test "invalid viewport and geometry fail safely"{var p=Mock{};try std.testing.expect(fit(&p,0,std.math.nan(f32),700)==null);p.transformedPoints[1].v[0]=std.math.nan(f32);try std.testing.expect(fit(&p,0,390,700)==null);}

test "fit failure reasons distinguish empty, small viewport, polar and invalid geometry" {
 var p=Mock{};
 try std.testing.expectError(error.ViewportTooSmall,fitDetailed(&p,0,390,180));
 try std.testing.expectError(error.PolarView,fitDetailed(&p,4,390,700));
 try std.testing.expectError(error.InvalidGeometry,fitDetailed(&p,0,std.math.nan(f32),700));
 for(0..3)|i|p.microbeCells[i].cohorts[0].biomass=0;
 try std.testing.expectError(error.NoNearbyLife,fitDetailed(&p,0,390,700));
}

//! Explicit one-shot navigation. Reads surviving life, never creates or tracks it.
const std=@import("std");
pub const Kind=enum{plants,rabbits};
pub const Visibility=enum{visible,sparse,submerged,rabbit};
pub const Found=struct{index:usize,position:[3]f32,visibility:Visibility};
pub const Error=error{InvalidGeometry,NoLife,UnsafeView,ViewportTooSmall};
fn normal(p:[3]f32)?[3]f32{var sum:f32=0;for(p)|v|{if(!std.math.isFinite(v))return null;sum+=v*v;}if(!std.math.isFinite(sum) or sum<=0)return null;const n=@sqrt(sum);return .{p[0]/n,p[1]/n,p[2]/n};}
fn dot(a:[3]f32,b:[3]f32)f32{return a[0]*b[0]+a[1]*b[1]+a[2]*b[2];}
pub fn find(p:anytype,kind:Kind,view:[3]f32,width:f32,height:f32)Error!Found{
 if(!std.math.isFinite(width) or !std.math.isFinite(height))return error.InvalidGeometry;
 // Keep the centered target clear of the full166px toolbar and84px footer.
 const toolbar:f32=if(width>=650)112 else 166;
 if(width<240 or height<2*(toolbar+20) or height<208)return error.ViewportTooSmall;
 const direction=normal(view) orelse return error.InvalidGeometry;
 var best:?Found=null;var best_rank:u8=255;var best_score:f32=-2;var any=false;
 if(kind==.plants){
  if(p.vegetation.len!=p.transformedPoints.len or p.waterMass.len!=p.vegetation.len)return error.InvalidGeometry;
  const conv=p.getKmPerWaterMass();if(!std.math.isFinite(conv) or conv<=0)return error.InvalidGeometry;
  for(p.vegetation,0..)|cover,i|{
   if(!std.math.isFinite(cover) or cover<0 or cover>1)return error.InvalidGeometry;if(cover==0)continue;any=true;
   const depth=p.waterMass[i]*conv;if(!std.math.isFinite(depth) or depth<0)return error.InvalidGeometry;
   const point=p.transformedPoints[i].data;const d=normal(point) orelse return error.InvalidGeometry;if(@abs(d[2])>0.94)continue;
   const visibility:Visibility=if(depth>0.0005).submerged else if(cover<0.08).sparse else .visible;
   const rank:u8=switch(visibility){.visible=>0,.sparse=>1,.submerged=>2,else=>unreachable};const score=dot(direction,d);
   if(rank<best_rank or (rank==best_rank and score>best_score)){best=.{.index=i,.position=point,.visibility=visibility};best_rank=rank;best_score=score;}
  }
 }else{
  for(p.lifeforms.items,0..)|rabbit,i|{any=true;const point=rabbit.position.data;const d=normal(point) orelse return error.InvalidGeometry;if(@abs(d[2])>0.94)continue;const score=dot(direction,d);if(score>best_score){best=.{.index=i,.position=point,.visibility=.rabbit};best_score=score;}}
 }
 return best orelse if(any)error.UnsafeView else error.NoLife;
}
const V=struct{data:[3]f32};
const Mock=struct{
 vegetation:[]const f32,waterMass:[]const f32,transformedPoints:[]const V,
 lifeforms:struct{items:[]const struct{position:V}}=.{.items=&.{}},
 fn getKmPerWaterMass(_: *@This())f32{return 1;}
};
test "explicit plant search prefers visible then sparse then submerged, stable ties"{
 const points=[_]V{.{.data=.{5000,0,0}},.{.data=.{0,5000,0}},.{.data=.{-5000,0,0}}};var covers=[_]f32{0.01,0.5,0.9};var water=[_]f32{0,0,0.001};var p=Mock{.vegetation=&covers,.waterMass=&water,.transformedPoints=&points};
 try std.testing.expectEqual(@as(usize,1),(try find(&p,.plants,.{1,0,0},390,700)).index);
 covers[1]=0;try std.testing.expectEqual(Visibility.sparse,(try find(&p,.plants,.{1,0,0},390,700)).visibility);
 covers[0]=0;try std.testing.expectEqual(Visibility.submerged,(try find(&p,.plants,.{1,0,0},390,700)).visibility);
 covers[2]=0;try std.testing.expectError(error.NoLife,find(&p,.plants,.{1,0,0},390,700));
}
test "empty rabbits and invalid or too-small view refuse without input changes"{
 var p=Mock{.vegetation=&.{},.waterMass=&.{},.transformedPoints=&.{}};
 try std.testing.expectError(error.NoLife,find(&p,.rabbits,.{1,0,0},390,700));
 try std.testing.expectError(error.ViewportTooSmall,find(&p,.plants,.{1,0,0},390,300));
 try std.testing.expectError(error.InvalidGeometry,find(&p,.plants,.{0,0,0},390,700));
 const points=[_]V{.{.data=.{0,0,5000}}};p.transformedPoints=&points;p.vegetation=&.{0.5};p.waterMass=&.{0};
 try std.testing.expectError(error.UnsafeView,find(&p,.plants,.{1,0,0},390,700));
}
test "rabbit choice uses actual position, stable nearest tie and no persistent identity"{
 const Animal=struct{position:V};const animals=[_]Animal{.{.position=.{.data=.{0,5000,0}}},.{.position=.{.data=.{5000,0,0}}}};
 var p=struct{vegetation:[]const f32=&.{},waterMass:[]const f32=&.{},transformedPoints:[]const V=&.{},lifeforms:struct{items:[]const Animal},fn getKmPerWaterMass(_: *@This())f32{return 1;}}{.lifeforms=.{.items=&animals}};
 const result=try find(&p,.rabbits,.{1,0,0},390,700);try std.testing.expectEqual(@as(usize,1),result.index);try std.testing.expectEqualDeep(animals[1].position.data,result.position);
}

test "wide390 landscape clears toolbar; malformed cover refuses"{
 const points=[_]V{.{.data=.{5000,0,0}}};var covers=[_]f32{0.5};var p=Mock{.vegetation=&covers,.waterMass=&.{0},.transformedPoints=&points};
 _=try find(&p,.plants,.{1,0,0},700,390);
 try std.testing.expectError(error.ViewportTooSmall,find(&p,.plants,.{1,0,0},390,360));
 covers[0]=1.01;try std.testing.expectError(error.InvalidGeometry,find(&p,.plants,.{1,0,0},700,390));
}

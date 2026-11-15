//! Read-only patch-level feeding-history schematic. Not current feeding or taxonomy.
const std=@import("std");
pub const Kind=enum{none,mixed,dominant};
pub fn classify(cohorts:anytype)Kind{
 var living:f64=0;var recorded:f64=0;
 for(cohorts)|c|{
  if(!std.math.isFinite(c.biomass) or c.biomass<=0 or c.lineage==0)continue;
  living+=c.biomass;
  if(std.math.isFinite(c.feeding) and c.feeding>0 and std.math.isFinite(c.lifetime_grazed) and c.lifetime_grazed>0)recorded+=c.biomass;
 }
 if(recorded<=0 or !std.math.isFinite(living))return .none;
 return if(recorded>=living*0.5) .dominant else .mixed;
}
test "history marker counts actual living ownership not capability or animal identity"{
 const C=struct{biomass:f32=1,lineage:u64=1,feeding:f32=0,lifetime_grazed:f32=0};
 var a=[_]C{.{},.{.lineage=2}};
 try std.testing.expectEqual(Kind.none,classify(a));a[0].feeding=1;try std.testing.expectEqual(Kind.none,classify(a));
 a[0].lifetime_grazed=0.01;try std.testing.expectEqual(Kind.dominant,classify(a));
 a[0].biomass=0.99;try std.testing.expectEqual(Kind.mixed,classify(a));
 a[0].biomass=0;try std.testing.expectEqual(Kind.none,classify(a));a[0].biomass=1;a[0].lineage=0;try std.testing.expectEqual(Kind.none,classify(a));
 a[0].lineage=1;a[0].feeding=std.math.inf(f32);try std.testing.expectEqual(Kind.none,classify(a));a[0].feeding=1;a[0].lifetime_grazed=std.math.nan(f32);try std.testing.expectEqual(Kind.none,classify(a));
 a[0].lifetime_grazed=1;a[0].biomass=std.math.nan(f32);try std.testing.expectEqual(Kind.none,classify(a));
}
test "classification is slot invariant and leaves source bitwise unchanged"{
 const C=struct{biomass:f32,lineage:u64,feeding:f32,lifetime_grazed:f32};
 const a=[_]C{.{.biomass=0.1,.lineage=1,.feeding=0.1,.lifetime_grazed=0.1},.{.biomass=0.8,.lineage=2,.feeding=0,.lifetime_grazed=0}};
 try std.testing.expectEqual(classify(a),classify([_]C{a[1],a[0]}));try std.testing.expectEqual(Kind.mixed,classify(a));
}

/// Selected patch first; all other mesh indices retain their relative order.
pub fn orderedIndex(cursor:usize,total:usize,selected:?usize)usize{
 if(selected)|s|{if(s<total){if(cursor==0)return s;const raw=cursor-1;return if(raw>=s)raw+1 else raw;}}
 return cursor;
}
pub fn fits(x:f32,y:f32,scale:f32,width:f32,height:f32,top:f32)bool{
 if(!std.math.isFinite(x) or !std.math.isFinite(y) or !std.math.isFinite(scale) or scale<=0)return false;
 return x-22*scale>=4 and x+22*scale<=width-4 and y-41*scale>=top and y+9*scale<=height-90;
}
test "selected order preserves all other indices with bounded count"{
 for(0..65)|n|for(0..n+1)|selected|{
  var prev:?usize=null;var seen=[_]bool{false}**65;
  for(0..n)|i|{const idx=orderedIndex(i,n,selected);try std.testing.expect(idx<n and !seen[idx]);seen[idx]=true;if(idx!=selected){if(prev)|p|try std.testing.expect(idx>p);prev=idx;}}
 };
 try std.testing.expectEqual(@as(usize,2),orderedIndex(2,4,null));
}
test "selected scale remains within toolbar footer and side occlusion bounds"{
 try std.testing.expect(fits(160,350,0.75,320,700,166));
 try std.testing.expect(!fits(10,350,0.75,320,700,166));
 try std.testing.expect(!fits(310,350,0.75,320,700,166));
 try std.testing.expect(!fits(160,190,0.75,320,700,166));
 try std.testing.expect(!fits(160,608,0.75,320,700,166));
 try std.testing.expect(!fits(std.math.nan(f32),350,0.75,320,700,166));
}

/// Conservative actual glyph/picker rectangle, including stroke margin below root.
pub fn overlaps(x:f32,y:f32,scale:f32,px:f32,py:f32,ps:f32)bool{
 return x-22*scale<px+22*ps and x+22*scale>px-22*ps and y-41*scale<py+9*ps and y+9*scale>py-41*ps;
}
test "selected footprint excludes nearby glyph bodies without blanket radius"{
 try std.testing.expect(overlaps(100,100,0.75,120,100,0.325));
 try std.testing.expect(overlaps(100,100,0.75,100,118,0.325));
 try std.testing.expect(!overlaps(100,100,0.75,140,100,0.325));
 try std.testing.expect(!overlaps(100,100,0.75,100,145,0.325));
}

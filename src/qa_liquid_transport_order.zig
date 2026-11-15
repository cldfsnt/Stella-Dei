const std=@import("std");
const Input=struct{mass:[]f32,elevation:[]f32,neighbors:[][6]usize,area:f64};
fn legacy(comptime W:usize,input:Input,reverse:bool)![]f32{
 @setFloatMode(.strict);const a=std.testing.allocator;const out=try a.dupe(f32,input.mass);const factor:f32=@min(@as(f32,0.00002)*1440/6,1.0/7.0);const km:f32=@floatCast(1.0/1000.0/input.area/1000.0*1e9);const blocks=out.len/W;
 for(0..blocks)|b|{const start=(if(reverse)blocks-1-b else b)*W;var old:[W]f32=undefined;var height:[W]f32=undefined;var shared:[W]f32=undefined;var removed=[_]f32{0}**W;
  for(0..W)|j|{old[j]=out[start+j];height[j]=input.elevation[start+j]+old[j]*km;shared[j]=old[j]*factor;}
  for(0..6)|dir|for(0..W)|j|{const t=input.neighbors[start+j][dir];const target=input.elevation[t]+input.mass[t]*km;var sent:f32=if(height[j]>target)@min(shared[j],(height[j]-target)/km*factor)else 0;if(t>=start and t<start+W)sent=0;out[t]+=sent;removed[j]+=sent;};
  for(0..W)|j|out[start+j]=old[j]-removed[j];
 }return out;
}
var rounded_signed:f64=0;var rounded_absolute:f64=0;
fn gather(input:Input,reverse:bool,promoted:bool)![]f32{
 @setFloatMode(.strict);const a=std.testing.allocator;const edges=try a.alloc([6]f64,input.mass.len);defer a.free(edges);const result=try a.alloc(f32,input.mass.len);rounded_signed=0;rounded_absolute=0;const factor:f64=@as(f32,@min(@as(f32,0.00002)*1440/6,1.0/7.0));const km:f64=@as(f32,@floatCast(1.0/1000.0/input.area/1000.0*1e9));
 for(0..input.mass.len)|step|{const i=if(reverse)input.mass.len-1-step else step;const h=@as(f64,input.elevation[i])+@as(f64,input.mass[i])*km;var total:f64=0;for(input.neighbors[i],0..)|j,k|{const head=@max(0,h-(@as(f64,input.elevation[j])+@as(f64,input.mass[j])*km));var duplicate=j==i;for(input.neighbors[i][0..k])|prior|{if(prior==j)duplicate=true;}
 const hi:f32=input.elevation[i]+input.mass[i]*@as(f32,@floatCast(km));const hj:f32=input.elevation[j]+input.mass[j]*@as(f32,@floatCast(km));
 const flow:f64=if(duplicate)0 else if(promoted)@min(@as(f64,input.mass[i])*factor,head/km*factor) else if(hi>hj) @as(f64,@min(input.mass[i]*@as(f32,@floatCast(factor)),(hi-hj)/@as(f32,@floatCast(km))*@as(f32,@floatCast(factor)))) else 0;
 edges[i][k]=flow;total+=flow;}try std.testing.expect(total<=input.mass[i]);}
 for(0..input.mass.len)|i|{var value:f64=input.mass[i];for(edges[i])|flow|value-=flow;for(input.neighbors[i],0..)|j,slot|{var duplicate=j==i;for(input.neighbors[i][0..slot])|prior|{if(prior==j)duplicate=true;}if(duplicate)continue;for(input.neighbors[j],0..)|target,k|if(target==i){value+=edges[j][k];};}try std.testing.expect(value>=0 and std.math.isFinite(value));result[i]=@floatCast(value);const error_value=@as(f64,result[i])-value;rounded_signed+=error_value;rounded_absolute+=@abs(error_value);}return result;
}
fn sum(x:[]const f32)f64{var s:f64=0;for(x)|v|s+=v;return s;}
fn differences(a:[]const f32,b:[]const f32)usize{var n:usize=0;for(a,b)|x,y|if(x!=y){n+=1;};return n;}
test "frozen actual world one liquid pass ordering and gather"{
 const a=std.testing.allocator;const path=try std.process.getEnvVarOwned(a,"QA_LIQUID_INPUT");defer a.free(path);const bytes=try std.fs.cwd().readFileAlloc(a,path,20*1024*1024);defer a.free(bytes);const parsed=try std.json.parseFromSlice(Input,a,bytes,.{});defer parsed.deinit();const d=parsed.value;const before=sum(d.mass);
 inline for(.{4,16})|w|{const f=try legacy(w,d,false);defer a.free(f);const r=try legacy(w,d,true);defer a.free(r);std.debug.print("LEGACY width={} cells={} tail={} changed_by_order={} forward_delta={e} reverse_delta={e}\n",.{w,d.mass.len,d.mass.len%w,differences(f,r),sum(f)-before,sum(r)-before});}
 for([_]bool{false,true})|promoted|{const f=try gather(d,false,promoted);defer a.free(f);const r=try gather(d,true,promoted);defer a.free(r);try std.testing.expectEqualSlices(f32,f,r);std.debug.print("GATHER promoted_head={} cells={} order_exact=true delta={e} endpoint_rounding_signed={e} endpoint_rounding_sumabs={e}\n",.{promoted,d.mass.len,sum(f)-before,rounded_signed,rounded_absolute});}
}
test "same lane edges suppressed and final partial block never donates"{
 var mass=[_]f32{1,0,0,0,1};var elevation=[_]f32{0}**5;var neighbors=[_][6]usize{.{1,0,0,0,0,0},.{0,1,1,1,1,1},.{2,2,2,2,2,2},.{3,3,3,3,3,3},.{1,4,4,4,4,4}};const d=Input{.mass=&mass,.elevation=&elevation,.neighbors=&neighbors,.area=1000};const old=try legacy(4,d,false);defer std.testing.allocator.free(old);try std.testing.expectEqualSlices(f32,&mass,old);std.debug.print("TOY same_lane_donor_unchanged={} tail_donor_unchanged={}\n",.{old[0]==1,old[4]==1});
}

test "gather includes tail and same lane and deduplicates repeated neighbor slots"{var mass=[_]f32{1,0,0,0,1};var elevation=[_]f32{0}**5;var neighbors=[_][6]usize{.{1,1,0,0,0,0},.{0,4,1,1,1,1},.{2,2,2,2,2,2},.{3,3,3,3,3,3},.{1,4,4,4,4,4}};const d=Input{.mass=&mass,.elevation=&elevation,.neighbors=&neighbors,.area=1000};const f=try gather(d,false,false);defer std.testing.allocator.free(f);const r=try gather(d,true,false);defer std.testing.allocator.free(r);try std.testing.expectEqualSlices(f32,f,r);try std.testing.expect(f[0]<1 and f[4]<1 and f[1]>0);try std.testing.expectEqual(f[0],f[4]);std.debug.print("GATHER_TOY same_lane_and_tail_donate=true duplicate_not_double=true delta={e}\n",.{sum(f)-sum(&mass)});}

from pathlib import Path
import shutil
r=Path(__file__).resolve().parents[2];src=r.parent/'site-tmp/rooted-conditions/src';dst=r.parent/'site-tmp/rooted-hardy/src';assert not dst.exists();shutil.copytree(src,dst)
p=dst/'rooted_founder.zig';s=p.read_text().replace('conditions:?Conditions=null,','conditions:?Conditions=null,structure:f32=0,')
s += '''
/// Explicit founder choice only; historical standard action unchanged.
pub fn previewHardy(p:anytype,index:usize)Receipt{var r=preview(p,index);if(r.status==.eligible)r.structure=0.5;return r;}
pub fn applyHardy(p:anytype,index:usize)Receipt{
 var r=apply(p,index);if(r.status!=.planted)return r;
 for(&p.microbeCells[index].cohorts)|*c|{if(c.lineage==r.lineage){c.structure=0.5;break;}}
 r.structure=0.5;return r;
}
'''
s=s.replace('.organization=r.organization};','.organization=r.organization,.structure=r.structure};');p.write_text(s)
p=dst/'main.zig';s=p.read_text();s=s.replace('token:u32,time:f64,','token:u32,hardy:bool=false,time:f64,').replace('.conditions=receipt.conditions}', '.conditions=receipt.conditions,.structure=receipt.structure}')
s=s.replace('pub fn rootedFounderForState(state:*PlayState,world:u32,point:u32,apply:bool)@import("rooted_founder.zig").Receipt{','''pub fn rootedFounderForState(state:*PlayState,world:u32,point:u32,apply:bool)@import("rooted_founder.zig").Receipt{return rootedFounderVariantForState(state,world,point,apply,false);}
pub fn rootedFounderVariantForState(state:*PlayState,world:u32,point:u32,apply:bool,hardy:bool)@import("rooted_founder.zig").Receipt{''')
s=s.replace('var receipt=if(apply) R.apply(&state.planet,point) else R.preview(&state.planet,point);','var receipt=if(hardy) (if(apply) R.applyHardy(&state.planet,point) else R.previewHardy(&state.planet,point)) else (if(apply) R.apply(&state.planet,point) else R.preview(&state.planet,point));')
s=s.replace('pub fn rootedPreviewForState(state:*PlayState,world:u32,point:u32)[*:0]const u8{','''pub fn rootedPreviewForState(state:*PlayState,world:u32,point:u32)[*:0]const u8{return rootedPreviewVariantForState(state,world,point,false);}
pub fn rootedPreviewVariantForState(state:*PlayState,world:u32,point:u32,hardy:bool)[*:0]const u8{''')
s=s.replace('const receipt=rootedFounderForState(state,world,point,false);','const receipt=rootedFounderVariantForState(state,world,point,false,hardy);').replace('.token=rooted_nonce,.time=', '.token=rooted_nonce,.hardy=hardy,.time=')
s=s.replace('rootedFounderForState(state,world,point,true),','rootedFounderVariantForState(state,world,point,true,plan.hardy),')
s+='''
/// Additive preview; existing apply consumes the immutable chosen variant.
export fn stella_hardy_rooted_founder_preview(world:u32,point:u32)[*:0]const u8{
 const state=webPlayState() orelse return rootedReceiptJson(.{.status=.disabled},PerformanceDetails.world_serial,point,0);
 return rootedPreviewVariantForState(state,world,point,true);
}
''';p.write_text(s)
print(dst)

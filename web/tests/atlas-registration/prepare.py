from pathlib import Path
import os
root=Path(os.environ.get('STELLA_SOURCE_ROOT',Path(__file__).resolve().parents[3]))
s=(root/'src/renderer.zig').read_text(); a=s.index('    pub fn toVgImage(');b=s.index('    pub fn deinit(',a);methods=s[a:b].replace('*Texture','*EngineTexture')
s=(root/'deps/nanovg/src/nanovg_gl.zig').read_text();a=s.index('    pub fn allocTexture(');b=s.index('    fn findTexture(',a);alloc=s[a:b]
text='''const std=@import("std");
const GLTexture=struct {id:i32,width:i32,height:i32,tex:u32,flags:struct{},tex_type:enum{rgba}};
const GLContext=struct { const Texture=GLTexture; textures:std.ArrayList(GLTexture),texture_id:i32=0,
'''+alloc+'''};
const nvg=struct {pub const gl=struct{pub const GLContext=GLCtx;};pub const Image=struct{handle:i32};ctx:*Context};
const GLCtx=GLContext;
const Context=struct{params:struct{user_ptr:*anyopaque}};
const EngineTexture=struct {texture:u32,nvgHandle:?i32=null,width:usize,height:usize,
'''+methods+'''};
test "actual registration body returns OOM without publishing or losing GL ownership; retries once" {
 var empty:[0]u8=.{};var fail=std.heap.FixedBufferAllocator.init(&empty);
 var glctx=GLContext{.textures=std.ArrayList(GLTexture).init(fail.allocator())};
 var ctx=Context{.params=.{.user_ptr=&glctx}};const vg=nvg{.ctx=&ctx};
 var texture=EngineTexture{.texture=73,.width=576,.height=384};
 const before=texture;
 try std.testing.expectError(error.OutOfMemory,texture.tryToVgImage(vg));
 try std.testing.expectEqualDeep(before,texture);try std.testing.expectEqual(@as(i32,0),glctx.texture_id);
 glctx.textures=std.ArrayList(GLTexture).init(std.testing.allocator);defer glctx.textures.deinit();
 const image=try texture.tryToVgImage(vg);try std.testing.expectEqual(@as(i32,1),image.handle);
 try std.testing.expectEqual(@as(u32,73),glctx.textures.items[0].tex);
 const again=texture.toVgImage(vg);try std.testing.expectEqual(image.handle,again.handle);
 try std.testing.expectEqual(@as(usize,1),glctx.textures.items.len);
}
'''
(Path(__file__).parent/'registration.test.zig').write_text(text)
p=(root/'src/states/play.zig').read_text();block=p[p.index('    fn loadAquaticAtlas('):p.index('    fn renderBlenderForm(')]
assert block.count('tryToVgImage(vg) catch null')==2
assert '.toVgImage(' not in block
print('PASS: both optional atlas registration paths are fallible; fixture extracted from current source')

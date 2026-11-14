const std=@import("std");
const GLTexture=struct {id:i32,width:i32,height:i32,tex:u32,flags:struct{},tex_type:enum{rgba}};
const GLContext=struct { const Texture=GLTexture; textures:std.ArrayList(GLTexture),texture_id:i32=0,
    pub fn allocTexture(ctx: *GLContext) !*Texture {
        var found_tex: ?*Texture = null;
        for (ctx.textures.items) |*tex| {
            if (tex.id == 0) {
                found_tex = tex;
                break;
            }
        }
        if (found_tex == null) {
            found_tex = try ctx.textures.addOne();
        }
        const tex = found_tex.?;
        tex.* = std.mem.zeroes(Texture);
        ctx.texture_id += 1;
        tex.id = ctx.texture_id;

        return tex;
    }

};
const nvg=struct {pub const gl=struct{pub const GLContext=GLCtx;};pub const Image=struct{handle:i32};ctx:*Context};
const GLCtx=GLContext;
const Context=struct{params:struct{user_ptr:*anyopaque}};
const EngineTexture=struct {texture:u32,nvgHandle:?i32=null,width:usize,height:usize,
    pub fn toVgImage(self: *EngineTexture, vg: nvg) nvg.Image {
        return self.tryToVgImage(vg) catch unreachable;
    }

    /// Optional textures may retain their GL ownership and fall back on OOM.
    /// Publish the NanoVG handle only after registration succeeds.
    pub fn tryToVgImage(self: *EngineTexture, vg: nvg) !nvg.Image {
        if (self.nvgHandle) |handle| {
            return .{ .handle = handle };
        } else {
            const ctx = @as(*nvg.gl.GLContext, @ptrCast(@alignCast(vg.ctx.params.user_ptr)));
            var tex = try ctx.allocTexture();
            tex.width = @as(i32, @intCast(self.width));
            tex.height = @as(i32, @intCast(self.height));
            tex.tex = self.texture;
            tex.flags = .{};
            tex.tex_type = .rgba;

            self.nvgHandle = tex.id;
            return .{ .handle = tex.id };
        }
    }

};
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

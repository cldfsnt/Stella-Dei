const std = @import("std");
pub fn build(b: *std.Build) void {
    const target = b.standardTargetOptions(.{});
    const exe = b.addExecutable(.{ .name = "stella-egl", .root_source_file = .{ .cwd_relative = b.option([]const u8, "source", "Test copy of main.zig") orelse "src/main.zig" }, .target = target, .optimize = .ReleaseSafe });
    exe.linkLibC();
    exe.linkSystemLibrary("m");
    exe.linkSystemLibrary("dl");
    const opts = b.addOptions();
    opts.addOption(bool, "tracy_enabled", false);
    exe.root_module.addOptions("build_options", opts);
    const imports = .{ .{ "gl", "deps/gl3v3.zig" }, .{ "glfw", "deps/web-vendor/mach-glfw/src/main.zig" }, .{ "zalgebra", "deps/web-vendor/zalgebra/src/main.zig" }, .{ "zigimg", "deps/web-vendor/zigimg/zigimg.zig" }, .{ "nanovg", "deps/nanovg/src/nanovg.zig" } };
    inline for (imports) |entry| {
        const m = b.createModule(.{ .root_source_file = b.path("../../" ++ entry[1]), .target = target, .optimize = .ReleaseSafe });
        m.addIncludePath(b.path("../../deps/web-vendor/glfw/include"));
        m.addIncludePath(b.path("../../deps/nanovg/src"));
        exe.root_module.addImport(entry[0], m);
    }
    exe.addIncludePath(b.path("../../deps"));
    exe.addIncludePath(b.path("../../deps/nanovg/src"));
    exe.addIncludePath(b.path("../../deps/web-vendor/glfw/include"));
    exe.addCSourceFiles(.{ .files = &.{ "../../deps/miniaudio.c", "../../deps/nanovg/src/fontstash.c", "../../deps/nanovg/src/stb_image.c", "egl-v21-watch-smoke-shim.c" }, .flags = &.{ "-DFONS_NO_STDIO", "-DSTBI_NO_STDIO", "-fno-sanitize=undefined" } });
    b.installArtifact(exe);
}

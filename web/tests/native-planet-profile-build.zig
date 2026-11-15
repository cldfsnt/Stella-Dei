const std = @import("std");
pub fn build(b: *std.Build) void {
    const target = b.standardTargetOptions(.{});

    const lib = b.addStaticLibrary(.{ .name = "stella", .root_source_file = .{ .cwd_relative = b.option([]const u8,"source","QA root").? }, .target = target, .optimize = .ReleaseSafe });
    lib.root_module.single_threaded = true;
    lib.linkLibC();
    lib.bundle_compiler_rt = true;

    lib.addIncludePath(b.path("../../deps"));
    const opts = b.addOptions();
    opts.addOption(bool, "tracy_enabled", false);
    opts.addOption(bool, "web_gl_debug", b.option(bool, "web-gl-debug", "Enable per-draw NanoVG GL error polling for diagnostic builds") orelse false);
    lib.root_module.addOptions("build_options", opts);
    const imports = .{ .{ "gl", "deps/gl3v3.zig" }, .{ "glfw", "deps/web-vendor/mach-glfw/src/main.zig" }, .{ "zalgebra", "deps/web-vendor/zalgebra/src/main.zig" }, .{ "zigimg", "deps/web-vendor/zigimg/zigimg.zig" }, .{ "nanovg", "deps/nanovg/src/nanovg.zig" } };
    inline for (imports) |entry| {
        const m = b.createModule(.{ .root_source_file = b.path("../../" ++ entry[1]), .target = target, .optimize = .ReleaseSafe });
        m.addIncludePath(b.path("../../deps/web-vendor/glfw/include"));
        m.addIncludePath(b.path("../../deps/nanovg/src"));

        lib.root_module.addImport(entry[0], m);
    }
    b.installArtifact(lib);
}

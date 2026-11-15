const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const root=path.resolve(__dirname,'../..');const read=p=>fs.readFileSync(path.join(root,p),'utf8');
test('web build defaults to explicit false with diagnostic opt in',()=>{
 assert.match(read('web-build.zig'),/"web_gl_debug".*b\.option\(bool, "web-gl-debug".*orelse false/);
 assert.match(read('web/build.sh'),/WEB_GL_DEBUG=\$\{STELLA_WEB_GL_DEBUG:-false\}/);
 assert.match(read('web/build.sh'),/-Dweb-gl-debug="\$WEB_GL_DEBUG"/);
 assert.match(read('web/build.sh'),/true\|false/);
});
test('renderer uses policy and retains independent shader validation',()=>{
 assert.match(read('src/renderer.zig'),/\.debug = @import\("render_diagnostics_policy.zig"\)\.nanoVGDebug\(is_web/);
 assert.match(read('src/render_diagnostics_policy.zig'),/return !is_web or web_opt_in/);
 const nvg=read('deps/nanovg/src/nanovg_gl.zig');
 assert.equal((nvg.match(/ctx\.options\.debug/g)||[]).length,1);
 assert.match(nvg,/if \(!ctx\.options\.debug\) return;\s*const err = gl\.getError\(\)/);
 assert.match(nvg,/gl\.COMPILE_STATUS/);assert.match(nvg,/gl\.LINK_STATUS/);
 assert.match(read('web/build.sh'),/-sASSERTIONS=1/);
});

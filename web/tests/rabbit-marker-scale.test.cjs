const test=require('node:test');const assert=require('node:assert/strict');const fs=require('node:fs');const path=require('node:path');
const root=path.resolve(__dirname,'../..');
test('rabbit badge scaling keeps every visible animal and existing two fills, no picking change',()=>{
 const s=fs.readFileSync(path.join(root,'src/states/play.zig'),'utf8');
 const a=s.indexOf('const marker_scale=@import("../rabbit_marker_scale.zig")');assert(a>0);
 const b=s.indexOf('vg.fillColor(nvg.rgba(8, 15, 28, 225));',a);const block=s.slice(a,b);
 assert.equal((block.match(/for \(/g)||[]).length,1);assert.equal((block.match(/vg\.fill\(\);/g)||[]).length,2);
 assert(block.includes('for (self.planet.lifeforms.items) |lifeform|'));
 assert(block.includes('p.dot(self.cameraPos.sub(p)) <= 0'));
 assert(block.includes('y > height - 90'));
 assert(block.includes('12*marker_scale'));assert(block.includes('4*marker_scale'));
 assert(!/\.append|\.remove|\.clear|pick|continue.*marker_scale/.test(block));
 assert(s.includes('biology_visuals.groundedRabbit(lifeform.position.data, animalScale)'));
});

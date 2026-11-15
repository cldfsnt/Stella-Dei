const test=require('node:test'),assert=require('node:assert/strict'),{copy}=require('../copy-report');
test('explicit local copy preserves exact report and exposes manual fallback',async()=>{
 let writes=[],shown=[];const clipboard={writeText:async text=>writes.push(text)};
 assert.equal(writes.length,0);const text='Build v45\nTarget 24, achieved 6\nRenderer: test';
 assert.equal(await copy({text,clipboard,show:t=>shown.push(t)}),'copied');assert.deepEqual(writes,[text]);assert.deepEqual(shown,[text]);
});
test('restricted or missing clipboard stays manually copyable',async()=>{
 let shown='';for(const clipboard of [null,{}, {writeText:async()=>{throw Error('restricted')}}]){
 assert.equal(await copy({text:'Local sample',clipboard,show:t=>shown=t}),'manual');assert.equal(shown,'Local sample');
 }
});
test('missing or oversized report never writes or displays stale data',async()=>{
 for(const text of ['',null,'x'.repeat(12001)])assert.equal(await copy({text,clipboard:{writeText:()=>assert.fail()},show:()=>assert.fail()}),'unavailable');
});

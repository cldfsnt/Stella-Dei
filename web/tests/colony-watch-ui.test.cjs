const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const html=fs.readFileSync(__dirname+'/../shell.html','utf8');
const code=html.slice(html.indexOf('const patchWatch=StellaPatchWatch.create('),html.indexOf("document.getElementById('close-life').onclick"));
const els=new Map(),el=id=>{if(!els.has(id))els.set(id,{hidden:false,open:false,textContent:'',handlers:{},addEventListener(type,fn){this.handlers[type]=fn;},close(){this.open=false;}});return els.get(id)};
let hooks;const ctl={start:()=>false,cancel(){}};
const ctx={StellaPatchWatch:{create:h=>{hooks=h;return ctl}},StellaColonyWatchDetails:require('../colony-watch-details'),document:{getElementById:el,addEventListener(){}},window:{addEventListener(){}},performance:{now:()=>0},Module:{},lifePoint:1,cancelFeedingSearch(){}};vm.createContext(ctx);
// Load the actual inline-action lifecycle helpers used by these handlers.
vm.runInContext(html.slice(html.indexOf('let lifePoint='),html.indexOf('function livingTraitLabel(')),ctx);
vm.runInContext('lifePoint=1;',ctx);vm.runInContext(code,ctx);
const s={start_members:[{id:'9007199254740993',biomass:1}],end_members:[]};
hooks.render('Watching',true,s);assert(el('patch-watch-colonies').hidden);assert(!el('patch-watch-colonies').open);
hooks.render('Complete',false,s);assert(!el('patch-watch-colonies').hidden);assert.match(el('patch-watch-colony-readout').textContent,/9007199254740993/);
el('patch-watch-colonies').open=true;hooks.render('Unavailable',false);assert(el('patch-watch-colonies').hidden);assert(!el('patch-watch-colonies').open);assert.equal(el('patch-watch-colony-readout').textContent,'');
hooks.render('Complete',false,s);el('patch-watch-colonies').open=true;el('watch-patch').onclick();assert(el('patch-watch-colonies').hidden);assert(!el('patch-watch-colonies').open);assert.equal(el('patch-watch-colony-readout').textContent,'');
hooks.render('Complete',false,s);el('cancel-patch-watch').onclick();assert(el('patch-watch-hud').hidden);
assert.match(html,/max-height:65vh;overflow:auto/);
console.log('PASS retained optional endpoint UI, active fold closure, exceptions, failed restart, dismissal and bounded scrolling');

assert.match(html,/body #patch-watch-colonies:not\(\[open\]\)\{display:block\}/);assert.match(html,/body #patch-watch-colonies\[hidden\]\{display:none\}/);

// Actual registered lifecycle callback clears the real inline-water nodes.
el('watch-water-change').hidden=false;el('watch-water-note').hidden=false;el('life-sheet').handlers.close();assert(el('watch-water-change').hidden);assert(el('watch-water-note').hidden);

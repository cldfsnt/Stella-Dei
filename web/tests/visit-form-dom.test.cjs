const test=require('node:test'),a=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm'),path=require('node:path');
const names=['Microbial mat','Cushion','Rosette','Ribbon','Branching','Canopy'];
function check(html){
 for(const id of ['world-ecology-panel','world-ecology-readout','world-form-actions','refresh-world-ecology'])a.match(html,new RegExp('id=(?:"'+id+'"|'+id+'(?=[ >]))'));
 const elements=new Map();function element(id){return {id,children:[],style:{},open:true,hidden:false,disabled:false,set textContent(v){this.text=v;this.children=[];},get textContent(){return this.text||'';},appendChild(v){this.children.push(v);},addEventListener(type,f){this['onEvent_'+type]=f;},close(){this.open=false;},focus(){}};}
 for(const id of ['more-menu','world-ecology-panel','group-observe','world-ecology-readout','world-form-actions','refresh-world-ecology'])elements.set(id,element(id));
 const doc={hidden:false,addEventListener(){},getElementById:id=>elements.get(id),createElement:()=>element('')};let code=1,calls=[],feedback=[],queue=[];
 const sample={status:'ready',mode:'origin',world:42,colonies:267,forms:names.map((form,form_id)=>({form,form_id,colony_count:[231,13,15,4,0,4][form_id],biomass_sum:[2,.2,.3,.02,0,.1][form_id]})),census_start_time:0,census_end_time:10,recent:null};
 const Module={started:true,failed:false,_stella_visit_growth_form(){},ccall(name,result,types,args){calls.push({name,result,types,args});return name==='stella_world_ecology'?JSON.stringify(sample):code;}};
 const ctx={document:doc,Module,WorldEcology:require('../world-ecology.js'),requestAnimationFrame:f=>queue.push(f),feedback:(...v)=>feedback.push(v),touchControls:{reset(){}},moreMenu:elements.get('more-menu'),canvas:{focus(){}}};vm.createContext(ctx);
 const start=html.indexOf('const worldEcology=WorldEcology.create('),end=html.indexOf('function refreshArrivalEffects()',start);a.ok(start>0&&end>start);vm.runInContext(html.slice(start,end),ctx);
 const refresh=()=>elements.get('refresh-world-ecology').onclick(),box=elements.get('world-form-actions');refresh();a.equal(box.children.length,6);a.equal(box.children[4].disabled,true);a.match(box.children[2].textContent,/Visit Rosette · 15 sampled/);
 box.children[2].onclick();a.equal(calls.at(-1).name,'stella_visit_growth_form');a.equal(JSON.stringify(calls.at(-1).types),'["number","number"]');a.equal(JSON.stringify(calls.at(-1).args),'[42,2]');a.equal(box.children.length,0);a.equal(elements.get('more-menu').open,false);a.match(feedback.at(-1)[0],/existing Rosette/);
 elements.get('more-menu').open=true;code=-2;refresh();box.children[5].onclick();a.match(feedback.at(-1)[0],/World changed or an action is busy/);a.equal(elements.get('more-menu').open,true);a.equal(box.children.length,0);
 refresh();const old=box.children[1];elements.get('world-ecology-panel').open=false;elements.get('world-ecology-panel').onEvent_toggle();const before=calls.length;old.onclick();a.equal(calls.length,before);a.equal(box.children.length,0);
 return {six_rows:true,zero_disabled:true,contract:[42,2],stale_refusal:true,closed_cancel:true};
}
test('actual shell form buttons bind current sample and cancel safely',()=>check(fs.readFileSync(path.join(__dirname,'../shell.html'),'utf8')));
if(require.main===module&&process.argv[2])console.log(JSON.stringify({artifact:process.argv[2],...check(fs.readFileSync(process.argv[2],'utf8'))}));
module.exports=check;

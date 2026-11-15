#!/usr/bin/env python3
"""Isolated arithmetic-only engine gate; known f32 tiny-N funding limitation remains."""
from pathlib import Path
import subprocess,sys,hashlib,json
r=Path(__file__).resolve().parents[2];o=Path(sys.argv[1]);subprocess.run([sys.executable,str(r/'web/tests/egl-natural60-prepare.py'),str(o)],check=True)
base=(r/'src/simulation/microbes.zig').read_text();candidate=(r/'src/experimental/realized_receipt_core.zig').read_text()
assert hashlib.sha256(candidate.encode()).hexdigest()=='9efae4e34a4588413fe59bd2395a19fdcc795a994980bea89e451f5b917898e3'
# Retain production module types and all non-step behavior. Transplant only frozen arithmetic function/helper bodies.
a=base.index('pub fn step(cell:');b=base.index('\n',a);ca=candidate.index('pub fn stepPaced(');cb=candidate.index('\n',ca)
# Find function boundary by balanced braces.
def end(s,start):
 p=s.index('{',start);depth=1;q=p+1
 while depth:
  depth+=(s[q]=='{')-(s[q]=='}');q+=1
 return q
body=candidate[candidate.index('{',ca)+1:end(candidate,ca)-1].replace('*pace[i]','')
old=base[a:end(base,a)].replace('pub fn step(', 'fn baselineStep(',1)
new='pub var qa_candidate:bool=false;\npub var qa_shadow_n_base:f64=0;pub var qa_shadow_n_new:f64=0;pub var qa_shadow_count:u64=0;\n'+old+'\nfn receiptStep(cell:*Cell,env:Environment,elapsed:f32) Flux {'+body+'}\n'
new+='''pub const Audit=struct{n_abs:f64=0,n_signed:f64=0,n_max:f64=0,c_abs:f64=0,c_signed:f64=0,c_max:f64=0,fixed_over:f64=0,recycled_over:f64=0};
pub var qa_audit:[2]Audit=.{.{},.{}};
fn preciseN(c:Cell)f64{var n:f64=c.nutrient;for(c.cohorts)|x|n+=@as(f64,x.biomass)*nutrient_per_carbon;return n;}
fn preciseC(c:Cell)f64{var v:f64=c.detritus;for(c.cohorts)|x|v+=x.biomass;return v;}
fn audit(i:usize,before:Cell,after:Cell,f:Flux,e:Environment)void{
 const n=preciseN(after)-preciseN(before);const c=preciseC(after)-preciseC(before)-@as(f64,f.fixed)+f.recycled;
 var q=&qa_audit[i];q.n_abs+=@abs(n);q.n_signed+=n;q.n_max=@max(q.n_max,@abs(n));q.c_abs+=@abs(c);q.c_signed+=c;q.c_max=@max(q.c_max,@abs(c));
 q.fixed_over=@max(q.fixed_over,@as(f64,f.fixed)-e.carbon_available);q.recycled_over=@max(q.recycled_over,@as(f64,f.recycled)-e.oxygen_carbon_capacity);
}
pub fn step(cell:*Cell,env:Environment,elapsed:f32) Flux {
 if(biomass(cell.*)>0){var x=cell.*;var y=cell.*;const before=preciseN(x);const xf=baselineStep(&x,env,elapsed);const yf=receiptStep(&y,env,elapsed);audit(0,cell.*,x,xf,env);audit(1,cell.*,y,yf,env);qa_shadow_n_base+=@abs(preciseN(x)-before);qa_shadow_n_new+=@abs(preciseN(y)-before);qa_shadow_count+=1;}
 return if(qa_candidate) receiptStep(cell,env,elapsed) else baselineStep(cell,env,elapsed);
}
'''
new+=candidate[candidate.index('\nfn boundedAdd('):]
(o/'simulation/microbes.zig').write_text(base[:a]+new+base[end(base,a):])
p=o/'main.zig';s=p.read_text();a=s.index('          const start_time=state.gameTime;');b=s.index('\n        try originSaveCheck',a)
s=s[:a]+r'''
          const frozen=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});
          const initial=try std.json.parseFromSlice(saves.schema.Save,a,frozen,.{.allocate=.alloc_always});
          const qa_dt:f32=if(std.posix.getenv("QA_RECEIPT_HALF")!=null)720 else 1440;
          const ticks:usize=if(qa_dt==720)1200 else 600;
          for(0..2)|arm|{
            try saves.apply(state,initial.value);micro.qa_candidate=arm==1;
            micro.qa_shadow_n_base=0;micro.qa_shadow_n_new=0;micro.qa_shadow_count=0;micro.qa_audit=.{.{},.{}};
            std.debug.assert(std.mem.eql(u8,frozen,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
            var initial_n:f64=0;var initial_c:f64=0;
            for(0..ticks+1)|tick|{
              if(tick>0){state.planet.simulate(game.loop,.{.dt=qa_dt,.timeScale=1,.solarConstant=state.solarConstant,.gameTime=state.gameTime,.planetRotationTime=state.planetRotationTime,.solarVector=state.simulationSolarVector()});state.gameTime+=qa_dt;}
              var n:f64=0;var c:f64=0;var count:usize=0;
              for(state.planet.microbeCells)|pc|{
                std.debug.assert(micro.validCell(pc,state.planet.microbeStats.next_lineage));n+=pc.nutrient;c+=pc.detritus;
                for(pc.cohorts)|co|{n+=@as(f64,co.biomass)*micro.nutrient_per_carbon;c+=co.biomass;if(co.biomass>0)count+=1;}
              }
              const area=state.planet.getMeanPointArea();const points:f64=@floatFromInt(state.planet.vertices.len);
              c+=state.planet.averageCarbonDioxideMass*points*1e9*(12.0/44.0)/area;
              std.debug.assert(std.math.isFinite(state.planet.averageOxygenMass) and state.planet.averageOxygenMass>=0);
              std.debug.assert(std.math.isFinite(state.planet.averageCarbonDioxideMass) and state.planet.averageCarbonDioxideMass>=0);
              if(tick==0){initial_n=n;initial_c=c;}
              if(tick%60==0)std.debug.print("RECEIPT_ENGINE {s}\n",.{try std.json.stringifyAlloc(a,.{.arm=arm,.dt=qa_dt,.tick=tick,.colonies=count,.n_residual=n-initial_n,.c_residual=c-initial_c,.shadow_old_abs_n=micro.qa_shadow_n_base,.shadow_new_abs_n=micro.qa_shadow_n_new,.shadow_count=micro.qa_shadow_count,.audit=micro.qa_audit,.births=state.planet.microbeStats.births},.{})});
            }
            // Exact serialization and equivalent restored-state continuation, not cross-model parity.
            const endpoint=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});
            const saved=try std.json.parseFromSlice(saves.schema.Save,a,endpoint,.{.allocate=.alloc_always});
            var continuation:?[]const u8=null;
            for(0..2)|repeat|{
              try saves.apply(state,saved.value);
              std.debug.assert(std.mem.eql(u8,endpoint,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
              for(0..10)|_|{state.planet.simulate(game.loop,.{.dt=qa_dt,.timeScale=1,.solarConstant=state.solarConstant,.gameTime=state.gameTime,.planetRotationTime=state.planetRotationTime,.solarVector=state.simulationSolarVector()});state.gameTime+=qa_dt;}
              const result=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});
              if(repeat==0)continuation=result else std.debug.assert(std.mem.eql(u8,continuation.?,result));
            }
            std.debug.print("RECEIPT_SAVE_PASS arm={d} exact_capture_load=true restored_resume_repeat=true\n",.{arm});
          }
          try saves.apply(state,initial.value);
          std.debug.assert(std.mem.eql(u8,frozen,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
          std.debug.print("RECEIPT_ENGINE_PASS original_restored=true tiny_N_limit_not_fixed=true\n",.{});
        }
'''+s[b:];p.write_text(s)
(o.parent/'receipt-provenance.json').write_text(json.dumps({'candidate_sha':hashlib.sha256(candidate.encode()).hexdigest(),'production_sha':hashlib.sha256(base.encode()).hexdigest(),'generated_sha':hashlib.sha256((o/'simulation/microbes.zig').read_bytes()).hexdigest()},indent=2)+'\n')

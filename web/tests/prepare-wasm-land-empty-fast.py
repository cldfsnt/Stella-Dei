from pathlib import Path
import shutil,json,hashlib
r=Path(__file__).resolve().parents[2];o=r.parent/'site-tmp/wasm-land-empty-fast';o.mkdir(exist_ok=True)
frozen=r.parent/'site-tmp/wasm-land-screen/candidate/src'
helper='''
    // Empty-cohort fast path only: no abiotic phase is omitted. Conservative
    // geometry/light preconditions avoid changing the old invalid-env refusal.
    pub fn landEmptyEnvironment(self:*Planet,i:usize,options:SimulationOptions) ?Microbes.Environment {
        const cell=self.microbeCells[i];
        for(cell.cohorts)|co|{
            if(co.biomass!=0 or co.support_mass!=0 or co.root_fraction<0 or co.root_fraction>1)return null;
            inline for(std.meta.fields(Microbes.Cohort))|field|{if(comptime @typeInfo(field.type)==.Float){if(!std.math.isFinite(@field(co,field.name)))return null;}}
        }
        if(!std.math.isFinite(cell.nutrient) or cell.nutrient<0 or !std.math.isFinite(cell.detritus) or cell.detritus<0)return null;
        const temperature=self.temperature[i];const depth=self.waterMass[i]*self.getKmPerWaterMass();
        if(!std.math.isFinite(temperature) or !std.math.isFinite(depth) or depth<0)return null;
        // With scale<=1 and each solar component<=1, normalized dot magnitude
        // is bounded below2, including ordinary f32 rounding. Extreme/invalid
        // geometry, brighter inputs and live cells retain the original path.
        if(!std.math.isFinite(options.solarConstant) or options.solarConstant<0 or options.solarConstant>1361)return null;
        var max_component:f32=0;
        const point:[3]f32=self.transformedPoints[i].data;const solar:[3]f32=options.solarVector.data;
        for(point,solar)|v,s|{
            if(!std.math.isFinite(v) or @abs(v)>1e10 or !std.math.isFinite(s) or @abs(s)>1)return null;
            max_component=@max(max_component,@abs(v));
        }
        if(max_component<1e-10)return null;
        return .{.temperature=temperature,.depth_km=depth,.light=0,.carbon_available=0,.oxygen_carbon_capacity=0};
    }
'''
# Type name from frozen source verified, not a production modification.
ptext=(frozen/'simulation/planet.zig').read_text()
import re
print(re.findall(r'pub const \w+ = struct',ptext)[-12:])
for arm in ['baseline','candidate']:
 d=o/arm/'src';shutil.copytree(frozen,d,dirs_exist_ok=True)
 if arm=='candidate':
  p=d/'simulation/planet.zig';s=p.read_text();needle='            const env=self.microbeEnvironment(i,@max(0,self.transformedPoints[i].norm().dot(options.solarVector))*std.math.clamp(options.solarConstant/1361,0,2));';assert s.count(needle)==1
  s=s.replace(needle,'            const env=self.landEmptyEnvironment(i,options) orelse self.microbeEnvironment(i,@max(0,self.transformedPoints[i].norm().dot(options.solarVector))*std.math.clamp(options.solarConstant/1361,0,2));')
  pos=s.index('    fn microbeEnvironment(');s=s[:pos]+helper+s[pos:];p.write_text(s)
 h=d/'qa_wasm_land.zig';hs=h.read_text()
 if arm=='candidate':
  proof=r'''
 const guard_options=P.SimulationOptions{.dt=1440,.timeScale=1,.gameTime=saved.game_time,.solarConstant=saved.solar_constant,.planetRotationTime=saved.rotation_time,.solarVector=za.Vec3.new(1,0,0)};
 if(p.landBeta.enabled){var wet:usize=0;var dry:usize=0;var living:usize=0;var tested=false;
 for(p.microbeCells,0..)|cell,i|{if(p.landEmptyEnvironment(i,guard_options)!=null){if(p.waterMass[i]>0)wet+=1 else dry+=1;
 if(!tested){const old=p.microbeCells[i];p.microbeCells[i].cohorts[0].biomass=std.math.nan(f32);std.debug.assert(p.landEmptyEnvironment(i,guard_options)==null);p.microbeCells[i]=old;p.microbeCells[i].cohorts[0].biomass=1;p.microbeCells[i].cohorts[0].root_fraction=0.25;std.debug.assert(p.landEmptyEnvironment(i,guard_options)==null);p.microbeCells[i]=old;tested=true;}}
 else {for(cell.cohorts)|co|{if(co.biomass>0){living+=1;break;}}}}
 std.debug.print("FAST_GUARD wet={} dry={} living={} invalid_live_refused={}\n",.{wet,dry,living,tested});}
'''
  hs=hs.replace(' var loop=Loop.init();',proof+'\n var loop=Loop.init();')
 hs=hs.replace(' var first_ms:f64=0;', ' var receipt_hash=std.hash.Wyhash.init(0);\n var first_ms:f64=0;');hs=hs.replace('saved.game_time+=1440;', 'saved.game_time+=1440;if(qa_enabled and p.landBeta.enabled){receipt_hash.update(std.mem.sliceAsBytes(p.landRootH));receipt_hash.update(std.mem.sliceAsBytes(p.landSoil));receipt_hash.update(std.mem.sliceAsBytes(p.landVapor));}');hs=hs.replace(' const elapsed=emscripten_get_now()-begin;', ' const elapsed=emscripten_get_now()-begin;std.debug.print("DELIVERED_HASH {d}\\n",.{receipt_hash.final()});');h.write_text(hs)
 (o/arm/'source-hashes.json').write_text(json.dumps({str(p.relative_to(d)):hashlib.sha256(p.read_bytes()).hexdigest()for p in d.rglob('*.zig')},indent=2))
shutil.copyfile(r.parent/'site-tmp/wasm-land-screen/graph.json',o/'graph.json')

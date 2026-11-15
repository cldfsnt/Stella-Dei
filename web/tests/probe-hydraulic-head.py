"""Local NumPy f32 arithmetic proxy, same represented states; no engine patch."""
from pathlib import Path
import json,numpy as np,hashlib
r=Path(__file__).resolve().parents[2];b=r.parent/'site-tmp';o=r/'web/tests/continuation-review/paid-hydration/soil-root-design/terrestrial-opportunity'
edges=[]
for line in (b/'propagule-graph/graph.jsonl').open():
 x=json.loads(line)
 if x['kind']=='cell':edges.extend((x['cell'],n)for n in sorted(set(x['neighbors'])-{x['cell']}))
e=np.array(edges);i=e[:,0];j=e[:,1];f=np.float32;conv=f(1.0/1000.0/7669529600.0/1000.0*1e9);fraction=f(.0048)
result=[]
for label,path in [('day30',b/'natural60-day30.json'),('day60',b/'natural60-day60.json'),('day90',b/'grazing-coupled/arm-0-day90.json')]:
 s=json.loads(path.read_text());mass=np.array(s['water'],dtype=np.float32);terrain=np.array(s['elevation'],dtype=np.float32);depth=mass*conv;head=terrain+depth;old_delta=head[i]-head[j];alt_delta=(terrain[i].astype('float64')-terrain[j].astype('float64'))+(depth[i].astype('float64')-depth[j].astype('float64'));shared=mass[i]*fraction
 old_flow=np.minimum(shared,np.maximum(f(0),(old_delta/conv)*fraction));alt_flow=np.minimum(shared.astype('float64'),np.maximum(0,alt_delta/float(conv)*float(fraction))).astype('float32');shallow=depth[i]*f(1000)<f(.2)
 def report(mask):
  z=int(mask.sum());return {'edges':z,'routing_disagreements':int(np.sum(mask&((old_delta>0)!=(alt_delta>0)))),'f32_ties_with_nonzero_relative_head':int(np.sum(mask&(old_delta==0)&(alt_delta!=0))),'different_proposed_transfer':int(np.sum(mask&(old_flow!=alt_flow))),'max_head_error_m':float(np.max(np.abs(old_delta[mask].astype('float64')-alt_delta[mask]))*1000)if z else 0,'sum_abs_transfer_difference_native':float(np.abs(old_flow[mask].astype('float64')-alt_flow[mask].astype('float64')).sum())}
 np.savez_compressed(o/f'head-edges-{label}.npz',source=i,target=j,current_delta_km=old_delta,relative_delta_km=alt_delta,current_transfer_native=old_flow,relative_transfer_native=alt_flow,shallow_source=shallow)
 row={'label':label,'source_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'unperturbed_all':report(np.ones(len(i),dtype=bool)),'unperturbed_shallow_source':report(shallow),'perturbations':[]}
 for delta in [.01,.02,.05]:
  newmass=(mass.astype('float64')+delta/1000/float(conv)).astype('float32');newdepth=newmass*conv;newhead=terrain+newdepth;represented=newdepth!=depth;headlost=represented&(newhead==head)
  newold_delta=newhead[i]-head[j];newalt_delta=(terrain[i].astype('float64')-terrain[j].astype('float64'))+(newdepth[i].astype('float64')-depth[j].astype('float64'));newshared=newmass[i]*fraction
  newoldflow=np.minimum(newshared,np.maximum(f(0),(newold_delta/conv)*fraction));newaltflow=np.minimum(newshared.astype('float64'),np.maximum(0,newalt_delta/float(conv)*float(fraction))).astype('float32')
  row['perturbations'].append({'added_m_requested':delta,'cells':len(mass),'mass_unchanged':int((newmass==mass).sum()),'depth_unchanged':int((~represented).sum()),'represented_depth_changes':int(represented.sum()),'represented_changes_lost_in_head':int(headlost.sum()),'shallow_cells':int((depth*1000<.2).sum()),'shallow_changes_lost_in_head':int((headlost&(depth*1000<.2)).sum()),'actual_edges_current_transfer_changes':int((newoldflow!=old_flow).sum()),'actual_edges_relative_transfer_changes':int((newaltflow!=alt_flow).sum()),'head_sensitivity_recovered_but_cap_still_equal':int((headlost[i]&(newalt_delta!=alt_delta)&(newaltflow==alt_flow)).sum())})
 # Fixed explanatory level-ground pair: same actual source terrain/depth on both sides.
 k=12352;m=mass[k];d=depth[k];h=head[k];witness=[]
 for delta in [.01,.02,.05]:
  nm=f(float(m)+delta/1000/float(conv));nd=f(nm*conv);nh=f(terrain[k]+nd);dd=float(nd)-float(d);od=float(f(nh-h));witness.append({'added_m_requested':delta,'represented_depth_increase_m':dd*1000,'current_head_increase_m':od*1000,'current_transfer_native':float(min(f(nm*fraction),f(max(0,od)/float(conv)*float(fraction)))),'relative_transfer_native':min(float(f(nm*fraction)),max(0,dd)/float(conv)*float(fraction))})
 row['synthetic_equal_level_pair_at_12352_scale']=witness;result.append(row)
(o/'head-probe.json').write_text(json.dumps({'scope':'local arithmetic; no actual scheduler or aggregate-flow claim','km_per_mass_f32':float(conv),'fraction_f32':float(fraction),'worlds':result},indent=2)+'\n')
for x in result:print(x['label'],x['unperturbed_all'],x['unperturbed_shallow_source']);print(x['perturbations']);print(x['synthetic_equal_level_pair_at_12352_scale'])

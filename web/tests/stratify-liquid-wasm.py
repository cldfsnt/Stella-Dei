#!/usr/bin/env python3
"""Existing-trace contextualization only; no engine rerun or acceptance retuning.
Bands use each cell's actual PRE-transport water depth, not future depth.
"""
import argparse,importlib.util,json,math,hashlib
from pathlib import Path
p=Path(__file__).with_name('liquid-wasm-oracle.py');spec=importlib.util.spec_from_file_location('oracle',p);O=importlib.util.module_from_spec(spec);spec.loader.exec_module(O)
NAMES=['[0,0.02)m','[0.02,0.2)m','[0.2,2)m','[2,100)m','[100,infinity)m']
def which(mass,area):
 a,b=area.as_integer_ratio()
 for i,(num,den) in enumerate([(1,50),(1,5),(2,1),(100,1)]):
  if mass*10**6*b*den<a*O.Q*num:return i
 return 4

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--trace',required=True);ap.add_argument('--graph',required=True);ap.add_argument('--audit',required=True);ap.add_argument('--output',required=True);a=ap.parse_args()
 graph=json.loads(Path(a.graph).read_text())['neighbors'];old=json.loads(Path(a.audit).read_text())
 bins=[dict(count=0,errors=[],signed=0,incoming=0,outgoing=0,pre=0,swallowed=0,max_relative=0.,zero_pre=0,max_cell=None)for _ in NAMES];ticks=0;area0=None
 for r in O.frames(a.trace):
  if r['magic']!=b'LQTRACE1':raise ValueError('requires candidate')
  n=r['n'];area=r['area'];area0=area if area0 is None else area0;assert area==area0;ticks+=1
  pre=list(map(O.f32units,r['pre']));post=list(map(O.f32units,r['post']));incoming=[0]*n;outgoing=[0]*n
  for i,ns in enumerate(graph):
   for k,j in enumerate(ns):v=O.f32units(r['edges'][6*i+k]);outgoing[i]+=v;incoming[j]+=v
  for i in range(n):
   err=post[i]-(pre[i]-outgoing[i]+incoming[i]);absolute=abs(err);b=bins[which(pre[i],area)]
   b['count']+=1;b['errors'].append(absolute);b['signed']+=err;b['incoming']+=incoming[i];b['outgoing']+=outgoing[i];b['pre']+=pre[i]
   if incoming[i]>outgoing[i] and post[i]==pre[i]:b['swallowed']+=1
   if pre[i]:b['max_relative']=max(b['max_relative'],absolute/pre[i])
   else:b['zero_pre']+=1
   if b['max_cell'] is None or absolute>b['max_cell']['error_units']:b['max_cell']={'cell':i,'tick':r['tick'],'error_units':absolute,'pre_depth_m':pre[i]*10**6/O.Q/area,'intended_net_native':(incoming[i]-outgoing[i])/O.Q}
 assert ticks==old['frames'];assert sum(sum(b['errors'])for b in bins)==int(old['sumabs_cell_error_A']['quantum_units']);assert sum(b['outgoing']for b in bins)==int(old['one_way_gross_transfer_T']['quantum_units'])
 result={'note':'Context only; frozen world A/T acceptance remains FAIL. Bands classify each actual pre-transport cell-step. Incoming/outgoing band ratios use different edge attribution and are not new acceptance gates. Incident flow double-counts world directed traffic. Percentiles nearest-rank over ALL cell-steps including zero error.','frames':ticks,'area_m2':area0,'bands':[]}
 for name,b in zip(NAMES,bins):
  e=sorted(b.pop('errors'));A=sum(e);count=len(e)
  percentile=lambda p:(e[max(0,math.ceil(p*count)-1)]*10**6/O.Q/area0 if count else None)
  row={'band':name,'cell_steps':count,'A_native':A/O.Q,'A_kg':A*10**9/O.Q,'signed_native':b['signed']/O.Q,'incoming_once_native':b['incoming']/O.Q,'outgoing_once_native':b['outgoing']/O.Q,'A_over_incoming_once':A/b['incoming'] if b['incoming'] else None,'A_over_outgoing_once':A/b['outgoing'] if b['outgoing'] else None,'A_over_incident':A/(b['incoming']+b['outgoing']) if b['incoming']+b['outgoing'] else None,'depth_error_m':{str(p):percentile(p)for p in [.5,.9,.99,.999,1.]},'max_relative_nonzero_initial_pool':b['max_relative'],'zero_initial_pool_steps':b['zero_pre'],'positive_net_receipts_swallowed':b['swallowed'],'max_error_witness':b['max_cell']}
  if row['max_error_witness']:row['max_error_witness']['error_units']=str(row['max_error_witness']['error_units'])
  result['bands'].append(row)
 result['sha256']={k:hashlib.sha256(Path(v).read_bytes()).hexdigest()for k,v in [('trace',a.trace),('graph',a.graph),('audit',a.audit)]};Path(a.output).write_text(json.dumps(result,indent=2)+'\n')
 print(a.trace,[(r['band'],r['cell_steps'],r['depth_error_m']['1.0'],r['positive_net_receipts_swallowed'])for r in result['bands']])
if __name__=='__main__':main()

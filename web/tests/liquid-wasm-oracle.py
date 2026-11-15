#!/usr/bin/env python3
"""Exact offline binary ledger for LQTRACE1/LQBASE01. No simulation or tolerance fitting.
Example: python liquid-wasm-oracle.py --graph graph.json --candidate candidate.bin --baseline baseline.bin --output audit.json
All integer ledgers use native mass quantum2^-149. Structural and operation-envelope
failures are fatal; practical D/A gates are reported as failures, never normalized away.
"""
import argparse, hashlib, json, math, struct
from pathlib import Path

Q=1<<149
D=(1<<53)-12                 # gamma12 =12/D
BD=2*D                      # common denominator for bound in quantum units

def units(x):
    if not math.isfinite(x) or x<0: raise ValueError('nonfinite/negative water')
    a,b=x.as_integer_ratio(); shift=149-(b.bit_length()-1)
    if shift<0: raise ValueError('accumulator below f32 dyadic lattice')
    return a<<shift

def f32units(bits):
    exp=(bits>>23)&255; mant=bits&0x7fffff
    if exp==255 or (bits>>31 and (exp or mant)):raise ValueError('nonfinite/negative f32 water')
    return mant if exp==0 else ((1<<23)|mant)<<(exp-1)

def spacing(bits):
    exp=(bits>>23)&255
    return 1 if exp==0 else 1<<(exp-1) # max finite adjacent spacing; maxfloat uses lower

def amount(n):
    return {'native':n/Q,'kg':n*10**9/Q,'quantum_units':str(n)}

def read_exact(f,n):
    b=f.read(n)
    if len(b)!=n:raise ValueError('truncated trace')
    return b

def frames(path):
    with open(path,'rb') as f:
        previous=None;area0=None;shape0=None;magic0=None
        while True:
            magic=f.read(8)
            if not magic:return
            if magic not in (b'LQTRACE1',b'LQBASE01'):raise ValueError('bad magic')
            n,tick,area=struct.unpack('<IId',read_exact(f,16))
            if n==0 or not math.isfinite(area) or area<=0:raise ValueError('invalid shape/area')
            if shape0 is not None and (shape0!=n or magic0!=magic):raise ValueError('trace shape/type changed')
            shape0=n;magic0=magic
            if previous is not None and tick!=previous+1:raise ValueError('nonconsecutive ticks')
            if area0 is not None and area!=area0:raise ValueError('area changed')
            previous=tick;area0=area
            pre=list(struct.unpack('<'+'I'*n,read_exact(f,4*n)))
            post=list(struct.unpack('<'+'I'*n,read_exact(f,4*n)))
            row={'n':n,'tick':tick,'area':area,'pre':pre,'post':post,'magic':magic}
            if magic==b'LQTRACE1':
                row['edges']=list(struct.unpack('<'+'I'*(6*n),read_exact(f,24*n)))
                row['acc']=list(struct.unpack('<'+'d'*n,read_exact(f,8*n)))
            yield row

def audit_frame(r,graph):
    n=r['n'];pre=list(map(f32units,r['pre']));post=list(map(f32units,r['post']))
    net=sum(post)-sum(pre)
    if r['magic']==b'LQBASE01':return {'tick':r['tick'],'n':n,'area_m2':r['area'],'inventory':sum(pre),'signed':net,'baseline':True}
    if len(graph)!=n:raise ValueError('graph length mismatch')
    incoming=[0]*n;outgoing=[0]*n
    for i,ns in enumerate(graph):
        if len(ns)!=6:raise ValueError('six graph slots required')
        seen=set()
        for k,j in enumerate(ns):
            if not isinstance(j,int) or not 0<=j<n or i not in graph[j]:raise ValueError('invalid reciprocal topology')
            v=f32units(r['edges'][i*6+k])
            if (j==i or j in seen) and v:raise ValueError('nonzero self/duplicate edge')
            seen.add(j);outgoing[i]+=v;incoming[j]+=v
        if outgoing[i]>pre[i]:raise ValueError('donor overspend')
    absolute=bound=acc_abs=cast_abs=warnings=0;warning_flow=0;max_error=0;max_depth=0.0;swallowed=0;bit_zero_changes=0
    for i in range(n):
        ideal=pre[i]-outgoing[i]+incoming[i]
        if ideal<0:raise ValueError('negative ideal balance')
        actual_acc=units(r['acc'][i]);size=pre[i]+outgoing[i]+incoming[i]
        ae=abs(actual_acc-ideal)
        if ae*D>12*size:raise ValueError(f'f64 accumulation exceeds gamma12 at cell{i}')
        gap=spacing(r['post'][i]);ce=abs(post[i]-actual_acc)
        if 2*ce>gap:raise ValueError(f'cast exceeds half f32 spacing at cell{i}')
        err=post[i]-ideal;bnum=24*size+gap*D
        if abs(err)*BD>bnum:raise ValueError(f'combined envelope exceeded at cell{i}')
        absolute+=abs(err);bound+=bnum;acc_abs+=ae;cast_abs+=ce
        incident=incoming[i]+outgoing[i]
        if incident and 128*bnum>BD*incident:warnings+=1;warning_flow+=incident
        if incoming[i]>outgoing[i] and post[i]==pre[i]:swallowed+=1
        if not incident and post[i]!=pre[i]:raise ValueError('zero-traffic cell changed value')
        if not incident and r['post'][i]!=r['pre'][i]:bit_zero_changes+=1
        max_error=max(max_error,abs(err));max_depth=max(max_depth,abs(err)*10**9/Q/(1000*r['area']))
    traffic=sum(outgoing)
    if sum(incoming)!=traffic:raise ValueError('edge double count')
    if sum(pre[i]-outgoing[i]+incoming[i] for i in range(n))!=sum(pre):raise ValueError('ideal global imbalance')
    return {'tick':r['tick'],'n':n,'area_m2':r['area'],'inventory':sum(pre),'signed':net,'absolute':absolute,'bound_numerator':bound,'traffic':traffic,'accumulation_absolute':acc_abs,'cast_absolute':cast_abs,'resolution_warning_cells':warnings,'warning_incident_units':warning_flow,'unresolved_positive_net_receipts':swallowed,'signed_zero_bit_changes':bit_zero_changes,'maximum_error_units':max_error,'maximum_depth_error_m':max_depth}

def report(rows):
    if not rows:raise ValueError('empty trace')
    sums={k:sum(r.get(k,0) for r in rows) for k in ['inventory','signed','absolute','bound_numerator','traffic','accumulation_absolute','cast_absolute']}
    sums['D']=sum(abs(r['signed']) for r in rows)
    result={'frames':len(rows),'signed':amount(sums['signed']),'sumabs_global_step_drift_D':amount(sums['D']),'sum_inventory_native':sums['inventory']/Q}
    if not rows[0].get('baseline'):
        result.update(sumabs_cell_error_A=amount(sums['absolute']),one_way_gross_transfer_T=amount(sums['traffic']),sum_derived_bound_native=sums['bound_numerator']/BD/Q,A_over_T=sums['absolute']/sums['traffic'] if sums['traffic'] else None,A_over_summed_inventory=sums['absolute']/sums['inventory'] if sums['inventory'] else None,A_over_initial_inventory=sums['absolute']/rows[0]['inventory'] if rows[0]['inventory'] else None,AT_gate_pass=(1000*sums['absolute']<=sums['traffic']),resolution_warning_cell_steps=sum(r['resolution_warning_cells'] for r in rows),unresolved_positive_net_receipts=sum(r['unresolved_positive_net_receipts'] for r in rows),maximum_depth_error_m=max(r['maximum_depth_error_m'] for r in rows))
    # Exact integer rows support independent recomputation of every aggregate.
    result['per_step']=[{k:(str(v) if type(v) is int and k not in ('tick','resolution_warning_cells','unresolved_positive_net_receipts','signed_zero_bit_changes') else v) for k,v in r.items()} for r in rows]
    return result,sums

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--graph',required=True);ap.add_argument('--candidate',required=True);ap.add_argument('--baseline');ap.add_argument('--output');ap.add_argument('--expected-ticks',type=int,default=60);a=ap.parse_args()
    g=json.loads(Path(a.graph).read_text());g=g['neighbors'] if isinstance(g,dict) else g
    candidate=[audit_frame(r,g) for r in frames(a.candidate)]
    if len(candidate)!=a.expected_ticks:raise ValueError('unexpected candidate horizon')
    out,cs=report(candidate)
    if candidate[0].get('baseline'):raise ValueError('candidate requires edge trace')
    if a.baseline:
        base=[audit_frame(r,g) for r in frames(a.baseline)]
        if [(r['tick'],r['n'],r['area_m2']) for r in base]!=[(r['tick'],r['n'],r['area_m2']) for r in candidate]:raise ValueError('horizon/shape/area mismatch')
        br,bs=report(base);out['baseline']=br;out['D_reduction_gate_pass']=2*cs['D']<=bs['D'];out['D_candidate_over_baseline']=cs['D']/bs['D'] if bs['D'] else None
    out['hashes']={k:hashlib.sha256(Path(p).read_bytes()).hexdigest() for k,p in [('graph',a.graph),('candidate',a.candidate)]+([('baseline',a.baseline)] if a.baseline else [])}
    out['all_local_envelopes_pass']=True;out['practical_gates_pass']=out['AT_gate_pass'] and out.get('D_reduction_gate_pass',True)
    text=json.dumps(out,indent=2)+'\n'
    if a.output:Path(a.output).write_text(text)
    else:print(text,end='')
    return 0 if out['practical_gates_pass'] else 2
if __name__=='__main__':raise SystemExit(main())

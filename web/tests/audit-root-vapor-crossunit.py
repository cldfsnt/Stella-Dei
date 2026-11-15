#!/usr/bin/env python3
"""Offline exact endpoint audit; no numerical/biological acceptance tolerance.
Input JSON list or {records:list}; fields are stored f64 values unless h_bits
provided (recommended); h values otherwise reconstruct as declared f32.
Returns nonzero on unfunded signal, malformed inputs, or nonzero physical residual.
A residual failure identifies an unresolved exact-ledger gate, not its cause.
"""
import json,math,struct,sys
from fractions import Fraction as F

def q(x):
    x=float(x)
    assert math.isfinite(x) and x>=0
    return F.from_float(x)

def audit(r):
    area=q(r['area_m2']);assert area>0
    soil=q(r['soil_before'])-q(r['soil_after'])
    vapor=q(r['vapor_after'])-q(r['vapor_before'])
    assert soil>=0 and vapor>=0
    demands=list(map(q,r['demands']));credits=list(map(q,r['credits']))
    assert len(demands)==len(credits)==4
    assert sum(credits)<=soil
    hs=[struct.unpack('<f',struct.pack('<I',int(x)))[0] for x in r['h_bits']] if 'h_bits' in r else [struct.unpack('<f',struct.pack('<f',float(x)))[0] for x in r['h']]
    assert len(hs)==4
    for d,c,h in zip(demands,credits,hs):
        assert c<=d and 0<=h<=1 and q(h)*d<=c
    residual=vapor*10**9-soil*area
    return residual

def main():
    raw=json.load(open(sys.argv[1]));rows=raw['records'] if isinstance(raw,dict) else raw
    residuals=[audit(r) for r in rows]
    total=sum(residuals,F(0));absolute=sum(map(abs,residuals),F(0))
    print(json.dumps({'events':len(rows),'nonzero_crossunit_residuals':sum(x!=0 for x in residuals),'signed_kg_exact':str(total),'sumabs_kg_exact':str(absolute),'signed_kg_approx':float(total),'sumabs_kg_approx':float(absolute)}))
    return 2 if absolute else 0
if __name__=='__main__':sys.exit(main())

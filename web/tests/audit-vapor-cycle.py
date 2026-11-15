import json,struct,fractions,sys
F=lambda x:fractions.Fraction.from_float(float(x))
rows=[]
for line in open(sys.argv[1]):
 if 'CYCLE {' not in line:continue
 r=json.loads(line[line.index('CYCLE ')+6:])
 # Zig prints f32 shortest-roundtrip decimals; reconstruct their declared types.
 for k in ['l0','l1','legacy_l','legacy_v']:r[k]=struct.unpack('f',struct.pack('f',r[k]))[0]
 assert F(r['soil0'])-F(r['soil1'])==F(r['v1'])-F(r['v0'])
 assert F(r['l0'])-F(r['l1'])==F(r['v2'])-F(r['v1'])
 assert F(r['v2'])-F(r['edge_source'])==F(r['edge_target'])-F(200)
 rows.append(r)
print('Exact Fraction phase/pulse/edge legs:',len(rows)*3)
for r in rows:
 if r['dt']==1440 and r['pulse']:print(json.dumps({k:r[k] for k in ['case','pulse_paid','evap_request','evap_paid','rain_request','rain_paid','edge_request','edge_paid']}))

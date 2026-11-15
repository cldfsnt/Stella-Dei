import json,re,struct,sys
from fractions import Fraction as F
f32=lambda s:F.from_float(struct.unpack('f',struct.pack('f',float(s)))[0])
paid=F(0);rows=[]
old={}
for l in open(sys.argv[2]):
 m=re.search(r'PATCH_RECEIPT fixture=(\d+) tick=(\d+) cell=(\d+) json=(.*)',l)
 if m:old[(int(m[1]),int(m[2]))]=json.loads(m[4])
for l in open(sys.argv[1]):
 m=re.search(r'PATCH_BITE cell=(\d+) before=(\S+) after=(\S+)',l)
 if m:paid+=f32(m[2])-f32(m[3])
 m=re.search(r'PATCH_RECEIPT fixture=(\d+) tick=(\d+) cell=(\d+) json=(.*)',l)
 if not m:continue
 r=json.loads(m[4]);prior=old[(int(m[1]),int(m[2]))]
 for key in ['start_time','end_time','seconds','before','after','grazed','net','bites']:assert r[key]==prior[key],key
 assert F(r['grazed'])==paid
 assert F(r['net'])==F(r['after'])-F(r['before'])
 assert F(r['other'])==F(r['net'])+paid
 rows.append(r);paid=F(0)
assert len(rows)==180 and paid==0
print(json.dumps({'records':len(rows),'prior_endpoints_bites_net_exact':True,'source_debits_exact':True,'other_is_derived_not_independent_physiology':True,'bites':sum(r['bites']for r in rows)},indent=2))

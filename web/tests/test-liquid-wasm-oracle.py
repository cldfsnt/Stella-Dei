import importlib.util,struct,unittest,io,tempfile,pathlib
p=pathlib.Path(__file__).with_name('liquid-wasm-oracle.py');spec=importlib.util.spec_from_file_location('oracle',p);o=importlib.util.module_from_spec(spec);spec.loader.exec_module(o)
def bits(x):return struct.unpack('<I',struct.pack('<f',x))[0]
def f32(x):return struct.unpack('<f',struct.pack('<f',x))[0]
g=[[1,0,0,0,0,0],[0,1,1,1,1,1]]
def fixture(mass=(1.,0.),flow=.1):
 f=f32(flow);a=float(mass[0])-f;b=float(mass[1])+f
 return dict(n=2,tick=1,area=100.,pre=list(map(bits,mass)),post=[bits(a),bits(b)],magic=b'LQTRACE1',edges=[bits(f)]+[0]*11,acc=[a,b])
class Oracle(unittest.TestCase):
 def test_normal_exact_gates(self):
  r=o.audit_frame(fixture(),g);self.assertGreater(r['traffic'],0);self.assertGreater(r['absolute'],0);self.assertLessEqual(r['absolute']*o.BD,r['bound_numerator']);self.assertTrue(o.report([r])[0]['AT_gate_pass'])
 def test_zero_and_signed_zero(self):
  r=fixture((-0.,0.),0);self.assertEqual(o.audit_frame(r,g)['absolute'],0)
 def test_smallest_subnormal(self):
  tiny=struct.unpack('<f',struct.pack('<I',1))[0];r=o.audit_frame(fixture((tiny,0.),tiny),g);self.assertEqual(r['absolute'],0)
 def test_largest_finite(self):
  largest=struct.unpack('<f',struct.pack('<I',0x7f7fffff))[0];r=o.audit_frame(fixture((largest,0.),0),g);self.assertEqual(r['absolute'],0)
 def test_donor(self):
  r=fixture((1.,0.),2.);r['post'][0]=bits(0.)
  with self.assertRaisesRegex(ValueError,'overspend'):o.audit_frame(r,g)
 def test_wrong_accumulator(self):
  r=fixture();r['acc'][1]+=1e-5
  with self.assertRaisesRegex(ValueError,'gamma12'):o.audit_frame(r,g)
 def test_wrong_cast(self):
  r=fixture();r['post'][1]+=2
  with self.assertRaisesRegex(ValueError,'cast'):o.audit_frame(r,g)
 def test_duplicate(self):
  r=fixture();r['edges'][1]=bits(.01)
  with self.assertRaisesRegex(ValueError,'self/duplicate'):o.audit_frame(r,g)
 def test_nan(self):
  r=fixture();r['pre'][0]=0x7fc00000
  with self.assertRaisesRegex(ValueError,'nonfinite'):o.audit_frame(r,g)
 def test_binary_parser_and_truncation(self):
  r=fixture();raw=b'LQTRACE1'+struct.pack('<IId',2,1,100.)+struct.pack('<4I',*(r['pre']+r['post']))+struct.pack('<12I',*r['edges'])+struct.pack('<2d',*r['acc'])
  with tempfile.TemporaryDirectory() as d:
   p=pathlib.Path(d)/'a.bin';p.write_bytes(raw);self.assertEqual(list(o.frames(p))[0],r);p.write_bytes(raw[:-1])
   with self.assertRaisesRegex(ValueError,'truncated'):list(o.frames(p))
 def test_budget_reduction_is_not_net_cancellation(self):
  rows=[dict(tick=1,inventory=100,signed=10,baseline=True),dict(tick=2,inventory=100,signed=-10,baseline=True)];r,s=o.report(rows);self.assertEqual(s['D'],20);self.assertEqual(s['signed'],0)
if __name__=='__main__':unittest.main()

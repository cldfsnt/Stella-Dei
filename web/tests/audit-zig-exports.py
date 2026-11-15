"""Audit actual exported tool bodies in copied QA code before claiming engine parity.

Exact source text, not semantic equivalence. Platform bridge exceptions must be
named explicitly with --allow and justified in the assay report. No normalization.
"""
import argparse,hashlib,json,pathlib,re,sys

def exports(text):
 out={}
 for m in re.finditer(r'(?m)^export fn (\w+)\(',text):
  start=text.find('{',m.end())
  if start<0:raise ValueError('missing body '+m[1])
  depth=0;i=start
  while i<len(text):
   if text.startswith('//',i) or text.startswith('\\\\',i):
    j=text.find('\n',i);i=len(text) if j<0 else j+1;continue
   if text[i] in '\"\'':
    quote=text[i];i+=1
    while i<len(text):
     if text[i]=='\\':i+=2;continue
     if text[i]==quote:i+=1;break
     i+=1
    continue
   if text[i]=='{':depth+=1
   elif text[i]=='}':
    depth-=1
    if depth==0:out[m[1]]=text[m.start():i+1];break
   i+=1
  else:raise ValueError('unterminated body '+m[1])
 return out

def audit(original,copied,allowed=()):
 a,b=exports(original),exports(copied);rows=[]
 for name in sorted(a.keys()|b.keys()):
  equal=a.get(name)==b.get(name);rows.append({'name':name,'exact':equal,'explicit_exception':name in allowed,'production_sha256':hashlib.sha256(a[name].encode()).hexdigest() if name in a else None,'copied_sha256':hashlib.sha256(b[name].encode()).hexdigest() if name in b else None})
 return {'exports':rows,'unexplained_mismatches':[r['name'] for r in rows if not r['exact'] and not r['explicit_exception']]}

def selftest():
 s='export fn alpha() void { const s="} {"; // }\n if(true){foo();} }\nexport fn beta() void {state.makeSelectedPond();}'
 assert len(exports(s))==2
 assert not audit(s,s)['unexplained_mismatches']
 assert audit(s,s.replace('makeSelectedPond','makeSelectedNursery'))['unexplained_mismatches']==['beta']
 assert not audit(s,s.replace('makeSelectedPond','makeSelectedNursery'),['beta'])['unexplained_mismatches']
 print('PASS: exact exports, brace-safe strings/comments, unintended pond substitution, explicit exception')

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('production',nargs='?');ap.add_argument('copied',nargs='?');ap.add_argument('--allow',action='append',default=[]);ap.add_argument('--output');ap.add_argument('--selftest',action='store_true');v=ap.parse_args()
 if v.selftest:selftest();sys.exit(0)
 if not v.production or not v.copied:ap.error('production and copied files required')
 r=audit(pathlib.Path(v.production).read_text(),pathlib.Path(v.copied).read_text(),v.allow)
 text=json.dumps(r,indent=2)+'\n'
 if v.output:pathlib.Path(v.output).write_text(text)
 else:print(text,end='')
 print('exports',len(r['exports']),'unexplained mismatches',r['unexplained_mismatches'],file=sys.stderr)
 sys.exit(bool(r['unexplained_mismatches']))

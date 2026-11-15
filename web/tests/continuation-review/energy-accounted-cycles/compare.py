from pathlib import Path
import gzip,re,json
here=Path(__file__).resolve().parent
old=gzip.decompress((here.parent/'energy-cycles/run.log.gz').read_bytes()).decode()
p=here/'run.log';new=p.read_text() if p.exists() else gzip.decompress(p.with_suffix('.log.gz').read_bytes()).decode()
def rows(text):
 out={}
 for line in text.splitlines():
  if line.startswith('CYCLES rate='):
   d=dict(re.findall(r'(\w+)=([^ ]+)',line));out[tuple(d[x] for x in ['rate','slow','habitat','crowded','swap','day'])]=d
 return out
before,after=rows(old),rows(new);assert before.keys()==after.keys()
result={'matched_daily_rows':len(before),'deltas':{},'slow_advantages':{},'daily_extinction_disagreements':sum((float(before[k][f])==0)!=(float(after[k][f])==0) for k in before for f in ['fast','slow_mass'])}
for f in ['fast','slow_mass','paid_fast','paid_slow','stress_fast','stress_slow','detritus','carbon','oxygen']:
 k=max(before,key=lambda k:abs(float(before[k][f])-float(after[k][f])));result['deltas'][f]={'max_abs_delta':abs(float(before[k][f])-float(after[k][f])),'case':k,'old':before[k][f],'candidate':after[k][f]}
for day in ['20','40','48']:
 result['slow_advantages'][day]={}
 for label,data in [('old',before),('candidate',after)]:
  selected=[v for k,v in data.items() if k[-1]==day and v['slow']!='1' and v['swap']=='0'];result['slow_advantages'][day][label]={'wins':sum(float(x['slow_mass'])>float(x['fast']) for x in selected),'settings':len(selected)}
(here/'trajectory-comparison.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='deltas'},indent=2))

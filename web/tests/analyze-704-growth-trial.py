from pathlib import Path
from fractions import Fraction as F
import json,hashlib
r=Path(__file__).resolve().parents[2];b=r.parent/'site-tmp/704-growth-trial'
def rows(name,tag):return [json.loads(l.split(' ',1)[1])for l in(b/name).read_text().splitlines()if l.startswith(tag+' ')]
out=[]
for arm in range(3):
 m=f'main-{arm}.log';rr=f'resume-{arm}.log';assert 'COMPLETE'in(b/m).read_text()and 'COMPLETE'in(b/rr).read_text()
 assert(b/f'arm-{arm}-60.json').read_bytes()==(b/f'resume-arm-{arm}-60.json').read_bytes()
 assert(b/f'arm-{arm}-2-trace.json').read_bytes()==(b/f'arm-{arm}-2-off.json').read_bytes()
 for tag in ['ROOT_WATER','USED_H','MORTALITY','HABITAT','PAID_GROWTH','PATCH','BIRTH']:assert [x for x in rows(m,tag)if x['tick']>30]==rows(rr,tag),(arm,tag)
 patch=rows(m,'PATCH');assert len(patch)==60
 phase={x['tick']:x for x in rows(m,'ROOT_WATER')if x['lineage']==704};used=rows(m,'USED_H');signed=F(0);absolute=F(0);rel=0
 for x in phase.values():
  debit=F(x['soil_before'])-F(x['soil_after']);assert F(x['credit'])+F(x['bare_credit'])<=debit;assert F(x['h'])*F(x['demand'])<=F(x['credit'])<=F(x['demand']);delta=(F(x['vapor_after'])-F(x['vapor_before']))*10**9-debit*F(x['area']);signed+=delta;absolute+=abs(delta)
  if debit:rel=max(rel,float(abs(delta)/(debit*F(x['area']))))
 for x in used:
  assert x['owner']==x['lineage']==704
  assert x['credit']==phase[x['tick']]['credit'];assert x['denominator']==max(x['entry_demand'],x['current_demand']);assert F(x['h'])*F(x['denominator'])<=F(x['credit']);assert 0<=x['effective_h']<=x['h']<=1
  if x['current_demand']<=0:assert x['h']==0
 final=json.loads((b/f'arm-{arm}-60.json').read_bytes());cs=[z['value']for z in final['origin']['cells'][36453]['sparse']];focal=next((c for c in cs if c['lineage']==704),None);hab=rows(m,'HABITAT');growth=rows(m,'PAID_GROWTH');births=rows(m,'BIRTH')
 item=dict(arm=arm,setup=rows(m,'SETUP')[0],action=rows(m,'WATER_ACTION'),root_pulses=sum(x['credit']>0 for x in phase.values()),root_credit=sum(x['credit']for x in phase.values()),used_records=len(used),max_used_h=max((x['effective_h']for x in used),default=0),paid_growth=sum(x['actual_carbon']for x in growth),habitat_changed_ticks=[x for x in hab if x['used']!=x['old']],habitat_trace=hab,final_focal=focal,final_patch=cs,children=[x['child']['lineage']for x in births if x['child']['parent']==704],depth_min=min(x['depth_m']for x in patch),depth_max=max(x['depth_m']for x in patch),patch_trace=patch,source_signed_kg=float(signed),source_sumabs_kg=float(absolute),source_max_relative=rel,fullstate_restart=True,trace_on_off_exact=True,completions=[l for l in(b/m).read_text().splitlines()if l.startswith('COMPLETE')])
 out.append(item)
# Starts differ only by explicit identity and prescribed selected standing-water action.
initial=json.load(open(b/'arm-0-0.json'));new=json.load(open(b/'arm-1-0.json'));control=json.load(open(b/'arm-2-0.json'));normal=lambda x: (x.update(version=10),x['beta_origin'].update(format='origin_land_beta_v3'),x['beta_origin']['config'].update(physiology_law=3))
normal(new);assert initial==new
control['water'][36453]=initial['water'][36453];normal(control);assert initial==control
end_old=json.load(open(b/'arm-0-60.json'));end_new=json.load(open(b/'arm-1-60.json'));normal(end_new);assert end_old==end_new
(b/'results.json').write_text(json.dumps(out,indent=2)+'\n')
for x in out:print(json.dumps({k:v for k,v in x.items()if k not in ['patch_trace','habitat_trace','final_patch','setup','habitat_changed_ticks']},indent=2));print('CHANGED_HABITAT',x['habitat_changed_ticks'][:3])
print('ALL_FRACTION_OWNER_FUNDING_IDENTITY_RESTART_PARITY_PASS')

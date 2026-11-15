from pathlib import Path
import json,sys,hashlib
baseline=json.loads(Path(sys.argv[1]).read_text());candidate=json.loads(Path(sys.argv[2]).read_text())
assert baseline['version']==6 and candidate['version']==7
assert baseline['origin']['model_revision']==5 and candidate['origin']['model_revision']==6
candidate['version']=6;candidate['origin']['model_revision']=5
for cell in candidate['origin']['cells']:
 for field in ['liquid_return','vapor_return']:
  assert cell.get(field,0)==0;cell.pop(field,None)
 for item in cell.get('sparse',[]):
  co=item['value']
  for field in ['retention_allocation','stored_water']:
   assert co.get(field,0)==0;co.pop(field,None)
assert baseline==candidate,'Old-field full save differs'
print(json.dumps({'exact_old_fields':True,'allowed_only_zero_new_fields_and_schema_revision':True,'baseline_sha256':hashlib.sha256(Path(sys.argv[1]).read_bytes()).hexdigest(),'candidate_sha256':hashlib.sha256(Path(sys.argv[2]).read_bytes()).hexdigest()}))

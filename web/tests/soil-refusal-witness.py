from fractions import Fraction as F
import json
soil=F(3,4)**26;vapor=1-soil;request=soil/4;target=vapor+request;rounded=F(float(target));credit=rounded-vapor;newsoil=soil-credit
assert F(float(newsoil))==newsoil and newsoil+rounded==soil+vapor
print(json.dumps({'accepted_steps_before_refusal':26,'old_soil':float(soil),'old_vapor':float(vapor),'requested':float(request),'exact_target_fraction':str(target),'nearest_target_error':str(rounded-target),'source_requested_debit_representable':F(float(soil-request))==soil-request,'receiver_requested_increment_representable':rounded==target,'bounded_receiver_credit':float(credit),'unspent_in_soil':str(request-credit),'actual_new_soil':float(newsoil),'exact_alternative_balance':True},indent=2))

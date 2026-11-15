#!/usr/bin/env python3
"""Preserve literal legacy optimized thermal arithmetic; beta uses separate entry."""
from pathlib import Path
import sys
p=Path(sys.argv[1]);s=p.read_text();a=s.index('    fn simulateTemperature(');b=s.index('    fn simulateTemperature_OpenCL(',a);body=s[a:b]
assert 'self.vaporMass32(i)'in body and 'simulateLandTemperature'not in s
legacy=body.replace('self.vaporMass32(i)','self.waterVaporMass[i]')
beta=body.replace('fn simulateTemperature(','fn simulateLandTemperature(')
s=s[:a]+legacy+beta+s[b:]
s=s.replace('                job.call(simulateTemperature, .{ self, loop, options, start, end }) catch unreachable;','                if(self.landBeta.enabled)job.call(simulateLandTemperature,.{ self, loop, options, start, end }) catch unreachable else job.call(simulateTemperature, .{ self, loop, options, start, end }) catch unreachable;')
s=s.replace('if (USE_OPENCL and self.clContext != null) {','if (USE_OPENCL and self.clContext != null and !self.landBeta.enabled) {')
s=s.replace('return self.vaporMass32(idx) + self.averageNitrogenMass','if(self.landBeta.enabled)return self.vaporMass32(idx)+self.averageNitrogenMass+self.averageOxygenMass+self.averageCarbonDioxideMass+1;\n        return self.waterVaporMass[idx] + self.averageNitrogenMass')
s=s.replace('return self.getAirPressure(self.getSubstanceDivider(), self.temperature[idx], self.vaporMass(idx));','if(self.landBeta.enabled)return self.getAirPressure(self.getSubstanceDivider(),self.temperature[idx],self.landVapor[idx]);\n        return self.getAirPressure(self.getSubstanceDivider(), self.temperature[idx], self.waterVaporMass[idx]);')
p.write_text(s)

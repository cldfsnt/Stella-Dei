#!/usr/bin/env python3
"""Depth/color contract only; native GL captures verify actual shader rendering."""
from pathlib import Path
import re, unittest
source=(Path(__file__).resolve().parents[2]/'src/shaders/terrain.fs').read_text()
a,b=map(float,re.search(r'float wet = smoothstep\(([^,]+), ([^,]+), waterElevation\);',source).groups())
def wet(metres):
    t=max(0,min(1,(metres/1000-a)/(b-a)))
    return t*t*(3-2*t)
class ShallowWater(unittest.TestCase):
    def test_dry_stays_dry(self): self.assertEqual(wet(0),0)
    def test_fifteen_metre_pond_reads_water(self): self.assertEqual(wet(15),1)
    def test_one_metre_habitat_is_visible(self): self.assertGreater(wet(1),.45)
    def test_ocean_unchanged(self): self.assertEqual(wet(1000),1)
    def test_continuous_shore(self): self.assertLess(wet(.5),wet(1))
if __name__=='__main__': unittest.main()

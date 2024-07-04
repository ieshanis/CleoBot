import unittest

from vgc.competition import get_pkm_points, STANDARD_TOTAL_POINTS
from vgc.util.generator.PkmRosterGenerators import RandomPkmRosterGenerator


class TestEncodingMethods(unittest.TestCase):

    def test_random_roster_generator(self):
        gen = RandomPkmRosterGenerator()
        roster = gen.gen_roster()
        for tmpl in roster:
            pkm = tmpl.gen_pkm([0, 1, 2, 3])
            points = get_pkm_points(pkm)
            if pkm.hp == 10.0:
                self.assertLess(points, STANDARD_TOTAL_POINTS + 4)
            else:
                self.assertLess(points, STANDARD_TOTAL_POINTS + 1)

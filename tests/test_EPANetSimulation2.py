import os
import math
import copy
import unittest
import epanettools
from epanettools.examples import simple
from  epanettools.epanettools import EPANetSimulation, Node, Link, Network, Nodes, \
    Links, Patterns, Pattern, Controls, Control

from unittest import skip, expectedFailure
from tests import tools_for_testing as tt


class Test1(unittest.TestCase):

    def setUp(self):
        print("SETUP!")
        file = os.path.join(os.path.dirname(simple.__file__), 'Net3.inp')
        self.es = EPANetSimulation(file)

    def tearDown(self):
        self.es.clean()
        print("TEAR DOWN!")

    @skip
    def test_false(self):
        assert False

    def test_patterns_are_retrieved_properly(self):
        p = self.es.network.patterns
        self.assertEqual(len(p), 5)  # there are five patterns
        [self.assertEqual(p[x].id, str(x))
         for x in range(1, len(p) + 1)]  # the ids of patterns are '1','2',..,'5' - how convienient!
        l = [len(p[x]) for x in range(1, len(p) + 1)]
        [self.assertEqual(x, 24) for x in l]  # all thoese patterns are 24 length
        # check a few values of pattern 1
        self.assertAlmostEqual(p[1][1], 1.34, delta=2)
        self.assertAlmostEqual(p[1][24], 1.67, delta=2)
        self.assertAlmostEqual(p[1][22], .96, delta=2)


def clt(fn, tc):
    tc.setUp()
    fn()
    tc.tearDown()


def main():
    tc = Test1()
    for a in dir(tc):
        if (a.startswith('test_pattern')):  # test_sync
            b = getattr(tc, a)
            if(hasattr(b, '__call__')):
                print ("calling %s **********************************" % a)
                clt(b, tc)


if __name__ == "__main__":
        main()

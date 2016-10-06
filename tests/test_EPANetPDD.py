import math
import os
import unittest
from unittest import expectedFailure
from unittest import skip

import epanettools
from epanettools.epanettools import Control
from epanettools.epanettools import Controls
from epanettools.epanettools import EPANetSimulation
from epanettools.epanettools import Link
from epanettools.epanettools import Links
from epanettools.epanettools import Network
from epanettools.epanettools import Node
from epanettools.epanettools import Nodes
from epanettools.epanettools import Pattern
from epanettools.epanettools import Patterns
from epanettools.examples import simple


class Test1(unittest.TestCase):

    def Error(self, e):
        if(e):
            s = "Epanet Error: %d : %s" % (e, self.es.ENgeterror(e, 500)[1])
            raise Exception(s)

    def setUp(self):
        print("SETUP!")
        file = os.path.join(os.path.dirname(simple.__file__), 'Net3.inp')
        self.es = EPANetSimulation(file)

    def tearDown(self):
        self.es.clean()
        print("TEAR DOWN!")

    def test_runs_a_simulation_with_pipe_closed_and_get_results_pdd_give_reasonable_results(self):
        # now do the same with pipe '247' closed.
        ind = self.es.network.links['247'].index
        dia = Link.value_type["EN_DIAMETER"]  # get the code for EN_STATUS
        # use old interface to set diameter to zero
        self.Error(self.es.ENsetlinkvalue(ind, dia, 0.1))  # now link diameter is small
        file = "1.inp"
        self.es.ENsaveinpfile(file)
        # now create a new object with the new file.
        es = EPANetSimulation(file, pdd=True)
        es.run()
        p = Node.value_type['EN_PRESSURE']
        d = Node.value_type['EN_DEMAND']
        self.assertAlmostEquals(es.network.nodes['215'].results[p][5], -1.3, places=1)
        self.assertAlmostEqual(es.network.nodes['215'].results[d][5], 0.0, places=1)

    def test_runs_a_normal_pressure_simulation_and_get_results_pdd_does_not_change_results(self):
        # self.fail("Not yet calling epanet emitter properly")
        def mod1():
            p = Node.value_type['EN_PRESSURE']
            self.assertAlmostEqual(self.es.network.nodes['103'].results[p][5], 59.301, places=3)
            self.assertAlmostEqual(self.es.network.nodes['125'].results[p][5], 66.051, places=3)
            self.assertEqual(self.es.network.time[5], 15213)
            self.assertEqual(self.es.network.tsteps[5], 2787)
            self.assertEqual(self.es.network.tsteps[6], 3600)
            self.assertEqual(len(self.es.network.time), len(self.es.network.nodes[1].results[p]))

            d = Node.value_type['EN_DEMAND']
            h = Node.value_type['EN_HEAD']
            self.assertAlmostEqual(self.es.network.nodes['103'].results[d][5], 101.232, places=3)
            self.assertAlmostEqual(self.es.network.nodes['103'].results[h][5], 179.858, places=3)

        def mod2():
            p = Link.value_type['EN_DIAMETER']
            self.assertAlmostEquals(
                self.es.network.links[1].results[p][0],
                99.0,
                places=1)  # index is not important. Diameter is fixed. !
            self.assertAlmostEquals(self.es.network.links['105'].results[p][0], 12.0, places=1)
            v = Link.value_type['EN_VELOCITY']
            self.assertAlmostEquals(self.es.network.links[2].results[v][22], 0.025, places=2)
            self.assertAlmostEquals(self.es.network.links['111'].results[v][1], 3.23, places=2)

        def mod3():
            p = Node.value_type['EN_PRESSURE']
            self.assertAlmostEqual(self.es.network.nodes['215'].results[p][5], 58.7571, places=3)
            self.assertAlmostEqual(self.es.network.nodes['225'].results[p][5], 58.320, places=3)

            d = Node.value_type['EN_DEMAND']
            self.assertAlmostEqual(self.es.network.nodes['215'].results[d][5], 70.064, places=3)
            self.assertAlmostEqual(self.es.network.nodes['225'].results[d][5], 17.328, places=3)

        def mod4():
            p = Node.value_type['EN_PRESSURE']
            self.assertAlmostEqual(self.es.network.nodes['215'].results[p][5], 58.7571, places=3)
            self.assertAlmostEqual(self.es.network.nodes['225'].results[p][5], 58.320, places=3)

            d = Node.value_type['EN_DEMAND']
            self.assertAlmostEqual(self.es.network.nodes['215'].results[d][5], 70.064, places=3)
            self.assertAlmostEqual(self.es.network.nodes['225'].results[d][5], 17.328, places=3)

        self.es.run()
        mod1()
        mod2()
        self.es.runq()
        q = Node.value_type['EN_QUALITY']
        self.assertAlmostEqual(self.es.network.nodes['117'].results[q][4], 85.317, places=3)
        self.assertAlmostEqual(self.es.network.nodes['117'].results[q][5], 100.0)
        e = Link.value_type['EN_ENERGY']
        self.assertAlmostEquals(self.es.network.links['111'].results[e][23], .00685, places=2)
        mod1()
        mod2()
        mod3()

        file = "1.inp"
        self.Error(self.es.ENsaveinpfile(file))
        # now create a new object with the new file.
        es = EPANetSimulation(file, pdd=True)
        es.run()
        mod1()
        mod2()
        mod3()


def clt(fn, tc):
    tc.setUp()
    fn()
    tc.tearDown()


def main():
    tc = Test1()
    for a in dir(tc):
        if (a.startswith('test_')):
        # if
        # (a.startswith('test_runs_a_simulation_with_pipe_closed_and_get_results_pdd_give_reasonable_results')):#test_')):
            b = getattr(tc, a)
            if(hasattr(b, '__call__')):
                print ("calling %s **********************************" % a)
                clt(b, tc)


if __name__ == "__main__":
        main()

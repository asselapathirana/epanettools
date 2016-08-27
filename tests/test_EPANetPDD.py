import os
import math
import unittest
import epanettools
from epanettools.examples import simple
from  epanettools.epanettools import EPANetSimulation, Node, Link, Network, Nodes, \
      Links, Patterns, Pattern, Controls, Control

from unittest import skip, expectedFailure


class Test1(unittest.TestCase):
    
    def setUp(self): 
        print("SETUP!")
        file = os.path.join(os.path.dirname(simple.__file__),'Net3.inp')
        self.es=EPANetSimulation(file)           

    def tearDown(self):
        self.es.clean()
        print("TEAR DOWN!")
        
    def test_runs_a_simulation_and_get_results(self):
        #self.fail("Not yet calling epanet emitter properly")
        def mod1():
            p=Node.value_type['EN_PRESSURE']
            self.assertAlmostEqual(self.es.network.nodes['103'].results[p][5],59.301,places=3)
            self.assertAlmostEqual(self.es.network.nodes['125'].results[p][5],66.051,places=3)
            self.assertEqual(self.es.network.time[5],15213)
            self.assertEqual(self.es.network.tsteps[5],2787)
            self.assertEqual(self.es.network.tsteps[6],3600)
            self.assertEqual(len(self.es.network.time),len(self.es.network.nodes[1].results[p]))

            d=Node.value_type['EN_DEMAND']
            h=Node.value_type['EN_HEAD']
            self.assertAlmostEqual(self.es.network.nodes['103'].results[d][5],101.232, places=3)
            self.assertAlmostEqual(self.es.network.nodes['103'].results[h][5],179.858, places=3)

        def mod2():
            p=Link.value_type['EN_DIAMETER']
            self.assertAlmostEquals(self.es.network.links[1].results[p][0],99.0,places=1) #index is not important. Diameter is fixed. !
            self.assertAlmostEquals(self.es.network.links['105'].results[p][0],12.0,places=1)
            v=Link.value_type['EN_VELOCITY']
            self.assertAlmostEquals(self.es.network.links[2].results[v][22],0.025,places=2)
            self.assertAlmostEquals(self.es.network.links['111'].results[v][1],3.23,places=2)

        self.es.run()
        mod1()
        mod2()
        self.es.runq()
        q=Node.value_type['EN_QUALITY']
        self.assertAlmostEqual(self.es.network.nodes['117'].results[q][4],85.317,places=3)
        self.assertAlmostEqual(self.es.network.nodes['117'].results[q][5],100.0)
        e=Link.value_type['EN_ENERGY']
        self.assertAlmostEquals(self.es.network.links['111'].results[e][23],.00685,places=2)
        mod1()
        mod2()  

tc=Test1()
def clt(fn):
    tc.setUp()
    fn()
    tc.tearDown()

def main():
    for a in dir(tc):
        if (a.startswith('test_')):
            b=getattr(tc,a)
            if(hasattr(b, '__call__')):
                print ("calling %s **********************************" % a )
                clt(b)
           


if __name__ == "__main__":
        main()
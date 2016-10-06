import copy
import math
import os
import sys
import unittest
from unittest import expectedFailure
from unittest import skip

from tests import tools_for_testing as tt

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

    def test_can_retrieve_patterns_with_correct_length_and_values(self):
        self.assertAlmostEqual(self.es.network.patterns[1][1],1.34,delta=.01 )
        self.assertAlmostEqual(self.es.network.patterns[1][2],1.94,delta=.01 )
        self.assertAlmostEqual(self.es.network.patterns[1][3],1.46,delta=.01 )
        self.assertEqual(len(self.es.network.patterns[1]),24)
        self.assertAlmostEqual(self.es.network.patterns[1][24],1.67,delta=.01)
        self.assertEqual(len(self.es.network.patterns),5)
        with self.assertRaises(KeyError):
            self.es.network.patterns[6]
        with self.assertRaises(KeyError):
            self.es.network.patterns[1][25]
            
            
    def test_set_patternvalue_changes_pattern_values(self):
        self.assertAlmostEqual(self.es.ENgetpatternvalue(1,3)[1],1.46,delta=.01 )
        self.assertEqual(self.es.ENsetpatternvalue(1,3,1.8),0)
        self.assertAlmostEqual(self.es.ENgetpatternvalue(1,3)[1],1.8,delta=.01 )
        
    def test_set_patternvalue_can_append_pattern_value(self):
        self.assertEqual(len(self.es.network.patterns[1]),24)
        with self.assertRaises(TypeError):
            self.assertEqual(self.es.ENsetpattern(6,1.,3),0)
            
    def test_ENsetpatterndim_will_allocate_a_pattern(self):
        index = self.create_pattern()
        self.assertEqual(self.es.ENsetpatterndim(index,24),0)
        self.assertEqual(self.es.ENgetpatternlen(index),[0,24])
        for i in range(25):
            p=self.es.ENgetpatternvalue(index,i+1)
            if(i<24):
                self.assertEqual(p[0],0)
                self.assertAlmostEqual(p[1],0.0, delta=.01)
            else:
                self.assertEqual(p[0],251)                

    def create_pattern(self):
        patId = "NewPattern";
        self.assertEqual(self.es.ENaddpattern(patId),0)
        ret,index=self.es.ENgetpatternindex(patId)
        return index

    def test_ENsetpattern_will_successfully_allocate_and_fill_an_exiting_pattern(self):
        index=self.create_pattern()
        pat=[1.0,2.0,3.0,4.0,8.0,9.0,10.0,11.0,
             1.5,2.5,3.5,4.5,8.5,9.5,10.5,11.5,
             1.6,2.6,3.6,4.6,8.6,9.6,10.6,11.6,]
        self.assertEqual(self.es.ENsetpattern(index,pat),0)
        self.assertEqual(self.es.ENgetpatternlen(index),[0,24])
        for i in range(len(pat)):
            p=self.es.ENgetpatternvalue(index,i+1)
            self.assertEqual(p[0],0)
            self.assertAlmostEqual(p[1],pat[i],delta=0.001)   
        
        

tc = None



def clt(tc,fn):
    tc.setUp()
    fn()
    tc.tearDown()


def main():
    tc = Test1()
    for a in dir(tc):
        if (a.startswith('test_')):  # test_sync
            b = getattr(tc, a)
            if(hasattr(b, '__call__')):
                print ("calling %s **********************************" % a)
                clt(tc,b)


if __name__ == "__main__":
    main()

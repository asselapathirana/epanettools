import copy
import math
import os
import sys
import unittest
from unittest import expectedFailure
from unittest import skip

from tests import tools_for_testing as tt

import epanettools
from epanettools.epanettools import EPANetSimulation
from epanettools.epanettools  import Link
from epanettools.epanettools import Links
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

    def test_EPANetSimulation_by_default_has_no_ADF_values(self):
        d= Link.value_type['EN_DIAMETER']
        self.assertAlmostEqual(self.es.network.links[1].results[d][0],99.,delta=1)
        self.assertRaises(AttributeError, getattr, self.es.network.links[1], "ADF")
        
    def test_EPANetSimulation_after_calling_adfcalc_has_ADF_values(self):
        d= Link.value_type['EN_DIAMETER']
        self.assertAlmostEqual(self.es.network.links[1].results[d][0],99.,delta=1)
        raised=False
        try:
            self.assertAlmostEqual(self.es.network.links[1].ADF,.05) 
        except AttributeError:
            raised=True
        self.assertTrue(raised,"Did not raise exception.")
        self.es.adfcalc()
        self.assertAlmostEqual(self.es.network.links[1].ADF,0.99996,delta=.001) 
        self.assertAlmostEqual(self.es.network.links['151'].ADF,0.974816, delta=0.001)    
      
        

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

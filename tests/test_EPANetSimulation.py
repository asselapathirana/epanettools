import os
import unittest
import epanettools

from unittest import skip, expectedFailure


class Test1(unittest.TestCase):
    def setup(): 
        print("SETUP!")
    
    def teardown():
        print("TEAR DOWN!")
    
    @skip  
    def test_false(self):
        assert False
        
    def test_can_import_EPANetSimulation(self):
        try:
            from epanettools.epanettools import EPANetSimulation
        except (Exception):
            assert False
    
    def test_properly_open_a_network_file(self):
        from  epanettools.epanettools import EPANetSimulation
        from epanettools.examples import simple
        
        self.assertRaises(FileNotFoundError, EPANetSimulation,"Silly file")
        file = os.path.join(os.path.dirname(simple.__file__),'Net3.inp')
        es=EPANetSimulation(file)
        self.assertNotEqual(file,es.inputfile)
        self.assertTrue(os.path.isfile(es.inputfile))
        self.assertFalse(os.path.isdir(es.inputfile))
        
    
def main():
    #test_false()
    tc=Test1()
    
    tc.test_properly_open_a_network_file()

if __name__ == "__main__":
        main()
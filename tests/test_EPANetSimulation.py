import os
import unittest
import epanettools
from epanettools.examples import simple
from  epanettools.epanettools import EPANetSimulation

from unittest import skip, expectedFailure


class Test1(unittest.TestCase):
    def setUp(self): 
        print("SETUP!")
        file = os.path.join(os.path.dirname(simple.__file__),'Net3.inp')
        self.es=EPANetSimulation(file)           
    
    def subTest(self):
        print("TEAR DOWN!")
    
    @skip  
    def test_false(self):
        assert False
        
    def test_can_import_EPANetSimulation(self):
        try:
            from epanettools.epanettools import EPANetSimulation
        except (Exception):
            assert False
            
    def test_non_existing_file_raise_error(self):
        self.assertRaises(FileNotFoundError, EPANetSimulation,"Silly file")
    
    def test_properly_open_a_network_file(self):
        import filecmp
        file = os.path.join(os.path.dirname(simple.__file__),'Net3.inp')
        es=EPANetSimulation(file)
        self.assertNotEqual(file,self.es.inputfile)
        self.assertTrue(os.path.isfile(self.es.inputfile))
        self.assertFalse(os.path.isdir(self.es.inputfile))
        # file names are unique
        self.assertEqual(len(set([EPANetSimulation(file).inputfile for i in range(100)])),100)
        # file content is identical to the original file
        self.assertTrue(filecmp.cmp(self.es.inputfile,file))
        # but names are not the same
        self.assertFalse(self.es.inputfile==file)
        
    def test_get_correct_network_information(self):
        from  epanettools.epanettools import EPANetSimulation
        from epanettools.examples import simple
        

        self.assertEqual(self.es.getNodes()[0],'10')
        self.assertEqual(self.es.getNodes()[2],'20')
        self.assertEqual(self.es.getNodes()[-1],'3')
        self.assertEqual(self.es.getNodes()[-4],'Lake')

        self.assertEqual(self.es.getLinks()[0],'20')
        self.assertEqual(self.es.getLinks()[2],'50')
        self.assertEqual(self.es.getLinks()[-1],'335')    
        
    def can_access_low_level_EN_type_functions(self):
        self.assertEqual(self.es.ENgetnodeid(3),[0,'20'])
    
def main():
    #test_false()
    tc=Test1()
    tc.setUp()
    tc.test_non_existing_file_raise_error()
    tc.can_access_low_level_EN_type_functions()
    tc.test_get_correct_network_information()

if __name__ == "__main__":
        main()
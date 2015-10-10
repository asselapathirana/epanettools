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
        n=self.es.nodes
        self.assertEqual(n[1].id,'10')
        self.assertEqual(n[3].id,'20')
        self.assertEqual(n[25].id,'129')
        self.assertEqual(n[94].id,'Lake')
        
        self.assertEqual(n[94].index,94)
        
        m=self.es.links
        self.assertEqual(m[1].id,'20')
        self.assertEqual(m[3].id,'50')
        self.assertEqual(m[119].id,'335')  
        self.assertEqual([m[1].start.id,m[1].end.id],['3','20'])
        self.assertEqual([m[118].start.id,m[118].end.id],['Lake','10'])
        
        
        self.assertEqual(m[119].index,119)
        
        # link or node can be searched with ID too. 
        self.assertEqual(n['Lake'].id,'Lake')
        self.assertEqual(n['Lake'].index,94)
        self.assertEqual(m['335'].id,'335')
        self.assertEqual(m['335'].index,119)
        
        # get the links connected to a node. 
        self.assertEqual(sorted([i.id for i in n['169'].links]),['183', '185', '187', '211'] )
        
    def test_can_access_low_level_EN_type_functions(self):
        self.assertEqual(self.es.ENgetnodeid(3),[0,'20'])
        
        
    def test_each_node_and_link_has_the_epanetsimulation_object_linked_to_it_as_variable_es(self):
        self.assertIsInstance(self.es.links[1].es,EPANetSimulation)
        self.assertIsInstance(self.es.nodes[1].es,EPANetSimulation)
    
    def test_runs_a_simulation_and_get_results(self):
        self.es.run()
        self.assertAlmostEqual(self.es.nodes['103'].pressure[5],59.3006591796875)
        self.assertAlmostEqual(self.es.nodes['125'].pressure[5],66.05056762695312)
        self.assertEqual(self.es.time[5],15213)
        self.assertEqual(len(self.es.time),len(self.es.nodes[1].pressure))
        
        self.assertAlmostEqual(self.es.nodes['103'].demand[5],101.23200225830078)
        self.assertAlmostEqual(self.es.nodes['103'].head[5],179.8582000732422)
        
        self.es.runq()
        self.assertAlmostEqual(self.es.nodes['117'].quality[4],85.31733703613281)
        self.assertAlmostEqual(self.es.nodes['117'].quality[5],100.0)
        
    @skip
    def test_hydraulic_file_is_saved_only_when_save_is_true(self):
        self.es.run(save=False)
        self.assertFalse(os.path.exists(self.es.hydraulicfile))
        self.es.run(save=True)
        self.assertTrue(os.path.exists(self.es.hydraulicfile))        

    @skip
    def test_clean_will_remove_results(self):
        self.assertTrue(os.path.exists(self.es.inputfile))        
        self.es.run()
        self.assertTrue(os.path.exists(self.es.rptfile))
        self.assertTrue(os.path.exists(self.es.hydraulicfile))         
        self.es.runq()
        self.assertTrue(os.path.exists(self.es.rptfile))
        self.assertTrue(os.path.exists(self.es.binfile))
        self.assertTrue(os.path.exists(self.es.hydraulicfile))         
        self.es.clean()
        self.assertTrue(os.path.exists(self.es.inputfile))
        self.assertFalse(os.path.exists(self.es.rptfile))
        self.assertFalse(os.path.exists(self.es.binfile))
        self.assertFalse(os.path.exists(self.es.hydraulicfile))

def main():
    #test_false()
    tc=Test1()
    tc.setUp()
    tc.test_non_existing_file_raise_error()
    tc.test_can_access_low_level_EN_type_functions()
    tc.test_get_correct_network_information()
    tc.test_each_node_and_link_has_the_epanetsimulation_object_linked_to_it_as_variable_es()
    tc.test_runs_a_simulation_and_get_results()
    tc.test_hydraulic_file_is_saved_only_when_save_is_true()
    tc.test_clean_will_remove_results()
    tc.test_destruction_will_remove_temporary_inputfile()

if __name__ == "__main__":
        main()
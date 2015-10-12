import os
import unittest
import epanettools
from epanettools.examples import simple
from  epanettools.epanettools import EPANetSimulation, Node, Link

from unittest import skip, expectedFailure


class Test1(unittest.TestCase):
    def setUp(self): 
        print("SETUP!")
        file = os.path.join(os.path.dirname(simple.__file__),'Net3.inp')
        self.es=EPANetSimulation(file)           
    
    def tearDown(self):
        self.es.clean()
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
        
        # types of nodes
        self.assertEqual(n[94].node_type,Node.node_types['RESERVOIR'])
        self.assertEqual(n[1].node_type,Node.node_types['JUNCTION'])
        self.assertEqual(n['2'].node_type,Node.node_types['TANK'])
        
        #types of links
        self.assertEqual(m['335'].link_type,Link.link_types['PUMP'])
        self.assertEqual(m['101'].link_type,Link.link_types['PIPE'])
        self.assertEqual(m[1].link_type,Link.link_types['PIPE'])
        
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
        def mod1():
            p=Node.result_type['EN_PRESSURE']
            self.assertAlmostEqual(self.es.nodes['103'].results[p][5],59.301,places=3)
            self.assertAlmostEqual(self.es.nodes['125'].results[p][5],66.051,places=3)
            self.assertEqual(self.es.time[5],15213)
            self.assertEqual(len(self.es.time),len(self.es.nodes[1].results[p]))
            
            d=Node.result_type['EN_DEMAND']
            h=Node.result_type['EN_HEAD']
            self.assertAlmostEqual(self.es.nodes['103'].results[d][5],101.232, places=3)
            self.assertAlmostEqual(self.es.nodes['103'].results[h][5],179.858, places=3)
        
        
        self.es.run()
        mod1()
        self.es.runq()
        q=Node.result_type['EN_QUALITY']
        self.assertAlmostEqual(self.es.nodes['117'].results[q][4],85.317,places=3)
        self.assertAlmostEqual(self.es.nodes['117'].results[q][5],100.0)
        mod1()
        


        
    
    def test_hydraulic_file_is_saved_only_when_save_is_true(self):
        self.es.run(save=False)
        self.assertFalse(os.path.exists(self.es.hydraulicfile))
        self.es.run(save=True)
        self.assertTrue(os.path.exists(self.es.hydraulicfile))        

    
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
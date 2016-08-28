import unittest
import difflib
import os
from epanettools import epanet2 as et
from epanettools.examples import simple


class Test1(unittest.TestCase):
    
    def compareFiles(self, first, second):
        with open(first, 'r') as myfile:
            f=myfile.read()
        with open(second, 'r') as myfile:
            s=myfile.read()
            
        s = difflib.SequenceMatcher(lambda x: x == " ",f,s)
        return s.get_opcodes()   
    
    def Error(self,e):
        if(e):
            s="Epanet Error: %d : %s" %(e,et.ENgeterror(e,500)[1])
            raise Exception(s)  
        
    def setUp(self): 
        print("SETUP!")
        self.file = os.path.join(os.path.dirname(simple.__file__),'Net3.inp')
        self.Error(et.ENopen(self.file,"t.rpt",""))      
    
    def tearDown(self):
        self.Error(et.ENclose())
        print("TEAR DOWN!")
        
    def test_alter_with_ENset_and_check_with_a_file(self):
        self.Error(et.ENsaveinpfile("1.inp"))
        self.Error(et.ENsetlinkvalue(81,0,9999))
        self.Error(et.ENsaveinpfile("2.inp"))
        self.assertEqual(self.compareFiles("1.inp","2.inp")[1],"('replace', 16946, 16983, 16946, 16983)")        
    

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
        


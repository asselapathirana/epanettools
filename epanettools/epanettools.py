from . import epanet2 as et
import tempfile, shutil, os

class Node():
    id=''
    elevation=float('nan')
    
class Link():
    id=''
    start=None
    end=None
    diameter=float('nan')
    length=float('nan')
    


class EPANetSimulation():
    
    
    def __init__(self,inputFileName):
        self.enOpenStatus=False
        self.OriginalInputFileName=inputFileName
        self.inputfile=self.create_temporary_copy(inputFileName)
        self.rptfile=self.inputfile[:-3]+".rpt"
        self.binfile=self.inputfile[:-3]+".bin"
        self._open()

    
    def Error(self,e):
        if(e):
            s="Epanet Error: %d : %s" %(ENgeterror(e,50),e)
            raise Exception(s)        
            
    def create_temporary_copy(self,path):    
        f=os.path.join(tempfile._get_default_tempdir(),next(tempfile._get_candidate_names())+".inp")
        shutil.copyfile(path,f)
        return f
    def _open(self): 
        if(not self.enOpenStatus):
            self._explicitly_open()
        self.enOpenStatus=True

    def _explicitly_open(self):
        self.Error(et.ENopen(self.inputfile,self.rptfile,self.binfile))

        
    def _reset(self):
        self.Error(et.ENclose())
        self.Error(et._explicitly_open())
        
        
    def getLinks(self):
        self._open()
        links={}
        for i in range(1,et.ENgetcount(et.EN_LINKCOUNT)[1]+1):
            link=Link()
            link.id=et.ENgetlinkid(i)[1]
            links[i]=link
        return links
    
    def getNodes(self):
        self._open()
        nodes={}
        for i in range(1,et.ENgetcount(et.EN_NODECOUNT)[1]+1):
                node=Node()
                node.id=et.ENgetnodeid(i)[1]
                node.elevation=et.ENgetnodevalue(i,et.EN_ELEVATION )
                nodes[i]=node
        return nodes
    
    
    def __getattribute__(self, name):
        try:
            return object.__getattribute__(self, name)
        except:
            pass
        self._open()
        if(hasattr(et,name)): # search legacy interface            
            return getattr(et,name)
        raise AttributeError("The attribute %s not found with this class or underlying c interface" % name)    
        

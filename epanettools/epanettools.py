from . import epanet2 as et
import tempfile, shutil, os, sys

"""" Never use ENOpen ENclose without keeping tab. -- always use _close and _open methods instead.
     Never use ENOpenH ENcloseH without keeping tab. -- always use _HClose and _HOpen methods instead."""

from . import tools

class Node():
    def __init__(self,es):
        self.es=es
        self.id=''
        self.elevation=float('nan')
        self.links=[]
    
class Link():
    def __init__(self,es):
        self.es=es
        self.id=''
        self.start=None
        self.end=None
        self.diameter=float('nan')
        self.length=float('nan')
    
class index_id_type(tools.TransformedDict):
    
    def __setitem__(self, key, value):
        v=self.__keytransform__(key)
        self.store[v] = value
        self.store[v].index=v
        
    def __keytransform__(self, key):
        if isinstance(key, str):
            for i,j in self.store.items():
                if (key==j.id):
                    return i
            raise KeyError("Key %s not found" % key)
        return key
    
class Nodes(index_id_type):
    pass

class Links(index_id_type):
    pass


class EPANetSimulation():
    
    
    def __init__(self,inputFileName):
        self._enOpenStatus=False
        self._enHOpenStatus=False
        self.OriginalInputFileName=inputFileName
        self.inputfile=self.create_temporary_copy(inputFileName)
        self.rptfile=self.inputfile[:-3]+"rpt"
        self.binfile=self.inputfile[:-3]+"bin"
        self.hydraulicfile=self.inputfile[:-3]+"hyd"
        self._open()
        self._getLinksAndNodes()


    def run(self, save=True):
        self._open()
        self.time=[]
        for i,node in self.nodes.items():
            node.demand=[]
            node.head=[]
            node.pressure=[]
        self._HOpen()
        if (save):
            init=1
        else:
            init=0
        et.ENinitH(init)
        while True :
            ret,t=et.ENrunH()
            self.time.append(t)
            # Retrieve hydraulic results for time t
            for  i,node in self.nodes.items():
                et.ENgetnodevalue(node.index, et.EN_PRESSURE )
                node.demand.append(et.ENgetnodevalue(node.index, et.EN_DEMAND )[1])
                node.head.append(et.ENgetnodevalue(node.index, et.EN_HEAD )[1])
                node.pressure.append(et.ENgetnodevalue(node.index, et.EN_PRESSURE )[1])
                
            ret,tstep=et.ENnextH()
            if (tstep<=0):
                break
        if(save):
            self.Error(et.ENsavehydfile(self.hydraulicfile))
        self._HClose()


 
    def runq(self):
        
        for i,node in self.nodes.items():
            node.quality=[]        
        self.Error(et.ENusehydfile(self.hydraulicfile))
        self.Error(et.ENopenQ()) 
        self.Error(et.ENinitQ(1))
        while(True):
            ret,t=et.ENrunQ()
            self.Error(ret)
            for i,node in self.nodes.items():
                node.quality.append(et.ENgetnodevalue(node.index, et.EN_QUALITY )[1])
            ret,tstep=et.ENnextQ()
            self.Error(ret)
            if(tstep<=0):
                break
        et.ENcloseQ();         
        
    
    def Error(self,e):
        if(e):
            s="Epanet Error: %d : %s" %(e,et.ENgeterror(e,500)[1])
            raise Exception(s)        
            
    def create_temporary_copy(self,path):    
        f=os.path.join(tempfile._get_default_tempdir(),next(tempfile._get_candidate_names())+".inp")
        shutil.copyfile(path,f)
        return f
    
    def _open(self): 
        if(not self._enOpenStatus):
            self.Error(et.ENopen(self.inputfile,self.rptfile,self.binfile))
            et.cvar.TmpDir=tempfile._get_default_tempdir()
            print("Opening",file=sys.stderr)
        self._enOpenStatus=True
        
    def _close(self):
        if(self._enOpenStatus):
            self.Error(et.ENclose())
            print("Closing",file=sys.stderr)
            self._enOpenStatus=False    


    def _HOpen(self):
        if(not self._enHOpenStatus):
            self.Error(et.ENopenH())
        self._enHOpenStatus=True
        
    def _HClose(self):
        if(self._enOpenStatus):
            self.Error(et.ENcloseH())
        self._enHOpenStatus=False
        
    def clean(self):
        """Delete all the files created by epanet run""" 
        self._close()
        try:
            os.remove(self.rptfile)
        except:
            pass
        try:
            os.remove(self.hydraulicfile)
        except:
            pass
        try:
            os.remove(self.binfile)
        except:
            pass        

        #print("Hydraulic file name ******************* %s", et.cvar.HydFname)
            

        
    def _reset(self):
        self._close()
        self._open()


        
        
    def _getLinksAndNodes(self):
        self.links=Links()
        self.nodes=Nodes()        
        self._open()
        for i in range(1,et.ENgetcount(et.EN_NODECOUNT)[1]+1):
            node=Node(self)
            node.id=et.ENgetnodeid(i)[1]
            node.elevation=et.ENgetnodevalue(i,et.EN_ELEVATION )[1]
            self.nodes[i]=node
        for i in range(1,et.ENgetcount(et.EN_LINKCOUNT)[1]+1):
            link=Link(self)
            link.id=et.ENgetlinkid(i)[1]
            ret,a,b=et.ENgetlinknodes(i)
            link.start=self.nodes[a]
            link.end=self.nodes[b]
            self.nodes[a].links.append(link)
            self.nodes[b].links.append(link)
            self.links[i]=link
    

    
    def __getattribute__(self, name):
        try:
            return object.__getattribute__(self, name)
        except:
            pass

        self._open()
        if(hasattr(et,name)): # search legacy interface            
            return getattr(et,name)
        raise AttributeError("The attribute %s not found with this class or underlying c interface" % name)    
        

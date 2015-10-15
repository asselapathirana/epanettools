from . import epanet2 as et
import tempfile, shutil, os, sys
from pickle import dumps

"""" Never use ENOpen ENclose without keeping tab. -- always use _close and _open methods instead.
     Never use ENOpenH ENcloseH without keeping tab. -- always use _HClose and _HOpen methods instead."""

from . import tools

class Node(object):
    node_types={'JUNCTION':0,'RESERVOIR':1,"TANK":2}
    computed_values_start=9
    value_type={
    "EN_ELEVATION":       0,
    "EN_BASEDEMAND":      1,
    "EN_PATTERN":         2,
    "EN_EMITTER":         3,
    "EN_INITQUAL":        4,
    "EN_SOURCEQUAL":      5,
    "EN_SOURCEPAT":       6,
    "EN_SOURCETYPE":      7,
    "EN_TANKLEVEL":       8,
    "EN_DEMAND":          9,
    "EN_HEAD":            10,
    "EN_PRESSURE":        11,
    "EN_QUALITY":         12,
    "EN_SOURCEMASS":      13,
    "EN_INITVOLUME":      14,
    "EN_MIXMODEL":        15,
    "EN_MIXZONEVOL":      16,
    "EN_TANKDIAM":        17,
    "EN_MINVOLUME":       18,
    "EN_VOLCURVE":        19,
    "EN_MINLEVEL":        20,
    "EN_MAXLEVEL":        21,
    "EN_MIXFRACTION":     22,
    "EN_TANK_KBULK":      23,    }

        

    def __init__(self,es):
        self.es=es
        self.id=''
        self.values={}
        self.links=[]
        self.node_type=-1 #default value is illegal.
        self.results={}
    
class Link():
    link_types={"CVPIPE":0, "PIPE":1, "PUMP":2, "PRV":3, "PSV":4, "PBV":5, "FCV":6, "TCV":7, "GPV":8}
    computed_values_start=8
    value_type={
            "EN_DIAMETER":    0,
            "EN_LENGTH":      1,
            "EN_ROUGHNESS":   2,
            "EN_MINORLOSS":   3,
            "EN_INITSTATUS":  4,
            "EN_INITSETTING": 5,
            "EN_KBULK":       6,
            "EN_KWALL":       7,
            "EN_FLOW":        8,
            "EN_VELOCITY":    9,
            "EN_HEADLOSS":    10,
            "EN_STATUS":      11,
            "EN_SETTING":     12,
            "EN_ENERGY":      13,    }
    
    def __init__(self,es):
        self.es=es
        self.id=''
        self.start=None
        self.end=None
        self.link_type=-1 #default value is illegal.
        self.results={}        
    
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

class Network(object):
    pass

class EPANetSimulation(object):
    
    
    def __init__(self,inputFileName):
        self._enOpenStatus=False
        self._enHOpenStatus=False
        #
        
        self.OriginalInputFileName=inputFileName
        self.inputfile=self.create_temporary_copy(inputFileName)
        self.rptfile=self.inputfile[:-3]+"rpt"
        self.binfile=self.inputfile[:-3]+"bin"
        self.hydraulicfile=self.inputfile[:-3]+"hyd"
        self._open()
        self._getLinksAndNodes()
        self.reset_results()
        self._getInputData()
        self._close()
        

        
            
        
    
    def _sync(self):
        return True
        
        
    def sync(self):
        """ Syncs the changes variable values with underlying toolkit system."""
        self._sync()

    def run(self, save=True):
        self.reset_results()
        self._open()
        #get the input_data results
        self._getInputData()
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
            for  i,node in self.network.nodes.items():
                self.get_node_result_set(node,input_data=False)
                
            for  i,link in self.network.links.items():
                    self.get_link_result_set(link,input_data=False)
                
            ret,tstep=et.ENnextH()
            if (tstep<=0):
                break
        if(save):
            self.Error(et.ENsavehydfile(self.hydraulicfile))
        self._HClose()
        self._close()

      


    def get_node_result_set(self,node,input_data=False):
        for key,rt in Node.value_type.items():
            if ((not input_data) and (rt>=node.computed_values_start)) or \
               ((input_data) and (rt< node.computed_values_start)):
                r,v=et.ENgetnodevalue(node.index,rt)
                if (r>100):
                    v=float('NaN')
                node.results[rt].append(v)
            
            
    def get_link_result_set(self,link,input_data=False):
        for key,rt in Link.value_type.items():
            if ((not input_data) and (rt>=Link.computed_values_start)) or \
               ((input_data) and (rt< Link.computed_values_start)):
                r,v=et.ENgetlinkvalue(link.index,rt)
                if (r>100):
                    v=float('NaN')
                link.results[rt].append(v)    
            
     
    def reset_results(self):
        self.time=[]
        for i,n in self.network.nodes.items():
            for key,rt in Node.value_type.items():
                n.results[rt]=[]
        for i,n in self.network.links.items():
            for key,rt in Link.value_type.items():
                n.results[rt]=[]        
        
     
     
     
    def runq(self):
        self.reset_results()
        self._open()
        #get the input_data results
        self._getInputData()        
        self.Error(et.ENusehydfile(self.hydraulicfile))
        self.Error(et.ENopenQ()) 
        self.Error(et.ENinitQ(1))
        while(True):
            ret,t=et.ENrunQ()
            self.time.append(t)
            self.Error(ret)
            for i,node in self.network.nodes.items():
                self.get_node_result_set(node,input_data=False)
            for  i,link in self.network.links.items():
                    self.get_link_result_set(link,input_data=False)             
            ret,tstep=et.ENnextQ()
            self.Error(ret)
            if(tstep<=0):
                break
        et.ENcloseQ();         
        self._close()
    
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
            #print("Opening",file=sys.stderr)
        self._enOpenStatus=True
        
    def _close(self):
        if(self._enOpenStatus):
            self.Error(et.ENclose())
            #print("Closing",file=sys.stderr)
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
            

        
    def _reset(self):
        self._close()
        self._open()


    def _getInputData(self):
        for  i,node in self.network.nodes.items():
            self.get_node_result_set(node,input_data=True)          
        for  i,link in self.network.links.items():
                self.get_link_result_set(link,input_data=True)  
                
        
    def _getLinksAndNodes(self):
        self.network=Network()
        self.network.links=Links()
        self.network.nodes=Nodes()
     
        self._open()
        for i in range(1,et.ENgetcount(et.EN_NODECOUNT)[1]+1):
            node=Node(self)
            node.id=et.ENgetnodeid(i)[1]
            r,t=et.ENgetnodetype(i)
            self.Error(r)
            node.node_type=t

            self.network.nodes[i]=node
        for i in range(1,et.ENgetcount(et.EN_LINKCOUNT)[1]+1):
            link=Link(self)
            link.id=et.ENgetlinkid(i)[1]
            ret,a,b=et.ENgetlinknodes(i)
            link.start=self.network.nodes[a]
            link.end=self.network.nodes[b]
            r,t=et.ENgetlinktype(i)
            self.Error(r)
            link.link_type=t   
        
            self.network.nodes[a].links.append(link)
            self.network.nodes[b].links.append(link)
            self.network.links[i]=link
    

    
    def __getattribute__(self, name):
        try:
            return object.__getattribute__(self, name)
        except:
            pass

        self._open()
        if(hasattr(et,name)): # search legacy interface            
            return getattr(et,name)
        raise AttributeError("The attribute %s not found with this class or underlying c interface" % name)    
        

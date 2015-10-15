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
        self.links=[]
        self.results={}
        
        
    def get_node_result_set(self,input_data=False):
        for key,rt in Node.value_type.items():
            if ((not input_data) and (rt>=Node.computed_values_start)) or \
               ((input_data) and (rt< Node.computed_values_start)):
                r,v=et.ENgetnodevalue(self.index,rt)
                if (r>100):
                    v=float('NaN')
                self.results[rt].append(v)
            
            

class Link(object):
    CLOSED=0
    OPENED=1
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
        self.results={}
        
        

    
    def get_link_result_set(self,input_data=False):
        for key,rt in Link.value_type.items():
            if ((not input_data) and (rt>=Link.computed_values_start)) or \
               ((input_data) and (rt< Link.computed_values_start)):
                r,v=et.ENgetlinkvalue(self.index,rt)
                if (r>100):
                    v=float('NaN')
                self.results[rt].append(v)       

class Pattern(tools.TransformedDict):
    
    def __init__(self,es):
        super(Pattern,self).__init__()
        self.es=es
    
class Control(object):
    
    control_types={'LOW_LEVEL_CONTROL':0, 'HIGH_LEVEL_CONTROL':1, 'TIMER_CONTROL':2, 'TIME_OF_DAY_CONTROL':3}

 
    def __init__(self,es):
        self.es=es
    
    
    
class index_id_type(tools.TransformedDict):
    
    def __setitem__(self, key, value):
        v=self.__keytransform__(key)
        self.store[v] = value
        self.store[v].index=v # the index of the entity is also saved as attribute in the item. 
        
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

class Patterns(index_id_type):
    pass

class Controls(index_id_type):
    pass

class Network(object):
    WaterQualityAnalysisTypes = {
    "EN_NONE":         0,
    "EN_CHEM":         1,
    "EN_AGE":          2,
    "EN_TRACE":        3,
    }
    EN_TRIALS =     0
    EN_ACCURACY =   1
    EN_TOLERANCE =  2
    EN_EMITEXPON =  3
    EN_DEMANDMULT = 4

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
        self._getNetworkData()
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
                node.get_node_result_set(input_data=False)
                
            for  i,link in self.network.links.items():
                link.get_link_result_set(input_data=False)
                
            ret,tstep=et.ENnextH()
            if (tstep<=0):
                break
        if(save):
            self.Error(et.ENsavehydfile(self.hydraulicfile))
        self._HClose()
        self._close()

      


 
            
     
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
                node.get_node_result_set(input_data=False)
            for  i,link in self.network.links.items():
                link.get_link_result_set(input_data=False)             
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
            node.get_node_result_set(input_data=True)          
        for  i,link in self.network.links.items():
                link.get_link_result_set(input_data=True)  
                
        
    def _getNetworkData(self):
        self.network=Network()
        self.network.links=Links()
        self.network.nodes=Nodes()
        self.network.patterns=Patterns()
        self.network.controls=Controls()

     
        self._open()
        for i in range(1,et.ENgetcount(et.EN_NODECOUNT)[1]+1):
            node=Node(self)
            k=et.ENgetnodeid(i)
            self.Error(k[0])
            node.id=k[1]
            r,t=et.ENgetnodetype(i)
            self.Error(r)
            node.node_type=t
            self.network.nodes[i]=node

        for i in range(1,et.ENgetcount(et.EN_LINKCOUNT)[1]+1):
            link=Link(self)
            k=et.ENgetlinkid(i)
            self.Error(k[0])
            link.id=k[1]
            ret,a,b=et.ENgetlinknodes(i)
            link.start=self.network.nodes[a]
            link.end=self.network.nodes[b]
            r,t=et.ENgetlinktype(i)
            self.Error(r)
            link.link_type=t   
        
            self.network.nodes[a].links.append(link)
            self.network.nodes[b].links.append(link)
            self.network.links[i]=link
            
        for i in range(1,et.ENgetcount(et.EN_PATCOUNT)[1]+1):
            pattern=Pattern(self)
            k=et.ENgetpatternid(i)
            self.Error(k[0])
            pattern.id=k[1]
            for j in range(1,et.ENgetpatternlen(i)[1]+1):
                pattern.store[j]=et.ENgetpatternvalue(i,j)[1]
                
            self.network.patterns[i]=pattern
    
        for i in range(1,et.ENgetcount(et.EN_CONTROLCOUNT)[1]+1):
                    c=Control(self)
                    k=et.ENgetcontrol(i)
                    self.Error(k[0])
                    c.ctype=k[1]
                    if(c.ctype>1): # no node is involved. for types 2 and 3!  
                        c.node=None
                    else:
                        c.node=self.network.nodes[k[4]]
                    c.level=k[5]
                    c.link=self.network.links[k[2]]
                    c.setting=k[3]
                    self.network.controls[i]=c
                    
        k=et.ENgetqualtype()
        self.Error(k[0])
        self.network.WaterQualityAnalysisType=k[1]
        if(k[2]==0):
            t=None
        else:
            t=self.network.nodes[k[2]]
        self.network.WaterQualityTraceNode=t        
   
        k=et.ENgetoption(Network.EN_ACCURACY)
        self.Error(k[0])
        self.network.en_accuracy=k[1]
        
        k=et.ENgetoption(Network.EN_DEMANDMULT)
        self.Error(k[0])
        self.network.en_demandmult=k[1]
        
        k=et.ENgetoption(Network.EN_EMITEXPON)
        self.Error(k[0])
        self.network.en_emitexpon=k[1]
        
        k=et.ENgetoption(Network.EN_TOLERANCE)
        self.Error(k[0])
        self.network.en_tolerance=k[1]  
        
        k=et.ENgetoption(Network.EN_TRIALS)
        self.Error(k[0])
        self.network.en_trials=k[1]        
    
    def __getattribute__(self, name):
        try:
            return object.__getattribute__(self, name)
        except:
            pass

        self._open()
        if(hasattr(et,name)): # search legacy interface            
            return getattr(et,name)
        raise AttributeError("The attribute %s not found with this class or underlying c interface" % name)    
        

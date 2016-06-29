from __future__ import print_function
from . import epanet2 as et
import tempfile, shutil, os, sys
from pickle import dumps

"""" Never use ENOpen ENclose without keeping tab. -- always use _close and _open methods instead.
     Never use ENOpenH ENcloseH without keeping tab. -- always use _HClose and _HOpen methods instead."""

from . import tools


def Error(e):
    if(e):
        s="Epanet Error: %d : %s" %(e,et.ENgeterror(e,500)[1])
        raise Exception(s) 
    
def check_and_return(result_list,silent=False):
    r=list(result_list)
    if(not silent):
        Error(r[0])
        
    if(r[0]>0):
        return float('nan')
    else:
        if(len(r)==2):
            return r[1]
        else:
            return r[1:]
    

class Node(object):
    node_types={'JUNCTION':0,'RESERVOIR':1,"TANK":2}
    input_values=  [0,1,2,3,4,5,6,7,8,14,15,16,17,18,19,20,21,22,23] # these are also the values that can be retrieved before running. 
    settable_values=[i for i in input_values if i not in [14,16,19]] # ENsetnodevalues works only with these. 
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

        

    def __init__(self,network,index=False):
        self.network=network
        self.links=[]
        self.results={}
        #get the inverse of value_type
        self.vti={b:a for a,b in self.value_type.items()} 
        if(index):
            self.readValues(index)
        
        
    def readValues(self,index):
        self.index=index 
        self.id=check_and_return(et.ENgetnodeid(index))
        self.node_type=check_and_return(et.ENgetnodetype(index)) 
        
    def get_node_result_set(self,input_data=False):
        
        for key,rt in Node.value_type.items():
            if ((not input_data) and (not rt in Node.input_values)) or \
               ((input_data) and (rt in Node.input_values)):
                self.results[rt].append(check_and_return(et.ENgetnodevalue(self.index,rt),silent=True))
                                                         
    def sync(self):
        for key,rt in Node.value_type.items():
            if (rt in Node.settable_values):
                et.ENsetnodevalue(self.index,rt,self.results[0][0])               
                
            
            

class Link(object):
    CLOSED=0
    OPENED=1
    link_types={"CVPIPE":0, "PIPE":1, "PUMP":2, "PRV":3, "PSV":4, "PBV":5, "FCV":6, "TCV":7, "GPV":8}
    settable_values=[0,1,2,3,4,5,6,7,11,12] # these are also the values that can be retrieved before running.
    input_values  =settable_values #use these for ENlsetlinkvalue()
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
    
    def __init__(self,network,index=False):
        self.network=network
        self.results={}
        if(index):
            self.readValues(index)
            
            
    def readValues(self,index):
        self.index=index 
        self.id=check_and_return(et.ENgetlinkid(index))
        self.link_type=check_and_return(et.ENgetlinktype(index)) 
        a,b=check_and_return(et.ENgetlinknodes(index))
        
        try:
            self.start=self.network.nodes[a]
            self.end=self.network.nodes[b]
            self.link_type=check_and_return(et.ENgetlinktype(index))
        
            self.network.nodes[a].links.append(self)
            self.network.nodes[b].links.append(self)
        except Exception as e:
            print("No Nodes present! Check if nodes have been read.",file=sys.stderr)
            raise(e)
        
    
    def get_link_result_set(self,input_data=False):
        for key,rt in Link.value_type.items():
            if ((not input_data) and (not rt in Link.input_values)) or \
               ((input_data) and (rt in  Link.input_values)):
                self.results[rt].append(check_and_return(et.ENgetlinkvalue(self.index,rt), silent=True))

    def sync(self):
        for key,rt in Link.value_type.items():
            if (rt in Link.settable_values):
                et.ENsetlinkvalue(self.index,rt,self.results[0][0])    

class Pattern(tools.TransformedDict):
    
    def __init__(self,es, index=False):
        super(Pattern,self).__init__()
        self.es=es
        if(index):
            self.readValues(index)
    
    def readValues(self,index):
        self.index=index
        self.id=check_and_return(et.ENgetpatternid(index))
        for j in range(1,check_and_return(et.ENgetpatternlen(index))+1):
            self[j]=et.ENgetpatternvalue(index,j)[1]        
        
    def sync(self):
        """"Pattrn syncing not implemented"""
        pass
    
    
class Control(object):
    
    control_types={'LOW_LEVEL_CONTROL':0, 'HIGH_LEVEL_CONTROL':1, 'TIMER_CONTROL':2, 'TIME_OF_DAY_CONTROL':3}

    def __init__(self,network, index=False):
        self.network=network
        if(index):
            self.readValues(index)
    
    def readValues(self,index):
        k=check_and_return(et.ENgetcontrol(index))
        self.ctype=k[0]
        if(self.ctype>1): # no node is involved. for types 2 and 3!  
            self.node=None
        else:
            self.node=self.network.nodes[k[3]]
        self.level=k[4]
        self.link=self.network.links[k[1]]
        self.setting=k[2]        
        
    def sync(self):
        """Not implemented yet."""
        pass
    
    
    
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
    
    def sync(self):
        for i,item in self.items():
            item.sync()        
    
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
    
    def __init__(self,es,readData=True):
        self.links=Links()
        self.nodes=Nodes()
        self.patterns=Patterns()
        self.controls=Controls() 
        self.es=es
        if(readData):
            self.read_data()
            
            
    def read_data(self):
        for i in range(1,et.ENgetcount(et.EN_NODECOUNT)[1]+1):
            self.nodes[i]=Node(self,index=i) 
            
        for i in range(1,et.ENgetcount(et.EN_LINKCOUNT)[1]+1):
            self.links[i]=Link(self,index=i)
            
        for i in range(1,et.ENgetcount(et.EN_PATCOUNT)[1]+1):
            self.patterns[i]=Pattern(self,index=i)
    
        for i in range(1,et.ENgetcount(et.EN_CONTROLCOUNT)[1]+1):
            self.controls[i]=Control(self,index=i)
                    
        self.getValues()        
        
    def reset_results(self):
        self.time=[]
        self.tsteps=[]
        for i,n in self.nodes.items():
            for key,rt in Node.value_type.items():
                n.results[rt]=[]
        for i,n in self.links.items():
            for key,rt in Link.value_type.items():
                n.results[rt]=[]      
    
    def _sync(self):
        """"Syncs the anything other than nodes, links, patterns, conrols"""
        pass
    
    def sync(self):
        self.nodes.sync()
        self.links.sync()
        self.patterns.sync()
        self.controls.sync()
        self._sync()
        
        
    def getValues(self):
        self.WaterQualityAnalysisType,k=check_and_return(et.ENgetqualtype())
        if(k==0):
            self.WaterQualityTraceNode=None
        else:
            self.WaterQualityTraceNode=self.nodes[k]
   
        self.en_accuracy=check_and_return(et.ENgetoption(Network.EN_ACCURACY))
        self.en_demandmult=check_and_return(et.ENgetoption(Network.EN_DEMANDMULT))
        self.en_emitexpon=check_and_return(et.ENgetoption(Network.EN_EMITEXPON))
        self.en_tolerance=check_and_return(et.ENgetoption(Network.EN_TOLERANCE))  
        self.en_trials=check_and_return(et.ENgetoption(Network.EN_TRIALS))        
    

class EPANetSimulation(object):
    
    
    def __init__(self,inputFileName):
        self._enOpenStatus=False
        self._enHOpenStatus=False
        self.OriginalInputFileName=inputFileName
        self.inputfile=self.create_temporary_copy(inputFileName)
        self.rptfile=self.inputfile[:-3]+"rpt"
        self.binfile=self.inputfile[:-3]+"bin"
        self.hydraulicfile=self.inputfile[:-3]+"hyd"
        self._open()
        self._getNetworkData()
        self.network.reset_results()
        self._getInputData()
        self._close()
      


    def _legacy_get(self,entitytype, index, param=-1):
        """Legacy interface 'get' ONLY FOR TESTING. 
        param : result type for LINK and NODE. timeperiod for PATTERN. For option it is not used
        """ 
        self._open()
        if (entitytype=="LINK"):
            return check_and_return(et.ENgetlinkvalue(index,param))
        if (entitytype=="NODE"):
            return check_and_return(et.ENgetnodevalue(index,param))
        if (entitytype=="PATTERN"):
            return check_and_return(et.ENgetpatternvalue(index,param))
        if (entitytype=="LINK"):
            return check_and_return(et.ENgetoption(index,param))
        raise (Exception,"UNKNOWN type")
        
        
    def sync(self):
        """ Syncs the changes variable values with underlying toolkit system."""
        self.network.sync()

    def run(self, save=True):
        self.network.reset_results()
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
            self.network.time.append(t)
            # Retrieve hydraulic results for time t
            for  i,node in self.network.nodes.items():
                node.get_node_result_set(input_data=False)
                
            for  i,link in self.network.links.items():
                link.get_link_result_set(input_data=False)
                
            ret,tstep=et.ENnextH()
            self.network.tsteps.append(tstep)
            
            if (tstep<=0):
                break
        if(save):
            Error(et.ENsavehydfile(self.hydraulicfile))
        self._HClose()
        self._close()
     
    def runq(self):
        self.network.reset_results()
        self._open()
        #get the input_data results
        self._getInputData()        
        Error(et.ENusehydfile(self.hydraulicfile))
        Error(et.ENopenQ()) 
        Error(et.ENinitQ(1))
        while(True):
            ret,t=et.ENrunQ()
            self.network.time.append(t)
            Error(ret)
            for i,node in self.network.nodes.items():
                node.get_node_result_set(input_data=False)
            for  i,link in self.network.links.items():
                link.get_link_result_set(input_data=False)             
            self.network.tsteps.append(check_and_return(et.ENnextQ()))
            if(self.network.tsteps[-1]==0):
                break
        et.ENcloseQ();         
        self._close()
    
       
            
    def create_temporary_copy(self,path):    
        f=os.path.join(tempfile._get_default_tempdir(),next(tempfile._get_candidate_names())+".inp")
        shutil.copyfile(path,f)
        return f
    
    def _open(self): 
        if(not self._enOpenStatus):
            Error(et.ENopen(self.inputfile,self.rptfile,self.binfile))
            et.cvar.TmpDir=tempfile._get_default_tempdir()
        self._enOpenStatus=True
        
    def _close(self):
        if(self._enOpenStatus):
            Error(et.ENclose())
            #print("Closing",file=sys.stderr)
            self._enOpenStatus=False    


    def _HOpen(self):
        if(not self._enHOpenStatus):
            Error(et.ENopenH())
        self._enHOpenStatus=True
        
    def _HClose(self):
        if(self._enOpenStatus):
            Error(et.ENcloseH())
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
        self._open()
        self.network=Network(self,readData=True)
        
        
    
    def __getattribute__(self, name):
        try:
            return object.__getattribute__(self, name)
        except:
            pass

        self._open()
        if(hasattr(et,name)): # search legacy interface            
            return getattr(et,name)
        raise AttributeError("The attribute %s not found with this class or underlying c interface" % name)    
        

from . import pdd as pd
class pdd_wrapper_class(object):
    
    def __init__(self,pdd=False):
        self.pd=pd
        self.set_pdd(pdd)
    
    def set_pdd(self,pdd=False):
        self.pdd=pdd
        
    def __getattribute__(self, name):
        try:
            return object.__getattribute__(self, name)
        except:
            pass
        
        if(name[-5:]=="_wrap"): # then the name already has wrap
            f=name
        else:
            if(self.pdd):
                f=name+"_wrap" 
            else:
                f=name
        if(hasattr(self.pd,name)): #
            #print ("Name:"+name+" f="+f)
            return getattr(self.pd,name)
        raise AttributeError("The attribute %s not found with this class or underlying c interface" % name) 
            
    
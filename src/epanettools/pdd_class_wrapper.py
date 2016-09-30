from . import pdd as pd


class pdd_wrapper_class(object):

    def __init__(self, pdd=False):
        self.pdd = pdd  # THIS MUST BE the first statement.
        self.pd = pd

    def __getattribute__(self, name):
        try:
            return object.__getattribute__(self, name)
        except:
            pass

        if(name[-5:] == "_wrap"):  # then the name already has wrap
            f = name
        else:
            if(self.pdd and name[:2] == "EN" and str.upper(name) != name and name[2] != '_'):
                f = name + "_wrap"
            else:
                f = name
        if(hasattr(self.pd, name)):
            # print ("Name:"+name+" f="+f)
            return getattr(self.pd, f)
        raise AttributeError(
            "The attribute %s not found with this class or underlying c interface" %
            name)

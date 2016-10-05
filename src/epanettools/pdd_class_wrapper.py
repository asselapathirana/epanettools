from . import pdd as pd


def Error(e):
    if(e):
        s = "Epanet Error: %d : %s" % (
            e, pdd_wrapper_class.ENgeterror(e, 500)[1])
        raise Exception(s)


class pdd_wrapper_class(object):

    def ENsetpattern(self, patternindex, pattern):
        """Replacement function for original ENsetpattern
        function in epanet toolkit. Avoids the need to have either
        (a) passing pointers from python to c or (b) having to importa
        and use numpy. """

        if(type(patternindex) == str):
            ret, patternindex = self.pd.ENgetpatternindex(patternindex)
            Error(ret)
        Error(self.pd.ENsetpatterndim(patternindex, len(pattern)))
        for i in range(1, len(pattern) + 1):
            Error(self.pd.ENsetpatternvalue(patternindex, i, pattern[i - 1]))
        return 0

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

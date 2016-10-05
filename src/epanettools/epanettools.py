from __future__ import print_function

import os
import shutil
import sys
import tempfile

from . import tools
from .pdd_class_wrapper import pdd_wrapper_class

"""" Never use ENOpen ENclose without keeping tab. -- always use _close and _open methods instead.
     Never use ENOpenH ENcloseH without keeping tab. -- always use _HClose and _HOpen methods instead."""


RIDICULOUS_VALUE = -999999999


def Error(e):
    if(e):
        s = "Epanet Error: %d : %s" % (
            e, pdd_wrapper_class.ENgeterror(e, 500)[1])
        raise Exception(s)


def check_and_return(result_list, silent=False):
    r = list(result_list)
    if(not silent):
        Error(r[0])

    if(r[0] > 0):
        return RIDICULOUS_VALUE
    else:
        if(len(r) == 2):
            return r[1]
        else:
            return r[1:]


class Node(object):
    node_types = {'JUNCTION': 0, 'RESERVOIR': 1, "TANK": 2}
    input_values = [0, 1, 2, 3, 4, 5, 6, 7,
                    8, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
    # these are also the values that can be retrieved before running.
    settable_values = [
        i for i in input_values if i not in [
            14,
            16,
            19]]  # ENsetnodevalues works only with these.
    value_type = {
        "EN_ELEVATION": 0,
        "EN_BASEDEMAND": 1,
        "EN_PATTERN": 2,
        "EN_EMITTER": 3,
        "EN_INITQUAL": 4,
        "EN_SOURCEQUAL": 5,
        "EN_SOURCEPAT": 6,
        "EN_SOURCETYPE": 7,
        "EN_TANKLEVEL": 8,
        "EN_DEMAND": 9,
        "EN_HEAD": 10,
        "EN_PRESSURE": 11,
        "EN_QUALITY": 12,
        "EN_SOURCEMASS": 13,
        "EN_INITVOLUME": 14,
        "EN_MIXMODEL": 15,
        "EN_MIXZONEVOL": 16,
        "EN_TANKDIAM": 17,
        "EN_MINVOLUME": 18,
        "EN_VOLCURVE": 19,
        "EN_MINLEVEL": 20,
        "EN_MAXLEVEL": 21,
        "EN_MIXFRACTION": 22,
        "EN_TANK_KBULK": 23, }

    def __init__(self, network, index=False):
        self.network = network
        self.pd = self.network.es.pd
        self.links = []
        self.results = {}
        self.results_original = {}
        # get the inverse of value_type
        self.vti = {b: a for a, b in self.value_type.items()}
        if(index):
            self.readValues(index)

    def readValues(self, index):
        self.index = index
        self.id = check_and_return(self.pd.ENgetnodeid(index))
        self.node_type = check_and_return(self.pd.ENgetnodetype(index))

    def get_node_result_set(self, input_data=False):

        for key, rt in Node.value_type.items():
            if ((not input_data) and (rt not in Node.input_values)) or \
               ((input_data) and (rt in Node.input_values)):
                k = check_and_return(
                    self.pd.ENgetnodevalue(self.index, rt), silent=True)
                self.results[rt].append(k)
                self.results_original[rt].append(k)

#     def sync(self):
#         for key,rt in Node.value_type.items():
#
#             if (rt in Node.settable_values):
#                 if(self.results[rt][0]==self.results_original[rt][0]):
#                     continue
#                 if(self.results[rt][0]!=RIDICULOUS_VALUE):
#                     self.pd.ENsetnodevalue(self.index,rt,self.results[rt][0])


class Link(object):
    CLOSED = 0
    OPENED = 1
    link_types = {
        "CVPIPE": 0,
        "PIPE": 1,
        "PUMP": 2,
        "PRV": 3,
        "PSV": 4,
        "PBV": 5,
        "FCV": 6,
        "TCV": 7,
        "GPV": 8}
    settable_values = [0, 1, 2, 3, 4, 5, 6, 7, 11, 12]
    # these are also the values that can be retrieved before running.
    input_values = settable_values  # use these for ENlsetlinkvalue()
    value_type = {
        "EN_DIAMETER": 0,
        "EN_LENGTH": 1,
        "EN_ROUGHNESS": 2,
        "EN_MINORLOSS": 3,
        "EN_INITSTATUS": 4,
        "EN_INITSETTING": 5,
        "EN_KBULK": 6,
        "EN_KWALL": 7,
        "EN_FLOW": 8,
        "EN_VELOCITY": 9,
        "EN_HEADLOSS": 10,
        "EN_STATUS": 11,
        "EN_SETTING": 12,
        "EN_ENERGY": 13, }

    def __init__(self, network, index=False):
        self.network = network
        self.pd = self.network.es.pd
        self.results = {}
        self.results_original = {}
        if(index):
            self.readValues(index)

    def readValues(self, index):
        self.index = index
        self.id = check_and_return(self.pd.ENgetlinkid(index))
        self.link_type = check_and_return(self.pd.ENgetlinktype(index))
        a, b = check_and_return(self.pd.ENgetlinknodes(index))

        try:
            self.start = self.network.nodes[a]
            self.end = self.network.nodes[b]
            self.link_type = check_and_return(self.pd.ENgetlinktype(index))

            self.network.nodes[a].links.append(self)
            self.network.nodes[b].links.append(self)
        except Exception as e:
            print(
                "No Nodes present! Check if nodes have been read.", file=sys.stderr)
            raise(e)

    def get_link_result_set(self, input_data=False):
        for key, rt in Link.value_type.items():
            if ((not input_data) and (rt not in Link.input_values)) or \
               ((input_data) and (rt in Link.input_values)):
                k = check_and_return(
                    self.pd.ENgetlinkvalue(self.index, rt), silent=True)
                self.results[rt].append(k)
                self.results_original[rt].append(k)

# def sync(self):
# for key,rt in Link.value_type.items():
# if (rt in Link.settable_values):
# if(self.results[rt][0]==self.results_original[rt][0]):
# continue
# if(self.results[rt][0]!=RIDICULOUS_VALUE):self.pd.ENsetlinkvalue(self.index,rt,self.results[rt][0])


class Pattern(tools.TransformedDict):

    def __init__(self, es, index=False):
        super(Pattern, self).__init__()
        self.es = es
        self.pd = self.es.pd
        if(index):
            self.readValues(index)

    def readValues(self, index):
        self.index = index
        self.id = check_and_return(self.pd.ENgetpatternid(index))
        for j in range(1, check_and_return(self.pd.ENgetpatternlen(index)) + 1):
            self[j] = self.pd.ENgetpatternvalue(index, j)[1]

# def sync(self):
# """"Pattrn syncing not implemented"""
# pass


class Control(object):

    control_types = {
        'LOW_LEVEL_CONTROL': 0,
        'HIGH_LEVEL_CONTROL': 1,
        'TIMER_CONTROL': 2,
        'TIME_OF_DAY_CONTROL': 3}

    def __init__(self, network, index=False):
        self.network = network
        self.pd = self.network.es.pd
        if(index):
            self.readValues(index)

    def readValues(self, index):
        k = check_and_return(self.pd.ENgetcontrol(index))
        self.ctype = k[0]
        if(self.ctype > 1):  # no node is involved. for types 2 and 3!
            self.node = None
        else:
            self.node = self.network.nodes[k[3]]
        self.level = k[4]
        self.link = self.network.links[k[1]]
        self.setting = k[2]

# def sync(self):
# """Not implemented yet."""
# pass


class index_id_type(tools.TransformedDict):

    def __setitem__(self, key, value):
        v = self.__keytransform__(key)
        self.store[v] = value
        self.store[
            v].index = v  # the index of the entity is also saved as attribute in the item.

    def __keytransform__(self, key):
        if isinstance(key, str):
            for i, j in self.store.items():
                if (key == j.id):
                    return i
            raise KeyError("Key %s not found" % key)
        return key

# def sync(self):
# for i,item in self.items():
# item.sync()


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
        "EN_NONE": 0,
        "EN_CHEM": 1,
        "EN_AGE": 2,
        "EN_TRACE": 3,
    }
    EN_TRIALS = 0
    EN_ACCURACY = 1
    EN_TOLERANCE = 2
    EN_EMITEXPON = 3
    EN_DEMANDMULT = 4

    def __init__(self, es, readData=True):
        self.links = Links()
        self.nodes = Nodes()
        self.patterns = Patterns()
        self.controls = Controls()
        self.es = es
        self.pd = es.pd
        if(readData):
            self.read_data()

    def read_data(self):
        for i in range(1, self.pd.ENgetcount(self.pd.EN_NODECOUNT)[1] + 1):
            self.nodes[i] = Node(self, index=i)

        for i in range(1, self.pd.ENgetcount(self.pd.EN_LINKCOUNT)[1] + 1):
            self.links[i] = Link(self, index=i)

        for i in range(1, self.pd.ENgetcount(self.pd.EN_PATCOUNT)[1] + 1):
            self.patterns[i] = Pattern(self, index=i)

        for i in range(1, self.pd.ENgetcount(self.pd.EN_CONTROLCOUNT)[1] + 1):
            self.controls[i] = Control(self, index=i)

        self.getValues()

    def reset_results(self):
        self.time = []
        self.tsteps = []
        for i, n in self.nodes.items():
            for key, rt in Node.value_type.items():
                n.results[rt] = []
                n.results_original[rt] = []
        for i, n in self.links.items():
            for key, rt in Link.value_type.items():
                n.results[rt] = []
                n.results_original[rt] = []

# def _sync(self):
# """"Syncs anything other than nodes, links, patterns, conrols"""
# pass
#
# def sync(self):
# self.nodes.sync()
# self.links.sync()
# self.patterns.sync()
# self.controls.sync()
# self._sync()

    def getValues(self):
        self.WaterQualityAnalysisType, k = check_and_return(
            self.pd.ENgetqualtype())
        if(k == 0):
            self.WaterQualityTraceNode = None
        else:
            self.WaterQualityTraceNode = self.nodes[k]

        self.en_accuracy = check_and_return(
            self.pd.ENgetoption(Network.EN_ACCURACY))
        self.en_demandmult = check_and_return(
            self.pd.ENgetoption(Network.EN_DEMANDMULT))
        self.en_emitexpon = check_and_return(
            self.pd.ENgetoption(Network.EN_EMITEXPON))
        self.en_tolerance = check_and_return(
            self.pd.ENgetoption(Network.EN_TOLERANCE))
        self.en_trials = check_and_return(
            self.pd.ENgetoption(Network.EN_TRIALS))


class EPANetSimulation(object):

    def __init__(self, inputFileName, pdd=False):
        self.initialize(inputFileName, pdd)

    def initialize(self, inputFileName=None, pdd=False):
        self.pd = pdd_wrapper_class(pdd)
        # print("Warning: no pdd")
        self._enOpenStatus = False
        self._enHOpenStatus = False
        if(inputFileName):
            self.OriginalInputFileName = inputFileName
        self.inputfile = self.create_temporary_copy(self.OriginalInputFileName)
        self.rptfile = self.inputfile[:-3] + "rpt"
        self.binfile = self.inputfile[:-3] + "bin"
        self.hydraulicfile = self.inputfile[:-3] + "hyd"
        self._open()
        self._getNetworkData()
        self.network.reset_results()
        self._getInputData()
        self._close()

    def _legacy_get(self, entitytype, index, param=-1):
        """Legacy interface 'get' ONLY FOR TESTING.
        param : result type for LINK and NODE. timeperiod for PATTERN. For option it is not used
        """
        self._open()
        if (entitytype == "LINK"):
            return check_and_return(self.pd.ENgetlinkvalue(index, param))
        if (entitytype == "NODE"):
            return check_and_return(self.pd.ENgetnodevalue(index, param))
        if (entitytype == "PATTERN"):
            return check_and_return(self.pd.ENgetpatternvalue(index, param))
        if (entitytype == "LINK"):
            return check_and_return(self.pd.ENgetoption(index, param))
        raise Exception

# def sync(self, i_know_what_i_am_doing=False):
# """ Syncs the changes variable values with underlying toolkit system."""
# if (not i_know_what_i_am_doing):
# raise Exception("Don't use sync. It is not yet properly implemented.")
# self.network.sync()
# now replace the original input file with this data.
# Error(self.pd.ENsaveinpfile(self.inputfile))
# self.initialize(self.inputfile)

    def run(self, save=True, pdd=True):
        self.network.reset_results()
        self._open()
        # get the input_data results
        self._getInputData()
        self._HOpen()
        if (save):
            init = 1
        else:
            init = 0
        self.pd.ENinitH(init)
        while True:
            ret, t = self.pd.ENrunH()
            self.network.time.append(t)
            # Retrieve hydraulic results for time t
            for i, node in self.network.nodes.items():
                node.get_node_result_set(input_data=False)

            for i, link in self.network.links.items():
                link.get_link_result_set(input_data=False)

            ret, tstep = self.pd.ENnextH()
            self.network.tsteps.append(tstep)

            if (tstep <= 0):
                break
        if(save):
            Error(self.pd.ENsavehydfile(self.hydraulicfile))
        self._HClose()
        self._close()

    def runq(self):
        self.network.reset_results()
        self._open()
        # get the input_data results
        self._getInputData()
        Error(self.pd.ENusehydfile(self.hydraulicfile))
        Error(self.pd.ENopenQ())
        Error(self.pd.ENinitQ(1))
        while(True):
            ret, t = self.pd.ENrunQ()
            self.network.time.append(t)
            Error(ret)
            for i, node in self.network.nodes.items():
                node.get_node_result_set(input_data=False)
            for i, link in self.network.links.items():
                link.get_link_result_set(input_data=False)
            self.network.tsteps.append(check_and_return(self.pd.ENnextQ()))
            if(self.network.tsteps[-1] == 0):
                break
        self.pd.ENcloseQ()
        self._close()

    def create_temporary_copy(self, path):
        f = os.path.join(
            tempfile._get_default_tempdir(),
            next(tempfile._get_candidate_names()) + ".inp")
        shutil.copyfile(path, f)
        return f

    def _open(self):
        if(not self._enOpenStatus):
            Error(self.pd.ENopen(self.inputfile, self.rptfile, self.binfile))
            self.pd.cvar.TmpDir = tempfile._get_default_tempdir()
        self._enOpenStatus = True

    def _close(self):
        if(self._enOpenStatus):
            # Bug! the ENclose cause core dumps on posix  -- No, on windows as
            # well!
            if(False):  # os.name!="posix"):
                Error(self.pd.ENclose())
            # print("Closing",file=sys.stderr)
            self._enOpenStatus = False

    def _HOpen(self):
        if(not self._enHOpenStatus):
            Error(self.pd.ENopenH())
        self._enHOpenStatus = True

    def _HClose(self):
        if(self._enOpenStatus):
            Error(self.pd.ENcloseH())
        self._enHOpenStatus = False

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
        for i, node in self.network.nodes.items():
            node.get_node_result_set(input_data=True)
        for i, link in self.network.links.items():
            link.get_link_result_set(input_data=True)

    def _getNetworkData(self):
        self._open()
        self.network = Network(self, readData=True)

    def __getattribute__(self, name):

        try:
            return object.__getattribute__(self, name)
        except:
            pass

        self._open()
        # if(hasattr(et,name)): # search legacy interface
        #     return getattr(et,name)
        if(hasattr(self.pd, name)):
            return getattr(self.pd, name)
        raise AttributeError(
            "The attribute %s not found with this class or underlying c interface" %
            name)

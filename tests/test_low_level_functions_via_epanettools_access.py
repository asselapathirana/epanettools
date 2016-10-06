import os
import sys
import unittest

from tests import tools_for_testing as tt

from epanettools.epanettools import EPANetSimulation
from epanettools.examples import simple


class Test1(unittest.TestCase):

    def Error(self, e):
        if(e):
            s = "Epanet Error: %d : %s" % (e, self.es.ENgeterror(e, 500)[1])
            raise Exception(s)

    def setUp(self):
        print("SETUP!")
        self.file = os.path.join(os.path.dirname(simple.__file__), 'Net3.inp')
        self.es = EPANetSimulation(self.file)

    def tearDown(self):
        # Bug! the ENclose cause core dumps on posix  -- No, on windows as well!
        if(False):  # os.name!="posix"):
            self.Error(self.es.ENclose())
        print("TEAR DOWN!")

    def test_alter_with_ENset_and_check_with_a_file(self):
        self.Error(self.es.ENsaveinpfile("1.inp"))
        self.Error(self.es.ENsetlinkvalue(81, 0, 9999))
        self.Error(self.es.ENsaveinpfile("2.inp"))
        self.assertEqual(tt.compareFiles("1.inp", "2.inp"), '16>1e+04; ')


tc = None


def clt(fn):
    tc.setUp()
    fn()
    tc.tearDown()


def main():
    tc = Test1()
    for a in dir(tc):
        if (a.startswith('test_pattern')):  # test_sync
            b = getattr(tc, a)
            if(hasattr(b, '__call__')):
                print ("calling %s **********************************" % a)
                clt(b)


if __name__ == "__main__":
    main()

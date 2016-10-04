import os
import sys
import unittest

from tests import tools_for_testing as tt

from epanettools import epanet2 as et
from epanettools import pdd as pd
from epanettools.examples import simple


class Test1(unittest.TestCase):

    def Error(self, e):
        if(e):
            s = "Epanet Error: %d : %s" % (e, et.ENgeterror(e, 500)[1])
            raise Exception(s)

    def setUp(self):
        print("SETUP!")
        self.file = os.path.join(os.path.dirname(simple.__file__), 'Net3.inp')
        self.Error(et.ENopen(self.file, "t.rpt", ""))

    def tearDown(self):
        self.Error(et.ENclose())
        print("TEAR DOWN!")

    def test_alter_with_ENset_and_check_with_a_file(self):
        self.Error(et.ENsaveinpfile("1.inp"))
        self.Error(et.ENsetlinkvalue(81, 0, 9999))
        self.Error(et.ENsaveinpfile("2.inp"))
        self.assertEqual(tt.compareFiles("1.inp", "2.inp"), '16>1e+04; ')

    def test_alter_with_ENset_via_PDD_and_check_with_a_file(self):
        self.Error(pd.ENopen(self.file, "t.rpt", ""))
        self.Error(pd.ENsaveinpfile_wrap("1.inp"))
        self.Error(pd.ENsetlinkvalue_wrap(81, 0, 788288))
        self.Error(pd.ENsaveinpfile_wrap("2.inp"))
        self.assertEqual(tt.compareFiles("1.inp", "2.inp"), '16>7.88e+05; ')
        self.Error(pd.ENclose())


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

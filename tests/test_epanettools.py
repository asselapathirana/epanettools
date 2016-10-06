import unittest

import epanettools


class Test1(unittest.TestCase):

    def setup(self):
        print("SETUP!")

    def teardown(self):
        print("TEAR DOWN!")

    def err(self, et, e):
        if(e > 0):
            print((e, et.ENgeterror(e, 25)))
            exit(5)

    def test_basic(self):
        import os
        from epanettools import epanet2 as et
        from epanettools.examples import simple

        file = os.path.join(os.path.dirname(simple.__file__), 'Net3.inp')
        ret = et.ENopen(file, "Net3.rpt", "Net3.dat")
        self.err(et, ret)

        ret, result = et.ENgetcount(et.EN_LINKCOUNT)

        # links
        assert (result == 119)

        ret, result = et.ENgetcount(et.EN_NODECOUNT)
        # nodes
        assert(result == 97)

        node = '105'
        ret, index = et.ENgetnodeindex(node)
        # index of node '105'
        assert(index == 12)

        #
        print(et.ENgetlinknodes(55))
        assert all([i == j for i, j in zip(et.ENgetlinknodes(55), [0, 5, 46])])

        ret, nnodes = et.ENgetcount(et.EN_NODECOUNT)
        nodes = []
        pres = []
        time = []
        for index in range(1, nnodes):
            ret, t = et.ENgetnodeid(index)
            nodes.append(t)
            t = []
            pres.append(t)
        print(nodes)
        assert(nodes == ['10', '15', '20', '35', '40', '50',
                         '60', '601', '61', '101', '103', '105',
                         '107', '109', '111', '113', '115', '117',
                         '119', '120', '121', '123', '125', '127',
                         '129', '131', '139', '141', '143', '145',
                         '147', '149', '151', '153', '157', '159',
                         '161', '163', '164', '166', '167', '169',
                         '171', '173', '177', '179', '181', '183',
                         '184', '185', '187', '189', '191', '193',
                         '195', '197', '199', '201', '203', '204',
                         '205', '206', '207', '208', '209', '211',
                         '213', '215', '217', '219', '225', '229',
                         '231', '237', '239', '241', '243', '247',
                         '249', '251', '253', '255', '257', '259',
                         '261', '263', '265', '267', '269', '271',
                         '273', '275', 'River', 'Lake', '1', '2'])

        self.err(et, et.ENopenH())
        self.err(et, et.ENinitH(0))
        while True:
            ret, t = et.ENrunH()
            time.append(t)
            self.err(et, ret)
            # Retrieve hydraulic results for time t
            for i in range(0, len(nodes)):
                ret, p = et.ENgetnodevalue(i + 1, et.EN_PRESSURE)
                pres[i].append(p)
            ret, tstep = et.ENnextH()
            self.err(et, ret)
            if (tstep <= 0):
                break
        ret = et.ENcloseH()
        print(pres[12])
        diffs = [abs(i - j) for i, j in zip(pres[12],
                                            [54.085777282714844, 60.99293518066406,
                                             63.03010940551758, 63.56983947753906,
                                             66.80770874023438, 63.989463806152344,
                                             63.49333190917969, 63.895835876464844,
                                             63.440582275390625, 63.90030288696289,
                                             63.43799591064453, 63.438758850097656,
                                             63.03285598754883, 63.005157470703125,
                                             63.1264533996582, 63.40403366088867,
                                             56.72084045410156, 56.622596740722656,
                                             56.47193908691406, 56.478843688964844,
                                             56.27402114868164, 55.576839447021484,
                                             55.0153923034668, 55.81755065917969,
                                             55.200626373291016, 53.8864860534668,
                                             55.024227142333984])]
        print([i for i in diffs])
        assert all([i < 1.e-5 for i in diffs])


import time

# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__ = "assela"
__date__ = "$Sep 30, 2011 12:59:16 PM$"


def err(e):
    if(e > 0):
        print((e, et.ENgeterror(e, 25)))
        exit(5)


if __name__ == "__main__":

    from epanettools import epanet2 as et
    ret = et.ENopen("Net3.inp", "Net3.rpt", "")
    err(ret)
    ret, result = et.ENgetcount(et.EN_LINKCOUNT)
    err(ret)
    print(("Network has ", result, " links."))
    ret, result = et.ENgetcount(et.EN_NODECOUNT)
    err(ret)
    print(("Network has ", result, " nodes."))
    node = '105'
    ret, index = et.ENgetnodeindex(node)
    print(("Node ", node, " has index : ", index))

    ret, nnodes = et.ENgetcount(et.EN_NODECOUNT)
    nodes = []
    pres = []
    for index in range(1, nnodes):
        ret, t = et.ENgetnodeid(index)
        nodes.append(t)
        t = []
        pres.append(t)

    print(nodes)
    err(et.ENopenH())
    err(et.ENinitH(0))
    while True:
        ret, t = et.ENrunH()
        time.append(t)
        err(ret)
        # Retrieve hydraulic results for time t
        for i in range(0, len(nodes)):
            ret, p = et.ENgetnodevalue(i + 1, et.EN_PRESSURE)
            pres[i].append(p)
        ret, tstep = et.ENnextH()
        err(ret)
        if (tstep <= 0):
            break
    ret = et.ENcloseH()
    print("")
    import matplotlib
    matplotlib.use("QT4Agg")
    import matplotlib.pyplot as plt

    for i in range(40, 50):
        plt.plot(time, pres[i], label=nodes[i])

    plt.legend(loc=1, bbox_to_anchor=(1, 1))

    plt.show()

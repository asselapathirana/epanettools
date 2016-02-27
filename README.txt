Epanet 2.0 Python calling interface 

Since version 0.4.0.1 the library is compatible with Python 3.0

What is it?
-----------
A python package enabling user to call all the `epanet programmers toolkit <http://www.epa.gov/nrmrl/wswrd/dw/epanet.html#toolkit>`_ functions within python scripts. 

Installation
------------
:Windows: 
	Use a Python ditribution that comes with a c copiler (use WinPython or PythonXY) ::
	
	   pip install epanettools
	
	
:POSIX (e.g. Linux, OS-X):
    Download source archive (zip file), extract and run (as root) ::
	
	   [sudo] python setup.py install
	   
    or just type ::
		
	   [sudo]  pip install epanettools


Usage:
------

::

    >>> import os, pprint
    >>> pp=pprint.PrettyPrinter() # we'll use this later. 
    >>> from  epanettools.epanettools import EPANetSimulation, Node, Link, Network, Nodes, \
    ... Links, Patterns, Pattern, Controls, Control # import all elements needed 
    >>> from epanettools.examples import simple # this is just to get the path of standard examples
    >>> file = os.path.join(os.path.dirname(simple.__file__),'Net3.inp') # open an example
    >>> es=EPANetSimulation(file) 
    



Node information

::

    >>> len(es.network.nodes)
    97
    >>> list(es.network.nodes)[:5] # just get indexes of nodes
    [1, 2, 3, 4, 5]
    >>> [es.network.nodes[x].id for x in list(es.network.nodes)[:5]] # Get ids of first five nodes. 
    ['10', '15', '20', '35', '40']
    >>> n=es.network.nodes
    >>> n[1].id
    '10'
    >>> n[94].id
    'Lake'
    >>> n['10'].index # get the index of the node with id '10' 
    1

Now links

::
    
    >>> m=es.network.links
    >>> len(m)
    119
    >>> m[1].id
    '20'
    >>> m[3].id
    '50'
    >>> m[119].id
    '335'

Information about connectivity

::

    >>> [m[1].start.id,m[1].end.id] # get the two ends of a link
    ['3', '20']
    >>> [m[118].start.id,m[118].end.id]
    ['Lake', '10']
    >>> sorted([i.id for i in n['169'].links]) # get the links connected to a node. 
    ['183', '185', '187', '211']

Types of links and nodes

::
    >>> pp.pprint(Node.node_types) # these are the type codes for nodes. 
    {'JUNCTION': 0, 'RESERVOIR': 1, 'TANK': 2}
    >>> n[94].node_type
    1
    >>> n[1].node_type
    0
    >>> n['2'].node_type
    2
    >>> pp.pprint(Link.link_types) # these are the type codes for links
    {'CVPIPE': 0,
     'FCV': 6,
     'GPV': 8,
     'PBV': 5,
     'PIPE': 1,
     'PRV': 3,
     'PSV': 4,
     'PUMP': 2,
     'TCV': 7}
    >>> m['335'].link_type # Pump
    2
    >>> m['101'].link_type # PIPE
    1
    >>> m[1].link_type # 
    1
    >>> [y.id for x,y in m.items() if y.link_type==Link.link_types['PUMP']] # get ids of pumps
    ['10', '335']
    >>> [y.id for x,y in n.items() if y.node_type==Node.node_types['TANK']] # get ids of tanks
    ['1', '2', '3']
    
Get some results of simulation. 

:: 

   >>> es.run()
   >>> p=Node.value_type['EN_PRESSURE']
   >>> print("%.3f" % es.network.nodes['103'].results[p][5] )
   59.301
   >>> d=Node.value_type['EN_DEMAND']
   >>> h=Node.value_type['EN_HEAD']
   >>> print("%.3f" % es.network.nodes['103'].results[d][5])
   101.232
   >>> print("%.3f" % es.network.nodes['103'].results[h][5])
   179.858
   >>> d=Link.value_type['EN_DIAMETER']
   >>> print("%.3f" % es.network.links[1].results[d][0])
   99.000
   >>> es.runq() # run water quality simulation 
   >>> q=Node.value_type['EN_QUALITY']
   >>> print("%.3f" % es.network.nodes['117'].results[q][4])
   85.317
   >>> e=Link.value_type['EN_ENERGY']
   >>> print("%.5f" % es.network.links['111'].results[e][23])
   0.00685




Legacy Interface
----------------

Do not use the following methods unless for compatibility!

::

    >>> import os
    >>> from epanettools import epanet2 as et
    >>> from epanettools.examples import simple 
    >>> file = os.path.join(os.path.dirname(simple.__file__),'Net3.inp')
    >>> ret=et.ENopen(file,"Net3.rpt","")
    
 
    
:Example 1: Retrieve simulation properties. 

Basic properties of the network


::

    >>> ret,result=et.ENgetcount(et.EN_LINKCOUNT) 	
    >>> print(ret) 	
    0
	>>> print(result)
	119
    >>> ret,result=et.ENgetcount(et.EN_NODECOUNT) 	
    >>> print(ret) 	
    0
    >>> print(result)
    97
	>>> node='105'
	>>> ret,index=et.ENgetnodeindex(node) 
	>>> print(ret)
	0
	>>> print ("Node " + node + " has index : " + str(index))
	Node 105 has index : 12


Get the list of nodes
	
::

    >>> ret,nnodes=et.ENgetcount(et.EN_NODECOUNT)
    >>> nodes=[]
    >>> pres=[]
    >>> time=[]
    >>> for index in range(1,nnodes):
    ...     ret,t=et.ENgetnodeid(index)
    ...     nodes.append(t)
    ...     t=[]
    ...     pres.append(t)
    >>> print (nodes)       #doctest: +ELLIPSIS
    ...                     #doctest: +NORMALIZE_WHITESPACE
	['10', '15', '20', '35', '40', '50', '60', ..., '275', 'River', 'Lake', '1', '2']

Get nodes indexes on either side of a link with given index

::

    >>> et.ENgetlinknodes(55) # note the first item in the list should be ignored. 
    [0, 5, 46]
    
    
::
    
    >>> patId = "NewPattern";
    >>> ret=et.ENaddpattern(patId)
    >>> print(ret)
    0
    >>> import numpy as np
    >>> patFactors=np.array([0.8, 1.1, 1.4, 1.1, 0.8, 0.7, 0.9, 0.0, 0.8, 0.8, 0.0, 0.0], 
    ...                      dtype=np.float32)
    >>> ret,patIndex=et.ENgetpatternindex(patId)
    >>> print(patIndex)
    6
    >>> et.ENsetpattern(patIndex, patFactors)
    0
    >>> et.ENgetpatternid(6)[1]
    'NewPattern'
    >>> et.ENgetpatternlen(6)
    [0, 12]
    >>> [round(et.ENgetpatternvalue(6,i)[1],3) for i in range(1,12+1)]
    [0.8, 1.1, 1.4, 1.1, 0.8, 0.7, 0.9, 0.0, 0.8, 0.8, 0.0, 0.0]
    >>> et.ENsetpatternvalue(6,9,3.3)
    0
    >>> [round(et.ENgetpatternvalue(6,i)[1],3) for i in range(1,12+1)]
    [0.8, 1.1, 1.4, 1.1, 0.8, 0.7, 0.9, 0.0, 3.3, 0.8, 0.0, 0.0]
    
    
Hydraulic Simulation
	
	
::

    >>> et.ENopenH()
    0
    >>> et.ENinitH(0)  
    0
    >>> while True :
    ...    ret,t=et.ENrunH()
    ...    time.append(t)
    ...    # Retrieve hydraulic results for time t
    ...    for  i in range(0,len(nodes)):
    ...        ret,p=et.ENgetnodevalue(i+1, et.EN_PRESSURE )
    ...        pres[i].append(p)
    ...    ret,tstep=et.ENnextH()
    ...    if (tstep<=0):
    ...        break
    >>> ret=et.ENcloseH()  
    >>> print([round(x,4) for x in pres[0]])   #doctest: +ELLIPSIS  
    ...                                         #doctest: +NORMALIZE_WHITESPACE
	[-0.6398, 40.1651, 40.891, 41.0433, ..., 0.569, -0.8864, 0.2997]


Pressure at the node '10'
	
	
::

    >>> ret,ind=et.ENgetnodeindex("10")
    >>> print (ind)
    1
    >>> print([round(x,4) for x in pres[ind+1]]) # remember epanet count starts at 1. 
    ...                                          #doctest: +ELLIPSIS  
    ...                                          #doctest: +NORMALIZE_WHITESPACE   
	[12.5657, 12.9353, 13.4351, 14.0307, ..., 13.1174, 13.3985, 13.5478]
	   
	   
	

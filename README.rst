========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |appveyor| |requires|
        | |coveralls|
    * - package
      - |version| |downloads| |wheel| |supported-versions| |supported-implementations|

.. |docs| image:: https://readthedocs.org/projects/epanettools/badge/?style=flat
    :target: https://readthedocs.org/projects/epanettools
    :alt: Documentation Status

.. |travis| image:: https://travis-ci.org/asselapathirana/epanettools.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/asselapathirana/epanettools

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/asselapathirana/epanettools?branch=master&svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/asselapathirana/epanettools

.. |requires| image:: https://requires.io/github/asselapathirana/epanettools/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/asselapathirana/epanettools/requirements/?branch=master

.. |coveralls| image:: https://coveralls.io/repos/asselapathirana/epanettools/badge.svg?branch=master&service=github
    :alt: Coverage Status
    :target: https://coveralls.io/r/asselapathirana/epanettools

.. |version| image:: https://img.shields.io/pypi/v/epanettools.svg?style=flat
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/epanettools

.. |downloads| image:: https://img.shields.io/pypi/dm/epanettools.svg?style=flat
    :alt: PyPI Package monthly downloads
    :target: https://pypi.python.org/pypi/epanettools

.. |wheel| image:: https://img.shields.io/pypi/wheel/epanettools.svg?style=flat
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/epanettools

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/epanettools.svg?style=flat
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/epanettools

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/epanettools.svg?style=flat
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/epanettools


.. end-badges

Epanet 2.0 Python calling interface

Epanet 2.0 Python calling interface 
 
Since version 0.5.0.1 the library has the epanet-emitter engine enabling Pressure-based Demand Analysis (http://assela.pathirana.net/EPANET-Emitter).

Since version 0.4.0.1 the library is compatible with Python 3.0

What is it?
-----------
A python package enabling user to call all the `epanet programmers toolkit <http://www.epa.gov/nrmrl/wswrd/dw/epanet.html>`_ functions within python scripts. 

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
  

  
Network properties are available (even before we run the simulation)

::

    >>> d=Link.value_type['EN_DIAMETER']
    >>> print("%.3f" % es.network.links[1].results[d][0])
    99.000
    
    >>> p1=es.network.patterns[1]
    >>> l=list(p1.values())
    >>> print("%2.1f "*len(l) % tuple(l )) # doctest: +NORMALIZE_WHITESPACE
    1.3 1.9 1.5 1.4 0.8 0.9 0.9 1.1 1.0 1.1 1.1 1.2 1.2 1.1 1.0 0.8 0.8 0.7 0.6 0.6 0.9 1.0 1.2 1.7  
    

    
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


Some advanced result queries

::

    >>> print("%.3f" % min(es.network.nodes['103'].results[p])) # minimum recorded pressure of node '103'
    44.169
    >>> n=es.network.nodes
    >>> # All nodes recording negative pressure. 
    >>> sorted([y.id for x,y in n.items() if min(y.results[p])<0])
    ['10']
    >>> # Nodes that deliver a flow of more than 4500 flow units
    >>> d=Node.value_type['EN_DEMAND']
    >>> j=Node.node_types['JUNCTION']
    >>> sorted([y.id for x,y in n.items() if ( max(y.results[d])>4500 and y.node_type==j )])
    ['203']


Changing the network
-----------------------
Currently the new (object-based) interface above only supports read access to the underlying network. To change the values of the network, it is recommended to use the Legacy interface calls.  Legacy calls can be accessed from within the new interface. The steps in changing network:

1. Create an object of EPANetSimulation with the network file
2. Change needed values using ENsetxxxx calls (just changing the attributes of EPANetSimulation will not  work!)
3. Save the changed data to a new file using ENsaveinpfile.
4. Create an object of EPANetSimulation with the new saved file. 

 Following is an example:

::

	>>> d=Link.value_type['EN_DIAMETER']
	>>> e=Node.value_type['EN_ELEVATION']
	>>> es.ENgetlinkvalue(81,d)[1] #low level interface
	16.0
	>>> es.network.links[81].results[d] # new interface
	[16.0]
	>>> es.ENgetnodevalue(55,e)[1] # low level interface
	15.5
	>>> es.network.nodes[55].results[e] #new interface
	[15.5]
	>>> r=es.ENsetlinkvalue(81,d,99) # now let's change values - link
	>>> r # zero means no error!
	0
	>>> r=es.ENsetnodevalue(55,e,18.25) # change elevation of node
	>>> r #zero means no error
	0
	>>> # Note: the original network is not changed! Only the low level values changed. This is a limitation of current implementation
	>>> es.network.links[81].results[d], es.ENgetlinkvalue(81,d)[1], es.network.nodes[55].results[e], es.ENgetnodevalue(55,e)[1] 
	([16.0], 99.0, [15.5], 18.25)
	>>> # to permanantly change values, the changed network has to  be written to a new file
	 >>> import tempfile, os
      	>>> f=os.path.join(tempfile.gettempdir(),"temp.inp")
      	>>> es.ENsaveinpfile(f) # save the changed file
      	0
      	>>> e2=EPANetSimulation(f)
       	>>> e2.network.links[81].results[d], e2.ENgetlinkvalue(81,d)[1], e2.network.nodes[55].results[e], e2.ENgetnodevalue(55,e)[1]
	([99.0], 99.0, [18.25], 18.25)
	>>> # now in both high level and low level interfaces, we have the right value. 
   	

Pattern manipulation
--------------------

::
    
    >>> patId = "NewPattern";
    >>> ret=es.ENaddpattern(patId)
    >>> print(ret)
    0
    >>> patFactors=[0.8, 1.1, 1.4, 1.1, 0.8, 0.7, 0.9, 0.0, 0.8, 0.8, 0.0, 0.0]
    >>> ret,patIndex=es.ENgetpatternindex(patId)
    >>> print(patIndex)
    6
    >>> es.ENsetpattern(patIndex, patFactors)
    0
    >>> es.ENgetpatternid(6)[1]
    'NewPattern'
    >>> es.ENgetpatternlen(6)
    [0, 12]
    >>> [round(es.ENgetpatternvalue(6,i)[1],3) for i in range(1,12+1)]
    [0.8, 1.1, 1.4, 1.1, 0.8, 0.7, 0.9, 0.0, 0.8, 0.8, 0.0, 0.0]
    >>> es.ENsetpatternvalue(6,9,3.3)
    0
    >>> [round(es.ENgetpatternvalue(6,i)[1],3) for i in range(1,12+1)]
    [0.8, 1.1, 1.4, 1.1, 0.8, 0.7, 0.9, 0.0, 3.3, 0.8, 0.0, 0.0]
    


PDD type analysis
-------------------------

Look at http://assela.pathirana.net/EPANET-Emitter  for details and desktop (windows only) application that does the same analysis. 

::

    >>> # lets create a pressure deficient network to demonstate this. 
    >>> d=Link.value_type['EN_DIAMETER']
    >>> l=es.network.links['247'] .index # get the index of '247' node.
    >>> r=es.ENsetlinkvalue(l,d,2.5) # now let's change values - link diameter to a  small value.
    >>> r # zero means no error!
    0
    >>> f=os.path.join(tempfile.gettempdir(),"temp.inp")
    >>> es.ENsaveinpfile(f) # save the changed file
    0
    >>> #now lets analyse this with 'normal' epanet engine
    >>> e2=EPANetSimulation(f, pdd=False) #note pdd=False is default, no need to write this
    >>> e2.run() #simulate
    >>> p=Node.value_type['EN_PRESSURE']
    >>> e2.network.nodes['225'].results[p][10] < -10.0 # we should get a large negative pressure value
    True
    >>> d=Node.value_type['EN_DEMAND']
    >>> print("%4.2f" %e2.network.nodes['225'].results[d][10]) # the demand does not change/ 
    25.08
    >>> e3=EPANetSimulation(f,pdd=True) # now we enable pdd
    >>> e3.run()
    >>> p225=e3.network.nodes['225'].results[p][10] # pressure should be nearly zero
    >>> (p225 > -3 and p225 < 3)
    True
    >>> d=Node.value_type['EN_DEMAND']
    >>> d225=e3.network.nodes['225'].results[d][10]  # the demand should be nearly zero
    >>> (d225 > -.1 and d225 < .1)
    True
    



Legacy Interface
----------------

Do not use the following methods unless for compatibility! As of versions > 0.8 pattern setting
using this interface is not available. 

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

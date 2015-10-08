Epanet 2.0 Python calling interface

Since version 0.4.0.1 the library is compatible with Python 3.0

What is it?
-----------
A python package enabling user to call all the `epanet programmers toolkit <http://www.epa.gov/nrmrl/wswrd/dw/epanet.html#toolkit>`_ functions within python scripts. 

Installation
------------
:Windows: 
	Download the MS Windows installer and run to install. Since version 0.4.0.1 "python wheels " packages are also provided. So, the following command can also be used to install on windows ::
	
	   pip install epanettools
	
	
:POSIX (e.g. Linux, OS-X):
    Download source archive (zip file), extract and run (as root) ::
	
	   [sudo] python setup.py install
	   
    or just type ::
		
	   [sudo]  pip install epanettools


Usage:
------

::

    >>> from epanettools import epanet2 as et
	>>> p="epanettools/examples/simple/"
    >>> ret=et.ENopen(p+"Net3.inp",p+"Net3.rpt","")
    
 
    
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
	   
	   
	

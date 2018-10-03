"""
Reduces the diameter of a pipe gradually and calculates pressure at the end of 
pipe for each value of the diameter.

"""
import matplotlib # we need matplotlib for plotting later
matplotlib.use('Qt5Agg') # Not esential. But QtAgg backend seems to work better for plotting
import matplotlib.pyplot as plt # for plotting later

from  epanettools import epanettools # import epanet package

# Epanet toolkit use an integer flag to denote diameter called EN_DIAMETER. Get it for later use
dia=epanettools.Link.value_type['EN_DIAMETER'] 
# ditto for pressure - EN_PRESSURE
pre=epanettools.Node.value_type['EN_PRESSURE']
# Open the network
es=epanettools.EPANetSimulation("simple.inp")
# What is the index of the link with ID P1?
linkindex=es.network.links['P1'].index
# range of diameters we want to test for. Largest to smallest
dias=range(1000,50,-10)
press=[] # A list to keep pressure values we calculate
ct=0
for d in dias: # loop through the diameters as d
    ct+=1
    print ("{} Diameter {} mm".format(ct,d)) # print d
    r=es.ENsetlinkvalue(linkindex,dia,d) # set the link P1 (whose index is linkindex) to d 
    if (r!=0): # r >0 is error. 
        print("Error")
    es.ENsaveinpfile('tmp1.inp') # save the modified file as 'tmp1.inp'
    es2=epanettools.EPANetSimulation('tmp1.inp') # open the new file with epanet
    es2.run() # run the simulation
    p=es2.network.nodes['N1'].results[pre][0] # get the pressure at node 'N1'
    if(p<0):
        break # if pressure is negative, just stop calculations
    press.append(p) # append pressure p to the press list.
dias=dias[:len(press)] # to plot we need x and y data to be of same length. 
                       # So, take first n values of dias, where n=len(press)
ax = plt.plot(dias,press, marker=".") # plot press against daias 
plt.xlabel("Diameter (mm)") # set axes labels
plt.ylabel("Pressure (m)")

plt.show() # show the plot. 

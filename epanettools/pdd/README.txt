Create a seperate interface file for pdd - called pdd.i
swig  -python  epanet2.i
swig -c++ -python pdd.i

then add the resulting *.c and *.cxx files to setup.py 
python setup.py test

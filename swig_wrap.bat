cd src/epanettools
swig -python epanet2.i
swig -c++ -python pdd.i
swig -c++ -python adf.i

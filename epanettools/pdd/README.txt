Now compiling is OK. 
Tests are passing for non emitter but, test_EPANetPDD.py is not really testinng PDD

Question: what is the most elegant (maintainable) way to have epanettools.py (in fact class EPANetSimulation)
to be duplicated to make all calls to pdd instead of normal epanet?
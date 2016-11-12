 %{
 #define SWIG_FILE_WITH_INIT
 /* Includes the header in the wrapper code */
 #include "./adf/adfandenergycalc.h"
 extern char TmpDir[200]; /* this makes it possible to overrride the TmpDir */ 
 %}


/* modify epanet2.h file as: 
1. Undefine __win32__ and WINDOWS 
2. for all output parameters, give the name value */
%module adf
 %include "typemaps.i"
 %include "cstring.i"
/* %include "numpy.i" 
 
 %init %{
 import_array();
 %} 
 
 %apply (float* IN_ARRAY1, int DIM1) {(float* floatarray, int nfloats)}; */
 
 /* read http://www.swig.org/Doc1.3/Arguments.html */
 /* 26-Aug-2016 : IMPORTANT: all output parameters in wrapper.h has to be named and then declared below. See epanet2.h and epanet2.i files for examples.
At the moment only a few were done to test.  
*/
 
 
 /* Parse the header file to generate wrappers */
 %include "./adf/adfandenergycalc.h"

 extern char TmpDir[200]; /* this makes it possible to overrride the TmpDir */
;

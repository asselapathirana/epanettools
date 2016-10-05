 %{
 #define SWIG_FILE_WITH_INIT
 /* Includes the header in the wrapper code */
 #include "./pdd/wrapper.h"
 #include "./epanet/epanet2.h"
 #include "./patch.h"
 extern char TmpDir[200]; /* this makes it possible to overrride the TmpDir */ 
 %}


/* modify epanet2.h file as: 
1. Undefine __win32__ and WINDOWS 
2. for all output parameters, give the name value */
%module pdd
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
 
 %apply int *OUTPUT { int *result };
 %apply int *OUTPUT { int *result1 };
 %apply int *OUTPUT { int *result2 };
 %apply long *OUTPUT { long *result };
 %apply float *OUTPUT { float *result };
 %apply float *OUTPUT {float *c1}
 %apply float *OUTPUT {float *c2}
 %apply int *OUTPUT {int *ci1}
 %apply int *OUTPUT {int *ci2}
 %apply int *OUTPUT {int *ci3}
 %apply double *OUTPUT { double *result };
 %cstring_bounded_output(char *result,   1024);


 
 /* Parse the header file to generate wrappers */
 %include "./pdd/wrapper.h"
 %include "./epanet/epanet2.h"
 %include "./patch.h"

 extern char TmpDir[200]; /* this makes it possible to overrride the TmpDir */
;
